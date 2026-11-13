
import tkinter as tk
import random
import subprocess
import threading


# =========================
# TEXT TO SPEECH
# =========================

def speak(text):
    def run_voice():
        safe_text = text.replace("'", "''")

        command = (
            "Add-Type -AssemblyName System.Speech; "
            "$voice = New-Object "
            "System.Speech.Synthesis.SpeechSynthesizer; "
            f"$voice.Speak('{safe_text}');"
        )

        try:
            subprocess.run(
                ["powershell", "-NoProfile", "-Command", command],
                creationflags=0x08000000
            )
        except Exception:
            pass

    threading.Thread(
        target=run_voice,
        daemon=True
    ).start()


# =========================
# MAIN APPLICATION
# =========================

class MiniGamesHub:

    def __init__(self, root):
        self.root = root
        self.root.title("Mini Games Hub")
        self.root.geometry("750x650")
        self.root.resizable(False, False)
        self.root.configure(bg="#101827")

        self.bg = "#101827"
        self.panel = "#1e293b"
        self.accent = "#6366f1"
        self.white = "#f8fafc"
        self.muted = "#94a3b8"

        self.current_game = None
        self.snake_job = None
        self.voice_enabled = True

        self.show_menu()

    def say(self, text):
        if self.voice_enabled:
            speak(text)

    def toggle_voice(self):
        self.voice_enabled = not self.voice_enabled

        if self.voice_enabled:
            self.voice_button.config(
                text="VOICE ON",
                bg="#15803d"
            )
            self.say("Voice enabled")
        else:
            self.voice_button.config(
                text="VOICE OFF",
                bg="#b91c1c"
            )

    def clear_screen(self):
        if self.snake_job is not None:
            self.root.after_cancel(self.snake_job)
            self.snake_job = None

        self.current_game = None

        for widget in self.root.winfo_children():
            widget.destroy()

    def title(self, text):
        tk.Label(
            self.root,
            text=text,
            font=("Arial", 27, "bold"),
            bg=self.bg,
            fg=self.white
        ).pack(pady=20)

    def button(self, parent, text, command, color=None):
        return tk.Button(
            parent,
            text=text,
            command=command,
            font=("Arial", 13, "bold"),
            bg=color or self.accent,
            fg="white",
            activebackground="#818cf8",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            width=20,
            height=2
        )

    def back_button(self):
        self.button(
            self.root,
            "Back to Menu",
            self.show_menu,
            "#475569"
        ).pack(pady=15)


       # =========================
    # MAIN MENU
    # =========================

    def show_menu(self):
        self.clear_screen()

        self.say("Welcome to Mini Games Hub")

        tk.Label(
            self.root,
            text="MINI GAMES HUB",
            font=("Arial", 32, "bold"),
            bg=self.bg,
            fg="#818cf8"
        ).pack(pady=(35, 5))

        tk.Label(
            self.root,
            text="Choose your favorite game!",
            font=("Arial", 14),
            bg=self.bg,
            fg=self.muted
        ).pack(pady=10)

        self.voice_button = self.button(
            self.root,
            "VOICE ON",
            self.toggle_voice,
            "#15803d"
        )
        self.voice_button.pack(pady=8)

        games = [
            ("Tic Tac Toe", self.tic_tac_toe),
            ("Rock Paper Scissors", self.rock_paper_scissors),
            ("Snake Game", self.snake_game),
            ("Memory Game", self.memory_game),
            ("CHATBOT ASSISTANT", self.chatbot)
        ]

        for name, command in games:
            self.button(
                self.root,
                name,
                command
            ).pack(pady=6)

        tk.Label(
            self.root,
            text="Made with Python 3.10.11",
            font=("Arial", 10),
            bg=self.bg,
            fg=self.muted
        ).pack(side="bottom", pady=15)

    # =========================
    # CHATBOT ASSISTANT
    # =========================

    def chatbot(self):

        self.chat_window = tk.Toplevel(self.root)
        self.chat_window.title("Game Assistant")
        self.chat_window.geometry("500x600")
        self.chat_window.configure(bg=self.bg)

        header = tk.Frame(
            self.chat_window,
            bg="#6366f1"
        )
        header.pack(fill="x")

        tk.Label(
            header,
            text="GAME ASSISTANT",
            font=("Arial", 20, "bold"),
            bg="#6366f1",
            fg="white"
        ).pack(pady=15)

        self.chat_display = tk.Text(
            self.chat_window,
            font=("Arial", 11),
            bg="#0f172a",
            fg="white",
            wrap="word",
            relief="flat",
            padx=12,
            pady=12,
            state="disabled"
        )

        self.chat_display.pack(
            fill="both",
            expand=True,
            padx=12,
            pady=12
        )

        self.chat_display.tag_config(
            "bot",
            foreground="#38bdf8"
        )

        self.chat_display.tag_config(
            "user",
            foreground="#4ade80"
        )

        input_frame = tk.Frame(
            self.chat_window,
            bg=self.bg
        )
        input_frame.pack(fill="x", padx=12, pady=10)

        self.chat_entry = tk.Entry(
            input_frame,
            font=("Arial", 12),
            bg="#1e293b",
            fg="white",
            insertbackground="white",
            relief="flat"
        )

        self.chat_entry.pack(
            side="left",
            fill="x",
            expand=True,
            ipady=12,
            padx=(0, 8)
        )

        self.chat_entry.bind(
            "<Return>",
            lambda event: self.send_message()
        )

        tk.Button(
            input_frame,
            text="SEND",
            font=("Arial", 11, "bold"),
            bg="#6366f1",
            fg="white",
            relief="flat",
            command=self.send_message
        ).pack(side="right", ipady=9)

        tk.Button(
            self.chat_window,
            text="SPEAK LAST ANSWER",
            font=("Arial", 10, "bold"),
            bg="#15803d",
            fg="white",
            relief="flat",
            command=self.speak_chat_answer
        ).pack(pady=10)

        self.last_chat_answer = "Welcome to Game Assistant!"

        self.add_chat_message(
            "BOT",
            "Hello! Welcome to Mini Games Hub! 👋\n\n"
            "I am your Game Assistant. 🎮\n\n"
            "Ask me how to play any game!"
        )

        self.chat_entry.focus_set()

    # =========================
    # CHAT MESSAGES
    # =========================

    def add_chat_message(self, sender, message):

        self.chat_display.config(state="normal")

        tag = "user" if sender == "YOU" else "bot"

        self.chat_display.insert(
            "end",
            f"\n{sender}:\n",
            tag
        )

        self.chat_display.insert(
            "end",
            message + "\n"
        )

        self.chat_display.config(state="disabled")
        self.chat_display.see("end")

    def send_message(self):

        message = self.chat_entry.get().strip()

        if not message:
            return

        self.add_chat_message("YOU", message)

        self.chat_entry.delete(0, "end")

        answer = self.get_bot_response(message)

        self.last_chat_answer = answer

        self.add_chat_message("BOT", answer)

        self.say(answer)

    def speak_chat_answer(self):
        self.say(self.last_chat_answer)


            # =========================
    # CHATBOT BRAIN
    # =========================

    def get_bot_response(self, message):

        msg = message.lower()

        if any(word in msg for word in ["hello", "hi", "hey", "pershendetje"]):
            return (
                "Hello! Welcome to Mini Games Hub! 👋\n"
                "I can help you with all four games!"
            )

        elif "help" in msg or "ndihme" in msg:
            return (
                "I can help you with:\n\n"
                "1. Tic Tac Toe\n"
                "2. Rock Paper Scissors\n"
                "3. Snake Game\n"
                "4. Memory Game\n\n"
                "Just write the name of a game!"
            )

        elif "tic tac toe" in msg:
            return (
                "TIC TAC TOE GUIDE\n\n"
                "1. The game has a 3x3 board.\n"
                "2. Player X starts first.\n"
                "3. Player O plays next.\n"
                "4. Choose empty squares.\n"
                "5. Get three symbols in a row to win!\n\n"
                "You can win horizontally, vertically "
                "or diagonally.\n\n"
                "TIP: Try to control the center!"
            )

        elif "rock paper scissors" in msg:
            return (
                "ROCK PAPER SCISSORS GUIDE\n\n"
                "Rock beats Scissors.\n"
                "Paper beats Rock.\n"
                "Scissors beats Paper.\n\n"
                "Same choices mean a draw!"
            )

        elif "snake" in msg:
            return (
                "SNAKE GAME GUIDE\n\n"
                "1. Use arrow keys to move.\n"
                "2. Eat the red food.\n"
                "3. Every food gives 10 points.\n"
                "4. Avoid hitting walls.\n"
                "5. Avoid hitting your own body.\n\n"
                "TIP: Plan your movements carefully!"
            )

        elif "memory" in msg:
            return (
                "MEMORY GAME GUIDE\n\n"
                "1. There are 16 hidden cards.\n"
                "2. Click one card to reveal it.\n"
                "3. Click another card.\n"
                "4. Find matching pairs.\n"
                "5. Find all 8 pairs to win!\n\n"
                "TIP: Remember card positions!"
            )

        elif any(word in msg for word in [
            "controls", "keyboard", "keys"
        ]):
            return (
                "GAME CONTROLS\n\n"
                "Snake:\n"
                "UP = Move up\n"
                "DOWN = Move down\n"
                "LEFT = Move left\n"
                "RIGHT = Move right\n\n"
                "Other games use mouse clicks."
            )

        elif any(word in msg for word in [
            "how to win", "winning", "tips", "strategy"
        ]):
            return (
                "WINNING TIPS!\n\n"
                "Tic Tac Toe: Control the center.\n"
                "Rock Paper Scissors: Change choices.\n"
                "Snake: Plan your movements.\n"
                "Memory: Remember card positions.\n\n"
                "Practice makes perfect!"
            )

        elif any(word in msg for word in [
            "thank you", "thanks", "thx"
        ]):
            return "You're welcome! Have fun playing! 😊"

        elif "bye" in msg:
            return "Goodbye! Thanks for playing! 🎮"

        else:
            return (
                "I'm your Mini Games Assistant!\n\n"
                "Try asking me:\n"
                "• How do I play Tic Tac Toe?\n"
                "• How do I play Snake?\n"
                "• How do I win?\n"
                "• What are the controls?\n"
                "• How does Memory Game work?"
            )

    # =========================
    # TIC TAC TOE
    # =========================

    def tic_tac_toe(self):

        self.clear_screen()
        self.current_game = "tic"

        self.say("Welcome to Tic Tac Toe")
        self.title("TIC TAC TOE")

        self.tic_board = [""] * 9
        self.tic_turn = "X"
        self.tic_over = False

        self.tic_status = tk.Label(
            self.root,
            text="Player X's turn",
            font=("Arial", 17, "bold"),
            bg=self.bg,
            fg="#38bdf8"
        )
        self.tic_status.pack(pady=10)

        board = tk.Frame(self.root, bg=self.bg)
        board.pack(pady=10)

        self.tic_buttons = []

        for i in range(9):

            btn = tk.Button(
                board,
                text="",
                font=("Arial", 25, "bold"),
                width=5,
                height=2,
                bg=self.panel,
                fg=self.white,
                activebackground="#334155",
                relief="flat",
                command=lambda n=i: self.tic_move(n)
            )

            btn.grid(
                row=i // 3,
                column=i % 3,
                padx=5,
                pady=5
            )

            self.tic_buttons.append(btn)

        self.button(
            self.root,
            "Restart",
            self.tic_tac_toe
        ).pack(pady=10)

        self.back_button()

    def tic_move(self, index):

        if self.tic_board[index] != "" or self.tic_over:
            return

        self.tic_board[index] = self.tic_turn

        color = (
            "#38bdf8"
            if self.tic_turn == "X"
            else "#f472b6"
        )

        self.tic_buttons[index].config(
            text=self.tic_turn,
            fg=color
        )

        winner = self.check_tic_winner()

        if winner:

            self.tic_status.config(
                text=f"Player {winner} wins!",
                fg="#4ade80"
            )

            self.say(f"Player {winner} wins!")
            self.tic_over = True
            return

        if "" not in self.tic_board:

            self.tic_status.config(
                text="It's a Draw!",
                fg="#facc15"
            )

            self.say("It's a draw!")
            self.tic_over = True
            return

        self.tic_turn = (
            "O" if self.tic_turn == "X" else "X"
        )

        self.tic_status.config(
            text=f"Player {self.tic_turn}'s turn"
        )

        self.say(f"Player {self.tic_turn}'s turn")

    def check_tic_winner(self):

        combinations = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),
            (0, 3, 6), (1, 4, 7), (2, 5, 8),
            (0, 4, 8), (2, 4, 6)
        ]

        for a, b, c in combinations:

            if (
                self.tic_board[a] != ""
                and self.tic_board[a]
                == self.tic_board[b]
                == self.tic_board[c]
            ):
                return self.tic_board[a]

        return None
        # =========================
    # ROCK PAPER SCISSORS
    # =========================

    def rock_paper_scissors(self):

        self.clear_screen()
        self.current_game = "rps"

        self.say("Welcome to Rock Paper Scissors")
        self.title("ROCK PAPER SCISSORS")

        self.rps_score = 0
        self.rps_computer = 0
        self.rps_draws = 0

        self.rps_choices = {
            "Rock": "Rock",
            "Paper": "Paper",
            "Scissors": "Scissors"
        }

        self.rps_result = tk.Label(
            self.root,
            text="Choose your move!",
            font=("Arial", 19, "bold"),
            bg=self.bg,
            fg=self.white
        )
        self.rps_result.pack(pady=25)

        self.rps_comparison = tk.Label(
            self.root,
            text="You VS Computer",
            font=("Arial", 17),
            bg=self.bg,
            fg="#38bdf8"
        )
        self.rps_comparison.pack(pady=15)

        choices_frame = tk.Frame(
            self.root,
            bg=self.bg
        )
        choices_frame.pack(pady=15)

        for choice in self.rps_choices:

            tk.Button(
                choices_frame,
                text=choice,
                font=("Arial", 15, "bold"),
                bg=self.panel,
                fg=self.white,
                activebackground="#334155",
                relief="flat",
                width=10,
                height=3,
                command=lambda c=choice: self.rps_play(c)
            ).pack(side="left", padx=7)

        self.rps_score_label = tk.Label(
            self.root,
            text="You: 0   Computer: 0   Draws: 0",
            font=("Arial", 14, "bold"),
            bg=self.bg,
            fg="#4ade80"
        )
        self.rps_score_label.pack(pady=20)

        self.button(
            self.root,
            "Restart",
            self.rock_paper_scissors
        ).pack(pady=5)

        self.back_button()

    def rps_play(self, player):

        computer = random.choice(
            list(self.rps_choices.keys())
        )

        self.rps_comparison.config(
            text=f"You: {player} VS Computer: {computer}"
        )

        if player == computer:

            self.rps_result.config(
                text="It's a Draw!",
                fg="#facc15"
            )

            self.say("It's a draw!")
            self.rps_draws += 1

        elif (
            (player == "Rock" and computer == "Scissors")
            or (player == "Paper" and computer == "Rock")
            or (player == "Scissors" and computer == "Paper")
        ):

            self.rps_result.config(
                text="You Win!",
                fg="#4ade80"
            )

            self.say("You win! Congratulations!")
            self.rps_score += 1

        else:

            self.rps_result.config(
                text="Computer Wins!",
                fg="#f87171"
            )

            self.say("Computer wins!")
            self.rps_computer += 1

        self.rps_score_label.config(
            text=(
                f"You: {self.rps_score}   "
                f"Computer: {self.rps_computer}   "
                f"Draws: {self.rps_draws}"
            )
        )

    # =========================
    # SNAKE GAME
    # =========================

    def snake_game(self):

        self.clear_screen()
        self.current_game = "snake"

        self.say("Welcome to Snake Game")
        self.title("SNAKE GAME")

        self.snake_size = 20
        self.snake_speed = 120

        self.snake_body = [
            (200, 200),
            (180, 200),
            (160, 200)
        ]

        self.snake_direction = "Right"
        self.snake_next_direction = "Right"
        self.snake_score = 0
        self.snake_running = True

        self.snake_score_label = tk.Label(
            self.root,
            text="Score: 0",
            font=("Arial", 16, "bold"),
            bg=self.bg,
            fg="#4ade80"
        )
        self.snake_score_label.pack(pady=5)

        self.snake_canvas = tk.Canvas(
            self.root,
            width=400,
            height=400,
            bg="#0f172a",
            highlightthickness=2,
            highlightbackground="#334155"
        )
        self.snake_canvas.pack(pady=5)

        self.snake_food = self.create_food()

        self.snake_draw()

        self.snake_message = tk.Label(
            self.root,
            text="Use ARROW KEYS to move",
            font=("Arial", 12),
            bg=self.bg,
            fg=self.muted
        )
        self.snake_message.pack(pady=5)

        self.button(
            self.root,
            "Restart",
            self.snake_game
        ).pack(pady=5)

        self.back_button()

        self.root.bind(
            "<KeyPress>",
            self.snake_key
        )

        self.snake_canvas.focus_set()

        self.snake_job = self.root.after(
            self.snake_speed,
            self.snake_update
        )

    def create_food(self):

        while True:

            food = (
                random.randrange(0, 400, 20),
                random.randrange(0, 400, 20)
            )

            if food not in self.snake_body:
                return food

    def snake_key(self, event):

        if self.current_game != "snake":
            return

        directions = {
            "Up": "Up",
            "Down": "Down",
            "Left": "Left",
            "Right": "Right"
        }

        key = event.keysym

        if key not in directions:
            return

        new_direction = directions[key]

        opposites = {
            "Up": "Down",
            "Down": "Up",
            "Left": "Right",
            "Right": "Left"
        }

        if new_direction != opposites[self.snake_direction]:
            self.snake_next_direction = new_direction

    def snake_draw(self):

        self.snake_canvas.delete("all")

        fx, fy = self.snake_food

        self.snake_canvas.create_oval(
            fx + 2,
            fy + 2,
            fx + 18,
            fy + 18,
            fill="#ef4444",
            outline=""
        )

        for i, (x, y) in enumerate(self.snake_body):

            color = (
                "#4ade80"
                if i == 0
                else "#16a34a"
            )

            self.snake_canvas.create_rectangle(
                x + 1,
                y + 1,
                x + 19,
                y + 19,
                fill=color,
                outline="#0f172a"
            )

    def snake_update(self):

        self.snake_job = None

        if (
            self.current_game != "snake"
            or not self.snake_running
        ):
            return

        directions = {
            "Up": (0, -20),
            "Down": (0, 20),
            "Left": (-20, 0),
            "Right": (20, 0)
        }

        self.snake_direction = self.snake_next_direction

        dx, dy = directions[self.snake_direction]

        x, y = self.snake_body[0]

        new_head = (x + dx, y + dy)

        ate_food = new_head == self.snake_food

        if not ate_food:
            collision_body = self.snake_body[:-1]
        else:
            collision_body = self.snake_body

        if (
            new_head[0] < 0
            or new_head[0] >= 400
            or new_head[1] < 0
            or new_head[1] >= 400
            or new_head in collision_body
        ):
            self.snake_game_over()
            return

        self.snake_body.insert(0, new_head)

        if ate_food:

            self.snake_score += 10

            self.snake_score_label.config(
                text=f"Score: {self.snake_score}"
            )

            self.snake_food = self.create_food()

        else:
            self.snake_body.pop()

        self.snake_draw()

        self.snake_job = self.root.after(
            self.snake_speed,
            self.snake_update
        )

    def snake_game_over(self):

        self.snake_running = False

        self.snake_message.config(
            text=f"GAME OVER! Final Score: {self.snake_score}",
            fg="#f87171"
        )

        self.say(
            f"Game over! Your final score is {self.snake_score}"
        )

    # =========================
    # MEMORY GAME
    # =========================

    def memory_game(self):

        self.clear_screen()
        self.current_game = "memory"

        self.say("Welcome to Memory Game")
        self.title("MEMORY GAME")

        self.memory_symbols = [
            "Apple", "Banana", "Grapes", "Cherry",
            "Lemon", "Watermelon", "Kiwi", "Strawberry"
        ]

        self.memory_cards = self.memory_symbols * 2

        random.shuffle(self.memory_cards)

        self.memory_buttons = []
        self.memory_open = []
        self.memory_matched = set()
        self.memory_moves = 0
        self.memory_locked = False

        self.memory_status = tk.Label(
            self.root,
            text="Find all matching pairs!",
            font=("Arial", 15, "bold"),
            bg=self.bg,
            fg="#38bdf8"
        )
        self.memory_status.pack(pady=5)

        self.memory_score = tk.Label(
            self.root,
            text="Moves: 0     Pairs: 0/8",
            font=("Arial", 13),
            bg=self.bg,
            fg=self.white
        )
        self.memory_score.pack(pady=5)

        board = tk.Frame(
            self.root,
            bg=self.bg
        )
        board.pack(pady=10)

        for i in range(16):

            btn = tk.Button(
                board,
                text="?",
                font=("Arial", 22, "bold"),
                width=5,
                height=2,
                bg=self.panel,
                fg=self.white,
                activebackground="#334155",
                relief="flat",
                command=lambda n=i: self.memory_flip(n)
            )

            btn.grid(
                row=i // 4,
                column=i % 4,
                padx=5,
                pady=5
            )

            self.memory_buttons.append(btn)

        self.button(
            self.root,
            "Restart",
            self.memory_game
        ).pack(pady=8)

        self.back_button()

    def memory_flip(self, index):

        if self.memory_locked:
            return

        if index in self.memory_matched:
            return

        if index in self.memory_open:
            return

        self.memory_buttons[index].config(
            text=self.memory_cards[index],
            bg="#475569"
        )

        self.memory_open.append(index)

        if len(self.memory_open) == 2:

            self.memory_moves += 1
            self.memory_locked = True

            first, second = self.memory_open

            if (
                self.memory_cards[first]
                == self.memory_cards[second]
            ):

                self.memory_matched.add(first)
                self.memory_matched.add(second)

                self.memory_buttons[first].config(
                    bg="#15803d"
                )

                self.memory_buttons[second].config(
                    bg="#15803d"
                )

                self.memory_open = []
                self.memory_locked = False

                self.memory_update_score()

                self.say("Correct match!")

                if len(self.memory_matched) == 16:

                    self.memory_status.config(
                        text="CONGRATULATIONS! YOU WON!",
                        fg="#4ade80"
                    )

                    self.say(
                        "Congratulations! You found all pairs! You won!"
                    )

            else:

                self.memory_update_score()

                self.say("Try again!")

                self.root.after(
                    900,
                    self.memory_hide
                )

    def memory_hide(self):

        if self.current_game != "memory":
            return

        for index in self.memory_open:

            self.memory_buttons[index].config(
                text="?",
                bg=self.panel
            )

        self.memory_open = []
        self.memory_locked = False

    def memory_update_score(self):

        pairs = len(self.memory_matched) // 2

        self.memory_score.config(
            text=(
                f"Moves: {self.memory_moves}     "
                f"Pairs: {pairs}/8"
            )
        )


# =========================
# START APPLICATION
# =========================

if __name__ == "__main__":

    root = tk.Tk()

    app = MiniGamesHub(root)

    root.mainloop()
