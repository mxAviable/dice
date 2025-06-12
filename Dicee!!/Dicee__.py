import tkinter as tk
import random
from PIL import Image, ImageTk
import itertools
from tkinter import simpledialog
import time




# Створюємо головне вікно гри
root = tk.Tk()
root.title("Diceee!")
root.state('zoomed')  # Розгортаємо вікно на весь екран
root.configure(bg="#1e1e1e")  # Встановлюємо темний фон
root.iconbitmap("icon.ico") # іконка

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

# Кольори
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

# Функція для показу превью з логотипом
import tkinter as tk
from PIL import Image, ImageTk
import time

def show_splash_screen():
    splash_frame = tk.Frame(root, bg='black')
    splash_frame.place(x=0, y=0, relwidth=1, relheight=1)

    screen_center_x = screen_width // 2
    screen_center_y = screen_height // 2

    # Завантаження логотипу
    try:
        logo_img = Image.open("dddice.png")
        logo_img = logo_img.resize((400, 400), Image.Resampling.LANCZOS)
        logo_photo = ImageTk.PhotoImage(logo_img)

        logo_label = tk.Label(splash_frame, image=logo_photo, bg='black')
        logo_label.image = logo_photo
        logo_label.place(relx=0.5, rely=0.5, anchor='center')
    except:
        logo_label = tk.Label(splash_frame, text="Diceee!", font=("Arial", 48, "bold"), fg="white", bg='black')
        logo_label.place(relx=0.5, rely=0.5, anchor='center')

    # Функція шейку
    def shake_logo():
        for _ in range(10):
            logo_label.place_configure(relx=0.5, rely=0.5, x=5)
            root.update()
            time.sleep(0.03)
            logo_label.place_configure(x=-5)
            root.update()
            time.sleep(0.03)
            logo_label.place_configure(x=0)
            root.update()
            time.sleep(0.03)

    def animate_splash():
        logo_label.destroy()

        # Коло, яке росте з центру
        circle_canvas = tk.Canvas(splash_frame, bg='black', highlightthickness=0)
        circle_canvas.place(x=0, y=0, relwidth=1, relheight=1)

        max_radius = int((screen_width ** 2 + screen_height ** 2) ** 0.5)

        for r in range(0, max_radius, 20):
            circle_canvas.delete("all")
            circle_canvas.create_oval(
                screen_center_x - r, screen_center_y - r,
                screen_center_x + r, screen_center_y + r,
                fill="#1f1f1f", outline=""
            )
            root.update()
            time.sleep(0.01)

        splash_frame.destroy()
        show_main_menu()

    # шейк
    root.after(500, shake_logo)
    # запуск анімації
    root.after(2000, animate_splash)



# Головне меню гри з двома кнопками режимів
def show_main_menu():
    # Очищаємо вікно від попередніх віджетів
    for widget in root.winfo_children():
        widget.destroy()

    # Відновлюємо фон
    background_label = tk.Label(root, image=board_photo)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    # лого гри
    logo_img = tk.PhotoImage(file="dddice.png").subsample(9, 9)
    label = tk.Label(root, image=logo_img, bg="#1e1e1e")
    label.image = logo_img  # зберігаємо посилання, щоб не зникло
    label.place(relx=0.98, rely=0.05, anchor="ne")

    label = tk.Label(root, image=logo_img, bg="#1e1e1e")
    label.image = logo_img  # зберігаємо посилання
    label.place(relx=0.98, rely=0.05, anchor="ne")


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

