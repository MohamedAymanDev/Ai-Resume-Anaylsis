const API_URL = "http://127.0.0.1:8000";

const registerForm =
    document.getElementById("registerForm");

const message =
    document.getElementById("message");


registerForm.addEventListener(
    "submit",
    async (event) => {

        event.preventDefault();


        const fullName =
            document.getElementById("fullName").value;

        const email =
            document.getElementById("email").value;

        const password =
            document.getElementById("password").value;


        message.textContent =
            "Creating account...";


        try {

            const response = await fetch(
                `${API_URL}/auth/register`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify({
                        full_name: fullName,
                        email: email,
                        password: password
                    })
                }
            );


            const data =
                await response.json();


            if (!response.ok) {

                message.textContent =
                    data.detail || "Registration failed.";

                return;
            }


            message.textContent =
                "Account created successfully!";


            setTimeout(() => {

                window.location.href =
                    "./login.html";

            }, 1000);


        } catch (error) {

            console.error(
                "REGISTER ERROR:",
                error
            );

            message.textContent =
                `Error: ${error.message}`;
        }

    }
);