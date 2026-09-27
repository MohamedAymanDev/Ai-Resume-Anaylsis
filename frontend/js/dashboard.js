const API_URL = "http://127.0.0.1:8000";

const token = localStorage.getItem("access_token");


// ====================
// Protect Dashboard
// ====================

if (!token) {
    window.location.href = "./login.html";
}


// ====================
// Logout
// ====================

const logoutBtn = document.getElementById("logoutBtn");

if (logoutBtn) {

    logoutBtn.addEventListener("click", () => {

        localStorage.removeItem("access_token");

        window.location.href = "./login.html";
    });

}


// ====================
// Resume Upload
// ====================

const uploadBtn = document.getElementById("uploadBtn");
const analyzeBtn = document.getElementById("analyzeBtn");

let currentResumeId = null;


// ====================
// Upload Resume
// ====================

uploadBtn.addEventListener("click", async () => {

    const fileInput = document.getElementById("resumeFile");
    const message = document.getElementById("uploadMessage");

    const file = fileInput.files[0];

    if (!file) {

        message.textContent =
            "Please select a resume first.";

        return;
    }


    const formData = new FormData();

    formData.append("file", file);


    message.textContent =
        "Uploading resume...";


    try {

        const response = await fetch(
            `${API_URL}/resumes/upload`,
            {
                method: "POST",

                headers: {
                    Authorization: `Bearer ${token}`
                },

                body: formData
            }
        );


        const data = await response.json();


        if (!response.ok) {

            message.textContent =
                data.detail || "Upload failed.";

            return;
        }


        currentResumeId = data.id;


        // Save resume ID
        localStorage.setItem(
            "resume_id",
            currentResumeId
        );


        message.textContent =
            `Resume uploaded successfully. Resume ID: ${data.id}`;


        // Enable Analyze button
        analyzeBtn.disabled = false;


    } catch (error) {

        console.error(
            "UPLOAD ERROR:",
            error
        );

        message.textContent =
            `Error: ${error.message}`;
    }

});


// ====================
// Analyze Resume
// ====================

analyzeBtn.addEventListener("click", async () => {

    const message =
        document.getElementById("uploadMessage");


    if (!currentResumeId) {

        currentResumeId =
            localStorage.getItem("resume_id");
    }


    if (!currentResumeId) {

        message.textContent =
            "Please upload a resume first.";

        return;
    }


    message.textContent =
        "AI is analyzing your resume...";


    analyzeBtn.disabled = true;


    try {

        const response = await fetch(
            `${API_URL}/resumes/${currentResumeId}/analyze`,
            {
                method: "POST",

                headers: {
                    Authorization: `Bearer ${token}`
                }
            }
        );


        const data = await response.json();


        if (!response.ok) {

            message.textContent =
                data.detail || "Analysis failed.";

            analyzeBtn.disabled = false;

            return;
        }


        message.textContent =
            "Resume analyzed successfully!";


        console.log(
            "Resume Analysis:",
            data
        );


        // Display analysis on page
        displayAnalysis(data);


        analyzeBtn.disabled = false;


    } catch (error) {

        console.error(
            "ANALYZE ERROR:",
            error
        );

        message.textContent =
            `Error: ${error.message}`;

        analyzeBtn.disabled = false;
    }

});


// ====================
// Display Analysis
// ====================

function displayAnalysis(data) {

    const analysisContent =
        document.getElementById(
            "analysisContent"
        );


    // Safety check
    if (!analysisContent) {

        console.error(
            "analysisContent element was not found."
        );

        return;
    }


    analysisContent.innerHTML = `

        <div class="analysis-item">

            <h3>
                📝 Professional Summary
            </h3>

            <p>
                ${data.summary || "No summary available."}
            </p>

        </div>


        <div class="analysis-item">

            <h3>
                💻 Technical Skills
            </h3>

            <div class="skills-container">

                ${
                    (data.technical_skills || [])
                    .map(
                        skill =>
                            `<span class="skill-tag">${skill}</span>`
                    )
                    .join("")
                }

            </div>

        </div>


        <div class="analysis-item">

            <h3>
                🤝 Soft Skills
            </h3>

            <div class="skills-container">

                ${
                    (data.soft_skills || [])
                    .map(
                        skill =>
                            `<span class="skill-tag">${skill}</span>`
                    )
                    .join("")
                }

            </div>

        </div>


        <div class="analysis-item">

            <h3>
                🎓 Education
            </h3>

            <ul class="analysis-list">

                ${
                    (data.education || [])
                    .map(
                        item =>
                            `<li>${item}</li>`
                    )
                    .join("")
                }

            </ul>

        </div>


        <div class="analysis-item">

            <h3>
                💼 Experience
            </h3>

            <ul class="analysis-list">

                ${
                    (data.experience || [])
                    .map(
                        item =>
                            `<li>${item}</li>`
                    )
                    .join("")
                }

            </ul>

        </div>

    `;
}

