let currentTab = "my_reports";
let currentPage = 1;
let editingReportId = null;


// =========================
// LOGIN CHECK
// =========================
function isLoggedIn() {
    return localStorage.getItem("access_token") !== null;
}


// =========================
// NAVBAR
// =========================
function updateNavigation() {
    const navMenu = document.getElementById("nav-menu");

    if (!navMenu) return;

    if (isLoggedIn()) {
        navMenu.innerHTML = `
            <button class="btn btn-light btn-sm" onclick="logout()">
                <i class="bi bi-box-arrow-right"></i>
                Logout
            </button>
        `;
    } else {
        navMenu.innerHTML = `
            <span class="text-white">
                <i class="bi bi-person-circle"></i>
                Guest
            </span>
        `;
    }
}


// =========================
// SWITCH TAB
// =========================
function switchTab(tab) {
    currentTab = tab;
    currentPage = 1;

    document.getElementById("myReportsTab")?.classList.remove("active");
    document.getElementById("feedTab")?.classList.remove("active");

    if (tab === "my_reports") {
        document.getElementById("myReportsTab")?.classList.add("active");
    }

    if (tab === "feed") {
        document.getElementById("feedTab")?.classList.add("active");
    }

    loadDashboardData(tab, 1);
}


// =========================
// LOAD DASHBOARD DATA
// =========================
async function loadDashboardData(tab = "my_reports", page = 1) {
    currentTab = tab;
    currentPage = page;

    const container = document.getElementById("reportListContainer");

    if (container) {
        container.innerHTML = `
            <div class="text-center text-muted py-4">
                <div class="spinner-border text-primary mb-2"></div>
                <p>Memuat laporan...</p>
            </div>
        `;
    }

    const response = await requestAPI(
        `/api/reports/?tab=${tab}&page=${page}`,
        "GET"
    );

    if (!response.ok) {
        console.error(response);

        if (container) {
            container.innerHTML = `
                <div class="alert alert-danger">
                    Gagal memuat data laporan.
                </div>
            `;
        }

        return;
    }

    const reports = response.data.results || [];

    renderList(reports);
    renderPagination(response.data.previous, response.data.next);
    loadSummaryStats();
}


// =========================
// RENDER REPORT LIST
// =========================
function renderList(reports) {
    const container = document.getElementById("reportListContainer");

    if (!container) return;

    if (reports.length === 0) {
        container.innerHTML = `
            <div class="alert alert-secondary">
                Belum ada laporan.
            </div>
        `;
        return;
    }

    container.innerHTML = reports.map(report => renderReportCard(report)).join("");
}


// =========================
// RENDER REPORT CARD
// =========================
function renderReportCard(report) {
    const progress = getStatusProgress(report.status);
    const badgeClass = getStatusBadgeClass(report.status);

    const editButton =
        report.is_owner && report.status === "DRAFT"
            ? `
                <button
                    class="btn btn-warning btn-sm"
                    onclick="editDraft(${report.id})"
                >
                    <i class="bi bi-pencil-square"></i>
                    Edit Draft
                </button>
            `
            : "";

    return `
        <div class="card shadow-sm mb-3 report-card">
            <div class="card-body">

                <div class="d-flex justify-content-between align-items-start mb-2">
                    <h5 class="mb-0">
                        ${report.title}
                    </h5>

                    <span class="badge ${badgeClass}">
                        ${report.status}
                    </span>
                </div>

                <p class="text-muted mb-1">
                    <i class="bi bi-geo-alt"></i>
                    ${report.location}
                </p>

                <p class="small text-muted mb-2">
                    <i class="bi bi-person"></i>
                    ${report.reporter}
                </p>

                <p>
                    ${report.description}
                </p>

                <div class="progress mb-2">
                    <div
                        class="progress-bar"
                        style="width:${progress}%"
                    >
                        ${progress}%
                    </div>
                </div>

                <small class="text-muted">
                    Update terakhir: ${formatDate(report.updated_at)}
                </small>

                <div class="mt-3">
                    ${editButton}
                </div>

            </div>
        </div>
    `;
}


// =========================
// STATUS HELPERS
// =========================
function getStatusProgress(status) {
    if (status === "DRAFT") return 25;
    if (status === "REPORTED") return 50;
    if (status === "VERIFIED") return 75;
    if (status === "IN_PROGRESS") return 90;
    if (status === "RESOLVED") return 100;

    return 0;
}


