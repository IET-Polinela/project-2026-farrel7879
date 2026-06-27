const routes = {

    // =====================================================
    // LOGIN
    // =====================================================
    login: `
        <div class="row justify-content-center">

            <div class="col-md-5">

                <div class="card shadow">

                    <div class="card-body">

                        <h3 class="text-center mb-4">
                            Login Citizen
                        </h3>

                        <form id="loginForm">

                            <div class="mb-3">
                                <label class="form-label">
                                    Username
                                </label>

                                <input
                                    id="loginUsername"
                                    class="form-control"
                                    required>
                            </div>

                            <div class="mb-3">

                                <label class="form-label">
                                    Password
                                </label>

                                <input
                                    id="loginPassword"
                                    type="password"
                                    class="form-control"
                                    required>

                            </div>

                            <button
                                class="btn btn-primary w-100"
                                type="submit">

                                Login

                            </button>

                            <a
                                href="#register"
                                class="btn btn-outline-success w-100 mt-2">

                                Buat Akun Baru

                            </a>

                        </form>

                    </div>

                </div>

            </div>

        </div>
    `,

    // =====================================================
    // REGISTER
    // =====================================================
    register: `
        <div class="row justify-content-center">

            <div class="col-md-5">

                <div class="card shadow">

                    <div class="card-body">

                        <h3 class="text-center mb-4">

                            Registrasi Citizen

                        </h3>

                        <form id="registerForm">

                            <div class="mb-3">

                                <label class="form-label">

                                    Username

                                </label>

                                <input
                                    id="registerUsername"
                                    class="form-control"
                                    required>

                            </div>

                            <div class="mb-3">

                                <label class="form-label">

                                    Email

                                </label>

                                <input
                                    id="registerEmail"
                                    type="email"
                                    class="form-control">

                            </div>

                            <div class="mb-3">

                                <label class="form-label">

                                    Password

                                </label>

                                <input
                                    id="registerPassword"
                                    type="password"
                                    class="form-control"
                                    required>

                            </div>

                            <div class="mb-3">

                                <label class="form-label">

                                    Konfirmasi Password

                                </label>

                                <input
                                    id="registerPassword2"
                                    type="password"
                                    class="form-control"
                                    required>

                            </div>

                            <button
                                type="submit"
                                class="btn btn-success w-100">

                                Daftar

                            </button>

                            <a
                                href="#login"
                                class="btn btn-outline-primary w-100 mt-2">

                                Sudah punya akun?

                            </a>

                        </form>

                    </div>

                </div>

            </div>

        </div>
    `,

    // =====================================================
    // DASHBOARD
    // =====================================================
    dashboard: `

        <div class="row">

            <!-- ========================= -->
            <!-- SIDEBAR -->
            <!-- ========================= -->

            <div class="col-lg-3">

                <div class="card mb-3">

                    <div class="card-body">

                        <button
                            id="btnBukaModal" class="btn btn-primary w-100 mb-2"
                            onclick="openCreateModal()">

                            + Laporan Baru

                        </button>

                    </div>

                </div>

                <div class="card" id="summaryStats">

                    <div class="card-body">

                        <h5>

                            Rekap Statistik

                        </h5>

                        <hr>

                        <p>

                            Draft

                            <span
                                id="badgeDraftCount"
                                class="badge bg-secondary float-end">

                                0

                            </span>

                        </p>

                        <p>

                            Diproses

                            <span
                                id="badgeProcessCount"
                                class="badge bg-primary float-end">

                                0

                            </span>

                        </p>

                        <p>

                            Selesai

                            <span
                                id="badgeDoneCount"
                                class="badge bg-success float-end">

                                0

                            </span>

                        </p>

                    </div>

                </div>

            </div>

            <!-- ========================= -->
            <!-- CONTENT -->
            <!-- ========================= -->

            <div class="col-lg-9">

                <div class="card">

                    <div class="card-body">

                        <ul class="nav nav-tabs mb-3">

                            <li class="nav-item">

                                <button
                                    id="myReportsTab"
                                    class="nav-link active"
                                    onclick="switchTab('my_reports')">

                                    Laporan Saya

                                </button>

                            </li>

                            <li class="nav-item">

                                <button
                                    id="tabFeedKota"
                                    class="nav-link"
                                    onclick="switchTab('feed')">

                                    Feed Kota

                                </button>

                            </li>

                        </ul>

                        <div
                            id="listContainer"
                            class="row g-3">

                        </div>

                        <div
                            id="paginationContainer"
                            class="mt-3">

                        </div>

                    </div>

                </div>

            </div>

        </div>
    `,
};


// =====================================================
// ROUTER
// =====================================================
function handleRouting() {

    const hash = window.location.hash.replace("#", "") || "login";

    const token = localStorage.getItem("access_token");

    // --------------------------------------------
    // Belum login
    // --------------------------------------------
    if (
        !token &&
        hash === "dashboard"
    ) {

        window.location.hash = "#login";
        return;

    }

    // --------------------------------------------
    // Sudah login
    // --------------------------------------------
    if (
        token &&
        (
            hash === "login" ||
            hash === "register"
        )
    ) {

        window.location.hash = "#dashboard";
        return;

    }

    const app = document.getElementById("app-content");

    app.innerHTML = routes[hash] || routes.login;

    if (typeof updateNavigation === "function") {
        updateNavigation();
    }

    switch (hash) {

        case "login":
            setupLoginForm();
            break;

        case "register":
            setupRegisterForm();
            break;

        case "dashboard":

            loadDashboardData(
                "my_reports",
                1
            );

            break;
    }

}


// =====================================================
// EVENTS
// =====================================================
window.addEventListener(
    "hashchange",
    handleRouting
);

window.addEventListener(
    "DOMContentLoaded",
    handleRouting
);