// ============================================================================
// LOGIN
// ============================================================================
function setupLoginForm() {

    const loginForm = document.getElementById("loginForm");

    if (!loginForm) {
        return;
    }

    loginForm.addEventListener("submit", async function (event) {

        event.preventDefault();

        const username = document.getElementById("loginUsername").value;
        const password = document.getElementById("loginPassword").value;

        const result = await requestAPI("/api/token/", "POST", {
            username: username,
            password: password,
        });

        if (result && result.ok) {

            // Simpan token sesuai spesifikasi Playwright
            localStorage.setItem("access_token", result.data.access);
            localStorage.setItem("refresh_token", result.data.refresh);
            localStorage.setItem("username", username);

            alert("Login berhasil");

            // Redirect ke dashboard
            window.location.hash = "#dashboard";

        } else if (result) {

            alert("Login gagal. Periksa username dan password.");

        }

    });

}

// ============================================================================
// LOGOUT
// ============================================================================
function logout() {

    // Hapus token satu per satu agar sesuai AUTH-05 & AUTH-06
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    localStorage.removeItem("username");

    alert("Logout berhasil");

    window.location.hash = "#login";

}

// ============================================================================
// REGISTER
// ============================================================================
function setupRegisterForm() {

    const registerForm = document.getElementById("registerForm");

    if (!registerForm) {
        return;
    }

    registerForm.addEventListener("submit", async function (event) {

        event.preventDefault();

        const username = document.getElementById("registerUsername").value;
        const email = document.getElementById("registerEmail").value;
        const password = document.getElementById("registerPassword").value;
        const password2 = document.getElementById("registerPassword2").value;

        const result = await requestAPI("/auth/api/register/", "POST", {
            username: username,
            email: email,
            password: password,
            password2: password2,
        });

        if (result && result.ok) {

            alert("Akun berhasil dibuat. Silakan login.");

            window.location.hash = "#login";

        } else if (result) {

            alert(result.data.detail || "Registrasi gagal.");

        }

    });

}