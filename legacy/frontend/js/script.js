document.addEventListener('DOMContentLoaded', function() {
    console.log('Registration form loaded, environment:', CONFIG.ENVIRONMENT);
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
        if (password.length < 9) {
            return {
                valid: false,
                message: 'Пароль должен содержать не менее 9 символов'
            };
        }
        
        if (!/^[A-Za-z0-9!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]*$/.test(password)) {
            return {
                valid: false,
                message: 'Пароль должен содержать только латинские буквы, цифры и специальные символы'
            };
        }
        
        return { valid: true, message: '' };
    }
    
    // Функция для проверки совпадения паролей
    function validatePasswordMatch(password, confirmPassword) {
        if (!confirmPassword) {
            return { valid: false, message: 'Подтвердите пароль' };
        }
        
        if (password !== confirmPassword) {
            return { valid: false, message: 'Пароли не совпадают' };
        }
        
        return { valid: true, message: '' };
    }
    
    // Новая функция для отображения ошибок
    function showError(input, errorElement, message, isError = true) {
        if (isError) {
            errorElement.textContent = message;
            errorElement.style.display = 'block';
            input.style.borderColor = '#e74c3c';
            input.style.backgroundColor = '#fdf2f2';
        } else {
            errorElement.style.display = 'none';
            input.style.borderColor = '#27ae60';
            input.style.backgroundColor = '#f2fdf2';
        }
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
        const validation = validatePassword(passwordInput.value);
        
        if (!validation.valid) {
            showError(passwordInput, passwordError, validation.message, true);
        } else {
            showError(passwordInput, passwordError, '✓ Пароль надежный', false);
        }
        
        // Также проверяем совпадение паролей
        const matchValidation = validatePasswordMatch(passwordInput.value, confirmPasswordInput.value);
        if (!matchValidation.valid && confirmPasswordInput.value) {
            showError(confirmPasswordInput, confirmPasswordError, matchValidation.message, true);
        } else if (confirmPasswordInput.value && passwordInput.value) {
            showError(confirmPasswordInput, confirmPasswordError, '✓ Пароли совпадают', false);
        }
        
        updateSubmitButton();
    });
    
    // Валидация при вводе подтверждения пароля
    confirmPasswordInput.addEventListener('input', function() {
        const validation = validatePasswordMatch(passwordInput.value, confirmPasswordInput.value);
        
        if (!validation.valid) {
            showError(confirmPasswordInput, confirmPasswordError, validation.message, true);
        } else if (passwordInput.value) {
            showError(confirmPasswordInput, confirmPasswordError, '✓ Пароли совпадают', false);
        }
        
        updateSubmitButton();
    });
    
    // Функция для обновления состояния кнопки отправки
    function updateSubmitButton() {
        const passwordValidation = validatePassword(passwordInput.value);
        const matchValidation = validatePasswordMatch(passwordInput.value, confirmPasswordInput.value);
        
        const isValid = passwordValidation.valid && 
                    matchValidation.valid && 
                    passwordInput.value && 
                    confirmPasswordInput.value;
        
        submitBtn.disabled = !isValid;
        submitBtn.classList.toggle('btn-disabled', !isValid);
    }
    // Обработчик отправки формы
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const passwordValidation = validatePassword(passwordInput.value);
        const matchValidation = validatePasswordMatch(passwordInput.value, confirmPasswordInput.value);
        
        if (!passwordValidation.valid || !matchValidation.valid) {
            // Показываем ошибки, если они есть
            if (!passwordValidation.valid) {
                showError(passwordInput, passwordError, passwordValidation.message, true);
            }
            if (!matchValidation.valid) {
                showError(confirmPasswordInput, confirmPasswordError, matchValidation.message, true);
            }
            return;
        }
        
        const userStatus = document.getElementById('status').value;
        localStorage.setItem('userStatus', userStatus);
        
        // Показываем успешное сообщение перед переходом
        showError(passwordInput, passwordError, '✓ Регистрация успешна!', false);
        showError(confirmPasswordInput, confirmPasswordError, '✓ Перенаправление...', false);
        
        setTimeout(() => {
            window.location.href = 'main.html';
        }, 1000);
    });
     updateSubmitButton();
});