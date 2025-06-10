import tkinter as tk
import random
from PIL import Image, ImageTk
import itertools
from tkinter import simpledialog

# Створюємо головне вікно гри
root = tk.Tk()
root.title("Diceee!")
root.state('zoomed')  # Розгортаємо вікно на весь екран
root.configure(bg="#1e1e1e")  # Встановлюємо темний фон

# Завантажуємо та підганяємо фон-дошку під розмір екрану
board_image = Image.open("board_bg.png")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
board_image = board_image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
board_photo = ImageTk.PhotoImage(board_image)

# Фоновий лейбл з картинкою, який займає все вікно
background_label = tk.Label(root, image=board_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Завантажуємо зображення кубиків 1-6, розмір 300x300 пікселів
dice_images = [ImageTk.PhotoImage(Image.open(f"dice{i}.png").resize((300, 300))) for i in range(1, 7)]

# Available jersey colors for football teams
JERSEY_COLORS = {
    "Red": "#ff0000",
    "Blue": "#0000ff",
    "Green": "#00ff00",
    "Yellow": "#ffff00",
    "White": "#ffffff",
    "Black": "#000000",
    "Orange": "#ffa500",
    "Purple": "#800080"
}

# Функція для створення стилізованих кнопок з однаковими параметрами
def styled_button(master, text, command=None, bg="#3a3f4b", fg="white", font_size=14, width=20, height=2):
    return tk.Button(
        master,
        text=text,
        font=("Arial", font_size, "bold"),
        command=command,
        bg=bg,
        fg=fg,
        activebackground="#555",
        activeforeground="white",
        bd=0,
        relief="flat",
        highlightthickness=0,
        padx=10,
        pady=10,
        width=width,
        height=height
    )

# Головне меню гри з двома кнопками режимів
def show_main_menu():
    # Очищаємо вікно від попередніх віджетів
    for widget in root.winfo_children():
        widget.destroy()

    # Відновлюємо фон
    background_label = tk.Label(root, image=board_photo)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Заголовок гри
    title = tk.Label(root, text="Diceee!", font=("Comic Sans MS", 36, "bold"), bg="#1e1e1e", fg="#FFD700")
    title.place(relx=0.98, rely=0.05, anchor="ne")

    # Контейнер для кнопок
    btn_frame = tk.Frame(root, bg="#1e1e1e")
    btn_frame.place(relx=0.5, rely=0.5, anchor="center")

    # Кнопка класичної гри
    btn_classic = styled_button(btn_frame, "Класична гра", command=start_classic_mode, bg="#4CAF50", font_size=20, width=25, height=2)
    btn_classic.pack(pady=15)

    # Кнопка футбольного турніру
    btn_football = styled_button(btn_frame, "Футбольний турнір", command=start_football_mode, bg="#2196F3", font_size=20, width=25, height=2)
    btn_football.pack(pady=15)

# Кнопка "Назад" у режимах, щоб повернутись до головного меню
def create_back_button(parent):
    back_btn = styled_button(parent, "⟵ Назад", command=show_main_menu, bg="#f44336", font_size=14, width=10, height=1)
    back_btn.place(relx=0.98, rely=0.05, anchor="ne")
    return back_btn

# Класичний режим гри
def start_classic_mode():
    # Очищаємо вікно
    for widget in root.winfo_children():
        widget.destroy()

    # Початкові змінні: рахунок, хто ходить, активність гри
    player1_score = 0
    player2_score = 0
    turn = 1
    game_active = True

    # Створюємо дві частини вікна: ліва - для кубика, права - для інформації
    left_frame = tk.Frame(root, bg="#1e1e1e")
    left_frame.pack(side=tk.LEFT, padx=50, pady=50, expand=True, fill=tk.BOTH)

    right_frame = tk.Frame(root, width=250, bg="#1e1e1e")
    right_frame.pack_propagate(False)
    right_frame.pack(side=tk.RIGHT, padx=50, pady=50, fill=tk.Y)

    # Додаємо кнопку назад у верхній правий кут
    create_back_button(root)

    # Віджет для показу кубика, початково 1
    dice_label = tk.Label(left_frame, image=dice_images[0], bg="#1e1e1e")
    dice_label.pack(expand=True) 

    # Інформаційна панель з рахунками та статусом ходу
    info_frame = tk.Frame(right_frame, bg="#1e1e1e")
    info_frame.place(relx=0.5, rely=0.15, anchor="n")

    # Highlight current player
    player1_label = tk.Label(info_frame, text="Гравець 1: 0", font=("Arial", 16), bg="#1e1e1e", fg="white")
    player1_label.pack(pady=8)

    player2_label = tk.Label(info_frame, text="Гравець 2: 0", font=("Arial", 16), bg="#1e1e1e", fg="white")
    player2_label.pack(pady=8)

    status_label = tk.Label(info_frame, text="Хід гравця 1", font=("Arial", 16, "bold"), bg="#1e1e1e", fg="#FFD700")
    status_label.pack(pady=20)

    def update_player_highlight():
        if turn == 1:
            player1_label.config(bg="#333333")
            player2_label.config(bg="#1e1e1e")
        else:
            player1_label.config(bg="#1e1e1e")
            player2_label.config(bg="#333333")

    update_player_highlight()

    # Канвас — це кнопка у вигляді кола з написом "Кинути"
    canvas = tk.Canvas(right_frame, width=120, height=120, highlightthickness=0, bg="#1e1e1e")
    canvas.place(relx=0.5, rely=0.7, anchor="center")

    circle = canvas.create_oval(0, 0, 120, 120, fill="#4CAF50", outline="#4CAF50")
    circle_text = canvas.create_text(60, 60, text="Кинути", fill="white", font=("Arial", 14, "bold"))

    rematch_btn = None  # Кнопка "Реванш" з'явиться по завершенню гри

    # Анімація кубика — швидке перемикання зображень кубика, щоб створити ефект обертання
    def animate_dice(callback):
        frames = itertools.cycle(dice_images)
        count = 0
        def update_frame():
            nonlocal count
            dice_label.config(image=next(frames))
            count += 1
            if count < 8:
                root.after(30, update_frame)
            else:
                callback()
        update_frame()

    # Коли гра завершилась: відключаємо кнопку, показуємо "Реванш"
    def finish_game():
        nonlocal game_active, rematch_btn
        game_active = False
        canvas.itemconfig(circle_text, state='hidden')
        canvas.itemconfig(circle, fill="#555")  # Змінюємо колір кнопки, щоб показати, що вона неактивна

        rematch_btn = styled_button(right_frame, "Реванш", restart_classic, bg="#607d8b", font_size=14, width=15, height=2)
        rematch_btn.place(relx=0.5, rely=0.85, anchor="center")

    # Починаємо гру заново, викликаючи функцію старту класичного режиму
    def restart_classic():
        nonlocal rematch_btn
        if rematch_btn:
            rematch_btn.destroy()
        start_classic_mode()

    # Основна функція, що виконується при натисканні кнопки "Кинути"
    def roll_dice():
        nonlocal player1_score, player2_score, turn, game_active
        if not game_active:
            return
        canvas.itemconfig(circle_text, state='hidden')  # Ховаємо текст під час анімації

        # Після анімації запускаємо функцію, яка додає результат до рахунку
        def apply_result():
            nonlocal player1_score, player2_score, turn, game_active
            roll = random.randint(1, 6)
            dice_label.config(image=dice_images[roll - 1])  # Показуємо випавший кубик

            # Додаємо результат до поточного гравця
            if turn == 1:
                player1_score += roll
                player1_label.config(text=f"Гравець 1: {player1_score}")
                turn = 2
                status_label.config(text="Хід гравця 2")
            else:
                player2_score += roll
                player2_label.config(text=f"Гравець 2: {player2_score}")
                turn = 1
                status_label.config(text="Хід гравця 1")

            update_player_highlight()

            # Перевірка на перемогу (хто першим набрав >=30)
            if player1_score >= 30 or player2_score >= 30:
                winner = "1" if player1_score >= 30 else "2"
                status_label.config(text=f"🎉 Гравець {winner} переміг!")
                finish_game()
            else:
                canvas.itemconfig(circle_text, state='normal')  # Відновлюємо кнопку для наступного ходу

        animate_dice(apply_result)

    # Прив'язка кліку миші до кнопки "Кинути"
    canvas.bind("<Button-1>", lambda e: roll_dice())

# Футбольний турнір — альтернатива класичній грі з двома командами та підрахунком очок
def start_football_mode():
    # Очищаємо вікно
    for widget in root.winfo_children():
        widget.destroy()

    create_back_button(root)

    # Ask for team names and colors
    team1_name = simpledialog.askstring("Назва команди", "Введіть назву першої команди:", parent=root)
    if team1_name is None or team1_name.strip() == "":
        team1_name = "Команда А"
    
    team2_name = simpledialog.askstring("Назва команди", "Введіть назву другої команди:", parent=root)
    if team2_name is None or team2_name.strip() == "":
        team2_name = "Команда Б"
    
    # Select colors for teams
    color_window = tk.Toplevel(root)
    color_window.title("Вибір кольорів форм")
    color_window.geometry("400x200")
    color_window.resizable(False, False)
    color_window.grab_set()
    
    tk.Label(color_window, text="Виберіть колір форми для кожної команди", font=("Arial", 12)).pack(pady=10)
    
    team1_color = tk.StringVar(value="Red")
    team2_color = tk.StringVar(value="Blue")
    
    color_frame = tk.Frame(color_window)
    color_frame.pack(pady=10)
    
    tk.Label(color_frame, text=f"{team1_name}:").grid(row=0, column=0, padx=5)
    team1_menu = tk.OptionMenu(color_frame, team1_color, *JERSEY_COLORS.keys())
    team1_menu.grid(row=0, column=1, padx=5)
    
    tk.Label(color_frame, text=f"{team2_name}:").grid(row=1, column=0, padx=5)
    team2_menu = tk.OptionMenu(color_frame, team2_color, *JERSEY_COLORS.keys())
    team2_menu.grid(row=1, column=1, padx=5)
    
    def confirm_colors():
        color_window.destroy()
        start_football_game(team1_name, team2_name, team1_color.get(), team2_color.get())
    
    tk.Button(color_window, text="Підтвердити", command=confirm_colors).pack(pady=10)

def start_football_game(team1_name, team2_name, team1_color, team2_color):
    # Змінні для гри
    teams = [team1_name, team2_name]  # Назви команд
    team_colors = [JERSEY_COLORS[team1_color], JERSEY_COLORS[team2_color]]  # Кольори команд
    team_scores = [0, 0]  # Рахунки обох команд
    total_rounds = 10  # Кількість раундів
    round_number = 1
    game_active = True

    # Показуємо назви команд та їхні рахунки
    scores_frame = tk.Frame(root, bg="#1e1e1e")
    scores_frame.pack(pady=20)
    
    team1_label = tk.Label(scores_frame, text=f"{teams[0]}: 0", font=("Arial", 20, "bold"), 
                          bg="#1e1e1e", fg=team_colors[0], underline=True)
    team1_label.pack(side=tk.LEFT)
    
    separator_label = tk.Label(scores_frame, text="  -  ", font=("Arial", 20, "bold"), bg="#1e1e1e", fg="white")
    separator_label.pack(side=tk.LEFT)
    
    team2_label = tk.Label(scores_frame, text=f"{teams[1]}: 0", font=("Arial", 20, "bold"), 
                          bg="#1e1e1e", fg=team_colors[1])
    team2_label.pack(side=tk.LEFT)

    # Показуємо зображення кубика (початково 1)
    dice_label = tk.Label(root, image=dice_images[0], bg="#1e1e1e")
    dice_label.pack()

    # Статус — хто зараз кидає кубик
    status_label = tk.Label(root, text=f"Раунд {round_number}. Хід {teams[round_number % 2]}", 
                           font=("Arial", 18, "bold"), bg="#1e1e1e", fg="#FFD700")
    status_label.pack(pady=10)

    btn_frame = tk.Frame(root, bg="#1e1e1e")
    btn_frame.pack(pady=20)

    def update_team_highlight():
        current_team = round_number % 2
        if current_team == 0:
            team1_label.config(underline=True)
            team2_label.config(underline=False)
        else:
            team1_label.config(underline=False)
            team2_label.config(underline=True)

    update_team_highlight()

    # Кнопка кидка кубика
    def roll_football():
        nonlocal round_number, game_active

        if not game_active:
            return

        roll = random.randint(1, 6)
        dice_label.config(image=dice_images[roll - 1])

        # Визначаємо, якій команді додаємо очки (по черзі)
        team_index = (round_number - 1) % 2
        team_scores[team_index] += roll

        team1_label.config(text=f"{teams[0]}: {team_scores[0]}")
        team2_label.config(text=f"{teams[1]}: {team_scores[1]}")

        # Кінець гри після останнього раунду
        if round_number == total_rounds:
            if team_scores[0] > team_scores[1]:
                status_label.config(text=f"🎉 {teams[0]} виграла турнір!")
            elif team_scores[1] > team_scores[0]:
                status_label.config(text=f"🎉 {teams[1]} виграла турнір!")
            else:
                status_label.config(text="Нічия! Спробуйте ще раз.")
            finish_football_game()
        else:
            round_number += 1
            next_team = teams[(round_number - 1) % 2]
            status_label.config(text=f"Раунд {round_number}. Хід {next_team}")
            update_team_highlight() 

    # Кнопки "Кинути кубик", "Реванш" та "Головне меню"
    def finish_football_game():
        roll_button.config(state=tk.DISABLED)

        rematch_btn = styled_button(btn_frame, "Реванш", lambda: start_football_mode(), bg="#607d8b", font_size=14, width=15, height=2)
        rematch_btn.pack(side=tk.LEFT, padx=10)

        newgame_btn = styled_button(btn_frame, "Головне меню", show_main_menu, bg="#f44336", font_size=14, width=15, height=2)
        newgame_btn.pack(side=tk.LEFT, padx=10)

    roll_button = styled_button(root, "Кинути кубик", roll_football, bg="#4CAF50", font_size=18, width=20, height=2)
    roll_button.pack(pady=10)

# Відразу запускаємо головне меню при старті
show_main_menu()
root.mainloop()