// ============================================================================
// API CONFIGURATION
// ============================================================================

// Sesuaikan dengan server Django lokal sesuai spesifikasi Playwright
const API_BASE_URL = "http://localhost:8000";

// ============================================================================
// GENERIC REQUEST FUNCTION
// ============================================================================
async function requestAPI(endpoint, method = "GET", bodyData = null) {

    // Ambil access token apabila tersedia
    const accessToken = localStorage.getItem("access_token");

    // Header default
    const headers = {
        "Content-Type": "application/json",
    };

    // Tambahkan Authorization apabila user sudah login
    if (accessToken) {
        headers["Authorization"] = `Bearer ${accessToken}`;
    }

    // Konfigurasi request
    const options = {
        method: method,
        headers: headers,
    };

    // Tambahkan body apabila ada
    if (bodyData !== null) {
        options.body = JSON.stringify(bodyData);
    }

    // Kirim request
    const response = await fetch(`${API_BASE_URL}${endpoint}`, options);

    // =========================================================================
    // INTERCEPTOR 401
    // Memenuhi AUTH-05 & AUTH-06
    // =========================================================================

    // Jangan jalankan interceptor ketika proses login
    if (
        response.status === 401 &&
        !endpoint.includes("/api/token/")
    ) {

        alert("Sesi Anda telah habis. Silakan login kembali.");

        // Hapus token yang digunakan Playwright
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
        localStorage.removeItem("username");

        // Redirect ke halaman login
        window.location.hash = "#login";

        // Tetap mengembalikan object agar aplikasi tidak error
        return {
            status: response.status,
            ok: false,
            data: {}
        };
    }

    // =========================================================================
    // PARSE JSON RESPONSE
    // =========================================================================

    let data = {};

    try {
        data = await response.json();
    } catch (error) {
        data = {};
    }

    // =========================================================================
    // RETURN RESULT
    // =========================================================================

    return {
        status: response.status,
        ok: response.ok,
        data: data,
    };
}