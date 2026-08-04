import customtkinter as ctk
import json
import os
import urllib.request
import urllib.parse
import threading
import re
import shutil
import time
import logging
import sys
from datetime import datetime
from tkinter import filedialog
from PIL import Image, ImageDraw, ImageFilter
import pygame
from dotenv import load_dotenv

# ==================== ЛОГИРОВАНИЕ ====================
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

# ==================== ЗАГРУЗКА ПЕРЕМЕННЫХ ОКРУЖЕНИЯ ====================
load_dotenv()
BOT_TOKEN = os.getenv("8802719388:AAFlZNJRNvOMjsD4il64D73xYzwvkJNWSko", "")
ADMIN_CHAT_ID = os.getenv("6955060768", "")

# ==================== КОНСТАНТЫ ====================
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

COLOR_BG = "#FFF0F5"
COLOR_PINK = "#FF69B4"
COLOR_DARK_PINK = "#FF1493"
COLOR_LIGHT_PINK = "#FFB6C1"
COLOR_WHITE = "#FFFFFF"
COLOR_HOVER = "#FFE4E1"
COLOR_GREEN = "#32CD32"
COLOR_RED = "#FF0000"
COLOR_BLUE = "#1E90FF"
COLOR_INPUT_BG = "#FFF5F7"
COLOR_YELLOW = "#FFD700"

