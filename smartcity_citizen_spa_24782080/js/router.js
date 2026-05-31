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
                <div class="card shadow-sm border-0 h-100">
                    <div class="card-body">
                        <h5>
                            <i class="bi bi-person-circle text-primary"></i>
                            Citizen Menu
                        </h5>
                        <hr>

                        <button class="btn btn-outline-primary w-100 mb-2">
                            <i class="bi bi-plus-circle"></i>
                            Laporan Baru
                        </button>

                        <button class="btn btn-outline-secondary w-100" onclick="logout()">
                            <i class="bi bi-box-arrow-right"></i>
                            Logout
                        </button>
                    </div>
                </div>
            </aside>

            <section class="col-12 col-lg-6">
                <div class="card shadow-sm border-0">
                    <div class="card-body">
                        <h4>
                            <i class="bi bi-speedometer2 text-success"></i>
                            Dashboard Citizen
                        </h4>
                        <p class="text-muted">
                            Selamat datang di Citizen Portal Smart City.
                        </p>

                        <div class="alert alert-info">
                            <i class="bi bi-info-circle-fill"></i>
                            Token JWT berhasil disimpan dan digunakan untuk autentikasi.
                        </div>
                    </div>
                </div>
            </section>

            <aside class="col-12 col-lg-3">
                <div class="card shadow-sm border-0 h-100">
                    <div class="card-body">
                        <h5>
                            <i class="bi bi-bell-fill text-warning"></i>
                            Informasi
                        </h5>
                        <hr>
                        <p class="text-muted">
                            Laporan dengan status DRAFT hanya dapat dilihat oleh pembuat laporan.
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
}

window.addEventListener("hashchange", handleRouting);
window.addEventListener("DOMContentLoaded", handleRouting);