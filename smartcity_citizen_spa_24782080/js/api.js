const API_BASE_URL = "http://103.151.63.87:8011";

async function requestAPI(endpoint, method = "GET", bodyData = null) {
    const accessToken = localStorage.getItem("access_token");

    const headers = {
        "Content-Type": "application/json",
    };

    if (accessToken) {
        headers["Authorization"] = `Bearer ${accessToken}`;
    }

    const options = {
        method: method,
        headers: headers,
    };

    if (bodyData !== null) {
        options.body = JSON.stringify(bodyData);
    }

    const response = await fetch(`${API_BASE_URL}${endpoint}`, options);

    let data = null;

    try {
        data = await response.json();
    } catch (error) {
        data = {};
    }

    return {
        status: response.status,
        ok: response.ok,
        data: data,
    };
}