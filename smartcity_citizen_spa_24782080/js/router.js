const routes = {
    login: `
        <div class="row justify-content-center">
            <div class="col-12 col-md-6 col-lg-4">
                <div class="card shadow-sm border-0">
                    <div class="card-body p-4">

                        <h4 class="text-center mb-4">
                            <i class="bi bi-shield-lock-fill text-primary"></i>
                            Login Citizen
                        </h4>

                        <form id="loginForm">

                            <div class="mb-3">
                                <label class="form-label">Username</label>
                                <input 
                                    type="text" 
                                    id="loginUsername" 
                                    class="form-control" 
                                    placeholder="Masukkan username"
                                    required
                                >
                            </div>

                            <div class="mb-3">
                                <label class="form-label">Password</label>
                                <input 
                                    type="password" 
                                    id="loginPassword" 
                                    class="form-control" 
                                    placeholder="Masukkan password"
                                    required
                                >
                            </div>

                            <button type="submit" class="btn btn-primary w-100">
                                <i class="bi bi-box-arrow-in-right"></i>
                                Login
                            </button>

                        </form>

                    </div>
                </div>
            </div>
        </div>
    `,

    dashboard: `
        <div class="row g-4">

            <aside class="col-12 col-lg-3">
                <div class="card shadow-sm border-0 mb-3">
                    <div class="card-body">
                        <h5>
                            <i class="bi bi-person-circle text-primary"></i>
                            Citizen Menu
                        </h5>
                        <hr>

                        <button 
                            class="btn btn-outline-primary w-100 mb-2"
                            onclick="openCreateModal()"
                        >
                            <i class="bi bi-plus-circle"></i>
                            Laporan Baru
                        </button>

                        <button 
                            class="btn btn-outline-secondary w-100"
                            onclick="logout()"
                        >
                            <i class="bi bi-box-arrow-right"></i>
                            Logout
                        </button>
                    </div>
                </div>

                <div class="card shadow-sm border-0">
                    <div class="card-body">
                        <h5>
                            <i class="bi bi-bar-chart-fill text-success"></i>
                            Rekap Status
                        </h5>
                        <hr>

                        <p class="mb-2">
                            <span class="badge bg-secondary">Draft</span>
                            <span id="draftCount" class="float-end fw-bold">0</span>
                        </p>

                        <p class="mb-2">
                            <span class="badge bg-primary">Diproses</span>
                            <span id="processCount" class="float-end fw-bold">0</span>
                        </p>

                        <p class="mb-0">
                            <span class="badge bg-success">Selesai</span>
                            <span id="doneCount" class="float-end fw-bold">0</span>
                        </p>
                    </div>
                </div>
            </aside>

            <section class="col-12 col-lg-6">
                <div class="card shadow-sm border-0 mb-3">
                    <div class="card-body">
                        <h4>
                            <i class="bi bi-speedometer2 text-success"></i>
                            Dashboard Citizen
                        </h4>
                        <p class="text-muted mb-0">
                            Pantau laporan pribadi dan linimasa laporan kota secara real-time.
                        </p>
                    </div>
                </div>

                <div class="card shadow-sm border-0">
                    <div class="card-body">

                        <ul class="nav nav-pills mb-3">
                            <li class="nav-item">
                                <button 
                                    class="nav-link active" 
                                    id="myReportsTab"
                                    onclick="switchTab('my_reports')"
                                >
                                    <i class="bi bi-journal-text"></i>
                                    Laporan Saya
                                </button>
                            </li>

                            <li class="nav-item">
                                <button 
                                    class="nav-link"
                                    id="feedTab"
                                    onclick="switchTab('feed')"
                                >
                                    <i class="bi bi-broadcast"></i>
                                    Feed Kota
                                </button>
                            </li>
                        </ul>

                        <div id="reportListContainer">
                            <p class="text-muted">Memuat data laporan...</p>
                        </div>

                        <div id="paginationContainer" class="mt-3"></div>

                    </div>
                </div>
            </section>

            <aside class="col-12 col-lg-3">
                <div class="card shadow-sm border-0 h-100">
                    <div class="card-body">
                        <h5>
                            <i class="bi bi-info-circle-fill text-info"></i>
                            Informasi
                        </h5>
                        <hr>
                        <p class="text-muted">
                            Draft hanya terlihat oleh pembuat laporan. Feed Kota hanya menampilkan laporan publik yang sudah diajukan.
                        </p>
                    </div>
                </div>
            </aside>

        </div>
    `,
};

function handleRouting() {
    const hash = window.location.hash.replace("#", "");
    const currentPage = hash || "login";

    const appContent = document.getElementById("app-content");

    appContent.innerHTML = routes[currentPage] || routes.login;

    if (currentPage === "login") {
        setupLoginForm();
    }

    if (currentPage === "dashboard") {
        updateNavigation();
        loadDashboardData("my_reports", 1);
    }
}

window.addEventListener("hashchange", handleRouting);
window.addEventListener("DOMContentLoaded", handleRouting);