document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('registrationForm');
    const passwordInput = document.getElementById('password');
    const confirmPasswordInput = document.getElementById('confirm-password');
    const passwordError = document.getElementById('passwordError');
    const confirmPasswordError = document.getElementById('confirmPasswordError');
    const togglePasswordBtn = document.getElementById('togglePassword');
    const toggleConfirmPasswordBtn = document.getElementById('toggleConfirmPassword');
    const submitBtn = document.getElementById('submitBtn');
    
    // Функция для проверки пароля
    function validatePassword(password) {
        // Проверка длины
        if (password.length < 9) {
            return 'Пароль должен содержать не менее 9 символов';
        }
        
        // Проверка на латиницу
        if (!/^[A-Za-z0-9!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]*$/.test(password)) {
            return 'Пароль должен содержать только латинские буквы, цифры и специальные символы';
        }
        
        return '';
    }
    
    // Функция для проверки совпадения паролей
    function validatePasswordMatch(password, confirmPassword) {
        if (password !== confirmPassword) {
            return 'Пароли не совпадают';
        }
        return '';
    }
    
    // Функция для переключения видимости пароля
    function togglePasswordVisibility(input, button) {
        if (input.type === 'password') {
            input.type = 'text';
            button.textContent = 'Скрыть';
        } else {
            input.type = 'password';
            button.textContent = 'Показать';
        }
    }
    
    // Обработчики для кнопок показа/скрытия пароля
    togglePasswordBtn.addEventListener('click', function() {
        togglePasswordVisibility(passwordInput, togglePasswordBtn);
    });
    
    toggleConfirmPasswordBtn.addEventListener('click', function() {
        togglePasswordVisibility(confirmPasswordInput, toggleConfirmPasswordBtn);
    });
    
    // Валидация при вводе пароля
    passwordInput.addEventListener('input', function() {
        const error = validatePassword(passwordInput.value);
        
        if (error) {
            passwordError.textContent = error;
            passwordError.style.display = 'block';
            passwordInput.style.borderColor = '#e74c3c';
        } else {
            passwordError.style.display = 'none';
            passwordInput.style.borderColor = '#e1e1e1';
        }
        
        // Также проверяем совпадение паролей
        const matchError = validatePasswordMatch(passwordInput.value, confirmPasswordInput.value);
        if (matchError && confirmPasswordInput.value) {
            confirmPasswordError.textContent = matchError;
            confirmPasswordError.style.display = 'block';
            confirmPasswordInput.style.borderColor = '#e74c3c';
        } else if (confirmPasswordInput.value) {
            confirmPasswordError.style.display = 'none';
            confirmPasswordInput.style.borderColor = '#e1e1e1';
        }
        
        updateSubmitButton();
    });
    
    // Валидация при вводе подтверждения пароля
    confirmPasswordInput.addEventListener('input', function() {
        const error = validatePasswordMatch(passwordInput.value, confirmPasswordInput.value);
        
        if (error) {
            confirmPasswordError.textContent = error;
            confirmPasswordError.style.display = 'block';
            confirmPasswordInput.style.borderColor = '#e74c3c';
        } else {
            confirmPasswordError.style.display = 'none';
            confirmPasswordInput.style.borderColor = '#e1e1e1';
        }
        
        updateSubmitButton();
    });
    
    // Функция для обновления состояния кнопки отправки
    function updateSubmitButton() {
        const passwordValid = !validatePassword(passwordInput.value);
        const passwordsMatch = !validatePasswordMatch(passwordInput.value, confirmPasswordInput.value);
        
        if (passwordValid && passwordsMatch && passwordInput.value && confirmPasswordInput.value) {
            submitBtn.disabled = false;
        } else {
            submitBtn.disabled = true;
        }
    }
    
    // Обработчик отправки формы
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const passwordError = validatePassword(passwordInput.value);
        const matchError = validatePasswordMatch(passwordInput.value, confirmPasswordInput.value);
        
        if (passwordError || matchError) {
            if (passwordError) {
                passwordError.textContent = passwordError;
                passwordError.style.display = 'block';
                passwordInput.style.borderColor = '#e74c3c';
            }
            
            if (matchError) {
                confirmPasswordError.textContent = matchError;
                confirmPasswordError.style.display = 'block';
                confirmPasswordInput.style.borderColor = '#e74c3c';
            }
            
            return;
        }
        
        // Если все проверки пройдены, можно отправить форму
        alert('Регистрация прошла успешно!');
        // Здесь обычно отправка данных на сервер
        // form.submit();
    });
    
    // Инициализация состояния кнопки отправки
    updateSubmitButton();
});