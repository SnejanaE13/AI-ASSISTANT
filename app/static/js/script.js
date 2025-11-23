document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("registrationForm");
    const messageDisplay = document.getElementById("message-display");
    const submitBtn = document.getElementById("submitBtn");
    const passwordInput = document.getElementById("password");
    const confirmPasswordInput = document.getElementById("confirm-password");
    const passwordError = document.getElementById("passwordError");
    const confirmPasswordError = document.getElementById("confirmPasswordError");
    const togglePassword = document.getElementById("togglePassword");
    const toggleConfirmPassword = document.getElementById("toggleConfirmPassword");

    const API_URL = "http://127.0.0.1:8000";

    if (localStorage.getItem("session_token")) {
        window.location.href = "/main";
        return;
    }

    function showMessage(message, isError = true) {
        messageDisplay.textContent = message;
        messageDisplay.className = isError ? "message-display error" : "message-display success";
        messageDisplay.style.display = "block";
    }

    function hideMessage() {
        messageDisplay.style.display = "none";
    }
    function validatePassword(password) {
        if (password.length < 8) {
            return {
                valid: false,
                message: 'Пароль должен содержать не менее 8 символов'
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

    function validatePasswordBeforeSubmit() {
        const password = passwordInput.value;
        const confirmPassword = confirmPasswordInput.value;
        let isValid = true;

        if (password.length < 8) {
            passwordError.textContent = "Пароль должен содержать не менее 8 символов.";
            isValid = false;
        } else {
            passwordError.textContent = "";
        }

        if (password !== confirmPassword) {
            confirmPasswordError.textContent = "Пароли не совпадают.";
            isValid = false;
        } else {
            confirmPasswordError.textContent = "";
        }

        return isValid;
    }

    function togglePasswordVisibility(input, button) {
        if (input.type === "password") {
            input.type = "text";
            button.textContent = "Скрыть";
        } else {
            input.type = "password";
            button.textContent = "Показать";
        }
    }

    togglePassword.addEventListener("click", () => togglePasswordVisibility(passwordInput, togglePassword));
    toggleConfirmPassword.addEventListener("click", () => togglePasswordVisibility(confirmPasswordInput, toggleConfirmPassword));

    form.addEventListener("input", () => {
        const isFormValid = validatePassword() && form.checkValidity();
        submitBtn.disabled = !isFormValid;
    });

    form.addEventListener("submit", async function (e) {
        e.preventDefault();
        hideMessage();
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

        const formData = new FormData(form);
        const userData = {
            last_name: formData.get("lastname"),
            first_name: formData.get("firstname"),
            second_name: formData.get("middlename") || null,
            role: formData.get("status"),
            email: formData.get("email"),
            password: formData.get("password"),
        };

        submitBtn.disabled = true;
        submitBtn.textContent = "Регистрация...";

        try {
            const response = await fetch(`${API_URL}/api/register`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(userData),
            });

            if (response.ok) {
                showMessage("Вы успешно зарегистрированы! Вы будете перенаправлены на страницу входа.", false);
                setTimeout(() => {
                    window.location.href = "/login";
                }, 2000);
            } else {
                const errorData = await response.json();
                showMessage(errorData.detail || "Произошла ошибка при регистрации.");
                submitBtn.disabled = false;
                submitBtn.textContent = "Зарегистрироваться";
            }
        } catch (error) {
            console.error("Ошибка сети:", error);
            showMessage("Не удалось подключиться к серверу. Попробуйте позже.");
            submitBtn.disabled = false;
            submitBtn.textContent = "Зарегистрироваться";
        }
    });
});