// ====================
// Load Saved Analysis
// ====================

async function loadSavedAnalysis() {

    const resumeId =
        localStorage.getItem("resume_id");

    if (!resumeId) {
        return;
    }


    try {

        const response = await fetch(
            `${API_URL}/resumes/${resumeId}/analysis`,
            {
                method: "GET",

                headers: {
                    Authorization: `Bearer ${token}`
                }
            }
        );


        if (!response.ok) {
            return;
        }


        const data = await response.json();

        console.log(
            "Saved analysis:",
            data
        );


        displayAnalysis(data);


    } catch (error) {

        console.error(
            "LOAD ANALYSIS ERROR:",
            error
        );
    }
}


// Load saved analysis when dashboard opens
loadSavedAnalysis();
// ====================
// Job Search & Matching
// ====================

const searchJobsBtn =
    document.getElementById("searchJobsBtn");

if (searchJobsBtn) {

    searchJobsBtn.addEventListener("click", searchAndMatchJobs);

}


async function searchAndMatchJobs() {

    const searchInput =
        document.getElementById("jobSearch");

    const locationInput =
        document.getElementById("locationSearch");

    const message =
        document.getElementById("jobSearchMessage");

    const jobResults =
        document.getElementById("jobResults");


    let resumeId =
        localStorage.getItem("resume_id");


    if (!resumeId) {

        message.textContent =
            "Please upload and analyze your resume first.";

        return;
    }


    const query =
        searchInput.value.trim();

    const location =
        locationInput.value.trim();


    message.textContent =
        "Finding matching jobs...";

    jobResults.innerHTML = "";


    const params = new URLSearchParams();


    if (query) {
        params.append("q", query);
    }

    if (location) {
        params.append("location", location);
    }


    try {

        const response = await fetch(
            `${API_URL}/matching/resume/${resumeId}/search?${params.toString()}`,
            {
                method: "POST",

                headers: {
                    Authorization: `Bearer ${token}`
                }
            }
        );


        const data =
            await response.json();


        if (!response.ok) {

            message.textContent =
                data.detail || "Job search failed.";

            return;
        }


        message.textContent =
            `${data.length} job(s) found.`;


        if (data.length === 0) {

            jobResults.innerHTML = `
                <p class="empty-message">
                    No matching jobs found.
                </p>
            `;

            return;
        }


        displayJobResults(data);


    } catch (error) {

        console.error(
            "JOB SEARCH ERROR:",
            error
        );

        message.textContent =
            `Error: ${error.message}`;
    }
}


// ====================
// Display Job Results
// ====================
function displayJobResults(jobs) {

    const jobResults =
        document.getElementById("jobResults");

    jobResults.innerHTML =
        jobs.map(job => `

            <div class="job-card">

                <h3>
                    ${job.job_title}
                </h3>

                <p class="job-company">
                    ${job.company}
                    ${job.location ? ` • ${job.location}` : ""}
                </p>

                <div class="match-score">
                    Match Score: ${job.match_score}%
                </div>

                <div class="job-skills">

                    <h4>
                        ✅ Matched Skills
                    </h4>

                    ${
                        job.matched_skills.length > 0

                        ? job.matched_skills
                            .map(
                                skill =>
                                    `<span class="skill-tag">${skill}</span>`
                            )
                            .join(" ")

                        : "<p>No matched skills.</p>"
                    }

                </div>

                <div class="job-skills">

                    <h4>
                        ❌ Missing Skills
                    </h4>

                    ${
                        job.missing_skills.length > 0

                        ? job.missing_skills
                            .map(
                                skill =>
                                    `<span class="skill-tag">${skill}</span>`
                            )
                            .join(" ")

                        : "<p>No missing required skills.</p>"
                    }

                </div>

                <button
                    class="career-advice-btn"
                    onclick="getCareerAdvice(${job.job_id})"
                >
                    🚀 Get Career Advice
                </button>

            </div>

        `).join("");
}

