// js/login.js
document.addEventListener('DOMContentLoaded', function() {
    console.log('Login form loaded, environment:', CONFIG.ENVIRONMENT);
    const form = document.querySelector('form');
    
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        
        if (!email || !password) {
            alert('Пожалуйста, заполните все поля');
            return;
        }
        
        // Просто переходим на главную
        window.location.href = 'main.html';
    
    });
})