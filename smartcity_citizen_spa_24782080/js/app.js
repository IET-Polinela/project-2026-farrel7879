function isLoggedIn() {
    return localStorage.getItem("access_token") !== null;
}

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