def start_classic_mode():
    for widget in root.winfo_children():
        widget.destroy()

    # Додаємо вибір кількості раундів і кидків
    settings_frame = tk.Frame(root, bg="#1e1e1e")
    settings_frame.pack(pady=50)

    tk.Label(settings_frame, text="Налаштування гри:", font=("Arial", 14), bg="#1e1e1e", fg="white").pack()

    # Вибір кількості раундів
    tk.Label(settings_frame, text="Кількість раундів:", font=("Arial", 12), bg="#1e1e1e", fg="white").pack()
    rounds_var = tk.IntVar(value=3)
    tk.Spinbox(settings_frame, from_=1, to=12, textvariable=rounds_var, font=("Arial", 12), width=3).pack(pady=5)

    # Вибір кількості кидків на гравця за раунд
    tk.Label(settings_frame, text="Кидків за раунд:", font=("Arial", 12), bg="#1e1e1e", fg="white").pack()
    rolls_var = tk.IntVar(value=5)
    tk.Spinbox(settings_frame, from_=1, to=10, textvariable=rolls_var, font=("Arial", 12), width=3).pack(pady=5)

    def start_game_with_settings():
        nonlocal rounds_var, rolls_var
        settings_frame.destroy()
        init_game(rounds_var.get(), rolls_var.get())

    start_btn = styled_button(settings_frame, "Почати гру", start_game_with_settings, bg="#4CAF50", font_size=14)
    start_btn.pack(pady=15)

    def init_game(total_rounds, rolls_per_player):
        player1_score = 0
        player2_score = 0
        turn = 1
        game_active = True
        current_round = 1
        player1_wins = 0
        player2_wins = 0
        rolls_left = rolls_per_player

        left_frame = tk.Frame(root, bg="#1e1e1e")
        left_frame.pack(side=tk.LEFT, padx=50, pady=50, expand=True, fill=tk.BOTH)

        right_frame = tk.Frame(root, width=250, bg="#1e1e1e")
        right_frame.pack_propagate(False)
        right_frame.pack(side=tk.RIGHT, padx=50, pady=50, fill=tk.Y)

        create_back_button(root)

        dice_label = tk.Label(left_frame, image=dice_images[0], bg="#1e1e1e")
        dice_label.pack(expand=True) 

        info_frame = tk.Frame(right_frame, bg="#1e1e1e")
        info_frame.place(relx=0.5, rely=0.15, anchor="n")

        rounds_label = tk.Label(info_frame, text=f"Раунд: {current_round}/{total_rounds}", font=("Arial", 12), bg="#1e1e1e", fg="white")
        rounds_label.pack(pady=5)

        wins_label = tk.Label(info_frame, text=f"Перемоги: {player1_wins}-{player2_wins}", font=("Arial", 12), bg="#1e1e1e", fg="white")
        wins_label.pack(pady=5)

        rolls_label = tk.Label(info_frame, text=f"Залишилось кидків: {rolls_left}", font=("Arial", 12), bg="#1e1e1e", fg="white")
        rolls_label.pack(pady=5)

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

        canvas = tk.Canvas(right_frame, width=120, height=120, highlightthickness=0, bg="#1e1e1e")
        canvas.place(relx=0.5, rely=0.7, anchor="center")

        circle = canvas.create_oval(0, 0, 120, 120, fill="#4CAF50", outline="#4CAF50")
        circle_text = canvas.create_text(60, 60, text="Кинути", fill="white", font=("Arial", 14, "bold"))

        rematch_btn = None

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

        def finish_round():
            nonlocal current_round, player1_wins, player2_wins, game_active, rolls_left
            winner = 1 if player1_score > player2_score else 2 if player2_score > player1_score else 0
            
            if winner != 0:
                if winner == 1:
                    player1_wins += 1
                else:
                    player2_wins += 1
                wins_label.config(text=f"Перемоги: {player1_wins}-{player2_wins}")
            
            status_text = ""
            if winner == 0:
                status_text = f"Раунд {current_round}: Нічия!"
            else:
                status_text = f"Раунд {current_round}: Перемога {winner}!"
                status_text = f"Раунд {current_round}: Перемога {winner}!"
            
            if current_round < total_rounds:
                current_round += 1
                rounds_label.config(text=f"Раунд: {current_round}/{total_rounds}")
                status_label.config(text=status_text + f"\nНаступний раунд...")
                root.after(2000, lambda: start_new_round())
            else:
                game_active = False
                if player1_wins > player2_wins:
                    status_label.config(text=f"🎉 1 виграв! {player1_wins}-{player2_wins}!")
                elif player2_wins > player1_wins:
                    status_label.config(text=f"🎉 2 виграв! {player1_wins}-{player2_wins}!")
                else:
                    status_label.config(text=f"⚖ Нічия! {player1_wins}-{player2_wins}!")
                finish_game()

        def start_new_round():
            nonlocal player1_score, player2_score, turn, rolls_left
            player1_score = 0
            player2_score = 0
            turn = 1
            rolls_left = rolls_per_player
            player1_label.config(text="Гравець 1: 0")
            player2_label.config(text="Гравець 2: 0")
            rolls_label.config(text=f"Залишилось кидків: {rolls_left}")
            status_label.config(text=f"Раунд {current_round} | Хід гравця 1")
            update_player_highlight()

        def finish_game():
            nonlocal game_active, rematch_btn, canvas
            game_active = False
            if canvas is not None:
                canvas.itemconfig(circle_text, state='hidden')
                canvas.itemconfig(circle, fill="#555")
                canvas.destroy()
                canvas = None

            rematch_btn = styled_button(right_frame, "Реванш", restart_classic, bg="#607d8b", font_size=14, width=15, height=2)
            rematch_btn.place(relx=0.5, rely=0.85, anchor="center")

        def restart_classic():
            nonlocal rematch_btn, canvas
            if rematch_btn is not None:
                rematch_btn.destroy()
                rematch_btn = None
            start_classic_mode()

        def roll_dice():
            nonlocal player1_score, player2_score, turn, rolls_left, game_active, canvas
            if not game_active or canvas is None:
                return
            canvas.itemconfig(circle_text, state='hidden')

            def apply_result():
                nonlocal player1_score, player2_score, turn, rolls_left
                roll = random.randint(1, 6)
                dice_label.config(image=dice_images[roll - 1])

                if turn == 1:
                    player1_score += roll
                    player1_label.config(text=f"Гравець 1: {player1_score}")
                else:
                    player2_score += roll
                    player2_label.config(text=f"Гравець 2: {player2_score}")

                rolls_left -= 1
                rolls_label.config(text=f"Залишилось кидків: {rolls_left}")

                if rolls_left > 0:
                    turn = 2 if turn == 1 else 1
                    status_label.config(text=f"Раунд {current_round} | Хід гравця {turn}")
                    update_player_highlight()
                    canvas.itemconfig(circle_text, state='normal')
                else:
                    finish_round()

            animate_dice(apply_result)

        canvas.bind("<Button-1>", lambda e: roll_dice())

