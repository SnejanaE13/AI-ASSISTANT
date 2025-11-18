// Динамическая конфигурация
const CONFIG = {
    // Автоматически определяем базовый URL
    API_BASE_URL: window.location.origin,
    
    // Определяем окружение по домену
    get ENVIRONMENT() {
        const hostname = window.location.hostname;
        if (hostname.includes('localhost') || hostname.includes('127.0.0.1') || hostname.includes('staging.')) {
            return 'development';
        }
        return 'production';
    },
    
    // Другие настройки
    APP_VERSION: '1.0.0',
    DEBUG: this.ENVIRONMENT === 'development'
};

// Использование в коде:
// const apiUrl = CONFIG.API_BASE_URL + '/api/endpoint';
// config.js - дополнение
const UI_MESSAGES = {
    // Уведомления
    NOTIFICATIONS: {
        SUCCESS: 'Операция выполнена успешно',
        ERROR: 'Произошла ошибка',
        WARNING: 'Внимание',
        INFO: 'Информация'
    },
    
    // Подтверждения
    CONFIRMATIONS: {
        LOGOUT: 'Вы уверены, что хотите выйти?',
        DELETE: 'Вы уверены, что хотите удалить этот элемент?',
        CANCEL: 'Вы уверены, что хотите отменить изменения?'
    },
    
    // Состояния загрузки
    LOADING: {
        PROCESSING: 'Обработка...',
        UPLOADING: 'Загрузка...',
        SAVING: 'Сохранение...'
    },
    
    // Пустые состояния
    EMPTY_STATES: {
        NO_STUDENTS: 'Студенты не найдены',
        NO_ASSIGNMENTS: 'Задания не найдены',
        NO_MATERIALS: 'Материалы не найдены',
        NO_MESSAGES: 'Сообщений пока нет'
    }
};

const ERROR_MESSAGES = {
    NETWORK: 'Ошибка соединения с сервером',
    UPLOAD: 'Ошибка загрузки файла',
    VALIDATION: 'Ошибка валидации данных',
    AUTH: 'Ошибка авторизации',
    PERMISSION: 'Недостаточно прав'
};