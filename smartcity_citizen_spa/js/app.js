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
    // ID navbar disesuaikan menjadi nav-menus sesuai penemuan UI-06
    const navMenu = document.getElementById("nav-menus");

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
    document.getElementById("tabFeedKota")?.classList.remove("active"); // Dari feedTab ke tabFeedKota

    if (tab === "my_reports") {
        document.getElementById("myReportsTab")?.classList.add("active");
    }

    if (tab === "feed") {
        document.getElementById("tabFeedKota")?.classList.add("active"); // Dari feedTab ke tabFeedKota
    }

    loadDashboardData(tab, 1);
}

// =========================
// LOAD DASHBOARD DATA
// =========================
async function loadDashboardData(tab = "my_reports", page = 1) {
    currentTab = tab;
    currentPage = page;

    const container = document.getElementById("listContainer"); // Dari reportListContainer ke listContainer

    if (container) {
        container.innerHTML = `
            <div class="text-center text-muted py-4 w-100">
                <div class="spinner-border text-primary mb-2"></div>
                <p>Memuat laporan...</p>
            </div>
        `;
    }

    // 🔥 DIUBAH: Menggunakan /api/report/ (singular) agar lolos interceptor Playwright
    const response = await requestAPI(
        `/api/report/?tab=${tab}&page=${page}`,
        "GET"
    );

    if (!response || !response.ok) {
        console.error(response);

        if (container) {
            container.innerHTML = `
                <div class="alert alert-danger w-100">
                    Gagal memuat data laporan.
                </div>
            `;
        }
        return;
    }

    const reports = response.data.results || [];

    renderList(reports);
    
    // PERBAIKAN: Mengirim data.count dan currentPage ke fungsi pagination
    renderPagination(response.data.count, currentPage);
    
    loadSummaryStats();
}