def start_football_mode():
    # Очищаємо вікно
    for widget in root.winfo_children():
        widget.destroy()

    create_back_button(root)

    # Головний фрейм для всього вмісту
    main_frame = tk.Frame(root, bg="#1e1e1e")
    main_frame.pack(pady=20)

    # Заголовок
    tk.Label(main_frame, text="Футбольний Турнір", font=("Arial", 24, "bold"), 
            bg="#1e1e1e", fg="white").grid(row=0, column=0, columnspan=4, pady=20)

    # Налаштування команд
    settings_frame = tk.Frame(main_frame, bg="#2e2e2e", padx=20, pady=20)
    settings_frame.grid(row=1, column=0, columnspan=4, pady=10)

    # Команда 1
    tk.Label(settings_frame, text="Команда 1:", font=("Arial", 12), 
            bg="#2e2e2e", fg="white").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    team1_entry = tk.Entry(settings_frame, font=("Arial", 12), width=15)
    team1_entry.grid(row=0, column=1, padx=5, pady=5)
    team1_entry.insert(0, "Команда А")
    
    team1_color = tk.StringVar(value="Red")
    tk.Label(settings_frame, text="Колір:", bg="#2e2e2e", fg="white").grid(row=0, column=2, padx=5, sticky="e")
    team1_menu = tk.OptionMenu(settings_frame, team1_color, *JERSEY_COLORS.keys())
    team1_menu.grid(row=0, column=3, padx=5, pady=5)

    # Команда 2
    tk.Label(settings_frame, text="Команда 2:", font=("Arial", 12), 
            bg="#2e2e2e", fg="white").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    team2_entry = tk.Entry(settings_frame, font=("Arial", 12), width=15)
    team2_entry.grid(row=1, column=1, padx=5, pady=5)
    team2_entry.insert(0, "Команда Б")
    
    team2_color = tk.StringVar(value="Blue")
    tk.Label(settings_frame, text="Колір:", bg="#2e2e2e", fg="white").grid(row=1, column=2, padx=5, sticky="e")
    team2_menu = tk.OptionMenu(settings_frame, team2_color, *JERSEY_COLORS.keys())
    team2_menu.grid(row=1, column=3, padx=5, pady=5)

    # Кількість раундів
    tk.Label(settings_frame, text="Кількість раундів:", font=("Arial", 12), 
            bg="#2e2e2e", fg="white").grid(row=2, column=0, padx=5, pady=10, sticky="e")
    rounds_var = tk.StringVar(value="10")
    rounds_entry = tk.Entry(settings_frame, font=("Arial", 12), width=5, textvariable=rounds_var)
    rounds_entry.grid(row=2, column=1, padx=5, pady=10, sticky="w")

    # Кнопка початку гри
    start_btn = styled_button(main_frame, "Почати гру", 
                            lambda: validate_and_start(
                                team1_entry.get(), 
                                team2_entry.get(), 
                                team1_color.get(), 
                                team2_color.get(),
                                rounds_var.get()
                            ), 
                            bg="#4CAF50", font_size=16, width=20, height=2)
    start_btn.grid(row=2, column=0, columnspan=4, pady=20)

