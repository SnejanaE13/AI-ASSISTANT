// js/student.js

// Инициализация интерфейса студента
function initStudentInterface() {
    console.log('Инициализация интерфейса студента в среде:', CONFIG.ENVIRONMENT);
    
    // Добавляем обработчики для чата студента
    const studentChatInput = document.querySelector('#student-assistant .chat-input');
    const studentChatBtn = document.querySelector('#student-assistant .btn');
    const studentChatMessages = document.getElementById('chat-messages');
    
    if (studentChatInput && studentChatBtn) {
        studentChatBtn.addEventListener('click', () => sendStudentMessage());
        studentChatInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                sendStudentMessage();
            }
        });
    }
    
    // Обработчики для быстрых действий в чате студента
    const quickActions = document.querySelectorAll('#student-assistant .quick-action');
    quickActions.forEach(action => {
        action.addEventListener('click', function() {
            const message = this.textContent;
            document.querySelector('#student-assistant .chat-input').value = message;
            sendStudentMessage();
        });
    });
    
    // Обработчики для загрузки файлов
    initStudentFileUploads();
}

// Инициализация загрузки файлов для студента
function initStudentFileUploads() {
    // Обработчики для анализа текста
    const textUpload = document.getElementById('upload-text');
    if (textUpload) {
        textUpload.addEventListener('change', function(e) {
            if (this.files.length > 0) {
                document.getElementById('analysis-result').style.display = 'block';
                document.getElementById('show-details-btn').style.display = 'block';
            }
        });
    }
    
    // Обработчики для видео и аудио
    const videoUpload = document.getElementById('upload-video');
    const audioUpload = document.getElementById('upload-audio');
    
    if (videoUpload) {
        videoUpload.addEventListener('change', handleStudentMediaUpload);
    }
    if (audioUpload) {
        audioUpload.addEventListener('change', handleStudentMediaUpload);
    }
}

// Обработка загрузки медиафайлов студента
function handleStudentMediaUpload(e) {
    const file = e.target.files[0];
    if (file) {
        alert(`Файл "${file.name}" загружен. Обработка видео/аудио будет реализована в полной версии.`);
    }
}

// Отправка сообщения в чате студента
function sendStudentMessage() {
    const chatInput = document.querySelector('#student-assistant .chat-input');
    const chatMessages = document.getElementById('chat-messages');
    
    if (!chatInput.value.trim()) return;
    
    // Добавляем сообщение пользователя
    const userMessage = document.createElement('div');
    userMessage.className = 'message user';
    userMessage.textContent = chatInput.value;
    chatMessages.appendChild(userMessage);
    
    // Очищаем поле ввода
    const userMessageText = chatInput.value;
    chatInput.value = '';
    
    // Прокручиваем вниз
    chatMessages.scrollTop = chatMessages.scrollHeight;
    
    // Имитируем ответ ассистента
    setTimeout(() => {
        const aiMessage = document.createElement('div');
        aiMessage.className = 'message ai';
        aiMessage.textContent = generateStudentAIResponse(userMessageText);
        chatMessages.appendChild(aiMessage);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }, 1000);
}

// Генерация ответа AI для студента
function generateStudentAIResponse(message) {
    const responses = {
        'грамматик': 'Давайте разберем правила грамматики. Какая конкретно тема вас интересует?',
        'произношени': 'Для улучшения произношения рекомендую практиковать фонетические упражнения. Хотите попробовать?',
        'диалог': 'Отлично! Давайте начнем диалог. Выберите тему: путешествия, работа, технологии или хобби.',
        'домашн': 'С удовольствием помогу с домашним заданием. Какой предмет или задание вызывает затруднения?',
        'тест': 'Для подготовки к тесту рекомендую повторить следующие темы: времена, модальные глаголы, условные предложения.',
        'default': 'Интересный вопрос! Я могу помочь с грамматикой, произношением, подготовкой к тестам или практикой диалогов. Что именно вас интересует?'
    };
    
    const lowerMessage = message.toLowerCase();
    for (const [key, response] of Object.entries(responses)) {
        if (lowerMessage.includes(key)) {
            return response;
        }
    }
    return responses.default;
}