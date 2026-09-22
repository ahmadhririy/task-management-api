const API_URL = "http://127.0.0.1:8000";


// ================= ELEMENTS =================

const authPage = document.getElementById("auth-page");
const dashboardPage = document.getElementById("dashboard-page");

const loginFormBox = document.getElementById("login-form");
const registerFormBox = document.getElementById("register-form");

const showRegisterBtn = document.getElementById("show-register");
const showLoginBtn = document.getElementById("show-login");

const loginForm = document.getElementById("loginForm");
const registerForm = document.getElementById("registerForm");

const logoutBtn = document.getElementById("logout-btn");

const userName = document.getElementById("user-name");
const avatar = document.querySelector(".avatar");
const profileButton = document.getElementById("profile-button");

const dashboardNav = document.getElementById("dashboard-nav");
const projectsNav = document.getElementById("projects-nav");
const tasksNav = document.getElementById("tasks-nav");
const profileNav = document.getElementById("profile-nav");

const pageTitle = document.getElementById("page-title");
const pageSubtitle = document.getElementById("page-subtitle");

const statsSection = document.getElementById("stats-section");
const projectsSection = document.getElementById("projects-section");
const tasksSection = document.getElementById("tasks-section");
const profileSection = document.getElementById("profile-section");

const projectsContainer = document.getElementById("projects-container");
const tasksContainer = document.getElementById("tasks-container");
const tasksSubtitle = document.getElementById("tasks-subtitle");

const projectCount = document.getElementById("project-count");
const taskCount = document.getElementById("task-count");
const completedCount = document.getElementById("completed-count");


// ================= PROJECT MODAL =================

const newProjectBtn = document.getElementById("new-project-btn");
const projectModal = document.getElementById("project-modal");
const closeProjectModal = document.getElementById("close-project-modal");
const projectForm = document.getElementById("projectForm");
const projectModalTitle = document.getElementById("project-modal-title");


// ================= TASK MODAL =================

const newTaskBtn = document.getElementById("new-task-btn");
const taskModal = document.getElementById("task-modal");
const closeTaskModal = document.getElementById("close-task-modal");
const taskForm = document.getElementById("taskForm");
const taskModalTitle = document.getElementById("task-modal-title");


// ================= PROFILE =================

const profileForm = document.getElementById("profileForm");
const passwordForm = document.getElementById("passwordForm");

const profileName = document.getElementById("profile-name");
const profileEmail = document.getElementById("profile-email");

const profileDisplayName =
    document.getElementById("profile-display-name");

const profileDisplayEmail =
    document.getElementById("profile-display-email");

const profileAvatar =
    document.getElementById("profile-avatar");

const deleteAccountBtn =
    document.getElementById("delete-account-btn");


// ================= NOTIFICATIONS =================

const toastContainer =
    document.getElementById("toast-container");

const confirmModal =
    document.getElementById("confirm-modal");

const confirmTitle =
    document.getElementById("confirm-title");

const confirmMessage =
    document.getElementById("confirm-message");

const confirmCancel =
    document.getElementById("confirm-cancel");

const confirmAction =
    document.getElementById("confirm-action");


// ================= STATE =================

let currentProjectId = null;
let editingProjectId = null;
let editingTaskId = null;

let projectsCache = [];


// ================= HELPERS =================

function getToken() {
    return localStorage.getItem("token");
}


function authHeaders() {
    return {
        "Authorization": `Bearer ${getToken()}`
    };
}