# ==================== ПЕРЕВОДЫ ====================
LANGUAGES = {
    "Русский": {
        "welcome": "🌸 Добро пожаловать! 🌸",
        "auth": "Фембой Авторизация",
        "login_tab": "✨ Вход",
        "register_tab": "🌸 Регистрация",
        "login_title": "Вход в аккаунт",
        "login_hint": "👤 Логин или Email",
        "login_entry_placeholder": "Введите логин или email",
        "password": "🔑 Пароль",
        "password_placeholder": "Введите пароль",
        "remember": "💾 Запомнить меня",
        "login_btn": "💖 Войти",
        "register_title": "Регистрация",
        "create_login": "👤 Придумайте логин",
        "login_placeholder": "my_cute_login",
        "email": "📧 Email",
        "email_placeholder": "example@mail.com",
        "create_password": "🔑 Придумайте пароль",
        "password_min": "Минимум 6 символов",
        "repeat_password": "🔑 Повторите пароль",
        "repeat_placeholder": "Повторите пароль",
        "register_btn": "🌸 Зарегистрироваться",
        "back": "← Назад",
        "welcome_back": "С возвращением!",
        "profile": "👤 Профиль",
        "music": "🎵 Музыка",
        "settings": "⚙️ Настройки",
        "messages": "💌 Сообщения",
        "help": "❓ Помощь",
        "logout": "🚪 Выйти",
        "now_playing": "🎶 Сейчас играет:",
        "playing": "▶️ Играет",
        "paused": "⏸️ Пауза",
        "stopped": "⏹️ Остановлен",
        "no_track": "Нет активного трека",
        "volume": "🔊 Громкость",
        "playlist": "📋 Плейлист",
        "playlist_empty": "Плейлист пуст 🎵\nДобавьте свою музыку!",
        "add_music": "➕ Добавить музыку",
        "settings_title": "⚙️ Настройки",
        "notifications": "🔔 Уведомления",
        "dark_theme": "🌙 Темная тема",
        "autoplay": "🎵 Автовоспроизведение",
        "language": "🌍 Язык",
        "save_settings": "💾 Сохранить",
        "help_title": "❓ Помощь",
        "contacts": "📞 Контакты",
        "love": "♥ С любовью ♥",
        "version": "FemboyApp V1.5",
        "fill_all": "❌ Заполните все поля!",
        "login_short": "❌ Логин от 3 символов",
        "invalid_email": "❌ Неверный email",
        "password_short": "❌ Пароль от 6 символов",
        "passwords_dont_match": "❌ Пароли не совпадают!",
        "login_taken": "❌ Логин занят!",
        "email_taken": "❌ Email используется!",
        "reg_success": "🎉 Регистрация успешна!",
        "user_not_found": "❌ Пользователь не найден!",
        "wrong_password": "❌ Неверный пароль!",
        "change_photo": "📸 Изменить фото",
        "status": "💎 Статус",
        "active": "Активен ✅",
        "busy": "Занят 🔴",
        "away": "Отошел 🟡",
        "invisible": "Невидимка 👻",
        "online": "В сети 🟢",
        "sleeping": "Сплю 💤",
        "settings_saved": "✅ Настройки сохранены!",
        "track_removed": "🗑️ Трек удален",
        "play_error": "❌ Ошибка воспроизведения",
        "no_track_to_play": "❌ Нет трека",
        "bio": "📝 О себе",
        "bio_placeholder": "Расскажите о себе...",
        "edit_profile": "✏️ Редактировать",
        "save_profile": "💾 Сохранить профиль",
        "profile_saved": "✅ Профиль сохранен!",
        "choose_status": "Выберите статус:",
        "registered": "📅 Регистрация:",
        "no_avatar": "🌸",
        # === СООБЩЕНИЯ ===
        "new_message": "✉️ Новое сообщение",
        "send_message": "📤 Отправить",
        "message_placeholder": "Введите сообщение...",
        "to_user": "Кому (логин):",
        "no_dialogs": "🌸 У вас пока нет диалогов\nНайдите пользователя и напишите!",
        "find_user": "🔍 Найти пользователя",
        "search_placeholder": "Введите логин для поиска",
        "user_not_found_msg": "❌ Пользователь не найден",
        "cannot_message_self": "❌ Нельзя писать самому себе",
        "message_sent": "✅ Сообщение отправлено!",
        "message_empty": "❌ Сообщение пустое",
        "delete_dialog": "🗑️ Удалить диалог",
        "dialog_deleted": "🗑️ Диалог удален",
        "no_messages_in_dialog": "💕 Нет сообщений в этом диалоге",
        "you": "Вы",
    },
    "English": {
        "welcome": "🌸 Welcome! 🌸",
        "auth": "Femboy Authorization",
        "login_tab": "✨ Login",
        "register_tab": "🌸 Register",
        "login_title": "Sign In",
        "login_hint": "👤 Username or Email",
        "login_entry_placeholder": "Enter username or email",
        "password": "🔑 Password",
        "password_placeholder": "Enter password",
        "remember": "💾 Remember me",
        "login_btn": "💖 Sign In",
        "register_title": "Registration",
        "create_login": "👤 Create username",
        "login_placeholder": "my_cute_login",
        "email": "📧 Email",
        "email_placeholder": "example@mail.com",
        "create_password": "🔑 Create password",
        "password_min": "Min 6 characters",
        "repeat_password": "🔑 Repeat password",
        "repeat_placeholder": "Repeat password",
        "register_btn": "🌸 Register",
        "back": "← Back",
        "welcome_back": "Welcome back!",
        "profile": "👤 Profile",
        "music": "🎵 Music",
        "settings": "⚙️ Settings",
        "messages": "💌 Messages",
        "help": "❓ Help",
        "logout": "🚪 Logout",
        "now_playing": "🎶 Now playing:",
        "playing": "▶️ Playing",
        "paused": "⏸️ Paused",
        "stopped": "⏹️ Stopped",
        "no_track": "No active track",
        "volume": "🔊 Volume",
        "playlist": "📋 Playlist",
        "playlist_empty": "Playlist empty 🎵\nAdd your music!",
        "add_music": "➕ Add Music",
        "settings_title": "⚙️ Settings",
        "notifications": "🔔 Notifications",
        "dark_theme": "🌙 Dark Theme",
        "autoplay": "🎵 Autoplay",
        "language": "🌍 Language",
        "save_settings": "💾 Save",
        "help_title": "❓ Help",
        "contacts": "📞 Contacts",
        "love": "♥ With love ♥",
        "version": "FemboyApp V1.5",
        "fill_all": "❌ Fill all fields!",
        "login_short": "❌ Username min 3 chars",
        "invalid_email": "❌ Invalid email",
        "password_short": "❌ Password min 6 chars",
        "passwords_dont_match": "❌ Passwords don't match!",
        "login_taken": "❌ Username taken!",
        "email_taken": "❌ Email already used!",
        "reg_success": "🎉 Registration successful!",
        "user_not_found": "❌ User not found!",
        "wrong_password": "❌ Wrong password!",
        "change_photo": "📸 Change Photo",
        "status": "💎 Status",
        "active": "Active ✅",
        "busy": "Busy 🔴",
        "away": "Away 🟡",
        "invisible": "Invisible 👻",
        "online": "Online 🟢",
        "sleeping": "Sleeping 💤",
        "settings_saved": "✅ Settings saved!",
        "track_removed": "🗑️ Track removed",
        "play_error": "❌ Playback error",
        "no_track_to_play": "❌ No track",
        "bio": "📝 About me",
        "bio_placeholder": "Tell about yourself...",
        "edit_profile": "✏️ Edit",
        "save_profile": "💾 Save Profile",
        "profile_saved": "✅ Profile saved!",
        "choose_status": "Choose status:",
        "registered": "📅 Registered:",
        "no_avatar": "🌸",
        # === MESSAGES ===
        "new_message": "✉️ New message",
        "send_message": "📤 Send",
        "message_placeholder": "Type a message...",
        "to_user": "To (username):",
        "no_dialogs": "🌸 No dialogs yet\nFind a user and write!",
        "find_user": "🔍 Find user",
        "search_placeholder": "Enter username to search",
        "user_not_found_msg": "❌ User not found",
        "cannot_message_self": "❌ Cannot message yourself",
        "message_sent": "✅ Message sent!",
        "message_empty": "❌ Message is empty",
        "delete_dialog": "🗑️ Delete dialog",
        "dialog_deleted": "🗑️ Dialog deleted",
        "no_messages_in_dialog": "💕 No messages in this dialog",
        "you": "You",
    },
    "Українська": {
        "welcome": "🌸 Ласкаво просимо! 🌸",
        "auth": "Фембой Авторизація",
        "login_tab": "✨ Вхід",
        "register_tab": "🌸 Реєстрація",
        "login_title": "Вхід в акаунт",
        "login_hint": "👤 Логін або Email",
        "login_entry_placeholder": "Введіть логін або email",
        "password": "🔑 Пароль",
        "password_placeholder": "Введіть пароль",
        "remember": "💾 Запам'ятати мене",
        "login_btn": "💖 Увійти",
        "register_title": "Реєстрація",
        "create_login": "👤 Придумайте логін",
        "login_placeholder": "my_cute_login",
        "email": "📧 Email",
        "email_placeholder": "example@mail.com",
        "create_password": "🔑 Придумайте пароль",
        "password_min": "Мінімум 6 символів",
        "repeat_password": "🔑 Повторіть пароль",
        "repeat_placeholder": "Повторіть пароль",
        "register_btn": "🌸 Зареєструватися",
        "back": "← Назад",
        "welcome_back": "З поверненням!",
        "profile": "👤 Профіль",
        "music": "🎵 Музика",
        "settings": "⚙️ Налаштування",
        "messages": "💌 Повідомлення",
        "help": "❓ Допомога",
        "logout": "🚪 Вийти",
        "now_playing": "🎶 Зараз грає:",
        "playing": "▶️ Грає",
        "paused": "⏸️ Пауза",
        "stopped": "⏹️ Зупинено",
        "no_track": "Немає треку",
        "volume": "🔊 Гучність",
        "playlist": "📋 Плейлист",
        "playlist_empty": "Плейлист порожній 🎵\nДодайте музику!",
        "add_music": "➕ Додати музику",
        "settings_title": "⚙️ Налаштування",
        "notifications": "🔔 Сповіщення",
        "dark_theme": "🌙 Темна тема",
        "autoplay": "🎵 Автовідтворення",
        "language": "🌍 Мова",
        "save_settings": "💾 Зберегти",
        "help_title": "❓ Допомога",
        "contacts": "📞 Контакти",
        "love": "♥ З любов'ю ♥",
        "version": "FemboyApp V1.5",
        "fill_all": "❌ Заповніть всі поля!",
        "login_short": "❌ Логін від 3 символів",
        "invalid_email": "❌ Невірний email",
        "password_short": "❌ Пароль від 6 символів",
        "passwords_dont_match": "❌ Паролі не співпадають!",
        "login_taken": "❌ Логін зайнятий!",
        "email_taken": "❌ Email використовується!",
        "reg_success": "🎉 Реєстрація успішна!",
        "user_not_found": "❌ Користувача не знайдено!",
        "wrong_password": "❌ Невірний пароль!",
        "change_photo": "📸 Змінити фото",
        "status": "💎 Статус",
        "active": "Активний ✅",
        "busy": "Зайнятий 🔴",
        "away": "Відійшов 🟡",
        "invisible": "Невидимка 👻",
        "online": "В мережі 🟢",
        "sleeping": "Сплю 💤",
        "settings_saved": "✅ Налаштування збережено!",
        "track_removed": "🗑️ Трек видалено",
        "play_error": "❌ Помилка відтворення",
        "no_track_to_play": "❌ Немає треку",
        "bio": "📝 Про себе",
        "bio_placeholder": "Розкажіть про себе...",
        "edit_profile": "✏️ Редагувати",
        "save_profile": "💾 Зберегти профіль",
        "profile_saved": "✅ Профіль збережено!",
        "choose_status": "Виберіть статус:",
        "registered": "📅 Реєстрація:",
        "no_avatar": "🌸",
        # === ПОВІДОМЛЕННЯ ===
        "new_message": "✉️ Нове повідомлення",
        "send_message": "📤 Надіслати",
        "message_placeholder": "Введіть повідомлення...",
        "to_user": "Кому (логін):",
        "no_dialogs": "🌸 Немає діалогів\nЗнайдіть користувача!",
        "find_user": "🔍 Знайти користувача",
        "search_placeholder": "Введіть логін для пошуку",
        "user_not_found_msg": "❌ Користувача не знайдено",
        "cannot_message_self": "❌ Не можна писати собі",
        "message_sent": "✅ Повідомлення надіслано!",
        "message_empty": "❌ Повідомлення порожнє",
        "delete_dialog": "🗑️ Видалити діалог",
        "dialog_deleted": "🗑️ Діалог видалено",
        "no_messages_in_dialog": "💕 Немає повідомлень",
        "you": "Ви",
    },
    "Беларуская": {
        "welcome": "🌸 Вітаем! 🌸",
        "auth": "Фембой Аўтарызацыя",
        "login_tab": "✨ Уваход",
        "register_tab": "🌸 Рэгістрацыя",
        "login_title": "Уваход у акаўнт",
        "login_hint": "👤 Логін або Email",
        "login_entry_placeholder": "Увядзіце логін або email",
        "password": "🔑 Пароль",
        "password_placeholder": "Увядзіце пароль",
        "remember": "💾 Запомніць мяне",
        "login_btn": "💖 Увайсці",
        "register_title": "Рэгістрацыя",
        "create_login": "👤 Прыдумайце логін",
        "login_placeholder": "my_cute_login",
        "email": "📧 Email",
        "email_placeholder": "example@mail.com",
        "create_password": "🔑 Прыдумайце пароль",
        "password_min": "Мінімум 6 сімвалаў",
        "repeat_password": "🔑 Паўтарыце пароль",
        "repeat_placeholder": "Паўтарыце пароль",
        "register_btn": "🌸 Зарэгістравацца",
        "back": "← Назад",
        "welcome_back": "З вяртаннем!",
        "profile": "👤 Профіль",
        "music": "🎵 Музыка",
        "settings": "⚙️ Налады",
        "messages": "💌 Паведамленні",
        "help": "❓ Дапамога",
        "logout": "🚪 Выйсці",
        "now_playing": "🎶 Зараз грае:",
        "playing": "▶️ Грае",
        "paused": "⏸️ Паўза",
        "stopped": "⏹️ Спынена",
        "no_track": "Няма трэка",
        "volume": "🔊 Гучнасць",
        "playlist": "📋 Плэйліст",
        "playlist_empty": "Плэйліст пусты 🎵\nДадайце музыку!",
        "add_music": "➕ Дадаць музыку",
        "settings_title": "⚙️ Налады",
        "notifications": "🔔 Апавяшчэнні",
        "dark_theme": "🌙 Цёмная тэма",
        "autoplay": "🎵 Аўтапрайграванне",
        "language": "🌍 Мова",
        "save_settings": "💾 Захаваць",
        "help_title": "❓ Дапамога",
        "contacts": "📞 Кантакты",
        "love": "♥ З любоўю ♥",
        "version": "FemboyApp V1.5",
        "fill_all": "❌ Запоўніце ўсе палі!",
        "login_short": "❌ Логін ад 3 сімвалаў",
        "invalid_email": "❌ Няправільны email",
        "password_short": "❌ Пароль ад 6 сімвалаў",
        "passwords_dont_match": "❌ Паролі не супадаюць!",
        "login_taken": "❌ Логін заняты!",
        "email_taken": "❌ Email выкарыстоўваецца!",
        "reg_success": "🎉 Рэгістрацыя паспяховая!",
        "user_not_found": "❌ Карыстальнік не знойдзены!",
        "wrong_password": "❌ Няправільны пароль!",
        "change_photo": "📸 Змяніць фота",
        "status": "💎 Статус",
        "active": "Актыўны ✅",
        "busy": "Заняты 🔴",
        "away": "Адышоў 🟡",
        "invisible": "Нябачны 👻",
        "online": "У сетцы 🟢",
        "sleeping": "Сплю 💤",
        "settings_saved": "✅ Налады захаваны!",
        "track_removed": "🗑️ Трэк выдалены",
        "play_error": "❌ Памылка прайгравання",
        "no_track_to_play": "❌ Няма трэка",
        "bio": "📝 Пра сябе",
        "bio_placeholder": "Раскажыце пра сябе...",
        "edit_profile": "✏️ Рэдагаваць",
        "save_profile": "💾 Захаваць профіль",
        "profile_saved": "✅ Профіль захаваны!",
        "choose_status": "Выберыце статус:",
        "registered": "📅 Рэгістрацыя:",
        "no_avatar": "🌸",
        # === ПАВЕДАМЛЕННІ ===
        "new_message": "✉️ Новае паведамленне",
        "send_message": "📤 Адправіць",
        "message_placeholder": "Увядзіце паведамленне...",
        "to_user": "Каму (логін):",
        "no_dialogs": "🌸 Няма дыялогаў\nЗнайдзіце карыстальніка!",
        "find_user": "🔍 Знайсці карыстальніка",
        "search_placeholder": "Увядзіце логін для пошуку",
        "user_not_found_msg": "❌ Карыстальнік не знойдзены",
        "cannot_message_self": "❌ Нельга пісаць сабе",
        "message_sent": "✅ Паведамленне адпраўлена!",
        "message_empty": "❌ Паведамленне пустое",
        "delete_dialog": "🗑️ Выдаліць дыялог",
        "dialog_deleted": "🗑️ Дыялог выдалены",
        "no_messages_in_dialog": "💕 Няма паведамленняў",
        "you": "Вы",
    },
    "Deutsch": {
        "welcome": "🌸 Willkommen! 🌸",
        "auth": "Femboy Autorisierung",
        "login_tab": "✨ Anmelden",
        "register_tab": "🌸 Registrieren",
        "login_title": "Anmeldung",
        "login_hint": "👤 Benutzername oder Email",
        "login_entry_placeholder": "Benutzername oder Email",
        "password": "🔑 Passwort",
        "password_placeholder": "Passwort eingeben",
        "remember": "💾 Angemeldet bleiben",
        "login_btn": "💖 Anmelden",
        "register_title": "Registrierung",
        "create_login": "👤 Benutzername erstellen",
        "login_placeholder": "my_cute_login",
        "email": "📧 Email",
        "email_placeholder": "example@mail.com",
        "create_password": "🔑 Passwort erstellen",
        "password_min": "Min 6 Zeichen",
        "repeat_password": "🔑 Passwort wiederholen",
        "repeat_placeholder": "Passwort wiederholen",
        "register_btn": "🌸 Registrieren",
        "back": "← Zurück",
        "welcome_back": "Willkommen zurück!",
        "profile": "👤 Profil",
        "music": "🎵 Musik",
        "settings": "⚙️ Einstellungen",
        "messages": "💌 Nachrichten",
        "help": "❓ Hilfe",
        "logout": "🚪 Abmelden",
        "now_playing": "🎶 Läuft:",
        "playing": "▶️ Spielt",
        "paused": "⏸️ Pausiert",
        "stopped": "⏹️ Gestoppt",
        "no_track": "Kein Track",
        "volume": "🔊 Lautstärke",
        "playlist": "📋 Playlist",
        "playlist_empty": "Playlist leer 🎵\nMusik hinzufügen!",
        "add_music": "➕ Musik hinzufügen",
        "settings_title": "⚙️ Einstellungen",
        "notifications": "🔔 Benachrichtigungen",
        "dark_theme": "🌙 Dunkles Thema",
        "autoplay": "🎵 Autoplay",
        "language": "🌍 Sprache",
        "save_settings": "💾 Speichern",
        "help_title": "❓ Hilfe",
        "contacts": "📞 Kontakte",
        "love": "♥ Mit Liebe ♥",
        "version": "FemboyApp V1.5",
        "fill_all": "❌ Alle Felder ausfüllen!",
        "login_short": "❌ Benutzername min 3",
        "invalid_email": "❌ Ungültige Email",
        "password_short": "❌ Passwort min 6",
        "passwords_dont_match": "❌ Passwörter gleich!",
        "login_taken": "❌ Benutzername vergeben!",
        "email_taken": "❌ Email verwendet!",
        "reg_success": "🎉 Registrierung!",
        "user_not_found": "❌ Benutzer nicht gefunden!",
        "wrong_password": "❌ Falsches Passwort!",
        "change_photo": "📸 Foto ändern",
        "status": "💎 Status",
        "active": "Aktiv ✅",
        "busy": "Beschäftigt 🔴",
        "away": "Abwesend 🟡",
        "invisible": "Unsichtbar 👻",
        "online": "Online 🟢",
        "sleeping": "Schlafend 💤",
        "settings_saved": "✅ Gespeichert!",
        "track_removed": "🗑️ Entfernt",
        "play_error": "❌ Fehler",
        "no_track_to_play": "❌ Kein Track",
        "bio": "📝 Über mich",
        "bio_placeholder": "Erzähle von dir...",
        "edit_profile": "✏️ Bearbeiten",
        "save_profile": "💾 Speichern",
        "profile_saved": "✅ Gespeichert!",
        "choose_status": "Status:",
        "registered": "📅 Registriert:",
        "no_avatar": "🌸",
        # === NACHRICHTEN ===
        "new_message": "✉️ Neue Nachricht",
        "send_message": "📤 Senden",
        "message_placeholder": "Nachricht eingeben...",
        "to_user": "An (Benutzer):",
        "no_dialogs": "🌸 Keine Dialoge\nFinde einen Benutzer!",
        "find_user": "🔍 Benutzer suchen",
        "search_placeholder": "Benutzername eingeben",
        "user_not_found_msg": "❌ Nicht gefunden",
        "cannot_message_self": "❌ Nicht an sich selbst",
        "message_sent": "✅ Gesendet!",
        "message_empty": "❌ Leere Nachricht",
        "delete_dialog": "🗑️ Löschen",
        "dialog_deleted": "🗑️ Gelöscht",
        "no_messages_in_dialog": "💕 Keine Nachrichten",
        "you": "Du",
    }
}

