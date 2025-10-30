// js/main.js

// URL нашего API
const API_URL = "http://127.0.0.1:8000";

// Инициализация при загрузке страницы
document.addEventListener("DOMContentLoaded", function () {
  createParticles();
  initializeApp();
});

// Инициализация приложения
function initializeApp() {
  // Проверяем наличие токена
  const token = localStorage.getItem("session_token");
  if (!token) {
    // Если токена нет, принудительно отправляем на логин
    window.location.href = "/login";
    return;
  }

  // Если токен есть, показываем интерфейс
  document.getElementById("app-interface").style.display = "block";

  // Получаем статус из localStorage (установлен при логине)
  const userStatus = localStorage.getItem("userStatus") || "student";

  if (userStatus === "teacher") {
    showTeacherInterface();
  } else {
    showStudentInterface();
  }
}

// Функция переключения пользователя (оставляем, если нужна для отладки)
function switchUser(type) {
  localStorage.setItem("userStatus", type);

  if (type === "teacher") {
    showTeacherInterface();
  } else {
    showStudentInterface();
  }
}

// Функция переключения между экранами
function switchScreen(userType, screenName, event) {
  // ... (логика переключения экранов остается без изменений)
  console.log("Переключение экрана:", userType, screenName);

  const screens = document.querySelectorAll(`#${userType}-interface .screen`);
  screens.forEach((screen) => {
    screen.classList.remove("active");
  });

  const targetScreen = document.getElementById(`${userType}-${screenName}`);
  if (targetScreen) {
    targetScreen.classList.add("active");
  }

  if (event) {
    const navItems = document.querySelectorAll(
      `#${userType}-interface .nav-item`,
    );
    navItems.forEach((item) => {
      item.classList.remove("active");
    });

    if (event.target.classList.contains("nav-item")) {
      event.target.classList.add("active");
    } else if (event.target.parentElement.classList.contains("nav-item")) {
      event.target.parentElement.classList.add("active");
    }
  }

  // Загружаем историю чата, если переключились на ассистента
  if (screenName === "assistant") {
    if (userType === "student") {
      loadStudentChatHistory();
    } else {
      // loadTeacherChatHistory(); // Аналогично для учителя
    }
  }
}

// Показать интерфейс преподавателя
function showTeacherInterface() {
  document.getElementById("teacher-interface").classList.add("active");
  document.getElementById("student-interface").classList.remove("active");
  initTeacherInterface();
}

// Показать интерфейс студента
function showStudentInterface() {
  document.getElementById("student-interface").classList.add("active");
  document.getElementById("teacher-interface").classList.remove("active");
  initStudentInterface();
}

// --- ОБНОВЛЕННАЯ Функция выхода ---
async function logout() {
  const token = localStorage.getItem("session_token");
  if (!token) {
    // Если токена нет, просто чистим localStorage
    clearSessionAndRedirect();
    return;
  }

  try {
    await fetch(`${API_URL}/api/logout`, {
      method: "POST",
      headers: {
        Authorization: token,
      },
    });
    // Независимо от ответа сервера (даже если токен уже истек),
    // чистим данные на клиенте
    clearSessionAndRedirect();
  } catch (error) {
    console.error("Ошибка при выходе:", error);
    // Все равно чистим данные на клиенте
    clearSessionAndRedirect();
  }
}

// Вспомогательная функция для очистки сессии
function clearSessionAndRedirect() {
  localStorage.removeItem("session_token");
  localStorage.removeItem("userStatus");
  window.location.href = "/login";
}

// Создаем частицы для фона
function createParticles() {
  // ... (логика частиц остается без изменений)
  const particles = document.getElementById("particles");
  if (!particles) return;
  const particleCount = 50;
  for (let i = 0; i < particleCount; i++) {
    const particle = document.createElement("div");
    particle.classList.add("particle");
    particle.style.left = `${Math.random() * 100}%`;
    particle.style.top = `${Math.random() * 100}%`;
    particle.style.animationDelay = `${Math.random() * 6}s`;
    const size = Math.random() * 4 + 2;
    particle.style.width = `${size}px`;
    particle.style.height = `${size}px`;
    particles.appendChild(particle);
  }
}

// --- Общая утилита для Fetch API с авторизацией ---
async function fetchWithAuth(endpoint, options = {}) {
  const token = localStorage.getItem("session_token");
  if (!token) {
    // Если токен пропал, отправляем на логин
    clearSessionAndRedirect();
    throw new Error("No authentication token found.");
  }

  const defaultHeaders = {
    "Content-Type": "application/json",
    Authorization: token,
  };

  const config = {
    ...options,
    headers: {
      ...defaultHeaders,
      ...options.headers,
    },
  };

  const response = await fetch(`${API_URL}${endpoint}`, config);

  if (response.status === 401) {
    // Если токен невалиден (истек, отозван)
    clearSessionAndRedirect();
    throw new Error("Session expired or invalid.");
  }

  return response;
}

// ... (остальные утилиты и обработчики)

// Глобальные обработчики событий
document.addEventListener("keydown", function (e) {
  if (e.ctrlKey && e.key === "k") {
    e.preventDefault();
    const searchInput = document.querySelector(".chat-input");
    if (searchInput) searchInput.focus();
  }
});

// Обработчики для общих элементов
function initCommonEventHandlers() {
  const logoutButtons = document.querySelectorAll(".btn-secondary");
  logoutButtons.forEach((btn) => {
    if (btn.textContent.includes("Выйти")) {
      btn.addEventListener("click", logout);
    }
  });
}

initCommonEventHandlers();