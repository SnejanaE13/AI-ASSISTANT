// js/student.js

// Инициализация интерфейса студента
function initStudentInterface() {
  console.log("Инициализация интерфейса студента");

  const studentChatInput = document.querySelector(
    "#student-assistant .chat-input",
  );
  const studentChatBtn = document.querySelector("#student-assistant .btn");

  if (studentChatInput && studentChatBtn) {
    studentChatBtn.addEventListener("click", sendStudentMessage);
    studentChatInput.addEventListener("keypress", (e) => {
      if (e.key === "Enter") {
        sendStudentMessage();
      }
    });
  }

  const quickActions = document.querySelectorAll(
    "#student-assistant .quick-action",
  );
  quickActions.forEach((action) => {
    action.addEventListener("click", function () {
      const message = this.textContent;
      studentChatInput.value = message;
      sendStudentMessage();
    });
  });

  initStudentFileUploads();

  // Загружаем историю чата при инициализации
  // loadStudentChatHistory(); // Лучше вызывать при переключении на вкладку
}

// ... (initStudentFileUploads и handleStudentMediaUpload остаются без изменений)
function initStudentFileUploads() {
  const textUpload = document.getElementById("upload-text");
  if (textUpload) {
    textUpload.addEventListener("change", function (e) {
      if (this.files.length > 0) {
        document.getElementById("analysis-result").style.display = "block";
        document.getElementById("show-details-btn").style.display = "block";
      }
    });
  }
  const videoUpload = document.getElementById("upload-video");
  const audioUpload = document.getElementById("upload-audio");
  if (videoUpload)
    videoUpload.addEventListener("change", handleStudentMediaUpload);
  if (audioUpload)
    audioUpload.addEventListener("change", handleStudentMediaUpload);
}
function handleStudentMediaUpload(e) {
  const file = e.target.files[0];
  if (file) {
    console.warn(
      `Файл "${file.name}" загружен. Обработка медиа не реализована в API.`,
    );
  }
}
// ---

// --- НОВАЯ: Загрузка истории чата ---
async function loadStudentChatHistory() {
  const chatMessages = document.getElementById("chat-messages");
  chatMessages.innerHTML =
    '<div class="message system">Загрузка истории...</div>'; // Очистка

  try {
    const response = await fetchWithAuth("/api/chat/history"); // Используем fetchWithAuth из main.js
    if (!response.ok) {
      throw new Error("Failed to load chat history");
    }

    const history = await response.json();
    chatMessages.innerHTML = ""; // Очистка "Загрузка..."

    if (history.length === 0) {
      chatMessages.innerHTML =
        '<div class="message ai">Привет! Задайте мне любой вопрос.</div>';
    }

    history.forEach((msg) => {
      addMessageToChatDOM(
        msg.content,
        msg.sender_type === "ai" ? "ai" : "user",
      );
    });
  } catch (error) {
    console.error("Ошибка загрузки истории:", error);
    chatMessages.innerHTML =
      '<div class="message system error">Не удалось загрузить историю чата.</div>';
  } finally {
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }
}

// --- ОБНОВЛЕНО: Отправка сообщения (с вызовом API) ---
async function sendStudentMessage() {
  const chatInput = document.querySelector("#student-assistant .chat-input");
  const messageText = chatInput.value.trim();

  if (!messageText) return;

  // 1. Добавляем сообщение пользователя в DOM
  addMessageToChatDOM(messageText, "user");
  chatInput.value = "";

  // 2. Добавляем индикатор загрузки AI
  const loadingMessage = addMessageToChatDOM("Печатает...", "ai loading");

  try {
    // 3. Отправляем запрос на API
    const response = await fetchWithAuth("/api/chat", {
      // fetchWithAuth из main.js
      method: "POST",
      body: JSON.stringify({ content: messageText }),
    });

    if (!response.ok) {
      throw new Error("Network response was not ok");
    }

    const aiData = await response.json();

    // 4. Обновляем "Печатает..." реальным ответом
    loadingMessage.textContent = aiData.content;
    loadingMessage.classList.remove("loading");
  } catch (error) {
    console.error("Ошибка отправки сообщения:", error);
    loadingMessage.textContent =
      "Ошибка: не удалось получить ответ от ассистента.";
    loadingMessage.classList.remove("loading");
    loadingMessage.classList.add("error");
  } finally {
    // Прокручиваем вниз
    const chatMessages = document.getElementById("chat-messages");
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }
}

// Вспомогательная функция для добавления сообщения в DOM
function addMessageToChatDOM(text, type) {
  const chatMessages = document.getElementById("chat-messages");
  const messageEl = document.createElement("div");
  messageEl.className = `message ${type}`; // type 'user', 'ai', или 'ai loading'
  messageEl.textContent = text;
  chatMessages.appendChild(messageEl);
  chatMessages.scrollTop = chatMessages.scrollHeight;
  return messageEl;
}