import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageDraw
import subprocess
import sqlite3

def open_main(event=None):
    subprocess.run(['python', 'main.py'])

# Создание или подключение к базе данных
conn = sqlite3.connect('C:/Users/sdas4/Desktop/M_D_M/cinema.db')
cursor = conn.cursor()

# Создание таблицы пользователей (если она не существует)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
''')
conn.commit()

# Добавляем тестового пользователя
def insert_test_user():
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", ('admin', 'password'))
        conn.commit()
    except sqlite3.IntegrityError:
        pass  # Если пользователь уже существует, ничего не делать

insert_test_user()

# Функция для авторизации
def login():
    username = username_entry.get()
    password = password_entry.get()

    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()

    if user:
        messagebox.showinfo("Успешно", "Авторизация прошла успешно!")
        root.destroy()  # Закрываем окно после успешной авторизации
    else:
        messagebox.showerror("Ошибка", "Неверный логин или пароль")

# Функция для регистрации нового пользователя
def open_registration_window():
    registration_window = tk.Toplevel(root)
    registration_window.title("Регистрация")
    registration_window.geometry('300x150')

    tk.Label(registration_window, text="Логин").grid(row=0, column=0)
    new_username_entry = tk.Entry(registration_window)
    new_username_entry.grid(row=0, column=1)

    tk.Label(registration_window, text="Пароль").grid(row=1, column=0)
    new_password_entry = tk.Entry(registration_window, show="*")
    new_password_entry.grid(row=1, column=1)

    def register():
        new_username = new_username_entry.get()
        new_password = new_password_entry.get()

        if not new_username or not new_password:
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены")
            return

        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (new_username, new_password))
            conn.commit()
            messagebox.showinfo("Успешно", "Регистрация прошла успешно!")
            registration_window.destroy()
        except sqlite3.IntegrityError:
            messagebox.showerror("Ошибка", "Пользователь с таким логином уже существует")

    register_button = tk.Button(registration_window, text="Зарегистрироваться", command=register, bg="lightblue", relief="raised")
    register_button.grid(row=2, column=1)

# Функция для восстановления аккаунта
def open_restore_account_window():
    restore_window = tk.Toplevel(root)
    restore_window.title("Восстановление аккаунта")
    restore_window.geometry('300x150')

    tk.Label(restore_window, text="Логин").grid(row=0, column=0)
    restore_username_entry = tk.Entry(restore_window)
    restore_username_entry.grid(row=0, column=1)

    tk.Label(restore_window, text="Пароль").grid(row=1, column=0)
    restore_password_entry = tk.Entry(restore_window, show="*")
    restore_password_entry.grid(row=1, column=1)

    def restore_account():
        restore_username = restore_username_entry.get()
        restore_password = restore_password_entry.get()

        if not restore_username or not restore_password:
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены")
            return

        cursor.execute("SELECT * FROM users WHERE username = ?", (restore_username,))
        user = cursor.fetchone()

        if user:
            cursor.execute("UPDATE users SET password = ? WHERE username = ?", (restore_password, restore_username))
            conn.commit()
            messagebox.showinfo("Успешно", f"Пароль для {restore_username} успешно восстановлен.")
            restore_window.destroy()
        else:
            messagebox.showerror("Ошибка", "Пользователь с таким логином не существует")

    restore_button = tk.Button(restore_window, text="Восстановить пароль", command=restore_account, bg="lightblue", relief="raised")
    restore_button.grid(row=2, column=1)

# Создание окна авторизации с фоном
root = tk.Tk()
root.title("Авторизация")
root.geometry('1920x1080')

# Загрузка фонового изображения
bg_image = Image.open('foto.png')
bg_image = bg_image.resize((1920, 1080), Image.Resampling.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)

# Создание виджета Canvas для размещения фонового изображения
canvas = tk.Canvas(root, width=1920, height=1080)
canvas.pack(fill="both", expand=True)

# Добавление фонового изображения на Canvas
canvas.create_image(0, 0, image=bg_photo, anchor="nw")

# Создание фрейма для размещения элементов ввода
frame = tk.Frame(root, bg="white")
frame.place(relx=0.5, rely=0.5, anchor="center")

# Поля для логина
tk.Label(frame, text="Логин", bg="white").grid(row=0, column=0)
username_entry = tk.Entry(frame)
username_entry.grid(row=0, column=1)

# Поля для пароля
tk.Label(frame, text="Пароль", bg="white").grid(row=1, column=0)
password_entry = tk.Entry(frame, show="*")
password_entry.grid(row=1, column=1)

# Функция для изменения цвета кнопок при наведении
def on_enter(event):
    event.widget['background'] = 'deepskyblue'

def on_leave(event):
    event.widget['background'] = 'lightblue'

# Кнопка для входа
login_button = tk.Button(frame, text="Войти", command=login, bg="lightblue", relief="raised")
login_button.grid(row=2, column=1)
login_button.bind("<Enter>", on_enter)
login_button.bind("<Leave>", on_leave)

# Кнопка для открытия окна регистрации
register_button = tk.Button(frame, text="Регистрация", command=open_registration_window, bg="lightblue", relief="raised")
register_button.grid(row=3, column=1)
register_button.bind("<Enter>", on_enter)
register_button.bind("<Leave>", on_leave)

# Кнопка для открытия окна восстановления аккаунта
restore_button = tk.Button(frame, text="Восстановление пароля", command=open_restore_account_window, bg="lightblue", relief="raised")
restore_button.grid(row=4, column=1)
restore_button.bind("<Enter>", on_enter)
restore_button.bind("<Leave>", on_leave)

# Обработчик закрытия окна
def on_closing():
    conn.close()  # Закрываем подключение к базе данных при закрытии окна
    root.destroy()

# Назначаем обработчик закрытия окна
root.protocol("WM_DELETE_WINDOW", on_closing)

# Запуск приложения
root.mainloop()



def exit_program(event=None):
    root.destroy()

def on_entry_click(event):
    if search_entry.get() == "Поиск":
        search_entry.delete(0, "end")
        search_entry.config(fg='black')

def on_focusout(event):
    if search_entry.get() == "":
        search_entry.insert(0, "Поиск")
        search_entry.config(fg='gray')

def on_click(event):
    if search_entry.get() == "" or search_entry.get() == "Поиск":
        search_entry.delete(0, "end")
        search_entry.insert(0, "Поиск")
        search_entry.config(fg='gray')

def create_rounded_image(image_path, radius):
    img = Image.open(image_path).convert("RGBA")
    mask = Image.new("L", img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0, img.size[0], img.size[1]), radius=radius, fill=255)

    rounded_img = Image.new("RGBA", img.size)
    rounded_img.paste(img, (0, 0), mask)
    return rounded_img

def update_movies_by_genre(event=None):
    genre = genres.get()

    for label in movie_labels:
        label.grid_forget()

    if genre == "комедия":
        show_movies([("com.jpg", "Росамах и Дедпул"), ("come2.jpg", "Не одна дома")])
    elif genre == "мультфильм":
        show_movies([("mul2.webp", "Гадкий я 4"), ("mul.jpg", "Кунг-фу панда 4")])
    elif genre == "боевик":
        show_movies([("bo.jpeg", "Брасок кобры"), ("bo2.jpg", "Железный кулак")])
    elif genre == "Все жанры":
        show_movies([("com.jpg", "Росамах и Дедпул"),
                     ("come2.jpg", "Не одна дома"),
                     ("mul2.webp", "Гадкий я 4"),
                     ("mul.jpg", "Кунг-фу панда 4"),
                     ("bo.jpeg", "Брасок кобры"),
                     ("bo2.jpg", "Железный кулак")])

def update_movies_by_search(event=None):
    search_term = search_entry.get().lower()

    for label in movie_labels:
        label.grid_forget()

    all_movies = [
        ("com.jpg", "Росамах и Дедпул"),
        ("come2.jpg", "Не одна дома"),
        ("mul2.webp", "Гадкий я 4"),
        ("mul.jpg", "Кунг-фу панда 4"),
        ("bo.jpeg", "Брасок кобры"),
        ("bo2.jpg", "Железный кулак"),
    ]

    filtered_movies = [movie for movie in all_movies if search_term in movie[1].lower()]
    show_movies(filtered_movies, search_term)

def show_movies(movies, search_term=""):
    for index, movie in enumerate(movies):
        img_path, title = movie
        rounded_img = create_rounded_image(img_path, radius=20)
        rounded_img.thumbnail((250, 300))
        img = ImageTk.PhotoImage(rounded_img)

        # Создаем рамку с черным фоном и обводкой
        label_frame = tk.Frame(movies_frame, bg='black', bd=10)  # Чёрный фон и обводка 10px
        label_frame.grid(row=0, column=index, padx=20, pady=20)

        label = tk.Label(label_frame, image=img, bg='black')  # Удален белый фон
        label.image = img  # Сохраняем ссылку на изображение
        label.pack()

        # Удаляем фон у текстового поля
        title_text = tk.Text(label_frame, height=1, width=20, bg='black', fg='white', bd=0, wrap=tk.WORD, font=("Helvetica", 14))
        title_text.insert(tk.END, title)
        title_text.configure(state=tk.NORMAL)
        start_idx = title.lower().find(search_term)

        if start_idx != -1:
            end_idx = start_idx + len(search_term)
            title_text.tag_add("highlight", f"1.{start_idx}", f"1.{end_idx}")
            title_text.tag_config("highlight", foreground="blue")

        title_text.configure(state=tk.DISABLED)
        title_text.pack()

        movie_labels.append(label_frame)

        if title == "Росамах и Дедпул":
            label.bind("<Button-1>", lambda e: play_video(r"C:\Users\Нематов Марк\Desktop\M_D_M\come2.mp4"))
        elif title == "Не одна дома":
            label.bind("<Button-1>", lambda e: play_video(r"C:\Users\Нематов Марк\Desktop\M_D_M\come1.mp4"))
        elif title == "Кунг-фу панда 4":
            label.bind("<Button-1>", lambda e: play_video(r"C:\Users\Нематов Марк\Desktop\M_D_M\mul1.mp4"))
        elif title == "Брасок кобры":
            label.bind("<Button-1>", lambda e: play_video(r"C:\Users\Нематов Марк\Desktop\M_D_M\bo1.mp4"))
        elif title == "Железный кулак":
            label.bind("<Button-1>", lambda e: play_video(r"C:\Users\Нематов Марк\Desktop\M_D_M\bo2.mp4"))
        elif title == "Гадкий я 4":
            label.bind("<Button-1>", lambda e: play_video(r"C:\Users\Нематов Марк\Desktop\M_D_M\mul2.mp4"))

def play_video(video_path):
    wmp_path = r"C:\Program Files (x86)\Windows Media Player\wmplayer.exe"
    subprocess.run([wmp_path, video_path, "/fullscreen"])

# Создаем основное окно
root = tk.Tk()
root.title("Кино Лента")
root.geometry("1920x1080")

# Устанавливаем фоновое изображение
bg_image = ImageTk.PhotoImage(Image.open("fon.png"))
background_label = tk.Label(root, image=bg_image)
background_label.place(relwidth=1, relheight=1)

link_style = {"font": ("Helvetica", 14), "fg": "white", "bg": "#35064f"}

header_frame = tk.Frame(root, bg='#35064f')
header_frame.pack(side=tk.TOP, fill=tk.X)

exit_label = tk.Label(header_frame, text="Выйти", **link_style)
exit_label.pack(side=tk.LEFT, padx=10, pady=10)
exit_label.bind("<Button-1>", exit_program)

center_frame = tk.Frame(header_frame, bg='#35064f')
center_frame.pack(side=tk.LEFT, expand=True)

genres = ttk.Combobox(center_frame, values=["Все жанры", "комедия", "мультфильм", "боевик"], state="readonly", height=10)
genres.set("Жанры")
genres.configure(font=("Helvetica", 12))
genres.pack(side=tk.LEFT, padx=10)
genres.bind("<<ComboboxSelected>>", update_movies_by_genre)

store_label = tk.Label(header_frame, text="Магазин игрушек", **link_style)
store_label.pack(side=tk.LEFT, padx=10, pady=10)
store_label.bind("<Button-1>", open_main)


entry_frame = tk.Frame(header_frame, bg='#35064f', bd=0)
entry_frame.pack(side=tk.RIGHT, padx=10, pady=10)

border_frame = tk.Frame(entry_frame, bg='white', bd=10)
border_frame.pack(pady=5)

search_entry = tk.Entry(border_frame, foreground='gray', font=("Helvetica", 12), justify='left', bd=0, relief="flat", width=25)
search_entry.insert(0, "Поиск")
search_entry.pack(pady=2, padx=5, fill=tk.X)

search_entry.bind("<FocusIn>", on_entry_click)
search_entry.bind("<FocusOut>", on_focusout)
search_entry.bind("<Button-1>", on_click)
search_entry.bind("<KeyRelease>", update_movies_by_search)

movies_frame = tk.Frame(root, bg='black')  # Задний фон для изображений
movies_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=(0, 10))  # Убрал нижний отступ

movie_labels = []

show_movies([
    ("com.jpg", "Росамах и Дедпул"),
    ("come2.jpg", "Не одна дома"),
    ("mul2.webp", "Гадкий я 4"),
    ("mul.jpg", "Кунг-фу панда 4"),
    ("bo.jpeg", "Брасок кобры"),
    ("bo2.jpg", "Железный кулак"),
])

root.mainloop()