function jsonAuthHeaders() {
    return {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${getToken()}`
    };
}


function escapeHTML(value) {
    const div = document.createElement("div");

    div.textContent = value ?? "";

    return div.innerHTML;
}


function getErrorMessage(data) {
    if (!data) {
        return "Something went wrong.";
    }

    if (typeof data.detail === "string") {
        return data.detail;
    }

    if (Array.isArray(data.detail)) {
        return data.detail
            .map(error => error.msg)
            .join("\n");
    }

    return "Something went wrong.";
}


// ================= TOAST =================

function showToast(message, type = "success") {
    const toast = document.createElement("div");

    toast.className = `toast ${type}`;

    let icon = "✓";

    if (type === "error") {
        icon = "!";
    }

    if (type === "info") {
        icon = "i";
    }

    toast.innerHTML = `
        <div class="toast-icon">
            ${icon}
        </div>

        <div class="toast-message"></div>
    `;

    toast.querySelector(
        ".toast-message"
    ).textContent = message;

    toastContainer.appendChild(toast);

    setTimeout(() => {
        toast.classList.add("hide");

        setTimeout(() => {
            toast.remove();
        }, 250);

    }, 3000);
}


// ================= CUSTOM CONFIRM =================

function showConfirm({
    title = "Confirm Action",
    message = "Are you sure?",
    confirmText = "Confirm"
}) {
    return new Promise(resolve => {

        confirmTitle.textContent = title;
        confirmMessage.textContent = message;
        confirmAction.textContent = confirmText;

        confirmModal.classList.remove("hidden");

        function cleanup(result) {
            confirmModal.classList.add("hidden");

            confirmAction.removeEventListener(
                "click",
                confirmHandler
            );

            confirmCancel.removeEventListener(
                "click",
                cancelHandler
            );

            resolve(result);
        }

        function confirmHandler() {
            cleanup(true);
        }

        function cancelHandler() {
            cleanup(false);
        }

        confirmAction.addEventListener(
            "click",
            confirmHandler
        );

        confirmCancel.addEventListener(
            "click",
            cancelHandler
        );
    });
}


// ================= LOGOUT =================

function logoutUser() {
    localStorage.removeItem("token");

    currentProjectId = null;
    editingProjectId = null;
    editingTaskId = null;

    projectsCache = [];

    dashboardPage.classList.add("hidden");
    authPage.classList.remove("hidden");

    loginFormBox.classList.remove("hidden");
    registerFormBox.classList.add("hidden");
}


// ================= LOGIN / REGISTER SWITCH =================

showRegisterBtn.addEventListener("click", () => {
    loginFormBox.classList.add("hidden");
    registerFormBox.classList.remove("hidden");
});


showLoginBtn.addEventListener("click", () => {
    registerFormBox.classList.add("hidden");
    loginFormBox.classList.remove("hidden");
});


// ================= REGISTER =================

registerForm.addEventListener("submit", async event => {
    event.preventDefault();

    const name =
        document.getElementById("register-name").value;

    const email =
        document.getElementById("register-email").value;

    const password =
        document.getElementById("register-password").value;

    try {
        const response = await fetch(
            `${API_URL}/users/register`,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    name,
                    email,
                    password
                })
            }
        );

        const data = await response.json();

        if (!response.ok) {
            showToast(
                getErrorMessage(data),
                "error"
            );

            return;
        }

        showToast(
            "Account created successfully!",
            "success"
        );

        registerForm.reset();

        registerFormBox.classList.add("hidden");
        loginFormBox.classList.remove("hidden");

    } catch (error) {
        console.error(error);

        showToast(
            "Could not connect to the server.",
            "error"
        );
    }
});


// ================= LOGIN =================

loginForm.addEventListener("submit", async event => {
    event.preventDefault();

    const email =
        document.getElementById("login-email").value;

    const password =
        document.getElementById("login-password").value;

    try {
        const response = await fetch(
            `${API_URL}/users/login`,
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    email,
                    password
                })
            }
        );

        const data = await response.json();

        if (!response.ok) {
            showToast(
                getErrorMessage(data),
                "error"
            );

            return;
        }

        localStorage.setItem(
            "token",
            data.access_token
        );

        loginForm.reset();

        await openDashboard();

        showToast(
            "Logged in successfully!",
            "success"
        );

    } catch (error) {
        console.error(error);

        showToast(
            "Could not connect to the server.",
            "error"
        );
    }
});


// ================= LOGOUT BUTTON =================

logoutBtn.addEventListener("click", () => {
    logoutUser();

    showToast(
        "Logged out successfully.",
        "info"
    );
});


// ================= CURRENT USER =================

async function getCurrentUser() {
    if (!getToken()) {
        return null;
    }

    try {
        const response = await fetch(
            `${API_URL}/users/me`,
            {
                headers: authHeaders()
            }
        );

        if (!response.ok) {
            if (
                response.status === 401 ||
                response.status === 403
            ) {
                localStorage.removeItem("token");
            }

            return null;
        }

        return await response.json();

    } catch (error) {
        console.error(error);

        return null;
    }
}


function updateUserUI(user) {
    userName.textContent = user.name;

    const firstLetter = user.name
        ? user.name.charAt(0).toUpperCase()
        : "U";

    avatar.textContent = firstLetter;
    profileAvatar.textContent = firstLetter;

    profileDisplayName.textContent = user.name;
    profileDisplayEmail.textContent = user.email;

    profileName.value = user.name;
    profileEmail.value = user.email;
}


// ================= DASHBOARD =================

async function openDashboard() {
    const user = await getCurrentUser();

    if (!user) {
        dashboardPage.classList.add("hidden");
        authPage.classList.remove("hidden");

        return;
    }

    authPage.classList.add("hidden");
    dashboardPage.classList.remove("hidden");

    updateUserUI(user);

    showDashboardPage();

    await loadProjects();
}


// ================= NAVIGATION =================

function setActiveNav(button) {
    dashboardNav.classList.remove("active");
    projectsNav.classList.remove("active");
    tasksNav.classList.remove("active");
    profileNav.classList.remove("active");

    button.classList.add("active");
}


function hideAllSections() {
    statsSection.classList.add("hidden");
    projectsSection.classList.add("hidden");
    tasksSection.classList.add("hidden");
    profileSection.classList.add("hidden");
}


function showDashboardPage() {
    setActiveNav(dashboardNav);

    pageTitle.textContent = "Dashboard";

    pageSubtitle.textContent =
        "Manage your projects and tasks.";

    hideAllSections();

    statsSection.classList.remove("hidden");
    projectsSection.classList.remove("hidden");
    tasksSection.classList.remove("hidden");
}


function showProjectsPage() {
    setActiveNav(projectsNav);

    pageTitle.textContent = "Projects";

    pageSubtitle.textContent =
        "Create and manage your projects.";

    hideAllSections();

    projectsSection.classList.remove("hidden");
}


function showTasksPage() {
    setActiveNav(tasksNav);

    pageTitle.textContent = "Tasks";

    pageSubtitle.textContent =
        "Manage tasks for your selected project.";

    hideAllSections();

    tasksSection.classList.remove("hidden");
}


async function showProfilePage() {
    setActiveNav(profileNav);

    pageTitle.textContent = "Profile";

    pageSubtitle.textContent =
        "Manage your account information.";

    hideAllSections();

    profileSection.classList.remove("hidden");

    const user = await getCurrentUser();

    if (!user) {
        logoutUser();

        showToast(
            "Your session has expired. Please login again.",
            "error"
        );

        return;
    }

    updateUserUI(user);
}


dashboardNav.addEventListener(
    "click",
    async () => {
        showDashboardPage();
        await loadProjects();
    }
);


projectsNav.addEventListener(
    "click",
    async () => {
        showProjectsPage();
        await loadProjects();
    }
);


tasksNav.addEventListener(
    "click",
    async () => {
        showTasksPage();

        if (currentProjectId) {
            await loadTasks(currentProjectId);

        } else {
            newTaskBtn.classList.add("hidden");

            tasksSubtitle.textContent =
                "Select a project first";

            tasksContainer.innerHTML = `
                <p class="empty-message">
                    Go to Projects and open a project first.
                </p>
            `;
        }
    }
);


profileNav.addEventListener(
    "click",
    showProfilePage
);


profileButton.addEventListener(
    "click",
    showProfilePage
);


// ================= LOAD PROJECTS =================

async function loadProjects() {
    try {
        const response = await fetch(
            `${API_URL}/projects`,
            {
                headers: authHeaders()
            }
        );

        if (
            response.status === 401 ||
            response.status === 403
        ) {
            logoutUser();

            showToast(
                "Your session has expired. Please login again.",
                "error"
            );

            return;
        }

        const projects = await response.json();

        if (!response.ok) {
            showToast(
                getErrorMessage(projects),
                "error"
            );

            return;
        }

        projectsCache = projects;

        renderProjects(projects);

        projectCount.textContent = projects.length;

        await loadAllTaskStats(projects);

    } catch (error) {
        console.error(error);

        showToast(
            "Could not load projects.",
            "error"
        );
    }
}


// ================= RENDER PROJECTS =================

function renderProjects(projects) {
    projectsContainer.innerHTML = "";

    if (projects.length === 0) {
        projectsContainer.innerHTML = `
            <p class="empty-message">
                No projects yet. Create your first project.
            </p>
        `;

        return;
    }

    projects.forEach(project => {
        const card =
            document.createElement("article");

        card.className = "project-card";

        card.innerHTML = `
            <div class="project-card-header">

                <span class="project-icon">
                    ${escapeHTML(
                        project.name
                            .charAt(0)
                            .toUpperCase()
                    )}
                </span>

            </div>

            <h3>
                ${escapeHTML(project.name)}
            </h3>

            <p>
                ${escapeHTML(
                    project.description ||
                    "No description"
                )}
            </p>

            <div class="project-footer">

                <button
                    class="open-project-btn"
                    data-action="open"
                    data-id="${project.id}"
                >
                    Open
                </button>

                <div class="project-actions">

                    <button
                        class="edit-btn"
                        data-action="edit"
                        data-id="${project.id}"
                    >
                        Edit
                    </button>

                    <button
                        class="delete-btn"
                        data-action="delete"
                        data-id="${project.id}"
                    >
                        Delete
                    </button>

                </div>

            </div>
        `;

        projectsContainer.appendChild(card);
    });
}


// ================= PROJECT BUTTONS =================

projectsContainer.addEventListener(
    "click",
    async event => {
        const button = event.target.closest(
            "button[data-action]"
        );

        if (!button) {
            return;
        }

        const projectId =
            Number(button.dataset.id);

        const action =
            button.dataset.action;

        if (action === "open") {
            await openProject(projectId);
        }

        if (action === "edit") {
            openEditProjectModal(projectId);
        }

        if (action === "delete") {
            await deleteProject(projectId);
        }
    }
);


// ================= OPEN PROJECT =================

async function openProject(projectId) {
    currentProjectId = projectId;

    const project = projectsCache.find(
        project => project.id === projectId
    );

    showTasksPage();

    newTaskBtn.classList.remove("hidden");

    if (project) {
        tasksSubtitle.textContent =
            `Project: ${project.name}`;
    } else {
        tasksSubtitle.textContent =
            "Project tasks";
    }

    await loadTasks(projectId);
}


// ================= PROJECT MODAL =================

newProjectBtn.addEventListener(
    "click",
    () => {
        editingProjectId = null;

        projectModalTitle.textContent =
            "Create Project";

        projectForm.reset();

        projectModal.classList.remove("hidden");
    }
);


closeProjectModal.addEventListener(
    "click",
    () => {
        projectModal.classList.add("hidden");
    }
);


projectModal.addEventListener(
    "click",
    event => {
        if (event.target === projectModal) {
            projectModal.classList.add("hidden");
        }
    }
);


function openEditProjectModal(projectId) {
    const project = projectsCache.find(
        project => project.id === projectId
    );

    if (!project) {
        return;
    }

    editingProjectId = projectId;

    projectModalTitle.textContent =
        "Edit Project";

    document.getElementById(
        "project-name"
    ).value = project.name;

    document.getElementById(
        "project-description"
    ).value = project.description || "";

    projectModal.classList.remove("hidden");
}


// ================= CREATE / UPDATE PROJECT =================

projectForm.addEventListener(
    "submit",
    async event => {
        event.preventDefault();

        const name =
            document.getElementById(
                "project-name"
            ).value;

        const description =
            document.getElementById(
                "project-description"
            ).value;

        const isEditing =
            editingProjectId !== null;

        const url = isEditing
            ? `${API_URL}/projects/${editingProjectId}`
            : `${API_URL}/projects`;

        const method =
            isEditing ? "PATCH" : "POST";

        try {
            const response = await fetch(
                url,
                {
                    method,

                    headers: jsonAuthHeaders(),

                    body: JSON.stringify({
                        name,
                        description
                    })
                }
            );

            const data =
                await response.json();

            if (!response.ok) {
                showToast(
                    getErrorMessage(data),
                    "error"
                );

                return;
            }

            projectForm.reset();

            projectModal.classList.add(
                "hidden"
            );

            editingProjectId = null;

            showToast(
                isEditing
                    ? "Project updated successfully!"
                    : "Project created successfully!",
                "success"
            );

            await loadProjects();

        } catch (error) {
            console.error(error);

            showToast(
                "Could not save project.",
                "error"
            );
        }
    }
);


// ================= DELETE PROJECT =================

async function deleteProject(projectId) {
    const confirmed = await showConfirm({
        title: "Delete Project?",

        message:
            "This project and all of its tasks will be permanently deleted.",

        confirmText: "Delete Project"
    });

    if (!confirmed) {
        return;
    }

    try {
        const response = await fetch(
            `${API_URL}/projects/${projectId}`,
            {
                method: "DELETE",
                headers: authHeaders()
            }
        );

        const data = await response.json();

        if (!response.ok) {
            showToast(
                getErrorMessage(data),
                "error"
            );

            return;
        }

        if (currentProjectId === projectId) {
            currentProjectId = null;

            newTaskBtn.classList.add(
                "hidden"
            );

            tasksSubtitle.textContent =
                "Select a project to view its tasks";

            tasksContainer.innerHTML = `
                <p class="empty-message">
                    Open a project to view its tasks.
                </p>
            `;
        }

        showToast(
            "Project deleted successfully.",
            "success"
        );

        await loadProjects();

    } catch (error) {
        console.error(error);

        showToast(
            "Could not delete project.",
            "error"
        );
    }
}


// ================= LOAD TASKS =================

async function loadTasks(projectId) {
    try {
        const response = await fetch(
            `${API_URL}/projects/${projectId}/tasks`,
            {
                headers: authHeaders()
            }
        );

        const tasks =
            await response.json();

        if (!response.ok) {
            showToast(
                getErrorMessage(tasks),
                "error"
            );

            return;
        }

        renderTasks(tasks, projectId);

    } catch (error) {
        console.error(error);

        showToast(
            "Could not load tasks.",
            "error"
        );
    }
}


// ================= RENDER TASKS =================

function renderTasks(tasks, projectId) {
    tasksContainer.innerHTML = "";

    if (tasks.length === 0) {
        tasksContainer.innerHTML = `
            <p class="empty-message">
                No tasks in this project.
                Click New Task to create one.
            </p>
        `;

        return;
    }

    tasks.forEach(task => {
        const item =
            document.createElement("div");

        item.className = "task-item";

        const statusClass =
            task.status === "in_progress"
                ? "in-progress"
                : task.status;

        const statusText =
            task.status === "in_progress"
                ? "In Progress"
                : task.status === "done"
                    ? "Done"
                    : "Todo";

        item.innerHTML = `
            <div class="task-info">

                <h3>
                    ${escapeHTML(task.title)}
                </h3>

                <p>
                    ${escapeHTML(
                        task.description ||
                        "No description"
                    )}
                </p>

            </div>

            <div class="task-actions">

                <span class="status ${statusClass}">
                    ${statusText}
                </span>

                <button
                    class="edit-btn"
                    data-action="edit-task"
                    data-project-id="${projectId}"
                    data-task-id="${task.id}"
                >
                    Edit
                </button>

                <button
                    class="delete-btn"
                    data-action="delete-task"
                    data-project-id="${projectId}"
                    data-task-id="${task.id}"
                >
                    Delete
                </button>

            </div>
        `;

        tasksContainer.appendChild(item);
    });
}


// ================= TASK BUTTONS =================

tasksContainer.addEventListener(
    "click",
    async event => {
        const button = event.target.closest(
            "button[data-action]"
        );

        if (!button) {
            return;
        }

        const projectId =
            Number(button.dataset.projectId);

        const taskId =
            Number(button.dataset.taskId);

        if (
            button.dataset.action ===
            "edit-task"
        ) {
            await openEditTaskModal(
                projectId,
                taskId
            );
        }

        if (
            button.dataset.action ===
            "delete-task"
        ) {
            await deleteTask(
                projectId,
                taskId
            );
        }
    }
);


// ================= NEW TASK =================

newTaskBtn.addEventListener(
    "click",
    () => {
        if (!currentProjectId) {
            showToast(
                "Open a project first.",
                "error"
            );

            return;
        }

        editingTaskId = null;

        taskModalTitle.textContent =
            "Create Task";

        taskForm.reset();

        document.getElementById(
            "task-status"
        ).value = "todo";

        taskModal.classList.remove("hidden");
    }
);


// ================= TASK MODAL =================

closeTaskModal.addEventListener(
    "click",
    () => {
        taskModal.classList.add("hidden");
    }
);


taskModal.addEventListener(
    "click",
    event => {
        if (event.target === taskModal) {
            taskModal.classList.add("hidden");
        }
    }
);


// ================= EDIT TASK =================

async function openEditTaskModal(
    projectId,
    taskId
) {
    try {
        const response = await fetch(
            `${API_URL}/projects/${projectId}/tasks/${taskId}`,
            {
                headers: authHeaders()
            }
        );

        const task =
            await response.json();

        if (!response.ok) {
            showToast(
                getErrorMessage(task),
                "error"
            );

            return;
        }

        currentProjectId = projectId;
        editingTaskId = taskId;

        taskModalTitle.textContent =
            "Edit Task";

        document.getElementById(
            "task-title"
        ).value = task.title;

        document.getElementById(
            "task-description"
        ).value = task.description || "";

        document.getElementById(
            "task-status"
        ).value = task.status;

        taskModal.classList.remove("hidden");

    } catch (error) {
        console.error(error);

        showToast(
            "Could not load task.",
            "error"
        );
    }
}


// ================= CREATE / UPDATE TASK =================

taskForm.addEventListener(
    "submit",
    async event => {
        event.preventDefault();

        if (!currentProjectId) {
            return;
        }

        const title =
            document.getElementById(
                "task-title"
            ).value;

        const description =
            document.getElementById(
                "task-description"
            ).value;

        const taskStatus =
            document.getElementById(
                "task-status"
            ).value;

        const isEditing =
            editingTaskId !== null;

        const url = isEditing
            ? `${API_URL}/projects/${currentProjectId}/tasks/${editingTaskId}`
            : `${API_URL}/projects/${currentProjectId}/tasks`;

        const method =
            isEditing ? "PATCH" : "POST";

        try {
            const response = await fetch(
                url,
                {
                    method,

                    headers: jsonAuthHeaders(),

                    body: JSON.stringify({
                        title,
                        description,
                        status: taskStatus
                    })
                }
            );

            const data =
                await response.json();

            if (!response.ok) {
                showToast(
                    getErrorMessage(data),
                    "error"
                );

                return;
            }

            taskForm.reset();

            taskModal.classList.add(
                "hidden"
            );

            editingTaskId = null;

            showToast(
                isEditing
                    ? "Task updated successfully!"
                    : "Task created successfully!",
                "success"
            );

            await loadTasks(
                currentProjectId
            );

            await loadProjects();

        } catch (error) {
            console.error(error);

            showToast(
                "Could not save task.",
                "error"
            );
        }
    }
);


// ================= DELETE TASK =================

async function deleteTask(
    projectId,
    taskId
) {
    const confirmed = await showConfirm({
        title: "Delete Task?",

        message:
            "This task will be permanently deleted.",

        confirmText: "Delete Task"
    });

    if (!confirmed) {
        return;
    }

    try {
        const response = await fetch(
            `${API_URL}/projects/${projectId}/tasks/${taskId}`,
            {
                method: "DELETE",
                headers: authHeaders()
            }
        );

        const data =
            await response.json();

        if (!response.ok) {
            showToast(
                getErrorMessage(data),
                "error"
            );

            return;
        }

        showToast(
            "Task deleted successfully.",
            "success"
        );

        await loadTasks(projectId);
        await loadProjects();

    } catch (error) {
        console.error(error);

        showToast(
            "Could not delete task.",
            "error"
        );
    }
}


// ================= PROFILE UPDATE =================

profileForm.addEventListener(
    "submit",
    async event => {
        event.preventDefault();

        const name =
            profileName.value.trim();

        const email =
            profileEmail.value.trim();

        try {
            const response = await fetch(
                `${API_URL}/users/me`,
                {
                    method: "PATCH",

                    headers:
                        jsonAuthHeaders(),

                    body: JSON.stringify({
                        name,
                        email
                    })
                }
            );

            const data =
                await response.json();

            if (!response.ok) {
                showToast(
                    getErrorMessage(data),
                    "error"
                );

                return;
            }

            updateUserUI(data);

            showToast(
                "Profile updated successfully!",
                "success"
            );

        } catch (error) {
            console.error(error);

            showToast(
                "Could not update profile.",
                "error"
            );
        }
    }
);


// ================= CHANGE PASSWORD =================

passwordForm.addEventListener(
    "submit",
    async event => {
        event.preventDefault();

        const currentPassword =
            document.getElementById(
                "current-password"
            ).value;

        const newPassword =
            document.getElementById(
                "new-password"
            ).value;

        const confirmPassword =
            document.getElementById(
                "confirm-password"
            ).value;

        if (newPassword !== confirmPassword) {
            showToast(
                "New passwords do not match.",
                "error"
            );

            return;
        }

        if (newPassword.length < 8) {
            showToast(
                "New password must be at least 8 characters.",
                "error"
            );

            return;
        }

        try {
            const response = await fetch(
                `${API_URL}/users/me/password`,
                {
                    method: "PATCH",

                    headers:
                        jsonAuthHeaders(),

                    body: JSON.stringify({
                        current_password:
                            currentPassword,

                        new_password:
                            newPassword
                    })
                }
            );

            const data =
                await response.json();

            if (!response.ok) {
                showToast(
                    getErrorMessage(data),
                    "error"
                );

                return;
            }

            passwordForm.reset();

            showToast(
                "Password changed successfully!",
                "success"
            );

        } catch (error) {
            console.error(error);

            showToast(
                "Could not change password.",
                "error"
            );
        }
    }
);


// ================= DELETE ACCOUNT =================

deleteAccountBtn.addEventListener(
    "click",
    async () => {
        const confirmed =
            await showConfirm({
                title: "Delete Account?",

                message:
                    "Your account, projects and tasks will be permanently deleted. This action cannot be undone.",

                confirmText:
                    "Delete Account"
            });

        if (!confirmed) {
            return;
        }

        try {
            const response = await fetch(
                `${API_URL}/users/me`,
                {
                    method: "DELETE",
                    headers: authHeaders()
                }
            );

            const data =
                await response.json();

            if (!response.ok) {
                showToast(
                    getErrorMessage(data),
                    "error"
                );

                return;
            }

            showToast(
                "Account deleted successfully.",
                "success"
            );

            setTimeout(() => {
                logoutUser();
            }, 700);

        } catch (error) {
            console.error(error);

            showToast(
                "Could not delete account.",
                "error"
            );
        }
    }
);


// ================= STATS =================

async function loadAllTaskStats(projects) {
    let totalTasks = 0;
    let totalCompleted = 0;

    for (const project of projects) {
        try {
            const response = await fetch(
                `${API_URL}/projects/${project.id}/tasks`,
                {
                    headers: authHeaders()
                }
            );

            if (!response.ok) {
                continue;
            }

            const tasks =
                await response.json();

            totalTasks += tasks.length;

            totalCompleted += tasks.filter(
                task =>
                    task.status === "done"
            ).length;

        } catch (error) {
            console.error(error);
        }
    }

    taskCount.textContent =
        totalTasks;

    completedCount.textContent =
        totalCompleted;
}


// ================= PAGE LOAD =================

window.addEventListener(
    "DOMContentLoaded",
    async () => {
        if (getToken()) {
            await openDashboard();
        }
    }
);