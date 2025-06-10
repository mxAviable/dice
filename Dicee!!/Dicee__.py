import tkinter as tk
import random
from PIL import Image, ImageTk
import itertools

root = tk.Tk()
root.title("Гра 'Кістки'")
root.geometry("500x350")
root.resizable(False, False)
root.configure(bg="#1e1e1e")  # Темний фон

dice_images = [ImageTk.PhotoImage(Image.open(f"dice{i}.png").resize((80, 80))) for i in range(1, 7)]

# --- Загальний стиль ---
def styled_button(master, text, command=None, bg="#3a3f4b", fg="white"):
    return tk.Button(
        master,
        text=text,
        font=("Arial", 12),
        command=command,
        bg=bg,
        fg=fg,
        activebackground="#555",
        activeforeground="white",
        bd=0,
        relief="flat",
        highlightthickness=0,
        padx=15,
        pady=10
    )

def show_main_menu():
    for widget in root.winfo_children():
        widget.destroy()

    title = tk.Label(root, text="Гра 'Кістки'", font=("Arial", 18, "bold"), bg="#1e1e1e", fg="white")
    title.pack(pady=20)

    btn_classic = styled_button(root, "Класична гра", command=start_classic_mode, bg="#4CAF50")
    btn_classic.pack(pady=10)

    btn_football = styled_button(root, "Футбольний турнір", command=start_football_mode, bg="#2196F3")
    btn_football.pack(pady=10)

# --- Класичний режим ---
def start_classic_mode():
    for widget in root.winfo_children():
        widget.destroy()

    player1_score = 0
    player2_score = 0
    turn = 1
    game_active = True

    left_frame = tk.Frame(root, bg="#1e1e1e")
    left_frame.pack(side=tk.LEFT, padx=20, pady=20)

    right_frame = tk.Frame(root, width=200, height=260, bg="#1e1e1e")
    right_frame.pack_propagate(False)
    right_frame.pack(side=tk.RIGHT, padx=20, pady=20)

    back_btn = styled_button(root, "⟵", command=show_main_menu, bg="#f44336")
    back_btn.place(x=460, y=10, width=30, height=30)

    dice_label = tk.Label(left_frame, image=dice_images[0], bg="#1e1e1e")
    dice_label.pack(pady=20)

    info_frame = tk.Frame(right_frame, bg="#1e1e1e")
    info_frame.place(relx=0.5, rely=0.2, anchor="center")

    player1_label = tk.Label(info_frame, text="Гравець 1: 0", font=("Arial", 12), bg="#1e1e1e", fg="white")
    player1_label.pack(pady=3)

    player2_label = tk.Label(info_frame, text="Гравець 2: 0", font=("Arial", 12), bg="#1e1e1e", fg="white")
    player2_label.pack(pady=3)

    status_label = tk.Label(info_frame, text="Хід гравця 1", font=("Arial", 12, "bold"), bg="#1e1e1e", fg="#FFD700")
    status_label.pack(pady=10)

    canvas = tk.Canvas(right_frame, width=80, height=80, highlightthickness=0, bg="#1e1e1e")
    canvas.place(relx=0.5, rely=0.7, anchor="center")

    circle = canvas.create_oval(0, 0, 80, 80, fill="#4CAF50", outline="#4CAF50")
    circle_text = canvas.create_text(40, 40, text="Кинути", fill="white", font=("Arial", 10, "bold"))

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

    def finish_game():
        nonlocal game_active, rematch_btn
        game_active = False
        canvas.itemconfig(circle_text, state='hidden')
        canvas.itemconfig(circle, fill="#555")

        rematch_btn = styled_button(right_frame, "Реванш", restart_classic, bg="#607d8b")
        rematch_btn.place(relx=0.5, rely=0.85, anchor="center")

    def restart_classic():
        nonlocal rematch_btn
        if rematch_btn:
            rematch_btn.destroy()
        start_classic_mode()

    def roll_dice():
        nonlocal player1_score, player2_score, turn, game_active
        if not game_active:
            return
        canvas.itemconfig(circle_text, state='hidden')

        def apply_result():
            nonlocal player1_score, player2_score, turn, game_active
            roll = random.randint(1, 6)
            dice_label.config(image=dice_images[roll - 1])
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
            if player1_score >= 30 or player2_score >= 30:
                winner = "1" if player1_score >= 30 else "2"
                status_label.config(text=f"🎉 Гравець {winner} переміг!")
                finish_game()
            else:
                canvas.itemconfig(circle_text, state='normal')

        animate_dice(apply_result)

    canvas.tag_bind(circle, "<Button-1>", lambda e: roll_dice())
    canvas.tag_bind(circle_text, "<Button-1>", lambda e: roll_dice())

