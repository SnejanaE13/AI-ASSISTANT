// js/main.js

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    console.log('App started in:', CONFIG.ENVIRONMENT, 'mode');
    // СРАЗУ показываем интерфейс
    document.getElementById('app-interface').style.display = 'block';
    
    createParticles();
    initializeApp();
});

// Инициализация приложения
function initializeApp() {
    // ПОКАЗЫВАЕМ переключатель
    document.getElementById('user-switcher').style.display = 'flex';
    
    // Получаем статус из localStorage (по умолчанию студент)
    const userStatus = localStorage.getItem('userStatus') || 'student';
    
    if (userStatus === 'teacher') {
        showTeacherInterface();
    } else {
        showStudentInterface();
    }
}

// Функция переключения пользователя
function switchUser(type) {
    localStorage.setItem('userStatus', type);
    
    if (type === 'teacher') {
        showTeacherInterface();
    } else {
        showStudentInterface();
    }
}
// Функция переключения между экранами
function switchScreen(userType, screenName, event) {
    console.log('Переключение экрана:', userType, screenName);
    
    // Скрыть все экраны для текущего пользователя
    const screens = document.querySelectorAll(`#${userType}-interface .screen`);
    screens.forEach(screen => {
        screen.classList.remove('active');
        screen.classList.remove('screen-slide-left', 'screen-slide-right');
    });
    
    // Показать выбранный экран с анимацией
    const targetScreen = document.getElementById(`${userType}-${screenName}`);
    if (targetScreen) {
        targetScreen.classList.add('active', 'screen-slide-left');
        console.log('Экран показан:', targetScreen.id);
    } else {
        console.error('Экран не найден:', `${userType}-${screenName}`);
    }
    
    // Обновить активное состояние в навигации
    const navItems = document.querySelectorAll(`#${userType}-interface .nav-item`);
    navItems.forEach(item => {
        item.classList.remove('active');
    });
    
    // Активировать текущий элемент навигации
    if (event && event.target.classList.contains('nav-item')) {
        event.target.classList.add('active');
    } else if (event && event.target.parentElement.classList.contains('nav-item')) {
        event.target.parentElement.classList.add('active');
    }
    
    // Вызываем инициализацию для конкретного экрана
    if (userType === 'student') {
        initStudentScreen(screenName);
    } else {
        initTeacherScreen(screenName);
    }
}

// Инициализация экранов студента
function initStudentScreen(screenName) {
    console.log('Инициализация экрана студента:', screenName);
    // Здесь можно добавить специфичную логику для каждого экрана
}

// Инициализация экранов преподавателя
function initTeacherScreen(screenName) {
    console.log('Инициализация экрана преподавателя:', screenName);
    // Здесь можно добавить специфичную логику для каждого экрана
}
// Показать интерфейс преподавателя
function showTeacherInterface() {
    document.getElementById('teacher-interface').classList.add('active');
    document.getElementById('student-interface').classList.remove('active');
    
    // Обновляем кнопки переключателя
    document.querySelectorAll('.user-btn').forEach(btn => btn.classList.remove('active'));
    document.querySelector('.user-btn:nth-child(2)').classList.add('active');
    
    initTeacherInterface();
}

// Показать интерфейс студента
function showStudentInterface() {
    document.getElementById('student-interface').classList.add('active');
    document.getElementById('teacher-interface').classList.remove('active');
    
    // Обновляем кнопки переключателя
    document.querySelectorAll('.user-btn').forEach(btn => btn.classList.remove('active'));
    document.querySelector('.user-btn:nth-child(1)').classList.add('active');
    
    initStudentInterface();
}

// Функция выхода
function logout() {
    if (confirm('Вы уверены, что хотите выйти?')) {
        window.location.href = 'login.html';
    }
}

// Создаем частицы для фона
function createParticles() {
    const particles = document.getElementById('particles');
    if (!particles) return;
    
    const particleCount = 50;
    
    for (let i = 0; i < particleCount; i++) {
        const particle = document.createElement('div');
        particle.classList.add('particle');
        
        particle.style.left = `${Math.random() * 100}%`;
        particle.style.top = `${Math.random() * 100}%`;
        particle.style.animationDelay = `${Math.random() * 6}s`;
        
        const size = Math.random() * 4 + 2;
        particle.style.width = `${size}px`;
        particle.style.height = `${size}px`;
        
        particles.appendChild(particle);
    }
}

// Утилиты для работы с данными
const AppUtils = {
    // Сохранение данных пользователя
    saveUserData: function(userType, userData) {
        localStorage.setItem('userType', userType);
        localStorage.setItem('userData', JSON.stringify(userData));
    },
    
    // Получение данных пользователя
    getUserData: function() {
        const data = localStorage.getItem('userData');
        return data ? JSON.parse(data) : null;
    },
    
    // Проверка авторизации
    isAuthenticated: function() {
        return localStorage.getItem('userType') !== null;
    },
    
    // Показать уведомление
    showNotification: function(message, type = 'info') {
        // Простая реализация уведомлений
        alert(message);
    },
    
// Загрузка данных с API
    fetchData: async function(endpoint) {
        try {
            const response = await fetch(`/api/${endpoint}`);
            return await response.json();
        } catch (error) {
            console.error('Ошибка загрузки данных:', error);
            this.showNotification('Ошибка загрузки данных', 'error');
            return null;
        }
    }
};
// Глобальные обработчики событий
document.addEventListener('keydown', function(e) {
    // Горячие клавиши
    if (e.ctrlKey && e.key === 'k') {
        e.preventDefault();
        // Поиск
        const searchInput = document.querySelector('.chat-input');
        if (searchInput) searchInput.focus();
    }
});

// Обработчики для общих элементов
function initCommonEventHandlers() {
 
    
    // Обработчики для карточек
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        card.addEventListener('click', function(e) {
            if (e.target.classList.contains('btn')) return;
            // Дополнительные действия при клике на карточку
        });
    });
}

// Инициализация общих обработчиков
initCommonEventHandlers();