// ====================
// Career Advisor
// ====================

async function getCareerAdvice(jobId) {

    const resumeId =
        localStorage.getItem("resume_id");

    if (!resumeId) {
        alert("Please upload and analyze your resume first.");
        return;
    }

    const jobResults =
        document.getElementById("jobResults");

    jobResults.insertAdjacentHTML(
        "beforeend",
        `
        <p id="careerLoading">
            🤖 AI is preparing your career advice...
        </p>
        `
    );

    try {

        const response = await fetch(
            `${API_URL}/career/resume/${resumeId}/job/${jobId}`,
            {
                method: "POST",

                headers: {
                    Authorization: `Bearer ${token}`
                }
            }
        );

        const data =
            await response.json();

        const loading =
            document.getElementById("careerLoading");

        if (loading) {
            loading.remove();
        }

        if (!response.ok) {

            alert(
                data.detail ||
                "Failed to get career advice."
            );

            return;
        }

        displayCareerAdvice(data);

    } catch (error) {

        console.error(
            "CAREER ADVICE ERROR:",
            error
        );

        const loading =
            document.getElementById("careerLoading");

        if (loading) {
            loading.remove();
        }

        alert(
            `Error: ${error.message}`
        );
    }
}
function displayCareerAdvice(data) {

    const advice = data.advice;

    const sources = data.sources || [];

    const existing =
        document.getElementById("careerAdvice");

    if (existing) {
        existing.remove();
    }

    const jobResults =
        document.getElementById("jobResults");

    const adviceHTML = `

        <div
            id="careerAdvice"
            class="analysis-section"
        >

            <h2>
                🚀 AI Career Advisor
            </h2>


            <div class="analysis-item">

                <h3>
                    💪 Strengths
                </h3>

                <ul class="analysis-list">

                    ${
                        advice.strengths
                            .map(
                                item =>
                                    `<li>${item}</li>`
                            )
                            .join("")
                    }

                </ul>

            </div>


            <div class="analysis-item">

                <h3>
                    ⚠️ Weaknesses
                </h3>

                <ul class="analysis-list">

                    ${
                        advice.weaknesses
                            .map(
                                item =>
                                    `<li>${item}</li>`
                            )
                            .join("")
                    }

                </ul>

            </div>


            <div class="analysis-item">

                <h3>
                    📚 Missing Skills
                </h3>

                <div class="skills-container">

                    ${
                        advice.missing_skills
                            .map(
                                skill =>
                                    `<span class="skill-tag">${skill}</span>`
                            )
                            .join("")
                    }

                </div>

            </div>


            <div class="analysis-item">

                <h3>
                    💡 Improvement Suggestions
                </h3>

                <ul class="analysis-list">

                    ${
                        advice.improvement_suggestions
                            .map(
                                item =>
                                    `<li>${item}</li>`
                            )
                            .join("")
                    }

                </ul>

            </div>


            <div class="analysis-item">

                <h3>
                    🎓 Recommended Certifications
                </h3>

                <ul class="analysis-list">

                    ${
                        advice.recommended_certifications
                            .map(
                                item =>
                                    `<li>${item}</li>`
                            )
                            .join("")
                    }

                </ul>

            </div>


            <div class="analysis-item">

                <h3>
                    📖 Learning Resources
                </h3>

                <ul class="analysis-list">

                    ${
                        advice.learning_resources
                            .map(
                                item =>
                                    `<li>${item}</li>`
                            )
                            .join("")
                    }

                </ul>

            </div>


            <div class="analysis-item">

                <h3>
                    🔎 RAG Sources
                </h3>

                <ul class="analysis-list">

                    ${
                        sources
                            .map(
                                source =>
                                    `<li>${source}</li>`
                            )
                            .join("")
                    }

                </ul>

            </div>

        </div>
    `;

    jobResults.insertAdjacentHTML(
        "afterend",
        adviceHTML
    );
}
// ====================
// Load Current User
// ====================

async function loadCurrentUser() {

    const userName =
        document.getElementById("userName");

    if (!userName) {
        return;
    }

    try {

        const response = await fetch(
            `${API_URL}/auth/me`,
            {
                method: "GET",

                headers: {
                    Authorization: `Bearer ${token}`
                }
            }
        );

        const data =
            await response.json();


        if (!response.ok) {

            console.error(
                "Failed to load user:",
                data
            );

            return;
        }


        userName.textContent =
            data.full_name;


    } catch (error) {

        console.error(
            "USER LOAD ERROR:",
            error
        );

    }
}