def validate_and_start(team1_name, team2_name, team1_color, team2_color, rounds_str):
    try:
        total_rounds = int(rounds_str)
        if total_rounds < 1:
            raise ValueError
    except ValueError:
        tk.messagebox.showerror("Помилка", "Будь ласка, введіть коректну кількість раундів (ціле число більше 0)")
        return
    
    if not team1_name.strip():
        team1_name = "Команда А"
    if not team2_name.strip():
        team2_name = "Команда Б"
    
    start_football_game(team1_name, team2_name, team1_color, team2_color, total_rounds)

def start_football_game(team1_name, team2_name, team1_color, team2_color, total_rounds):
    # Очищаємо вікно
    for widget in root.winfo_children():
        widget.destroy()

    create_back_button(root)

    # Змінні для гри
    teams = [team1_name, team2_name]  # Назви команд
    team_colors = [JERSEY_COLORS[team1_color], JERSEY_COLORS[team2_color]]  # Кольори команд
    team_scores = [0, 0]  # Рахунки обох команд
    round_number = 1
    game_active = True

    # Головний фрейм для гри
    game_frame = tk.Frame(root, bg="#1e1e1e")
    game_frame.pack(pady=20)

    # Показуємо назви команд та їхні рахунки
    scores_frame = tk.Frame(game_frame, bg="#1e1e1e")
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
    dice_label = tk.Label(game_frame, image=dice_images[0], bg="#1e1e1e")
    dice_label.pack()

    # Статус — хто зараз кидає кубик
    status_label = tk.Label(game_frame, text=f"Раунд {round_number}/{total_rounds}. Хід {teams[round_number % 2]}", 
                           font=("Arial", 18, "bold"), bg="#1e1e1e", fg="#FFD700")
    status_label.pack(pady=10)

    btn_frame = tk.Frame(game_frame, bg="#1e1e1e")
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

        # Визначаємо, якій команді додаємо очки
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
            status_label.config(text=f"Раунд {round_number}/{total_rounds}. Хід {next_team}")
            update_team_highlight() 

    def finish_football_game():
        nonlocal game_active
        game_active = False
        
        # Фрейм для кнопок після гри
        end_btn_frame = tk.Frame(game_frame, bg="#1e1e1e")
        end_btn_frame.pack(pady=20)

        styled_button(end_btn_frame, "Реванш", 
                    lambda: start_football_game(team1_name, team2_name, team1_color, team2_color, total_rounds), 
                    bg="#607d8b", font_size=14, width=15, height=2).pack(side=tk.LEFT, padx=10)
        
        styled_button(end_btn_frame, "Нова гра", start_football_mode, 
                    bg="#2196F3", font_size=14, width=15, height=2).pack(side=tk.LEFT, padx=10)
        
        styled_button(end_btn_frame, "Головне меню", show_main_menu, 
                    bg="#f44336", font_size=14, width=15, height=2).pack(side=tk.LEFT, padx=10)

    roll_button = styled_button(game_frame, "Кинути кубик", roll_football, bg="#4CAF50", font_size=18, width=20, height=2)
    roll_button.pack(pady=10)

# Запускаємо спочатку превью з логотипом, потім головне меню
show_splash_screen()
root.mainloop()