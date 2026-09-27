const API_URL = "http://127.0.0.1:8000";
localStorage.removeItem("access_token");
localStorage.removeItem("resume_id");

const loginForm = document.getElementById("loginForm");
const message = document.getElementById("message");


loginForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    const formData = new URLSearchParams();

    formData.append("username", email);
    formData.append("password", password);

    try {
        const response = await fetch(`${API_URL}/auth/login`, {
            method: "POST",

            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            },

            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            message.textContent = data.detail || "Login failed";
            return;
        }

        localStorage.setItem("access_token", data.access_token);

        message.textContent = "Login successful!";

        window.location.href = "./index.html";

    } catch (error) {

        console.error(error);

        message.textContent =
            "Cannot connect to the server.";
    }
});