loadCurrentUser();

const navTabs =
    document.querySelectorAll(".nav-tab");

const dashboardSections =
    document.querySelectorAll(".dashboard-section");


navTabs.forEach(tab => {

    tab.addEventListener("click", () => {

        const targetSection =
            tab.dataset.section;


        // Remove active state from all tabs
        navTabs.forEach(item => {
            item.classList.remove("active");
        });


        // Hide all sections
        dashboardSections.forEach(section => {
            section.classList.remove("active-section");
        });


        // Activate clicked tab
        tab.classList.add("active");


        // Show selected section
        const section =
            document.getElementById(targetSection);

        if (section) {
            section.classList.add("active-section");
        }

    });

});
const addJobBtn =
    document.getElementById("addJobBtn");

if (addJobBtn) {
    addJobBtn.addEventListener("click", addJob);
}


async function addJob() {

    const message =
        document.getElementById("jobManagementMessage");

    const editingJobId =
        document.getElementById("addJobBtn").dataset.editingJobId;    


    const title =
        document.getElementById("jobTitle").value.trim();

    const company =
        document.getElementById("jobCompany").value.trim();

    const location =
        document.getElementById("jobLocation").value.trim();

    const description =
        document.getElementById("jobDescription").value.trim();

    const requiredSkills =
        document.getElementById("requiredSkills").value
            .split(",")
            .map(skill => skill.trim())
            .filter(Boolean);

    const preferredSkills =
        document.getElementById("preferredSkills").value
            .split(",")
            .map(skill => skill.trim())
            .filter(Boolean);

    const experienceLevel =
        document.getElementById("experienceLevel").value.trim();

    const education =
        document.getElementById("jobEducation").value.trim();


    if (!title || !company || !description) {

        message.textContent =
            "Please fill in Job Title, Company, and Description.";

        return;
    }


    message.textContent =
        "Adding job...";


    try {

        const response = await fetch(
            editingJobId
                ? `${API_URL}/jobs/${editingJobId}`
                : `${API_URL}/jobs/`,
            {
                method: editingJobId
                    ? "PUT"
                    : "POST",

                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`
                },

                body: JSON.stringify({

                    title: title,

                    company: company,

                    location: location || null,

                    description: description,

                    required_skills: requiredSkills,

                    preferred_skills: preferredSkills,

                    experience_level:
                        experienceLevel || null,

                    education:
                        education || null

                })
            }
        );


        const data =
            await response.json();


        if (!response.ok) {

            message.textContent =
                data.detail || "Failed to add job.";

            return;
        }


        message.textContent =
                editingJobId
                    ? "Job updated successfully!"
                    : "Job added successfully!";

            clearJobForm();

            delete document
                .getElementById("addJobBtn")
                .dataset.editingJobId;

            document.getElementById("addJobBtn").textContent =
                "Add Job";

            loadManagedJobs();


    } catch (error) {

        console.error(
            "ADD JOB ERROR:",
            error
        );

        message.textContent =
            `Error: ${error.message}`;
    }
}
// ====================
// Load Managed Jobs
// ====================

const loadJobsBtn =
    document.getElementById("loadJobsBtn");

if (loadJobsBtn) {

    loadJobsBtn.addEventListener(
        "click",
        loadManagedJobs
    );

}


async function loadManagedJobs() {

    const container =
        document.getElementById("managedJobs");


    if (!container) {
        return;
    }


    container.innerHTML = `
        <p class="empty-message">
            Loading jobs...
        </p>
    `;


    try {

        const response = await fetch(
            `${API_URL}/jobs/`,
            {
                method: "GET",

                headers: {
                    Authorization: `Bearer ${token}`
                }
            }
        );


        const data =
            await response.json();


        if (!response.ok) {

            container.innerHTML = `
                <p class="empty-message">
                    ${data.detail || "Failed to load jobs."}
                </p>
            `;

            return;
        }


        displayManagedJobs(data);


    } catch (error) {

        console.error(
            "LOAD JOBS ERROR:",
            error
        );


        container.innerHTML = `
            <p class="empty-message">
                Error: ${error.message}
            </p>
        `;
    }
}


// ====================
// Display Managed Jobs
// ====================

function displayManagedJobs(jobs) {

    const container =
        document.getElementById("managedJobs");


    if (!container) {
        return;
    }


    if (jobs.length === 0) {

        container.innerHTML = `
            <p class="empty-message">
                No jobs available.
            </p>
        `;

        return;
    }


    container.innerHTML =
        jobs.map(job => `

            <div class="managed-job-card">

                <h3>
                    ${job.title}
                </h3>


                <p class="managed-job-company">

                    ${job.company}

                    ${
                        job.location
                            ? ` • ${job.location}`
                            : ""
                    }

                </p>


                <p class="managed-job-description">
                    ${job.description}
                </p>


                <div class="job-skills">

                    <h4>
                        Required Skills
                    </h4>


                    ${
                        (job.required_skills || [])
                            .map(
                                skill =>
                                    `<span class="skill-tag">${skill}</span>`
                            )
                            .join(" ")
                    }

                </div>


                <div class="job-skills">

                    <h4>
                        Preferred Skills
                    </h4>


                    ${
                        (job.preferred_skills || []).length > 0

                        ?

                        job.preferred_skills
                            .map(
                                skill =>
                                    `<span class="skill-tag">${skill}</span>`
                            )
                            .join(" ")

                        :

                        "<p>No preferred skills.</p>"
                    }

                </div>


                                <div class="job-actions">

                    <button
                        class="edit-job-btn"
                        onclick="editJob(${job.id})"
                    >
                        ✏️ Edit
                    </button>

                    <button
                        class="delete-job-btn"
                        onclick="deleteJob(${job.id})"
                    >
                        🗑️ Delete
                    </button>

                </div>

            </div>

        `).join("");
}


// ====================
// Delete Job
// ====================

async function deleteJob(jobId) {

    const confirmed =
        confirm(
            "Are you sure you want to delete this job?"
        );


    if (!confirmed) {
        return;
    }


    try {

        const response = await fetch(
            `${API_URL}/jobs/${jobId}`,
            {
                method: "DELETE",

                headers: {
                    Authorization: `Bearer ${token}`
                }
            }
        );


        if (!response.ok) {

            const data =
                await response.json();

            alert(
                data.detail ||
                "Failed to delete job."
            );

            return;
        }


        loadManagedJobs();


    } catch (error) {

        console.error(
            "DELETE JOB ERROR:",
            error
        );


        alert(
            `Error: ${error.message}`
        );
    }
}


// ====================
// Clear Job Form
// ====================

function clearJobForm() {

    document.getElementById("jobTitle").value = "";

    document.getElementById("jobCompany").value = "";

    document.getElementById("jobLocation").value = "";

    document.getElementById("jobDescription").value = "";

    document.getElementById("requiredSkills").value = "";

    document.getElementById("preferredSkills").value = "";

    document.getElementById("experienceLevel").value = "";

    document.getElementById("jobEducation").value = "";
}
// ====================
// Edit Job
// ====================

async function editJob(jobId) {

    try {

        const response = await fetch(
            `${API_URL}/jobs/${jobId}`,
            {
                method: "GET",

                headers: {
                    Authorization: `Bearer ${token}`
                }
            }
        );


        const job =
            await response.json();


        if (!response.ok) {

            alert(
                job.detail || "Failed to load job."
            );

            return;
        }


        // Fill form with job data

        document.getElementById("jobTitle").value =
            job.title || "";

        document.getElementById("jobCompany").value =
            job.company || "";

        document.getElementById("jobLocation").value =
            job.location || "";

        document.getElementById("jobDescription").value =
            job.description || "";

        document.getElementById("requiredSkills").value =
            (job.required_skills || []).join(", ");

        document.getElementById("preferredSkills").value =
            (job.preferred_skills || []).join(", ");

        document.getElementById("experienceLevel").value =
            job.experience_level || "";

        document.getElementById("jobEducation").value =
            job.education || "";


        // Save ID of job being edited

        document
            .getElementById("addJobBtn")
            .dataset.editingJobId = jobId;


        // Change button text

        document.getElementById("addJobBtn").textContent =
            "Update Job";


        // Scroll to form

        document
            .querySelector(".job-form")
            .scrollIntoView({
                behavior: "smooth"
            });


    } catch (error) {

        console.error(
            "EDIT JOB ERROR:",
            error
        );

        alert(
            `Error: ${error.message}`
        );
    }
}