# --- Футбольний режим ---
def start_football_mode():
    for widget in root.winfo_children():
        widget.destroy()

    back_btn = styled_button(root, "⟵", show_main_menu, bg="#f44336")
    back_btn.place(x=460, y=10, width=30, height=30)

    label_instr = tk.Label(root, text="Введіть назви команд:", font=("Arial", 14), bg="#1e1e1e", fg="white")
    label_instr.pack(pady=10)

    team1_entry = tk.Entry(root, font=("Arial", 12))
    team1_entry.insert(0, "Команда 1")
    team1_entry.pack(pady=5)

    team2_entry = tk.Entry(root, font=("Arial", 12))
    team2_entry.insert(0, "Команда 2")
    team2_entry.pack(pady=5)

    def start_tournament():
        teams = [team1_entry.get().strip() or "Команда 1", team2_entry.get().strip() or "Команда 2"]
        for widget in root.winfo_children():
            widget.destroy()

        team_scores = [0, 0]
        round_number = 1
        total_rounds = 10
        game_active = True

        back_btn = styled_button(root, "⟵", show_main_menu, bg="#f44336")
        back_btn.place(x=460, y=10, width=30, height=30)

        title_label = tk.Label(root, text="Футбольний турнір", font=("Arial", 18, "bold"), bg="#1e1e1e", fg="white")
        title_label.pack(pady=10)

        scores_label = tk.Label(root, text=f"{teams[0]}: 0  -  {teams[1]}: 0", font=("Arial", 14), bg="#1e1e1e", fg="white")
        scores_label.pack(pady=10)

        status_label = tk.Label(root, text=f"Раунд {round_number}. Хід {teams[0]}", font=("Arial", 12), bg="#1e1e1e", fg="#FFD700")
        status_label.pack(pady=10)

        dice_label = tk.Label(root, image=dice_images[0], bg="#1e1e1e")
        dice_label.pack(pady=10)

        rematch_btn = None
        newgame_btn = None

        def finish_football_game():
            nonlocal game_active, rematch_btn, newgame_btn
            game_active = False
            roll_button.pack_forget()

            rematch_btn = styled_button(root, "Реванш", restart_tournament, bg="#607d8b")
            rematch_btn.pack(side=tk.LEFT, padx=50, pady=10)

            newgame_btn = styled_button(root, "Нова гра", show_main_menu, bg="#4CAF50")
            newgame_btn.pack(side=tk.RIGHT, padx=50, pady=10)

        def restart_tournament():
            nonlocal rematch_btn, newgame_btn
            if rematch_btn:
                rematch_btn.destroy()
            if newgame_btn:
                newgame_btn.destroy()
            start_football_mode()

        def roll_football_dice():
            nonlocal round_number, game_active
            if not game_active:
                return
            dice_roll = random.randint(1, 6)
            dice_label.config(image=dice_images[dice_roll - 1])

            current_team = (round_number - 1) % 2
            team_scores[current_team] += dice_roll
            scores_label.config(text=f"{teams[0]}: {team_scores[0]}  -  {teams[1]}: {team_scores[1]}")

            if round_number >= total_rounds:
                if team_scores[0] > team_scores[1]:
                    status_label.config(text=f"🏆 Перемогла {teams[0]}!")
                elif team_scores[1] > team_scores[0]:
                    status_label.config(text=f"🏆 Перемогла {teams[1]}!")
                else:
                    status_label.config(text="Нічия! 🏆")
                finish_football_game()
            else:
                round_number += 1
                next_team = (round_number - 1) % 2
                status_label.config(text=f"Раунд {round_number}. Хід {teams[next_team]}")

        roll_button = styled_button(root, "Кинути кубик", roll_football_dice, bg="#2196F3")
        roll_button.pack(pady=20)

    start_btn = styled_button(root, "Почати турнір", start_tournament, bg="#4CAF50")
    start_btn.pack(pady=20)

show_main_menu()
root.mainloop()