STATUSES = ["active", "online", "busy", "away", "sleeping", "invisible"]


class FemBoyAuthApp:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.title("🌸 FemboyApp")
        self.window.geometry("450x700")
        self.window.minsize(400, 600)
        
        # Файлы
        self.users_file = "users.json"
        self.session_file = "session.json"
        self.settings_file = "app_settings.json"
        self.photos_dir = "photos"
        self.music_dir = "music"
        self.messages_file = "messages.json"
        
        for d in [self.photos_dir, self.music_dir]:
            if not os.path.exists(d):
                os.makedirs(d)
        
        # Данные
        self.registered_users = {}
        self.current_user = None
        self.remember_me = ctk.BooleanVar(value=True)
        
        # Музыка (привязана к пользователю)
        self.playlist = []
        self.current_track_index = -1
        self.is_playing = False
        self.is_paused = False
        self.music_volume = 0.5
        self.track_length = 0
        self.track_start_time = 0
        self.music_position = 0
        self.is_seeking = False
        
        # Сообщения
        self.all_messages = {}  # {"user1_user2": [{"from": "user1", "text": "...", "time": "..."}]}
        self.current_dialog_with = None  # с кем открыт диалог
        
        # Настройки
        self.app_settings = {
            "notifications": True, "dark_theme": False,
            "volume": 0.5, "autoplay": True, "language": "Русский"
        }
        
        self.lang = LANGUAGES["Русский"]
        
        # Инициализация pygame
        try:
            pygame.mixer.init()
            pygame.mixer.music.set_volume(self.music_volume)
        except Exception as e:
            logging.error(f"Ошибка инициализации pygame: {e}")
            print(f"⚠️ Аудио недоступно: {e}")
        
        # Загрузка данных
        self.load_users()
        self.load_settings()
        self.load_messages()
        # НЕ загружаем плейлист здесь! Загрузим после логина
        
        # Тема
        if self.app_settings.get("dark_theme"):
            ctk.set_appearance_mode("dark")
        
        # Центрирование окна
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (450 // 2)
        y = (self.window.winfo_screenheight() // 2) - (700 // 2)
        self.window.geometry(f"450x700+{x}+{y}")
        
        # Контейнер
        self.main_container = ctk.CTkFrame(self.window, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True)
        
        # Запуск обновлений
        self.update_track_progress()
        self.check_music_end()
        self.check_new_messages()
        
        # Автологин
        if not self.try_auto_login():
            self.show_auth_screen()
    
    def t(self, key):
        return self.lang.get(key, key)
    
    def t_status(self, status_key):
        return self.t(status_key)
    
    # ==================== ФАЙЛЫ ПОЛЬЗОВАТЕЛЕЙ ====================
    def load_users(self):
        if os.path.exists(self.users_file):
            try:
                with open(self.users_file, 'r', encoding='utf-8') as f:
                    self.registered_users = json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                logging.error(f"Ошибка загрузки users: {e}")
                self.registered_users = {}
    
    def save_users(self):
        try:
            with open(self.users_file, 'w', encoding='utf-8') as f:
                json.dump(self.registered_users, f, indent=2, ensure_ascii=False)
        except IOError as e:
            logging.error(f"Ошибка сохранения users: {e}")
    
    def load_settings(self):
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    saved = json.load(f)
                    self.app_settings.update(saved)
            except (json.JSONDecodeError, IOError) as e:
                logging.error(f"Ошибка загрузки settings: {e}")
        self.music_volume = self.app_settings.get("volume", 0.5)
        self.lang = LANGUAGES.get(self.app_settings.get("language", "Русский"), LANGUAGES["Русский"])
        try:
            pygame.mixer.music.set_volume(self.music_volume)
        except: pass
    
    def save_settings(self):
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.app_settings, f, indent=2, ensure_ascii=False)
        except IOError as e:
            logging.error(f"Ошибка сохранения settings: {e}")
    
    def save_session(self, login):
        try:
            with open(self.session_file, 'w', encoding='utf-8') as f:
                json.dump({"login": login, "timestamp": datetime.now().isoformat()}, f)
        except IOError as e:
            logging.error(f"Ошибка сохранения session: {e}")
    
    def load_session(self):
        if os.path.exists(self.session_file):
            try:
                with open(self.session_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                logging.error(f"Ошибка загрузки session: {e}")
        return None
    
    def clear_session(self):
        try:
            if os.path.exists(self.session_file):
                os.remove(self.session_file)
        except IOError as e:
            logging.error(f"Ошибка удаления session: {e}")
    
    # ==================== ПЛЕЙЛИСТ (ПРИВЯЗАН К ПОЛЬЗОВАТЕЛЮ) ====================
    def get_user_playlist_file(self):
        if not self.current_user:
            return None
        return f"playlist_{self.current_user['login']}.json"
    
    def load_playlist(self):
        """Загружает плейлист ТЕКУЩЕГО пользователя"""
        pf = self.get_user_playlist_file()
        if not pf:
            self.playlist = []
            return
        if os.path.exists(pf):
            try:
                with open(pf, 'r', encoding='utf-8') as f:
                    self.playlist = json.load(f)
                # Очистка от несуществующих файлов
                self.playlist = [t for t in self.playlist if os.path.exists(t.get('path', ''))]
            except (json.JSONDecodeError, IOError) as e:
                logging.error(f"Ошибка загрузки playlist: {e}")
                self.playlist = []
        else:
            self.playlist = []
    
    def save_playlist(self):
        """Сохраняет плейлист ТЕКУЩЕГО пользователя"""
        pf = self.get_user_playlist_file()
        if not pf:
            return
        try:
            with open(pf, 'w', encoding='utf-8') as f:
                json.dump(self.playlist, f, indent=2, ensure_ascii=False)
        except IOError as e:
            logging.error(f"Ошибка сохранения playlist: {e}")
    
    def try_auto_login(self):
        session = self.load_session()
        if session and session.get('login'):
            login = session['login']
            if login in self.registered_users:
                self.current_user = self.registered_users[login]
                self.load_playlist()  # Загружаем плейлист этого юзера
                self.show_main_menu()
                return True
        return False
    
    # ==================== СООБЩЕНИЯ ====================
    def load_messages(self):
        if os.path.exists(self.messages_file):
            try:
                with open(self.messages_file, 'r', encoding='utf-8') as f:
                    self.all_messages = json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                logging.error(f"Ошибка загрузки messages: {e}")
                self.all_messages = {}
        else:
            self.all_messages = {}
    
    def save_messages(self):
        try:
            with open(self.messages_file, 'w', encoding='utf-8') as f:
                json.dump(self.all_messages, f, indent=2, ensure_ascii=False)
        except IOError as e:
            logging.error(f"Ошибка сохранения messages: {e}")
    
    def get_dialog_key(self, user1, user2):
        """Генерирует ключ диалога (независимо от порядка)"""
        return "_".join(sorted([user1, user2]))
    
    def get_dialog_messages(self, other_user):
        """Получить сообщения диалога с пользователем"""
        if not self.current_user:
            return []
        key = self.get_dialog_key(self.current_user['login'], other_user)
        return self.all_messages.get(key, [])
    
    def send_message_to(self, to_login, text):
        """Отправить сообщение пользователю"""
        if not self.current_user:
            return False
        if to_login == self.current_user['login']:
            return False
        if to_login not in self.registered_users:
            return False
        if not text.strip():
            return False
        
        key = self.get_dialog_key(self.current_user['login'], to_login)
        if key not in self.all_messages:
            self.all_messages[key] = []
        
        self.all_messages[key].append({
            "from": self.current_user['login'],
            "to": to_login,
            "text": text.strip(),
            "time": datetime.now().isoformat(),
            "read": False
        })
        self.save_messages()
        return True
    
    def get_user_dialogs(self):
        """Получить список пользователей, с которыми есть диалог"""
        if not self.current_user:
            return []
        my_login = self.current_user['login']
        dialogs = set()
        for key in self.all_messages.keys():
            users = key.split("_")
            if len(users) == 2 and my_login in users:
                other = users[0] if users[1] == my_login else users[1]
                dialogs.add(other)
        return list(dialogs)
    
    def has_unread_messages(self, from_user):
        """Проверить есть ли непрочитанные от пользователя"""
        if not self.current_user:
            return False
        msgs = self.get_dialog_messages(from_user)
        for m in msgs:
            if m['to'] == self.current_user['login'] and not m.get('read', False):
                return True
        return False
    
    def mark_dialog_read(self, other_user):
        """Пометить все сообщения от пользователя как прочитанные"""
        if not self.current_user:
            return
        key = self.get_dialog_key(self.current_user['login'], other_user)
        if key in self.all_messages:
            for m in self.all_messages[key]:
                if m['to'] == self.current_user['login']:
                    m['read'] = True
            self.save_messages()
    
    def delete_dialog(self, other_user):
        """Удалить диалог с пользователем"""
        if not self.current_user:
            return
        key = self.get_dialog_key(self.current_user['login'], other_user)
        if key in self.all_messages:
            del self.all_messages[key]
            self.save_messages()
    
    def count_unread_total(self):
        """Общее количество непрочитанных"""
        if not self.current_user:
            return 0
        count = 0
        my_login = self.current_user['login']
        for key, msgs in self.all_messages.items():
            for m in msgs:
                if m['to'] == my_login and not m.get('read', False):
                    count += 1
        return count
    
    # ==================== TELEGRAM ====================
    def send_telegram_message(self, message):
        if not BOT_TOKEN or not ADMIN_CHAT_ID:
            return False
        try:
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
            data = {'chat_id': ADMIN_CHAT_ID, 'text': message, 'parse_mode': 'HTML'}
            encoded_data = urllib.parse.urlencode(data).encode('utf-8')
            req = urllib.request.Request(url, data=encoded_data)
            req.add_header('Content-Type', 'application/x-www-form-urlencoded')
            with urllib.request.urlopen(req, timeout=5) as r:
                return json.loads(r.read().decode('utf-8')).get('ok', False)
        except Exception as e:
            logging.error(f"Telegram error: {e}")
            return False
    
    # ==================== АВАТАР ====================
    def make_circle_avatar(self, file_path, size=300):
        try:
            img = Image.open(file_path).convert("RGBA")
            w, h = img.size
            min_dim = min(w, h)
            left = (w - min_dim) // 2
            top = (h - min_dim) // 2
            img = img.crop((left, top, left + min_dim, top + min_dim))
            img = img.resize((size, size), Image.Resampling.LANCZOS)
            mask = Image.new('L', (size, size), 0)
            ImageDraw.Draw(mask).ellipse((0, 0, size, size), fill=255)
            result = Image.new('RGBA', (size, size), (0, 0, 0, 0))
            result.paste(img, (0, 0), mask)
            return result
        except Exception as e:
            logging.error(f"Ошибка создания аватара: {e}")
            return None
    
    def get_avatar_path(self, login=None):
        if not login:
            login = self.current_user['login'] if self.current_user else "default"
        return os.path.join(self.photos_dir, f"{login}_avatar.png")
    
    def load_avatar_image(self, size=150, login=None):
        path = self.get_avatar_path(login)
        if os.path.exists(path):
            try:
                pil_img = Image.open(path).resize((size, size), Image.Resampling.LANCZOS)
                return ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(size, size))
            except: pass
        return None
    
    # ==================== МУЗЫКА ====================
    def get_track_length(self, file_path):
        try:
            sound = pygame.mixer.Sound(file_path)
            return sound.get_length()
        except: return 0
    
    def format_time(self, seconds):
        if seconds < 0: seconds = 0
        return f"{int(seconds // 60)}:{int(seconds % 60):02d}"
    
    def format_msg_time(self, iso_time):
        try:
            dt = datetime.fromisoformat(iso_time)
            now = datetime.now()
            if dt.date() == now.date():
                return dt.strftime("%H:%M")
            elif (now - dt).days < 7:
                return dt.strftime("%a %H:%M")
            else:
                return dt.strftime("%d.%m %H:%M")
        except:
            return ""
    
    def play_music(self, file_path, start_pos=0.0):
        try:
            if not os.path.exists(file_path):
                return False
            pygame.mixer.music.load(file_path)
            if start_pos > 0:
                try:
                    pygame.mixer.music.play(start=start_pos)
                except:
                    pygame.mixer.music.play()
            else:
                pygame.mixer.music.play()
            self.is_playing = True
            self.is_paused = False
            self.track_start_time = time.time() - start_pos
            self.track_length = self.get_track_length(file_path)
            self.music_position = start_pos
            return True
        except Exception as e:
            logging.error(f"Ошибка воспроизведения: {e}")
            self.is_playing = False
            return False
    
    def pause_music(self):
        if self.is_playing and not self.is_paused:
            pygame.mixer.music.pause()
            self.is_paused = True
            self.music_position = time.time() - self.track_start_time
        elif self.is_paused:
            try:
                pygame.mixer.music.unpause()
                self.is_paused = False
                self.track_start_time = time.time() - self.music_position
            except:
                if 0 <= self.current_track_index < len(self.playlist):
                    self.play_music(self.playlist[self.current_track_index]['path'], self.music_position)
                    self.is_paused = False
    
    def stop_music(self):
        try:
            pygame.mixer.music.stop()
        except: pass
        self.is_playing = False
        self.is_paused = False
        self.music_position = 0
        self.track_length = 0
    
    def seek_music(self, position):
        if self.is_playing and self.track_length > 0 and 0 <= position < self.track_length:
            try:
                was_paused = self.is_paused
                pygame.mixer.music.stop()
                try:
                    pygame.mixer.music.play(start=position)
                except:
                    pygame.mixer.music.play()
                self.track_start_time = time.time() - position
                self.music_position = position
                if was_paused:
                    pygame.mixer.music.pause()
            except Exception as e:
                logging.error(f"Ошибка перемотки: {e}")
    
    def set_volume(self, volume):
        self.music_volume = max(0.0, min(volume, 1.25))
        try:
            pygame.mixer.music.set_volume(min(self.music_volume, 1.0))
        except: pass
        self.app_settings["volume"] = self.music_volume
        self.save_settings()
    
    def get_current_position(self):
        if self.is_playing and not self.is_paused:
            return time.time() - self.track_start_time
        return self.music_position
    
    def update_track_progress(self):
        try:
            if (hasattr(self, 'progress_slider') and 
                self.is_playing and 
                not self.is_seeking):
                current_pos = self.get_current_position()
                if self.track_length > 0:
                    self.progress_slider.set(min(current_pos / self.track_length, 1.0))
                if hasattr(self, 'time_label'):
                    self.time_label.configure(
                        text=f"{self.format_time(current_pos)} / {self.format_time(self.track_length)}"
                    )
        except: pass
        self.window.after(500, self.update_track_progress)
    
    def check_music_end(self):
        try:
            if self.is_playing and not self.is_paused:
                if not pygame.mixer.music.get_busy():
                    if self.app_settings.get("autoplay", True):
                        self.play_next()
                    else:
                        self.stop_music()
        except: pass
        self.window.after(1000, self.check_music_end)
    
    def check_new_messages(self):
        """Проверка новых сообщений (можно добавить обновление UI)"""
        self.window.after(3000, self.check_new_messages)
    
    def play_next(self):
        if len(self.playlist) > 0:
            self.current_track_index = (self.current_track_index + 1) % len(self.playlist)
            self.play_music(self.playlist[self.current_track_index]['path'])
    
    def play_previous(self):
        if len(self.playlist) > 0:
            if self.get_current_position() > 3:
                self.play_music(self.playlist[self.current_track_index]['path'])
            else:
                self.current_track_index = (self.current_track_index - 1) % len(self.playlist)
                self.play_music(self.playlist[self.current_track_index]['path'])
    
    def add_music_files(self):
        files = filedialog.askopenfilenames(
            title="Выберите музыку",
            filetypes=[("Аудио", "*.mp3 *.wav *.ogg *.flac")]
        )
        for fp in files:
            try:
                fn = os.path.basename(fp)
                dp = os.path.join(self.music_dir, f"{self.current_user['login']}_{fn}")
                c = 1
                while os.path.exists(dp):
                    n, e = os.path.splitext(fn)
                    dp = os.path.join(self.music_dir, f"{self.current_user['login']}_{n}_{c}{e}")
                    c += 1
                shutil.copy2(fp, dp)
                self.playlist.append({
                    'name': os.path.splitext(fn)[0],
                    'path': dp,
                    'added_at': datetime.now().isoformat()
                })
            except Exception as e:
                logging.error(f"Ошибка добавления трека: {e}")
        self.save_playlist()
    
    def remove_track(self, index):
        if 0 <= index < len(self.playlist):
            try:
                t = self.playlist.pop(index)
                if os.path.exists(t['path']):
                    try: os.remove(t['path'])
                    except: pass
                self.save_playlist()
                if index == self.current_track_index:
                    self.stop_music()
                    self.current_track_index = -1 if len(self.playlist) == 0 else min(index, len(self.playlist) - 1)
            except Exception as e:
                logging.error(f"Ошибка удаления трека: {e}")
    
    # ==================== UI УТИЛИТЫ ====================
    def clear_container(self):
        for w in self.main_container.winfo_children():
            try: w.destroy()
            except: pass
    
    def _bind_mousewheel(self, widget):
        def _on_mousewheel(event):
            try:
                if sys.platform == "darwin":
                    delta = -1 * event.delta
                else:
                    delta = -1 * (event.delta / 120)
                canvas = None
                for child in widget.winfo_children():
                    if isinstance(child, ctk.CTkCanvas):
                        canvas = child
                        break
                if canvas:
                    canvas.yview_scroll(int(delta * 4), "units")
            except: pass
        try:
            widget.bind("<MouseWheel>", _on_mousewheel, add="+")
        except: pass
    
    def back_to_menu(self):
        """Универсальный возврат в меню"""
        self.current_dialog_with = None
        self.show_main_menu()
    
    # ==================== АВТОРИЗАЦИЯ ====================
    def show_auth_screen(self):
        self.clear_container()
        self.current_user = None
        self.current_dialog_with = None
        self.playlist = []  # Очищаем при выходе
        self.stop_music()
        
        mf = ctk.CTkScrollableFrame(self.main_container, fg_color=COLOR_BG, corner_radius=30)
        mf.pack(fill="both", expand=True, padx=15, pady=15)
        self._bind_mousewheel(mf)
        
        ctk.CTkLabel(mf, text=self.t("welcome"), font=("Arial", 24, "bold"), text_color=COLOR_PINK).pack(pady=(25, 5))
        ctk.CTkLabel(mf, text=self.t("auth"), font=("Arial", 12), text_color=COLOR_LIGHT_PINK).pack(pady=(0, 20))
        
        tf = ctk.CTkFrame(mf, fg_color="transparent")
        tf.pack(fill="x", padx=30, pady=10)
        
        self.login_btn = ctk.CTkButton(
            tf, text=self.t("login_tab"), command=lambda: self.show_login_page(),
            corner_radius=25, height=38, font=("Arial", 14, "bold"),
            fg_color=COLOR_PINK, hover_color=COLOR_DARK_PINK
        )
        self.login_btn.pack(side="left", expand=True, padx=5)
        
        self.register_btn = ctk.CTkButton(
            tf, text=self.t("register_tab"), command=lambda: self.show_register_page(),
            corner_radius=25, height=38, font=("Arial", 14, "bold"),
            fg_color=COLOR_HOVER, text_color=COLOR_PINK, hover_color=COLOR_LIGHT_PINK
        )
        self.register_btn.pack(side="right", expand=True, padx=5)
        
        self.form_container = ctk.CTkFrame(mf, fg_color="transparent")
        self.form_container.pack(fill="both", expand=True, padx=20, pady=10)
        
        self.message_label = ctk.CTkLabel(
            mf, text="", font=("Arial", 11, "bold"), 
            text_color=COLOR_DARK_PINK, wraplength=380
        )
        self.message_label.pack(pady=5)
        
        ctk.CTkLabel(mf, text=self.t("love"), font=("Arial", 11), text_color=COLOR_LIGHT_PINK).pack(pady=(15, 0))
        ctk.CTkLabel(mf, text=self.t("version"), font=("Arial", 10, "bold"), text_color=COLOR_LIGHT_PINK).pack(pady=(0, 15))
        
        self.show_login_page()
    
    def show_login_page(self):
        for w in self.form_container.winfo_children():
            try: w.destroy()
            except: pass
        
        self.login_btn.configure(fg_color=COLOR_PINK, text_color="white")
        self.register_btn.configure(fg_color=COLOR_HOVER, text_color=COLOR_PINK)
        
        ctk.CTkLabel(self.form_container, text=self.t("login_title"), 
                    font=("Arial", 18, "bold"), text_color=COLOR_PINK).pack(pady=(10, 20))
        ctk.CTkLabel(self.form_container, text=self.t("login_hint"), 
                    font=("Arial", 12), text_color=COLOR_PINK).pack(anchor="w", pady=(5, 3))
        
        le = ctk.CTkEntry(
            self.form_container, 
            placeholder_text=self.t("login_entry_placeholder"),
            height=42, corner_radius=20,
            border_color=COLOR_LIGHT_PINK, fg_color=COLOR_INPUT_BG, 
            text_color=COLOR_PINK, font=("Arial", 13)
        )
        le.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(self.form_container, text=self.t("password"), 
                    font=("Arial", 12), text_color=COLOR_PINK).pack(anchor="w", pady=(5, 3))
        pe = ctk.CTkEntry(
            self.form_container, 
            placeholder_text=self.t("password_placeholder"),
            height=42, corner_radius=20,
            border_color=COLOR_LIGHT_PINK, fg_color=COLOR_INPUT_BG,
            text_color=COLOR_PINK, show="•", font=("Arial", 13)
        )
        pe.pack(fill="x", pady=(0, 10))
        
        ctk.CTkCheckBox(
            self.form_container, text=self.t("remember"),
            variable=self.remember_me, font=("Arial", 11),
            text_color=COLOR_PINK, fg_color=COLOR_PINK,
            hover_color=COLOR_DARK_PINK,
            checkmark_color="white", border_color=COLOR_LIGHT_PINK
        ).pack(pady=(0, 15))
        
        ctk.CTkButton(
            self.form_container, text=self.t("login_btn"),
            command=lambda: self.login(le.get().strip(), pe.get()),
            height=42, corner_radius=20, 
            fg_color=COLOR_PINK, hover_color=COLOR_DARK_PINK,
            font=("Arial", 15, "bold")
        ).pack(fill="x", pady=10)
    
    def show_register_page(self):
        for w in self.form_container.winfo_children():
            try: w.destroy()
            except: pass
        
        self.register_btn.configure(fg_color=COLOR_PINK, text_color="white")
        self.login_btn.configure(fg_color=COLOR_HOVER, text_color=COLOR_PINK)
        
        ctk.CTkLabel(self.form_container, text=self.t("register_title"),
                    font=("Arial", 18, "bold"), text_color=COLOR_PINK).pack(pady=(10, 15))
        
        ctk.CTkLabel(self.form_container, text=self.t("create_login"),
                    font=("Arial", 12), text_color=COLOR_PINK).pack(anchor="w", pady=(5, 3))
        rl = ctk.CTkEntry(
            self.form_container, placeholder_text=self.t("login_placeholder"),
            height=42, corner_radius=20, border_color=COLOR_LIGHT_PINK,
            fg_color=COLOR_INPUT_BG, text_color=COLOR_PINK, font=("Arial", 13)
        )
        rl.pack(fill="x", pady=(0, 12))
        
        ctk.CTkLabel(self.form_container, text=self.t("email"),
                    font=("Arial", 12), text_color=COLOR_PINK).pack(anchor="w", pady=(5, 3))
        re = ctk.CTkEntry(
            self.form_container, placeholder_text=self.t("email_placeholder"),
            height=42, corner_radius=20, border_color=COLOR_LIGHT_PINK,
            fg_color=COLOR_INPUT_BG, text_color=COLOR_PINK, font=("Arial", 13)
        )
        re.pack(fill="x", pady=(0, 12))
        
        ctk.CTkLabel(self.form_container, text=self.t("create_password"),
                    font=("Arial", 12), text_color=COLOR_PINK).pack(anchor="w", pady=(5, 3))
        rp = ctk.CTkEntry(
            self.form_container, placeholder_text=self.t("password_min"),
            height=42, corner_radius=20, border_color=COLOR_LIGHT_PINK,
            fg_color=COLOR_INPUT_BG, text_color=COLOR_PINK, show="•", font=("Arial", 13)
        )
        rp.pack(fill="x", pady=(0, 12))
        
        ctk.CTkLabel(self.form_container, text=self.t("repeat_password"),
                    font=("Arial", 12), text_color=COLOR_PINK).pack(anchor="w", pady=(5, 3))
        rpr = ctk.CTkEntry(
            self.form_container, placeholder_text=self.t("repeat_placeholder"),
            height=42, corner_radius=20, border_color=COLOR_LIGHT_PINK,
            fg_color=COLOR_INPUT_BG, text_color=COLOR_PINK, show="•", font=("Arial", 13)
        )
        rpr.pack(fill="x", pady=(0, 20))
        
        ctk.CTkButton(
            self.form_container, text=self.t("register_btn"),
            command=lambda: self.register(rl.get().strip(), re.get().strip(), 
                                          rp.get(), rpr.get()),
            height=42, corner_radius=20,
            fg_color=COLOR_PINK, hover_color=COLOR_DARK_PINK,
            font=("Arial", 15, "bold")
        ).pack(fill="x", pady=10)
    
    def register(self, login, email, pw, pwr):
        if not all([login, email, pw, pwr]):
            self.message_label.configure(text=self.t("fill_all"), text_color=COLOR_DARK_PINK)
            return
        if len(login) < 3:
            self.message_label.configure(text=self.t("login_short"), text_color=COLOR_DARK_PINK)
            return
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            self.message_label.configure(text=self.t("invalid_email"), text_color=COLOR_DARK_PINK)
            return
        if len(pw) < 6:
            self.message_label.configure(text=self.t("password_short"), text_color=COLOR_DARK_PINK)
            return
        if pw != pwr:
            self.message_label.configure(text=self.t("passwords_dont_match"), text_color=COLOR_DARK_PINK)
            return
        if login in self.registered_users:
            self.message_label.configure(text=self.t("login_taken"), text_color=COLOR_DARK_PINK)
            return
        for d in self.registered_users.values():
            if d.get('email') == email:
                self.message_label.configure(text=self.t("email_taken"), text_color=COLOR_DARK_PINK)
                return
        
        self.registered_users[login] = {
            "login": login, "email": email, "password": pw,
            "registered_at": datetime.now().isoformat(),
            "bio": "", "status": "active"
        }
        self.save_users()
        self.message_label.configure(text=self.t("reg_success"), text_color=COLOR_GREEN)
        self.show_login_page()
        self.window.after(1200, lambda: self.login(login, pw))
    
    def login(self, login_input, password):
        if not login_input or not password:
            self.message_label.configure(text=self.t("fill_all"), text_color=COLOR_DARK_PINK)
            return
        ud = None
        if login_input in self.registered_users:
            ud = self.registered_users[login_input]
        else:
            for d in self.registered_users.values():
                if d.get('email') == login_input:
                    ud = d
                    break
        if not ud:
            self.message_label.configure(text=self.t("user_not_found"), text_color=COLOR_DARK_PINK)
            return
        if password == ud.get('password'):
            self.current_user = ud
            if self.remember_me.get():
                self.save_session(ud['login'])
            self.load_playlist()  # Загружаем плейлист этого юзера
            self.show_main_menu()
        else:
            self.message_label.configure(text=self.t("wrong_password"), text_color=COLOR_DARK_PINK)
    
    # ==================== ГЛАВНОЕ МЕНЮ ====================
    def show_main_menu(self):
        self.clear_container()
        self.current_dialog_with = None
        mf = ctk.CTkScrollableFrame(self.main_container, fg_color=COLOR_BG, corner_radius=30)
        mf.pack(fill="both", expand=True, padx=15, pady=15)
        self._bind_mousewheel(mf)
        
        tf = ctk.CTkFrame(mf, fg_color=COLOR_PINK, corner_radius=20)
        tf.pack(fill="x", padx=15, pady=15)
        
        avatar_path = self.get_avatar_path()
        if os.path.exists(avatar_path):
            try:
                pil_img = Image.open(avatar_path).resize((60, 60), Image.Resampling.LANCZOS)
                avatar_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(60, 60))
                ctk.CTkLabel(tf, image=avatar_img, text="").pack(pady=(15, 5))
            except:
                ctk.CTkLabel(tf, text="🌸", font=("Arial", 40)).pack(pady=(15, 5))
        else:
            ctk.CTkLabel(tf, text="🌸", font=("Arial", 40)).pack(pady=(15, 5))
        
        ctk.CTkLabel(tf, text=self.t("welcome_back"), 
                    font=("Arial", 22, "bold"), text_color="white").pack(pady=5)
        ctk.CTkLabel(tf, text=f"👤 {self.current_user['login']}", 
                    font=("Arial", 16), text_color=COLOR_HOVER).pack(pady=(0, 15))
        
        menu = ctk.CTkFrame(mf, fg_color="transparent")
        menu.pack(fill="both", expand=True, padx=15, pady=10)
        
        # Сообщения с бейджем непрочитанных
        msg_frame = ctk.CTkFrame(menu, fg_color="transparent")
        msg_frame.pack(fill="x", pady=4)
        
        unread = self.count_unread_total()
        msg_text = self.t("messages")
        if unread > 0:
            msg_text = f"{msg_text} 🔴{unread}"
        
        ctk.CTkButton(
            msg_frame, text=msg_text, command=self.show_messages,
            height=50, corner_radius=25,
            fg_color="white", text_color=COLOR_PINK, hover_color=COLOR_HOVER,
            font=("Arial", 15, "bold"),
            border_width=2, border_color=COLOR_LIGHT_PINK
        ).pack(side="left", fill="x", expand=True)
        
        for text, cmd in [
            (self.t("profile"), self.show_profile),
            (self.t("music"), self.show_music),
            (self.t("settings"), self.show_settings),
            (self.t("help"), self.show_help)
        ]:
            ctk.CTkButton(
                menu, text=text, command=cmd, height=50, corner_radius=25,
                fg_color="white", text_color=COLOR_PINK, hover_color=COLOR_HOVER,
                font=("Arial", 15, "bold"),
                border_width=2, border_color=COLOR_LIGHT_PINK
            ).pack(fill="x", pady=4)
        
        ctk.CTkButton(
            mf, text=self.t("logout"), command=self.logout,
            height=40, corner_radius=20,
            fg_color=COLOR_DARK_PINK, hover_color=COLOR_RED,
            font=("Arial", 13, "bold")
        ).pack(fill="x", padx=15, pady=(15, 5))
        ctk.CTkLabel(mf, text=self.t("love"), 
                    font=("Arial", 11), text_color=COLOR_LIGHT_PINK).pack(pady=(15, 0))
        ctk.CTkLabel(mf, text=self.t("version"), 
                    font=("Arial", 10, "bold"), text_color=COLOR_LIGHT_PINK).pack(pady=(0, 15))
    
    # ==================== ПРОФИЛЬ ====================
    def show_profile(self):
        self.clear_container()
        frame = ctk.CTkScrollableFrame(self.main_container, fg_color=COLOR_BG, corner_radius=30)
        frame.pack(fill="both", expand=True, padx=15, pady=15)
        self._bind_mousewheel(frame)
        
        top_bar = ctk.CTkFrame(frame, fg_color="transparent")
        top_bar.pack(fill="x", pady=(10, 5))
        ctk.CTkButton(
            top_bar, text=self.t("back"), command=self.back_to_menu,
            fg_color="transparent", text_color=COLOR_PINK,
            hover_color=COLOR_HOVER, font=("Arial", 13, "bold"),
            corner_radius=20, height=35, width=100
        ).pack(side="left")
        
        ctk.CTkButton(
            top_bar, text=self.t("edit_profile"), command=self.edit_profile,
            fg_color=COLOR_PINK, hover_color=COLOR_DARK_PINK,
            corner_radius=20, height=35, font=("Arial", 12, "bold")
        ).pack(side="right")
        
        ctk.CTkLabel(frame, text=self.t("profile"), 
                    font=("Arial", 24, "bold"), text_color=COLOR_PINK).pack(pady=10)
        
        avatar_frame = ctk.CTkFrame(frame, fg_color="white", corner_radius=20)
        avatar_frame.pack(fill="x", padx=20, pady=10)
        
        avatar_img = self.load_avatar_image(150)
        if avatar_img:
            ctk.CTkLabel(avatar_frame, image=avatar_img, text="").pack(pady=(20, 10))
        else:
            ctk.CTkLabel(
                avatar_frame, text=self.t("no_avatar"), font=("Arial", 80),
                fg_color=COLOR_HOVER, corner_radius=75, width=150, height=150
            ).pack(pady=(20, 10))
        
        ctk.CTkButton(
            avatar_frame, text=self.t("change_photo"), command=self.change_avatar,
            fg_color=COLOR_LIGHT_PINK, hover_color=COLOR_PINK,
            corner_radius=20, height=38, font=("Arial", 13, "bold"),
            text_color=COLOR_DARK_PINK
        ).pack(fill="x", padx=30, pady=(5, 20))
        
        info_frame = ctk.CTkFrame(frame, fg_color="white", corner_radius=20)
        info_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(info_frame, text=f"👤 {self.current_user['login']}", 
                    font=("Arial", 22, "bold"), text_color=COLOR_DARK_PINK).pack(pady=(20, 5))
        
        status_key = self.current_user.get('status', 'active')
        status_text = self.t_status(status_key)
        status_colors = {
            'active': '#32CD32', 'online': '#00FF00', 'busy': '#FF0000',
            'away': '#FFA500', 'sleeping': '#9370DB', 'invisible': '#808080'
        }
        status_color = status_colors.get(status_key, '#32CD32')
        
        status_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
        status_frame.pack(pady=5)
        ctk.CTkLabel(status_frame, text="●", font=("Arial", 16), 
                    text_color=status_color).pack(side="left", padx=(0, 5))
        ctk.CTkLabel(status_frame, text=f"{self.t('status')}: {status_text}", 
                    font=("Arial", 13, "bold"), text_color=COLOR_LIGHT_PINK).pack(side="left")
        
        ctk.CTkLabel(info_frame, text=f"📧 {self.current_user['email']}", 
                    font=("Arial", 13), text_color=COLOR_LIGHT_PINK).pack(pady=5)
        ctk.CTkLabel(info_frame, 
                    text=f"{self.t('registered')} {self.current_user.get('registered_at', '')[:10]}", 
                    font=("Arial", 12), text_color=COLOR_LIGHT_PINK).pack(pady=(0, 15))
        
        bio = self.current_user.get('bio', '').strip()
        if bio:
            bio_frame = ctk.CTkFrame(frame, fg_color="white", corner_radius=20)
            bio_frame.pack(fill="x", padx=20, pady=10)
            ctk.CTkLabel(bio_frame, text=self.t("bio"), 
                        font=("Arial", 14, "bold"), text_color=COLOR_PINK).pack(pady=(15, 5), padx=20, anchor="w")
            ctk.CTkLabel(bio_frame, text=bio, 
                        font=("Arial", 13), text_color=COLOR_DARK_PINK,
                        wraplength=350, justify="left").pack(pady=(0, 15), padx=20, anchor="w")
        
        ctk.CTkButton(
            frame, text=self.t("logout"), command=self.logout,
            fg_color=COLOR_DARK_PINK, hover_color=COLOR_RED,
            corner_radius=20, height=40, font=("Arial", 14, "bold")
        ).pack(fill="x", padx=20, pady=10)
    
    def edit_profile(self):
        self.clear_container()
        frame = ctk.CTkScrollableFrame(self.main_container, fg_color=COLOR_BG, corner_radius=30)
        frame.pack(fill="both", expand=True, padx=15, pady=15)
        self._bind_mousewheel(frame)
        
        ctk.CTkButton(
            frame, text=self.t("back"), command=self.show_profile,
            fg_color="transparent", text_color=COLOR_PINK,
            hover_color=COLOR_HOVER, font=("Arial", 13, "bold"),
            corner_radius=20, height=35
        ).pack(anchor="w", pady=(10, 5))
        
        ctk.CTkLabel(frame, text=self.t("edit_profile"), 
                    font=("Arial", 22, "bold"), text_color=COLOR_PINK).pack(pady=10)
        
        avatar_frame = ctk.CTkFrame(frame, fg_color="white", corner_radius=20)
        avatar_frame.pack(fill="x", padx=20, pady=10)
        
        avatar_img = self.load_avatar_image(120)
        if avatar_img:
            ctk.CTkLabel(avatar_frame, image=avatar_img, text="").pack(pady=(15, 10))
        else:
            ctk.CTkLabel(
                avatar_frame, text=self.t("no_avatar"), font=("Arial", 60),
                fg_color=COLOR_HOVER, corner_radius=60, width=120, height=120
            ).pack(pady=(15, 10))
        
        ctk.CTkButton(
            avatar_frame, text=self.t("change_photo"), command=lambda: self.change_avatar_edit(self.edit_profile),
            fg_color=COLOR_LIGHT_PINK, hover_color=COLOR_PINK,
            corner_radius=20, height=35, font=("Arial", 12, "bold"),
            text_color=COLOR_DARK_PINK
        ).pack(fill="x", padx=30, pady=(5, 15))
        
        bio_frame = ctk.CTkFrame(frame, fg_color="white", corner_radius=20)
        bio_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(bio_frame, text=self.t("bio"), 
                    font=("Arial", 14, "bold"), text_color=COLOR_PINK).pack(pady=(15, 5), padx=20, anchor="w")
        
        self.bio_text = ctk.CTkTextbox(
            bio_frame, height=100, corner_radius=15,
            border_color=COLOR_LIGHT_PINK, border_width=2,
            fg_color=COLOR_INPUT_BG, text_color=COLOR_DARK_PINK,
            font=("Arial", 13)
        )
        self.bio_text.pack(fill="x", padx=20, pady=(0, 5))
        self.bio_text.insert("1.0", self.current_user.get('bio', ''))
        
        status_frame = ctk.CTkFrame(frame, fg_color="white", corner_radius=20)
        status_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(status_frame, text=self.t("choose_status"), 
                    font=("Arial", 14, "bold"), text_color=COLOR_PINK).pack(pady=(15, 10), padx=20, anchor="w")
        
        status_grid = ctk.CTkFrame(status_frame, fg_color="transparent")
        status_grid.pack(fill="x", padx=15, pady=(0, 15))
        
        self.status_var = ctk.StringVar(value=self.current_user.get('status', 'active'))
        self.status_buttons = {}
        
        status_colors_map = {
            'active': '#32CD32', 'online': '#00FF00', 'busy': '#FF0000',
            'away': '#FFA500', 'sleeping': '#9370DB', 'invisible': '#808080'
        }
        
        for i, st in enumerate(STATUSES):
            row, col = divmod(i, 2)
            is_selected = self.status_var.get() == st
            btn = ctk.CTkButton(
                status_grid, 
                text=f"● {self.t_status(st)}",
                command=lambda s=st: self.select_status(s),
                fg_color=status_colors_map.get(st, COLOR_LIGHT_PINK) if is_selected else "white",
                text_color="white" if is_selected else COLOR_PINK,
                hover_color=status_colors_map.get(st, COLOR_PINK),
                corner_radius=15, height=40,
                font=("Arial", 12, "bold"),
                border_width=2, 
                border_color=status_colors_map.get(st, COLOR_LIGHT_PINK)
            )
            btn.grid(row=row, column=col, padx=5, pady=5, sticky="ew")
            self.status_buttons[st] = btn
        
        status_grid.grid_columnconfigure(0, weight=1)
        status_grid.grid_columnconfigure(1, weight=1)
        
        self.edit_message = ctk.CTkLabel(frame, text="", font=("Arial", 12, "bold"))
        self.edit_message.pack(pady=5)
        
        ctk.CTkButton(
            frame, text=self.t("save_profile"), command=self.save_profile,
            fg_color=COLOR_GREEN, hover_color="#228B22",
            corner_radius=20, height=45, font=("Arial", 15, "bold")
        ).pack(fill="x", padx=20, pady=(10, 5))
        
        ctk.CTkButton(
            frame, text=self.t("back"), command=self.show_profile,
            fg_color="transparent", text_color=COLOR_PINK,
            hover_color=COLOR_HOVER, font=("Arial", 12),
            corner_radius=20, height=35
        ).pack(pady=(5, 10))
    
    def select_status(self, status):
        self.status_var.set(status)
        status_colors_map = {
            'active': '#32CD32', 'online': '#00FF00', 'busy': '#FF0000',
            'away': '#FFA500', 'sleeping': '#9370DB', 'invisible': '#808080'
        }
        for st, btn in self.status_buttons.items():
            is_selected = st == status
            btn.configure(
                fg_color=status_colors_map.get(st, COLOR_LIGHT_PINK) if is_selected else "white",
                text_color="white" if is_selected else COLOR_PINK
            )
    
    def change_avatar(self):
        self.change_avatar_internal(self.show_profile)
    
    def change_avatar_edit(self, callback):
        self.change_avatar_internal(callback)
    
    def change_avatar_internal(self, callback):
        fp = filedialog.askopenfilename(
            title="Выберите фото",
            filetypes=[("Изображения", "*.png *.jpg *.jpeg *.gif *.bmp")]
        )
        if fp:
            try:
                avatar = self.make_circle_avatar(fp, size=300)
                if avatar:
                    avatar.save(self.get_avatar_path(), "PNG")
            except Exception as e:
                logging.error(f"Ошибка сохранения аватара: {e}")
            callback()
    
    def save_profile(self):
        try:
            bio = self.bio_text.get("1.0", "end-1c").strip()
            new_status = self.status_var.get()
            
            if len(bio) > 500:
                self.edit_message.configure(text="❌ Био слишком длинное (макс 500)", text_color=COLOR_RED)
                return
            
            login = self.current_user['login']
            self.registered_users[login]['bio'] = bio
            self.registered_users[login]['status'] = new_status
            self.current_user = self.registered_users[login]
            self.save_users()
            
            self.edit_message.configure(text=self.t("profile_saved"), text_color=COLOR_GREEN)
            self.window.after(800, self.show_profile)
        except Exception as e:
            logging.error(f"Ошибка сохранения профиля: {e}")
            self.edit_message.configure(text="❌ Ошибка", text_color=COLOR_RED)
    
    # ==================== МУЗЫКА ====================
    def show_music(self):
        self.clear_container()
        frame = ctk.CTkScrollableFrame(self.main_container, fg_color=COLOR_BG, corner_radius=30)
        frame.pack(fill="both", expand=True, padx=15, pady=15)
        self._bind_mousewheel(frame)
        
        ctk.CTkButton(
            frame, text=self.t("back"), command=self.back_to_menu,
            fg_color="transparent", text_color=COLOR_PINK,
            hover_color=COLOR_HOVER, font=("Arial", 13, "bold"),
            corner_radius=20, height=35
        ).pack(anchor="w", pady=(10, 10))
        ctk.CTkLabel(frame, text=self.t("music"), 
                    font=("Arial", 22, "bold"), text_color=COLOR_PINK).pack(pady=10)
        
        np = ctk.CTkFrame(frame, fg_color="white", corner_radius=15)
        np.pack(fill="x", padx=20, pady=10)
        
        if self.is_playing and 0 <= self.current_track_index < len(self.playlist):
            tn = self.playlist[self.current_track_index]['name']
            st = self.t("playing") if not self.is_paused else self.t("paused")
        else:
            tn = self.t("no_track")
            st = self.t("stopped")
        
        ctk.CTkLabel(np, text=self.t("now_playing"), 
                    font=("Arial", 13, "bold"), text_color=COLOR_PINK).pack(pady=(15, 5))
        ctk.CTkLabel(np, text=tn, font=("Arial", 16, "bold"), 
                    text_color=COLOR_DARK_PINK, wraplength=350).pack(pady=5)
        ctk.CTkLabel(np, text=st, font=("Arial", 12), 
                    text_color=COLOR_LIGHT_PINK).pack(pady=(0, 5))
        
        cp = self.get_current_position()
        self.time_label = ctk.CTkLabel(
            np, text=f"{self.format_time(cp)} / {self.format_time(self.track_length)}",
            font=("Arial", 14, "bold"), text_color=COLOR_PINK
        )
        self.time_label.pack(pady=5)
        
        self.progress_slider = ctk.CTkSlider(
            np, from_=0, to=1, number_of_steps=100,
            command=self.on_progress_change,
            fg_color=COLOR_HOVER, progress_color=COLOR_PINK,
            button_color=COLOR_DARK_PINK, button_hover_color=COLOR_PINK
        )
        self.progress_slider.pack(fill="x", padx=20, pady=(5, 15))
        if self.track_length > 0 and self.is_playing:
            self.progress_slider.set(min(cp / self.track_length, 1.0))
        else:
            self.progress_slider.set(0)
        
        ctr = ctk.CTkFrame(frame, fg_color="transparent")
        ctr.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkButton(ctr, text="⏮️", command=self.play_previous_refresh, 
                     width=50, height=45, corner_radius=15,
                     fg_color=COLOR_LIGHT_PINK, hover_color=COLOR_PINK, 
                     font=("Arial", 18)).pack(side="left", padx=3)
        
        btn_text = "⏸️" if (self.is_playing and not self.is_paused) else "▶️"
        ctk.CTkButton(ctr, text=btn_text, command=self.play_pause_refresh, 
                     width=60, height=45, corner_radius=15,
                     fg_color=COLOR_PINK, hover_color=COLOR_DARK_PINK, 
                     font=("Arial", 18)).pack(side="left", padx=3)
        
        ctk.CTkButton(ctr, text="⏭️", command=self.play_next_refresh, 
                     width=50, height=45, corner_radius=15,
                     fg_color=COLOR_LIGHT_PINK, hover_color=COLOR_PINK, 
                     font=("Arial", 18)).pack(side="left", padx=3)
        ctk.CTkButton(ctr, text="⏹️", command=self.stop_music_refresh, 
                     width=50, height=45, corner_radius=15,
                     fg_color=COLOR_DARK_PINK, hover_color=COLOR_RED, 
                     font=("Arial", 18)).pack(side="left", padx=3)
        
        vf = ctk.CTkFrame(frame, fg_color="white", corner_radius=15)
        vf.pack(fill="x", padx=20, pady=10)
        vr = ctk.CTkFrame(vf, fg_color="transparent")
        vr.pack(fill="x", padx=15, pady=(15, 5))
        ctk.CTkLabel(vr, text=self.t("volume"), 
                    font=("Arial", 13, "bold"), text_color=COLOR_PINK).pack(side="left")
        vp = int(self.music_volume * 100)
        self.volume_value_label = ctk.CTkLabel(
            vr, text=f"{vp}%", font=("Arial", 18, "bold"), 
            text_color=COLOR_RED if self.music_volume > 1.0 else COLOR_DARK_PINK, 
            width=70
        )
        self.volume_value_label.pack(side="right")
        
        self.volume_slider = ctk.CTkSlider(
            vf, from_=0, to=1.25, number_of_steps=25,
            command=self.on_volume_change,
            fg_color=COLOR_HOVER, progress_color=COLOR_PINK,
            button_color=COLOR_DARK_PINK, button_hover_color=COLOR_PINK
        )
        self.volume_slider.pack(fill="x", padx=20, pady=(5, 5))
        self.volume_slider.set(self.music_volume)
        
        vl = ctk.CTkFrame(vf, fg_color="transparent")
        vl.pack(fill="x", padx=20, pady=(0, 10))
        ctk.CTkLabel(vl, text="0%", font=("Arial", 9), 
                    text_color=COLOR_LIGHT_PINK).pack(side="left")
        ctk.CTkLabel(vl, text="50%", font=("Arial", 9), 
                    text_color=COLOR_LIGHT_PINK).pack(side="left", expand=True)
        ctk.CTkLabel(vl, text="100%", font=("Arial", 9), 
                    text_color=COLOR_LIGHT_PINK).pack(side="left", expand=True)
        ctk.CTkLabel(vl, text="125%", font=("Arial", 9, "bold"), 
                    text_color=COLOR_PINK).pack(side="right")
        
        pl = ctk.CTkFrame(frame, fg_color="white", corner_radius=15)
        pl.pack(fill="x", padx=20, pady=10)
        ctk.CTkLabel(pl, text=self.t("playlist"), 
                    font=("Arial", 15, "bold"), text_color=COLOR_PINK).pack(pady=(15, 10))
        
        if len(self.playlist) == 0:
            ctk.CTkLabel(pl, text=self.t("playlist_empty"), 
                        font=("Arial", 13), text_color=COLOR_LIGHT_PINK, 
                        justify="center").pack(pady=20)
        else:
            for i, track in enumerate(self.playlist):
                tr = ctk.CTkFrame(pl, fg_color=COLOR_HOVER if i == self.current_track_index else "transparent",
                                 corner_radius=8)
                tr.pack(fill="x", padx=10, pady=3)
                ctk.CTkButton(
                    tr, text="▶️", command=lambda idx=i: self.play_track_refresh(idx), 
                    width=35, height=30, corner_radius=10,
                    fg_color=COLOR_PINK, hover_color=COLOR_DARK_PINK, 
                    font=("Arial", 12)
                ).pack(side="left", padx=(5, 10))
                tt = f"🎵 {i+1}. {track['name']}" if i == self.current_track_index else f"{i+1}. {track['name']}"
                ctk.CTkLabel(tr, text=tt, 
                            font=("Arial", 12, "bold" if i == self.current_track_index else "normal"),
                            text_color=COLOR_PINK).pack(side="left", fill="x", expand=True)
                ctk.CTkButton(
                    tr, text="🗑️", command=lambda idx=i: self.delete_track_refresh(idx), 
                    width=35, height=30, corner_radius=10,
                    fg_color=COLOR_DARK_PINK, hover_color=COLOR_RED, 
                    font=("Arial", 12)
                ).pack(side="right", padx=(10, 5))
        
        ctk.CTkButton(
            frame, text=self.t("add_music"), command=self.add_music_files_refresh,
            fg_color=COLOR_GREEN, hover_color="#228B22", corner_radius=20, 
            height=40, font=("Arial", 14, "bold")
        ).pack(fill="x", padx=20, pady=10)
        ctk.CTkButton(
            frame, text=self.t("back"), command=self.back_to_menu,
            fg_color="transparent", text_color=COLOR_PINK,
            hover_color=COLOR_HOVER, font=("Arial", 12),
            corner_radius=20, height=35
        ).pack(pady=10)
    
    def on_progress_change(self, value):
        if self.is_playing and self.track_length > 0:
            self.is_seeking = True
            self.seek_music(value * self.track_length)
            self.window.after(300, lambda: setattr(self, 'is_seeking', False))
    
    def on_volume_change(self, value):
        self.set_volume(value)
        vp = int(value * 100)
        if hasattr(self, 'volume_value_label'):
            self.volume_value_label.configure(
                text=f"{vp}%", 
                text_color=COLOR_RED if value > 1.0 else COLOR_DARK_PINK
            )
    
    def play_pause_refresh(self):
        if self.is_playing and not self.is_paused:
            self.pause_music()
        elif self.is_paused:
            self.pause_music()
        elif len(self.playlist) > 0:
            if self.current_track_index < 0 or self.current_track_index >= len(self.playlist):
                self.current_track_index = 0
            self.play_music(self.playlist[self.current_track_index]['path'])
        self.show_music()
    
    def play_next_refresh(self): 
        self.play_next()
        self.show_music()
    
    def play_previous_refresh(self): 
        self.play_previous()
        self.show_music()
    
    def stop_music_refresh(self): 
        self.stop_music()
        self.current_track_index = -1
        self.show_music()
    
    def play_track_refresh(self, index):
        if 0 <= index < len(self.playlist):
            self.current_track_index = index
            self.play_music(self.playlist[index]['path'])
            self.show_music()
    
    def delete_track_refresh(self, index):
        self.remove_track(index)
        if self.current_track_index >= len(self.playlist):
            self.current_track_index = len(self.playlist) - 1
        self.show_music()
    
    def add_music_files_refresh(self): 
        self.add_music_files()
        self.show_music()
    
    # ==================== СООБЩЕНИЯ ====================
    def show_messages(self):
        self.clear_container()
        frame = ctk.CTkScrollableFrame(self.main_container, fg_color=COLOR_BG, corner_radius=30)
        frame.pack(fill="both", expand=True, padx=15, pady=15)
        self._bind_mousewheel(frame)
        
        ctk.CTkButton(
            frame, text=self.t("back"), command=self.back_to_menu,
            fg_color="transparent", text_color=COLOR_PINK,
            hover_color=COLOR_HOVER, font=("Arial", 13, "bold"),
            corner_radius=20, height=35
        ).pack(anchor="w", pady=(10, 10))
        
        ctk.CTkLabel(frame, text=self.t("messages"), 
                    font=("Arial", 24, "bold"), text_color=COLOR_PINK).pack(pady=10)
        
        # Поиск пользователя
        search_frame = ctk.CTkFrame(frame, fg_color="white", corner_radius=15)
        search_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(search_frame, text=self.t("to_user"), 
                    font=("Arial", 12, "bold"), text_color=COLOR_PINK).pack(pady=(10, 5), padx=15, anchor="w")
        
        search_entry = ctk.CTkEntry(
            search_frame, placeholder_text=self.t("search_placeholder"),
            height=38, corner_radius=15,
            border_color=COLOR_LIGHT_PINK, fg_color=COLOR_INPUT_BG,
            text_color=COLOR_PINK, font=("Arial", 13)
        )
        search_entry.pack(fill="x", padx=15, pady=(0, 5))
        
        search_msg = ctk.CTkLabel(search_frame, text="", font=("Arial", 11), text_color=COLOR_RED)
        search_msg.pack(pady=2)
        
        ctk.CTkButton(
            search_frame, text=self.t("find_user"),
            command=lambda: self.find_user_for_message(search_entry.get().strip(), search_msg),
            fg_color=COLOR_PINK, hover_color=COLOR_DARK_PINK,
            corner_radius=15, height=35, font=("Arial", 13, "bold")
        ).pack(fill="x", padx=15, pady=(5, 15))
        
        # Список диалогов
        dialogs_label = ctk.CTkLabel(frame, text="💬 Диалоги:", 
                                    font=("Arial", 14, "bold"), text_color=COLOR_PINK)
        dialogs_label.pack(pady=(10, 5), padx=20, anchor="w")
        
        dialogs = self.get_user_dialogs()
        if not dialogs:
            ctk.CTkLabel(frame, text=self.t("no_dialogs"), 
                        font=("Arial", 13), text_color=COLOR_LIGHT_PINK, 
                        justify="center").pack(pady=20)
        else:
            for other in dialogs:
                self.create_dialog_button(frame, other)
    
    def create_dialog_button(self, parent, other_user):
        """Создание кнопки диалога"""
        has_unread = self.has_unread_messages(other_user)
        messages = self.get_dialog_messages(other_user)
        last_msg = messages[-1] if messages else None
        
        dialog_frame = ctk.CTkFrame(parent, fg_color="white", corner_radius=12)
        dialog_frame.pack(fill="x", padx=20, pady=3)
        
        # Аватарка
        avatar_img = self.load_avatar_image(size=45, login=other_user)
        if avatar_img:
            ctk.CTkLabel(dialog_frame, image=avatar_img, text="", width=50).pack(side="left", padx=(10, 5), pady=10)
        else:
            ctk.CTkLabel(dialog_frame, text="🌸", font=("Arial", 25), 
                        width=50, height=50, fg_color=COLOR_HOVER, corner_radius=25
            ).pack(side="left", padx=(10, 5), pady=10)
        
        # Текст
        text_frame = ctk.CTkFrame(dialog_frame, fg_color="transparent")
        text_frame.pack(side="left", fill="both", expand=True, padx=5, pady=10)
        
        name_text = f"👤 {other_user}"
        if has_unread:
            name_text += " 🔴"
        ctk.CTkLabel(text_frame, text=name_text, 
                    font=("Arial", 14, "bold"), text_color=COLOR_PINK,
                    anchor="w").pack(fill="x")
        
        if last_msg:
            preview = last_msg['text'][:30] + ("..." if len(last_msg['text']) > 30 else "")
            time_str = self.format_msg_time(last_msg['time'])
            preview_text = f"{preview} • {time_str}"
            ctk.CTkLabel(text_frame, text=preview_text, 
                        font=("Arial", 11), text_color=COLOR_LIGHT_PINK,
                        anchor="w").pack(fill="x")
        
        # Кнопки
        ctk.CTkButton(
            dialog_frame, text="💬",
            command=lambda u=other_user: self.open_dialog(u),
            width=40, height=40, corner_radius=10,
            fg_color=COLOR_PINK, hover_color=COLOR_DARK_PINK,
            font=("Arial", 16)
        ).pack(side="right", padx=(5, 5))
        
        ctk.CTkButton(
            dialog_frame, text="🗑️",
            command=lambda u=other_user: self.confirm_delete_dialog(u),
            width=40, height=40, corner_radius=10,
            fg_color=COLOR_RED, hover_color="#AA0000",
            font=("Arial", 14)
        ).pack(side="right", padx=(0, 5))
    
    def find_user_for_message(self, username, msg_label):
        if not username:
            msg_label.configure(text="❌ Введите логин", text_color=COLOR_RED)
            return
        if username == self.current_user['login']:
            msg_label.configure(text=self.t("cannot_message_self"), text_color=COLOR_RED)
            return
        if username not in self.registered_users:
            msg_label.configure(text=self.t("user_not_found_msg"), text_color=COLOR_RED)
            return
        msg_label.configure(text=f"✅ {username}", text_color=COLOR_GREEN)
        self.window.after(500, lambda: self.open_dialog(username))
    
    def open_dialog(self, other_user):
        """Открыть диалог с пользователем"""
        if other_user not in self.registered_users:
            return
        if other_user == self.current_user['login']:
            return
        
        self.current_dialog_with = other_user
        self.mark_dialog_read(other_user)
        self.show_dialog()
    
    def show_dialog(self):
        self.clear_container()
        frame = ctk.CTkFrame(self.main_container, fg_color=COLOR_BG)
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Шапка
        header = ctk.CTkFrame(frame, fg_color=COLOR_PINK, corner_radius=15, height=60)
        header.pack(fill="x", pady=(0, 10))
        header.pack_propagate(False)
        
        ctk.CTkButton(
            header, text="←", command=self.show_messages,
            width=40, height=40, corner_radius=10,
            fg_color="white", text_color=COLOR_PINK,
            hover_color=COLOR_HOVER, font=("Arial", 18, "bold")
        ).pack(side="left", padx=10, pady=10)
        
        # Аватарка собеседника
        avatar_img = self.load_avatar_image(size=40, login=self.current_dialog_with)
        if avatar_img:
            ctk.CTkLabel(header, image=avatar_img, text="").pack(side="left", padx=5, pady=10)
        else:
            ctk.CTkLabel(header, text="🌸", font=("Arial", 20),
                        fg_color=COLOR_HOVER, corner_radius=20, width=40, height=40
            ).pack(side="left", padx=5, pady=10)
        
        ctk.CTkLabel(header, text=self.current_dialog_with, 
                    font=("Arial", 16, "bold"), text_color="white"
        ).pack(side="left", padx=5)
        
        # Область сообщений
        msg_frame = ctk.CTkScrollableFrame(frame, fg_color="white", corner_radius=15)
        msg_frame.pack(fill="both", expand=True, pady=(0, 10))
        self._bind_mousewheel(msg_frame)
        
        messages = self.get_dialog_messages(self.current_dialog_with)
        if not messages:
            ctk.CTkLabel(msg_frame, text=self.t("no_messages_in_dialog"), 
                        font=("Arial", 13), text_color=COLOR_LIGHT_PINK, 
                        justify="center").pack(pady=30)
        else:
            for msg in messages:
                self.create_message_bubble(msg_frame, msg)
        
        # Поле ввода
        input_frame = ctk.CTkFrame(frame, fg_color="white", corner_radius=15)
        input_frame.pack(fill="x", pady=(0, 5))
        
        self.msg_entry = ctk.CTkEntry(
            input_frame, placeholder_text=self.t("message_placeholder"),
            height=40, corner_radius=20,
            border_color=COLOR_LIGHT_PINK, fg_color=COLOR_INPUT_BG,
            text_color=COLOR_PINK, font=("Arial", 13)
        )
        self.msg_entry.pack(side="left", fill="x", expand=True, padx=(10, 5), pady=10)
        self.msg_entry.bind("<Return>", lambda e: self.send_current_message())
        
        ctk.CTkButton(
            input_frame, text=self.t("send_message"),
            command=self.send_current_message,
            width=100, height=40, corner_radius=20,
            fg_color=COLOR_PINK, hover_color=COLOR_DARK_PINK,
            font=("Arial", 13, "bold")
        ).pack(side="right", padx=(5, 10), pady=10)
    
    def create_message_bubble(self, parent, msg):
        is_mine = msg['from'] == self.current_user['login']
        
        bubble_frame = ctk.CTkFrame(parent, fg_color="transparent")
        bubble_frame.pack(fill="x", padx=10, pady=2)
        
        if is_mine:
            container = ctk.CTkFrame(bubble_frame, fg_color="transparent")
            container.pack(side="right")
            bubble = ctk.CTkFrame(container, fg_color=COLOR_PINK, corner_radius=15)
            bubble.pack(side="right", padx=5)
            
            ctk.CTkLabel(bubble, text=msg['text'], 
                        font=("Arial", 13), text_color="white",
                        wraplength=250, justify="left"
            ).pack(padx=12, pady=(8, 2))
            
            time_text = self.format_msg_time(msg['time'])
            ctk.CTkLabel(bubble, text=time_text, 
                        font=("Arial", 9), text_color=COLOR_HOVER
            ).pack(padx=12, pady=(0, 5))
        else:
            container = ctk.CTkFrame(bubble_frame, fg_color="transparent")
            container.pack(side="left")
            bubble = ctk.CTkFrame(container, fg_color=COLOR_HOVER, corner_radius=15)
            bubble.pack(side="left", padx=5)
            
            ctk.CTkLabel(bubble, text=msg['text'], 
                        font=("Arial", 13), text_color=COLOR_DARK_PINK,
                        wraplength=250, justify="left"
            ).pack(padx=12, pady=(8, 2))
            
            time_text = self.format_msg_time(msg['time'])
            ctk.CTkLabel(bubble, text=f"{self.current_dialog_with} • {time_text}", 
                        font=("Arial", 9), text_color=COLOR_LIGHT_PINK
            ).pack(padx=12, pady=(0, 5))
    
    def send_current_message(self):
        if not self.current_dialog_with:
            return
        text = self.msg_entry.get().strip()
        if not text:
            return
        if self.send_message_to(self.current_dialog_with, text):
            self.msg_entry.delete(0, "end")
            self.show_dialog()  # Обновляем
        else:
            self.msg_entry.configure(border_color=COLOR_RED)
            self.window.after(1000, lambda: self.msg_entry.configure(border_color=COLOR_LIGHT_PINK))
    
    def confirm_delete_dialog(self, other_user):
        self.delete_dialog(other_user)
        self.show_messages()
    
    # ==================== НАСТРОЙКИ ====================
    def show_settings(self):
        self.clear_container()
        frame = ctk.CTkScrollableFrame(self.main_container, fg_color=COLOR_BG, corner_radius=30)
        frame.pack(fill="both", expand=True, padx=15, pady=15)
        self._bind_mousewheel(frame)
        
        ctk.CTkButton(
            frame, text=self.t("back"), command=self.back_to_menu,
            fg_color="transparent", text_color=COLOR_PINK,
            hover_color=COLOR_HOVER, font=("Arial", 13, "bold"),
            corner_radius=20, height=35
        ).pack(anchor="w", pady=(10, 10))
        ctk.CTkLabel(frame, text=self.t("settings_title"), 
                    font=("Arial", 24, "bold"), text_color=COLOR_PINK).pack(pady=20)
        
        self.setting_vars = {}
        for text, key in [
            (self.t("notifications"), "notifications"),
            (self.t("dark_theme"), "dark_theme"),
            (self.t("autoplay"), "autoplay")
        ]:
            sf = ctk.CTkFrame(frame, fg_color="white", corner_radius=12)
            sf.pack(fill="x", padx=20, pady=5)
            ctk.CTkLabel(sf, text=text, font=("Arial", 14, "bold"), 
                        text_color=COLOR_PINK).pack(side="left", padx=15, pady=12)
            var = ctk.BooleanVar(value=self.app_settings.get(key, False))
            self.setting_vars[key] = var
            ctk.CTkSwitch(sf, text="", variable=var, 
                         fg_color=COLOR_PINK, progress_color=COLOR_DARK_PINK
            ).pack(side="right", padx=15, pady=12)
        
        lf = ctk.CTkFrame(frame, fg_color="white", corner_radius=12)
        lf.pack(fill="x", padx=20, pady=5)
        ctk.CTkLabel(lf, text=self.t("language"), 
                    font=("Arial", 14, "bold"), text_color=COLOR_PINK).pack(side="left", padx=15, pady=12)
        lv = ctk.StringVar(value=self.app_settings.get("language", "Русский"))
        self.setting_vars["language"] = lv
        ctk.CTkOptionMenu(
            lf, values=list(LANGUAGES.keys()),
            variable=lv, fg_color=COLOR_PINK, 
            button_color=COLOR_DARK_PINK,
            button_hover_color=COLOR_PINK, font=("Arial", 13)
        ).pack(side="right", padx=15, pady=12)
        
        ctk.CTkButton(
            frame, text=self.t("save_settings"), command=self.save_app_settings,
            fg_color=COLOR_GREEN, hover_color="#228B22", 
            corner_radius=20, height=45, font=("Arial", 15, "bold")
        ).pack(fill="x", padx=20, pady=20)
    
    def save_app_settings(self):
        for key, var in self.setting_vars.items():
            if isinstance(var, ctk.BooleanVar):
                self.app_settings[key] = var.get()
            elif isinstance(var, ctk.StringVar):
                self.app_settings[key] = var.get()
        self.save_settings()
        self.lang = LANGUAGES.get(self.app_settings.get("language", "Русский"), LANGUAGES["Русский"])
        if self.app_settings.get("dark_theme"):
            ctk.set_appearance_mode("dark")
        else:
            ctk.set_appearance_mode("light")
        self.show_main_menu()
    
    # ==================== ПОМОЩЬ ====================
    def show_help(self):
        self.clear_container()
        frame = ctk.CTkScrollableFrame(self.main_container, fg_color=COLOR_BG, corner_radius=30)
        frame.pack(fill="both", expand=True, padx=15, pady=15)
        self._bind_mousewheel(frame)
        ctk.CTkButton(
            frame, text=self.t("back"), command=self.back_to_menu,
            fg_color="transparent", text_color=COLOR_PINK,
            hover_color=COLOR_HOVER, font=("Arial", 13, "bold"),
            corner_radius=20, height=35
        ).pack(anchor="w", pady=(10, 10))
        ctk.CTkLabel(frame, text=self.t("help_title"), 
                    font=("Arial", 24, "bold"), text_color=COLOR_PINK).pack(pady=20)
        
        cf = ctk.CTkFrame(frame, fg_color="white", corner_radius=15)
        cf.pack(fill="x", padx=20, pady=10)
        ctk.CTkLabel(cf, text=self.t("contacts"), 
                    font=("Arial", 16, "bold"), text_color=COLOR_PINK).pack(pady=(15, 10))
        ctk.CTkLabel(cf, text="📱 Telegram: @FemBoyLoverOwO", 
                    font=("Arial", 13), text_color=COLOR_BLUE).pack(pady=5)
        ctk.CTkLabel(cf, text="📧 femboyloversupport@gmail.com", 
                    font=("Arial", 13), text_color=COLOR_DARK_PINK).pack(pady=(0, 15))
        
        ctk.CTkLabel(frame, text=self.t("love"), 
                    font=("Arial", 11), text_color=COLOR_LIGHT_PINK).pack(pady=(15, 0))
        ctk.CTkLabel(frame, text=self.t("version"), 
                    font=("Arial", 10, "bold"), text_color=COLOR_LIGHT_PINK).pack(pady=(0, 15))
    
    def logout(self):
        self.stop_music()
        # Сохраняем плейлист текущего юзера и очищаем
        self.save_playlist()
        self.playlist = []
        self.current_track_index = -1
        self.clear_session()
        self.current_user = None
        self.current_dialog_with = None
        self.show_auth_screen()
    
    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    print("🌸 FemboyApp V1.5")
    print("🌍 Поддерживаемые языки: " + ", ".join(LANGUAGES.keys()))
    
    if not BOT_TOKEN or not ADMIN_CHAT_ID:
        print("⚠️ Создайте файл .env с BOT_TOKEN и ADMIN_CHAT_ID")
    
    try:
        app = FemBoyAuthApp()
        app.run()
    except Exception as e:
        logging.critical(f"Критическая ошибка: {e}")
        print(f"❌ Критическая ошибка: {e}")
