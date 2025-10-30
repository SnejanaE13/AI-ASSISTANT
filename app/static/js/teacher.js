// js/teacher.js

// Инициализация интерфейса преподавателя
function initTeacherInterface() {
    console.log('Инициализация интерфейса преподавателя');
    
    // Инициализация чата преподавателя
    initTeacherChat();
    
    // Инициализация управления студентами
    initStudentsManagement();
    
    // Инициализация управления заданиями
    initAssignmentsManagement();
    
    // Инициализация аналитики
    initAnalytics();
    
    // Инициализация контента
    initContentManagement();
}
// Скрытие переключателя пользователей
function hideUserSwitcher() {
    const userSwitcher = document.getElementById('user-switcher');
    if (userSwitcher) {
        userSwitcher.style.display = 'none';
    }
    
    // Также можно скрыть через CSS класс
    const switcherElements = document.querySelectorAll('.user-selector, .user-switcher');
    switcherElements.forEach(element => {
        element.style.display = 'none';
    });
}
// Инициализация чата преподавателя
function initTeacherChat() {
    const teacherChatInput = document.querySelector('#teacher-assistant .chat-input');
    const teacherChatBtn = document.querySelector('#teacher-assistant .btn');
    const teacherChatMessages = document.getElementById('teacher-chat-messages');
    
    if (teacherChatInput && teacherChatBtn) {
        teacherChatBtn.addEventListener('click', () => sendTeacherMessage());
        teacherChatInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                sendTeacherMessage();
            }
        });
    }
    
    // Обработчики для быстрых действий в чате преподавателя
    const teacherQuickActions = document.querySelectorAll('#teacher-assistant .quick-action');
    teacherQuickActions.forEach(action => {
        action.addEventListener('click', function() {
            const message = this.textContent;
            document.querySelector('#teacher-assistant .chat-input').value = message;
            sendTeacherMessage();
        });
    });
}

// Отправка сообщения в чате преподавателя
function sendTeacherMessage() {
    const chatInput = document.querySelector('#teacher-assistant .chat-input');
    const chatMessages = document.getElementById('teacher-chat-messages');
    
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
        aiMessage.textContent = generateTeacherAIResponse(userMessageText);
        chatMessages.appendChild(aiMessage);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }, 1000);
}

// Генерация ответа AI для преподавателя
function generateTeacherAIResponse(message) {
    const responses = {
        'анализ': 'Готов предоставить детальный анализ успеваемости студентов. Какую именно группу или период вас интересует?',
        'планирован': 'Помогу составить план урока. Укажите тему, длительность и уровень студентов.',
        'тест': 'Могу сгенерировать тест по указанной теме. Какой уровень сложности и количество вопросов предпочтительны?',
        'проверк': 'Готов помочь с проверкой заданий. Загрузите работы студентов для автоматического анализа.',
        'материал': 'В базе есть разнообразные учебные материалы. Какую тему или навык вы хотите развивать?',
        'студент': 'Информация о студентах доступна в разделе "Студенты". Могу предоставить аналитику по успеваемости.',
        'задани': 'Управление заданиями доступно в соответствующем разделе. Могу помочь с созданием новых заданий.',
        'расписан': 'Ваше расписание доступно в разделе "Расписание". Могу помочь с планированием уроков.',
        'групп': 'Статистика по группам доступна в разделе "Аналитика".',
        'default': 'Как преподавательский ассистент, я могу помочь с анализом успеваемости, планированием уроков, созданием тестов и проверкой работ. Чем могу быть полезен?'
    };
    
    const lowerMessage = message.toLowerCase();
    for (const [key, response] of Object.entries(responses)) {
        if (lowerMessage.includes(key)) {
            return response;
        }
    }
    return responses.default;
}

// Управление студентами
function initStudentsManagement() {
    // Поиск студентов
    const searchInput = document.querySelector('#teacher-students .chat-input');
    if (searchInput) {
        searchInput.addEventListener('input', function(e) {
            filterStudents(e.target.value);
        });
    }
    
    // Фильтры студентов
    const filters = document.querySelectorAll('#teacher-students .quick-action');
    filters.forEach(filter => {
        filter.addEventListener('click', function() {
            const filterType = this.textContent.toLowerCase();
            applyStudentFilter(filterType);
        });
    });
}

// Фильтрация студентов
function filterStudents(searchTerm) {
    const studentItems = document.querySelectorAll('#teacher-students .feature-item');
    studentItems.forEach(item => {
        const studentName = item.querySelector('.feature-text').textContent.toLowerCase();
        if (studentName.includes(searchTerm.toLowerCase()) || searchTerm === '') {
            item.style.display = 'flex';
        } else {
            item.style.display = 'none';
        }
    });
}

