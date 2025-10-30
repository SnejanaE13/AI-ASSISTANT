document.addEventListener("DOMContentLoaded", function () {
  console.log("Страница авторизации загружена и готова!");

  const form = document.getElementById("loginForm");
  const messageDisplay = document.getElementById("message-display");
  const submitBtn = form.querySelector(".submit-btn");

  // URL нашего API
  const API_URL = "http://127.0.0.1:8000"; // Убедись, что порт совпадает

  // Функция для показа сообщений
  function showMessage(message, isError = true) {
    messageDisplay.textContent = message;
    messageDisplay.className = isError
      ? "message-display error"
      : "message-display success";
    messageDisplay.style.display = "block";
  }

  // Функция для скрытия сообщений
  function hideMessage() {
    messageDisplay.style.display = "none";
  }

  form.addEventListener("submit", async function (e) {
    e.preventDefault();
    hideMessage();

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    if (!email || !password) {
      showMessage("Пожалуйста, введите email и пароль.");
      return;
    }

    // Блокируем кнопку
    submitBtn.disabled = true;
    submitBtn.textContent = "Вход...";

    try {
      const response = await fetch(`${API_URL}/api/login`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email: email, password: password }),
      });

      if (response.ok) {
        // Успех
        const data = await response.json();

        // Сохраняем токен и роль в localStorage (как ожидает main.js)
        localStorage.setItem("session_token", data.session_token);
        localStorage.setItem("userStatus", data.user_role); // 'student' или 'teacher'

        showMessage("Успешный вход! Перенаправление...", false);

        // Переход на главную страницу
        setTimeout(() => {
          window.location.href = "/main";
        }, 1000);
      } else {
        // Ошибка (401, 404 и т.д.)
        const errorData = await response.json();
        showMessage(errorData.detail || "Ошибка входа.");
        submitBtn.disabled = false;
        submitBtn.textContent = "Войти";
      }
    } catch (error) {
      console.error("Ошибка сети:", error);
      showMessage("Не удалось подключиться к серверу.");
      submitBtn.disabled = false;
      submitBtn.textContent = "Войти";
    }
  });
});