function getStatusBadgeClass(status) {
    if (status === "DRAFT") return "bg-secondary";
    if (status === "REPORTED") return "bg-primary";
    if (status === "VERIFIED") return "bg-info";
    if (status === "IN_PROGRESS") return "bg-warning text-dark";
    if (status === "RESOLVED") return "bg-success";

    return "bg-dark";
}


function formatDate(dateString) {
    if (!dateString) return "-";

    const date = new Date(dateString);

    return date.toLocaleString("id-ID", {
        dateStyle: "medium",
        timeStyle: "short",
    });
}


// =========================
// PAGINATION
// =========================
function renderPagination(previous, next) {
    const container = document.getElementById("paginationContainer");

    if (!container) return;

    container.innerHTML = `
        <div class="d-flex justify-content-between">

            <button
                class="btn btn-outline-secondary"
                ${!previous ? "disabled" : ""}
                onclick="loadDashboardData(currentTab, currentPage - 1)"
            >
                <i class="bi bi-chevron-left"></i>
                Previous
            </button>

            <span class="align-self-center text-muted">
                Page ${currentPage}
            </span>

            <button
                class="btn btn-outline-primary"
                ${!next ? "disabled" : ""}
                onclick="loadDashboardData(currentTab, currentPage + 1)"
            >
                Next
                <i class="bi bi-chevron-right"></i>
            </button>

        </div>
    `;
}


// =========================
// SIDEBAR STATS
// =========================
async function loadSummaryStats() {
    const response = await requestAPI(
        "/api/reports/?tab=my_reports&page_size=1000",
        "GET"
    );

    if (!response.ok) return;

    const reports = response.data.results || [];

    const draft = reports.filter(r => r.status === "DRAFT").length;

    const process = reports.filter(
        r =>
            r.status === "REPORTED" ||
            r.status === "VERIFIED" ||
            r.status === "IN_PROGRESS"
    ).length;

    const done = reports.filter(r => r.status === "RESOLVED").length;

    document.getElementById("draftCount").textContent = draft;
    document.getElementById("processCount").textContent = process;
    document.getElementById("doneCount").textContent = done;
}


// =========================
// OPEN CREATE MODAL
// =========================
function openCreateModal() {
    editingReportId = null;

    document.getElementById("reportForm")?.reset();

    document.getElementById("reportModalLabel").innerHTML = `
        <i class="bi bi-pencil-square"></i>
        Buat Laporan
    `;

    const modal = new bootstrap.Modal(
        document.getElementById("reportModal")
    );

    modal.show();
}


// =========================
// EDIT DRAFT
// =========================
async function editDraft(id) {
    const response = await requestAPI(
        `/api/reports/${id}/`,
        "GET"
    );

    if (!response.ok) {
        alert("Gagal mengambil data laporan.");
        return;
    }

    const report = response.data;

    editingReportId = id;

    document.getElementById("reportTitle").value = report.title;
    document.getElementById("reportCategory").value = report.category;
    document.getElementById("reportLocation").value = report.location;
    document.getElementById("reportDescription").value = report.description;

    document.getElementById("reportModalLabel").innerHTML = `
        <i class="bi bi-pencil-square"></i>
        Edit Draft
    `;

    const modal = new bootstrap.Modal(
        document.getElementById("reportModal")
    );

    modal.show();
}


// =========================
// SUBMIT REPORT
// =========================
async function submitReport(targetStatus) {
    const payload = {
        title: document.getElementById("reportTitle").value,
        category: document.getElementById("reportCategory").value,
        location: document.getElementById("reportLocation").value,
        description: document.getElementById("reportDescription").value,
        status: targetStatus,
    };

    let endpoint = "/api/reports/";
    let method = "POST";

    if (editingReportId !== null) {
        endpoint = `/api/reports/${editingReportId}/`;
        method = "PATCH";
    }

    const response = await requestAPI(endpoint, method, payload);

    if (response.status === 201 || response.status === 200) {
        const modalElement = document.getElementById("reportModal");
        const modalInstance = bootstrap.Modal.getInstance(modalElement);

        modalInstance.hide();

        document.getElementById("reportForm").reset();

        editingReportId = null;

        await loadDashboardData(currentTab, currentPage);

        alert("Laporan berhasil disimpan.");
    } else {
        console.error(response);
        alert("Gagal menyimpan laporan.");
    }
}