// Применение фильтров студентов
function applyStudentFilter(filterType) {
    const studentItems = document.querySelectorAll('#teacher-students .feature-item');
    const filterButtons = document.querySelectorAll('#teacher-students .quick-action');
    
    // Сбрасываем активные кнопки
    filterButtons.forEach(btn => btn.classList.remove('active'));
    
    // Активируем текущую кнопку
    event.target.classList.add('active');
    
    studentItems.forEach(item => {
        const statusBadge = item.querySelector('.status-badge');
        const status = statusBadge.textContent.toLowerCase();
        
        switch(filterType) {
            case 'все студенты':
                item.style.display = 'flex';
                break;
            case 'отстающие':
                item.style.display = status.includes('отста') ? 'flex' : 'none';
                break;
            case 'лучшие':
                item.style.display = status.includes('актив') && !status.includes('отста') ? 'flex' : 'none';
                break;
            case 'новые':
                item.style.display = 'flex'; // Здесь можно добавить логику для новых студентов
                break;
            default:
                item.style.display = 'flex';
        }
    });
}

// Управление заданиями
function initAssignmentsManagement() {
    // Фильтры заданий
    const assignmentFilters = document.querySelectorAll('#teacher-assignments .quick-action');
    assignmentFilters.forEach(filter => {
        filter.addEventListener('click', function() {
            const filterType = this.textContent.toLowerCase();
            filterAssignments(filterType);
        });
    });
}

// Фильтрация заданий
function filterAssignments(filterType) {
    const assignmentItems = document.querySelectorAll('#teacher-assignments .feature-item');
    const filterButtons = document.querySelectorAll('#teacher-assignments .quick-action');
    
    // Сбрасываем активные кнопки
    filterButtons.forEach(btn => btn.classList.remove('active'));
    
    // Активируем текущую кнопку
    event.target.classList.add('active');
    
    assignmentItems.forEach(item => {
        const statusBadge = item.querySelector('.status-badge');
        const status = statusBadge.textContent.toLowerCase();
        
        switch(filterType) {
            case 'все задания':
                item.style.display = 'flex';
                break;
            case 'текущие':
                item.style.display = status.includes('актив') || status.includes('проверк') ? 'flex' : 'none';
                break;
            case 'просроченные':
                item.style.display = status.includes('просроч') || status.includes('сроч') ? 'flex' : 'none';
                break;
            case 'проверенные':
                item.style.display = status.includes('проверен') ? 'flex' : 'none';
                break;
            default:
                item.style.display = 'flex';
        }
    });
}

// Управление контентом
function initContentManagement() {
    // Фильтры материалов
    const contentFilters = document.querySelectorAll('#teacher-content .quick-action');
    contentFilters.forEach(filter => {
        filter.addEventListener('click', function() {
            const filterType = this.textContent.toLowerCase();
            filterContent(filterType);
        });
    });
}

// Фильтрация контента
function filterContent(filterType) {
    const contentItems = document.querySelectorAll('#teacher-content .feature-item');
    const filterButtons = document.querySelectorAll('#teacher-content .quick-action');
    
    // Сбрасываем активные кнопки
    filterButtons.forEach(btn => btn.classList.remove('active'));
    
    // Активируем текущую кнопку
    event.target.classList.add('active');
    
    contentItems.forEach(item => {
        switch(filterType) {
            case 'все материалы':
                item.style.display = 'flex';
                break;
            case 'грамматика':
                item.style.display = item.querySelector('.feature-text').textContent.toLowerCase().includes('грамматик') ? 'flex' : 'none';
                break;
            case 'лексика':
                item.style.display = item.querySelector('.feature-text').textContent.toLowerCase().includes('лексик') || 
                                   item.querySelector('.feature-text').textContent.toLowerCase().includes('глагол') ? 'flex' : 'none';
                break;
            case 'аудирование':
                item.style.display = item.querySelector('.feature-text').textContent.toLowerCase().includes('аудирован') ? 'flex' : 'none';
                break;
            case 'мои закладки':
                item.style.display = 'flex'; // Здесь можно добавить логику закладок
                break;
            default:
                item.style.display = 'flex';
        }
    });
}

// Аналитика
function initAnalytics() {
    console.log('Инициализация аналитики преподавателя');
    // Здесь можно добавить инициализацию графиков
}

// Создание нового задания
function createNewAssignment() {
    const title = prompt('Введите название задания:');
    if (title) {
        const description = prompt('Введите описание задания:');
        const deadline = prompt('Введите срок выполнения (дд.мм.гггг):');
        
        alert(`Задание "${title}" создано!\nОписание: ${description}\nСрок: ${deadline}`);
        
        // Здесь можно добавить логику сохранения задания
    }
}

// Добавление нового студента
function addNewStudent() {
    const name = prompt('Введите имя студента:');
    if (name) {
        const email = prompt('Введите email студента:');
        const level = prompt('Введите уровень студента (A1, A2, B1, B2, C1, C2):');
        
        alert(`Студент ${name} добавлен!\nEmail: ${email}\nУровень: ${level}`);
        
        // Здесь можно добавить логику сохранения студента
    }
}

// Создание нового материала
function createNewMaterial() {
    const title = prompt('Введите название материала:');
    if (title) {
        const type = prompt('Введите тип материала (PDF, видео, тест, статья):');
        const description = prompt('Введите описание материала:');
        
        alert(`Материал "${title}" создан!\nТип: ${type}\nОписание: ${description}`);
        
        // Здесь можно добавить логику сохранения материала
    }
}

// Генерация упражнения
function generateExercise() {
    alert('Упражнение сгенерировано! Проверьте раздел "Контент".');
}