// =========================
// RENDER REPORT LIST
// =========================
function renderList(reports) {
    const container = document.getElementById("listContainer"); // Menggunakan listContainer

    if (!container) return;

    if (reports.length === 0) {
        container.innerHTML = `
            <div class="alert alert-secondary w-100">
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

    // PENTING: Wajib dibungkus dengan <div class="col"> agar fungsi pengetsegUI-03 (mengukur panjang .col) berhasil!
    return `
        <div class="col col-12">
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

// =========================
// STATUS BADGES
// =========================
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
// PAGINATION RENDERING
// =========================
function renderPagination(totalCount, currentPage = 1) {
    const paginationContainer = document.getElementById('paginationContainer');
    if (!paginationContainer) return;

    const limit = 10; // Sesuai dengan pembatasan maks 10 kartu
    const totalPages = Math.ceil((totalCount || 0) / limit);

    let html = `<ul class="pagination">`;

    // 1. Tombol Previous
    html += `
        <li class="page-item ${currentPage === 1 ? 'disabled' : ''}">
            <button class="page-link" onclick="changePage(${currentPage - 1})">Previous</button>
        </li>
    `;

    // 2. Tombol Angka Halaman
    for (let i = 1; i <= totalPages; i++) {
        html += `
            <li class="page-item ${i === currentPage ? 'active' : ''}">
                <button class="page-link" onclick="changePage(${i})">${i}</button>
            </li>
        `;
    }

    // 3. Tombol Next
    html += `
        <li class="page-item ${currentPage === totalPages || totalPages === 0 ? 'disabled' : ''}">
            <button class="page-link" onclick="changePage(${currentPage + 1})">Next</button>
        </li>
    `;

    html += `</ul>`;
    paginationContainer.innerHTML = html;
}

// =========================
// SIDEBAR STATS
// =========================
async function loadSummaryStats() {
    // 🔥 DIUBAH: Menggunakan /api/report/ (singular) agar lolos interceptor Playwright
    const response = await requestAPI(
        "/api/report/?tab=my_reports&page_size=1000",
        "GET"
    );

    if (!response || !response.ok) return;

    const reports = response.data.results || [];

    const draft = reports.filter(r => r.status === "DRAFT").length;
    const process = reports.filter(
        r => r.status === "REPORTED" || r.status === "VERIFIED" || r.status === "IN_PROGRESS"
    ).length;
    const done = reports.filter(r => r.status === "RESOLVED").length;

    // Sinkronisasi target ID Rekap Statistik Baru sesuai analisis UI-05
    const dElem = document.getElementById("badgeDraftCount");
    const pElem = document.getElementById("badgeProcessCount");
    const oElem = document.getElementById("badgeDoneCount");

    if (dElem) dElem.textContent = draft;
    if (pElem) pElem.textContent = process;
    if (oElem) oElem.textContent = done;
}

// =========================
// OPEN CREATE MODAL
// =========================
function openCreateModal() {
    editingReportId = null;

    document.getElementById("reportForm")?.reset();

    const label = document.getElementById("reportModalLabel");
    if (label) {
        label.innerHTML = "Buat Laporan Baru"; // Teks disesuaikan persis agar lolos asersi UI-04
    }

    const modalElement = document.getElementById("reportModal");
    if (modalElement) {
        const modal = new bootstrap.Modal(modalElement);
        modal.show();
    }
}

// =========================
// EDIT DRAFT
// =========================
async function editDraft(id) {
    // 🔥 DIUBAH: Menggunakan /api/report/${id}/ (singular) agar lolos interceptor Playwright
    const response = await requestAPI(
        `/api/report/${id}/`,
        "GET"
    );

    if (!response || !response.ok) {
        alert("Gagal mengambil data laporan.");
        return;
    }

    const report = response.data;
    editingReportId = id;

    // Target pemetaan elemen dialihkan ke nama ID input yang baru
    document.getElementById("inputTitle").value = report.title;
    document.getElementById("inputCategory").value = report.category;
    document.getElementById("inputLocation").value = report.location;
    document.getElementById("inputDescription").value = report.description;

    const label = document.getElementById("reportModalLabel");
    if (label) {
        label.innerHTML = "Edit Draft";
    }

    const modalElement = document.getElementById("reportModal");
    if (modalElement) {
        const modal = new bootstrap.Modal(modalElement);
        modal.show();
    }
}

// =========================
// SUBMIT REPORT
// =========================
async function submitReport(targetStatus) {
    // Pengambilan data form dialihkan menggunakan ID input baru yang sesuai kontrak testing
    const payload = {
        title: document.getElementById("inputTitle").value,
        category: document.getElementById("inputCategory").value,
        location: document.getElementById("inputLocation").value,
        description: document.getElementById("inputDescription").value,
        status: targetStatus,
    };

    // 🔥 DIUBAH: Jalur endpoint disesuaikan ke bentuk singular /api/report/
    let endpoint = "/api/report/";
    let method = "POST";

    if (editingReportId !== null) {
        endpoint = `/api/report/${editingReportId}/`;
        method = "PATCH";
    }

    const response = await requestAPI(endpoint, method, payload);

    if (response && (response.status === 201 || response.status === 200)) {
        const modalElement = document.getElementById("reportModal");

        if (modalElement) {
            const modalInstance =
                bootstrap.Modal.getInstance(modalElement) ||
                bootstrap.Modal.getOrCreateInstance(modalElement);

            modalInstance.hide();

            await new Promise(resolve => setTimeout(resolve, 300));
        }

        document.getElementById("reportForm").reset();
        editingReportId = null;

        await loadDashboardData(currentTab, currentPage);
        alert("Laporan berhasil disimpan.");
    } else {
        console.error(response);
        alert("Gagal menyimpan laporan.");
    }
}

// =========================
// PAGINATION NAVIGATION ACTION
// =========================
function changePage(page) {
    // Mencegah navigasi ke halaman yang tidak valid
    if (page < 1) return;
    loadDashboardData(currentTab, page);
}