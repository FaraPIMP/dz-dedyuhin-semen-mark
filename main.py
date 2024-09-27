import tkinter as tk
from PIL import Image, ImageTk, ImageDraw


# Словарь с фотографиями и их категориями
photos = {
    "pylemet.png": "Мультфильм",
    "panda.png": "Мультфильм",
    "figurki.png": "Мультфильм",
    "avtomat.png": "Боевики",
    "granata.png": "Боевики",
    "saldatik.png": "Боевики",
    "dedpyl.png": "Комедия",
    "rasamaxa.png": "Комедия",
    "dom.png": "Комедия",
}

def show_photos(category):
    """Показывает фотографии выбранной категории."""
    # Скрываем все фотографии
    for label in photo_labels:
        label.place_forget()

    # Показываем фотографии выбранной категории
    x = 225
    y = 75
    row = 1
    column = 1
    for filename, cat in photos.items():
        if category == "Общая" or cat == category:
            img = ImageTk.PhotoImage(Image.open(filename).resize((250, 250),))
            label = tk.Label(root, image=img)
            label.image = img
            label.place(x=x, y=y, width=250, height=250)
            photo_labels.append(label)
            if category != "Общая":
                x += 275
            else:
                if column < 4:
                    x += 350
                    column += 1
                else:
                    if row < 3:
                        x = 200
                        y += 275
                        column = 1
                        row += 1
                    else:
                        x = 200
                        y = screen_height - 800
                        column = 1
                        row = 1

# Создаем главное окно
root = tk.Tk()
root.title("Магазин игрушек")

# Получаем размеры экрана
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Устанавливаем размеры окна на весь экран
root.geometry(f"{screen_width}x{screen_height}+0+0")

# Добавление заднего фона
image = Image.open("foto.png")
photo = ImageTk.PhotoImage(image.resize((screen_width, screen_height),))
background_label = tk.Label(root, image=photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Список меток для фотографий
photo_labels = []

# Добавление кнопок
button_frame = tk.Frame(root)
button_frame.pack(pady=20)

buttons = [
    "Общая",
    "Боевики",
    "Комедия",
    "Мультфильм"
]

for text in buttons:
    button = tk.Button(button_frame, text=text, command=lambda cat=text: show_photos(cat))
    button.pack(side=tk.LEFT, padx=5)


# Показываем все фотографии при запуске программы
show_photos("Общая")

root.mainloop()
