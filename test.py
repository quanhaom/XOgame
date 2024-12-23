import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import pygame
import random

class CaroGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Cờ Caro")
        self.root.geometry("500x800")
        pygame.mixer.init()
        self.sound_enabled = True
        self.click_sound = "click.wav" 
        self.background_sound = "background.mp3" 
        self.play_background_sound()
        try:
            self.bg_image = Image.open("background.jpg") 
            resized_image = self.bg_image.resize((500, 800), Image.Resampling.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(resized_image)
        except FileNotFoundError:
            messagebox.showerror("Error", "Background image file not found!")
            self.bg_image = Image.new("RGB", (500, 800), color="gray") 
            self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        self.bg_label = tk.Label(self.root, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.title_label = tk.Label(self.root, text="CỜ CARO", font=("Arial", 36, "bold"), bg="#ffffff", fg="white")
        self.title_label.place(relx=0.5, y=50, anchor="center")
        self.mode_frame = tk.Frame(self.root, bg="#ffffff")
        self.mode_frame.place(relx=0.5, rely=0.8, anchor="center")

        button_style = {
            "font": ("Arial", 18),
            "bg": "#ffffff",
            "activebackground": "#ffffff",
            "bd": 0, 
            "highlightthickness": 0,
            "fg": "black"
        }
        tk.Button(self.mode_frame, text="1 Người chơi", command=self.start_pvc, **button_style).pack(pady=10)
        tk.Button(self.mode_frame, text="2 Người chơi", command=self.start_pvp, **button_style).pack(pady=10)
        tk.Button(self.mode_frame, text="Hướng dẫn", command=self.show_instructions, **button_style).pack(pady=10)
        self.sound_button = tk.Button(self.root, text="🔊", font=("Arial", 20), command=self.toggle_sound)
        self.sound_button.place(x=400, y=20)
        self.board_frame = None
        self.board_size = 10
        self.board = []
        self.current_player = "X"
        self.game_mode = None 
    def play_background_sound(self):
        if self.sound_enabled: 
            try:
                pygame.mixer.music.load(self.background_sound)
                pygame.mixer.music.play(-1) 
            except pygame.error:
                messagebox.showwarning("Lỗi âm thanh", "Không tìm thấy file âm thanh nền!")
    def toggle_sound(self):
        self.sound_enabled = not self.sound_enabled
        self.sound_button.config(text="🔊" if self.sound_enabled else "🔇")
        
        if self.sound_enabled:
            if not pygame.mixer.music.get_busy(): 
                self.play_background_sound()
            else:
                pygame.mixer.music.unpause()  
        else:
            pygame.mixer.music.pause()
    def play_sound(self):
        try:
            click_sound = pygame.mixer.Sound(self.click_sound) 
            click_sound.play()
        except pygame.error:
            messagebox.showwarning("Lỗi âm thanh", "Không tìm thấy file âm thanh click!")
    def play_draw_sound(self):
        try:
            draw_sound = pygame.mixer.Sound("draw.wav")
            draw_sound.play()
        except pygame.error:
            messagebox.showwarning("Lỗi âm thanh", "Không tìm thấy file âm thanh hòa!")
    def play_win_sound(self):
        try:
            draw_sound = pygame.mixer.Sound("win.wav")
            draw_sound.play()
        except pygame.error:
            messagebox.showwarning("Lỗi âm thanh", "Không tìm thấy file âm thanh hòa!")
    def play_lose_sound(self):
        try:
            draw_sound = pygame.mixer.Sound("lose.wav")
            draw_sound.play()
        except pygame.error:
            messagebox.showwarning("Lỗi âm thanh", "Không tìm thấy file âm thanh hòa!")

    def show_instructions(self):
        instructions = (
            "Cờ Caro là trò chơi giữa hai người chơi hoặc người chơi với máy.\n\n"
            "- Mỗi người luân phiên đánh dấu 'X' hoặc 'O' trên bàn cờ.\n"
            "- Mục tiêu: đạt 5 ký tự liên tiếp theo hàng, cột, hoặc chéo.\n"
            "- Trong chế độ Người vs Máy, máy sẽ chơi với dấu 'O'.\n"
            "- Người chơi nhấp chuột vào ô trống để đánh dấu."
        )
        messagebox.showinfo("Hướng dẫn", instructions)
    def start_pvp(self):
        self.game_mode = "pvp"
        self.show_board_size_selection()

    def start_pvc(self):
        self.game_mode = "pvc"
        self.show_board_size_selection()

    def show_board_size_selection(self):
        self.mode_frame.destroy()

        self.size_frame = tk.Frame(self.root, bg="#ffffff")
        self.size_frame.place(relx=0.5, rely=0.5, anchor="center")

        button_style1 = {
            "font": ("Arial", 50),
            "bg": "#ffffff", 
            "activebackground": "#ffffff",  
            "bd": 0,  
            "highlightthickness": 0,  
            "fg": "black"  
        }
        try:
            self.button_image1 = Image.open("3x3.jpg") 
            self.button_image1 = self.button_image1.resize((150, 150), Image.Resampling.LANCZOS)
            self.button_photo1 = ImageTk.PhotoImage(self.button_image1)
        except FileNotFoundError:
            messagebox.showerror("Error", "Button image file not found!")
            self.button_photo = None

        button_style1.update({
            "image": self.button_photo1,
            "compound": "center",
            "width": 500,
            "height": 200
        })        
        button_style2 = {
            "font": ("Arial", 50),
            "bg": "#ffffff", 
            "activebackground": "#ffffff", 
            "bd": 0,  
            "highlightthickness": 0,
            "fg": "black" 
        }
        try:
            self.button_image1 = Image.open("5x5.jpg")  
            self.button_image1 = self.button_image1.resize((150, 150), Image.Resampling.LANCZOS)
            self.button_photo1 = ImageTk.PhotoImage(self.button_image1)
        except FileNotFoundError:
            messagebox.showerror("Error", "Button image file not found!")
            self.button_photo = None

        button_style2.update({
            "image": self.button_photo1,
            "compound": "center",
            "width": 500,
            "height": 200
        })        
        button_style3 = {
            "font": ("Arial", 50),
            "bg": "#ffffff", 
            "activebackground": "#ffffff", 
            "bd": 0,
            "highlightthickness": 0,
            "fg": "black"
        }
        try:
            self.button_image1 = Image.open("7x7.jpg") 
            self.button_image1 = self.button_image1.resize((150, 150), Image.Resampling.LANCZOS)
            self.button_photo1 = ImageTk.PhotoImage(self.button_image1)
        except FileNotFoundError:
            messagebox.showerror("Error", "Button image file not found!")
            self.button_photo = None

        button_style3.update({
            "image": self.button_photo1,
            "compound": "center",
            "width": 500,
            "height": 200
        })
        tk.Button(self.size_frame, text="", command=lambda: self.setup_game(3), **button_style1).pack(pady=10)
        tk.Button(self.size_frame, text="", command=lambda: self.setup_game(5), **button_style2).pack(pady=10)
        tk.Button(self.size_frame, text="", command=lambda: self.setup_game(7), **button_style3).pack(pady=10)

    def setup_game(self, size):
        self.board_size = size
        self.win_condition = self.calculate_win_condition(size)

        self.size_frame.destroy()
        self.mode_frame.destroy()
        self.board = [[None for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.board_frame = tk.Frame(self.root)

        for i in range(self.board_size):
            for j in range(self.board_size):
                btn = tk.Button(self.board_frame, text=" ", font=("Arial", 40 if self.board_size == 5 else 65 if self.board_size ==3 else 27), width=3, height=1,
                                command=lambda x=i, y=j: self.make_move(x, y))
                btn.grid(row=i, column=j, sticky="nsew")
                self.board[i][j] = btn
        for i in range(self.board_size):
            self.board_frame.grid_rowconfigure(i, weight=1)
            self.board_frame.grid_columnconfigure(i, weight=1)

        self.board_frame.place(relx=0.5, rely=0.5, anchor="center")

        self.win_condition_label = tk.Label(self.root, text=f"Điều kiện thắng: {self.win_condition} trên cùng 1 hàng", font=("Arial", 16), bg="#ffffff")
        self.win_condition_label.place(relx=0.5, rely=0.9, anchor="center") 

        self.turn_label = tk.Label(self.root, text=f"Lượt chơi của : {self.current_player}", font=("Arial", 16), bg="#ffffff")
        self.turn_label.place(relx=0.5, rely=0.85, anchor="center") 

        self.exit_button = tk.Button(self.root, text=" X ", font=("Arial", 20), command=self.back_to_main_menu, bg="#ffffff")
        self.exit_button.place(x=450, y=20)

    def back_to_main_menu(self):
        if self.board_frame:
            self.board_frame.destroy()
            self.board_frame = None
        if self.size_frame:
            self.size_frame.destroy()
            self.size_frame = None
        if self.win_condition_label:
            self.win_condition_label.destroy()
            self.win_condition_label = None
            self.exit_button.destroy()
            self.turn_label.destroy()
        
        self.current_player = "X"
        self.game_mode = None 

        self.mode_frame = tk.Frame(self.root, bg="#ffffff")
        self.mode_frame.place(relx=0.5, rely=0.8, anchor="center")

        button_style = {
            "font": ("Arial", 18),
            "bg": "#ffffff",
            "activebackground": "#ffffff",
            "bd": 0,
            "highlightthickness": 0,
            "fg": "black"
        }

        tk.Button(self.mode_frame, text="1 Người chơi", command=self.start_pvc, **button_style).pack(pady=10)
        tk.Button(self.mode_frame, text="2 Người chơi", command=self.start_pvp, **button_style).pack(pady=10)
        tk.Button(self.mode_frame, text="Hướng dẫn", command=self.show_instructions, **button_style).pack(pady=10)

    def calculate_win_condition(self, size):
        if size == 3:
            return 3
        elif size == 5:
            return 4
        elif size == 7:
            return 5
        return 5

    def make_move(self, x, y):
        if self.board[x][y]["text"] == " ":
            self.play_sound()
            self.board[x][y]["text"] = self.current_player
            
            if self.check_winner(x, y):
                self.play_win_sound()
                messagebox.showinfo("Kết quả", f"Người chơi '{self.current_player}' thắng!")
                self.reset_game() 
                return

            if self.game_mode == "pvp":
                self.current_player = "O" if self.current_player == "X" else "X"
            elif self.game_mode == "pvc" and self.current_player == "X":
                self.current_player = "O"
                self.computer_move()

            self.turn_label.config(text=f"Lượt chơi của : {self.current_player}")
        else:
            messagebox.showwarning("Cảnh báo", "Ô này đã được đánh dấu. Hãy chọn ô khác.")

    def computer_move(self):
        empty_cells = [
            (i, j) 
            for i in range(self.board_size) 
            for j in range(self.board_size) 
            if self.board[i][j]["text"] == " "
        ]
        if not empty_cells:
            return
        for x, y in empty_cells:
            self.current_player = "O"
            self.board[x][y]["text"] = "O"
            if self.check_winner(x, y):
                self.play_lose_sound()
                messagebox.showinfo("Kết quả", "Máy thắng!")
                self.reset_game()
                return
            self.board[x][y]["text"] = " " 
        for x, y in empty_cells:
            self.current_player = "X"
            self.board[x][y]["text"] = "X"
            if self.check_winner(x, y):
                self.board[x][y]["text"] = "O" 
                return
            self.board[x][y]["text"] = " "
        x, y = random.choice(empty_cells)
        self.board[x][y]["text"] = "O"
        self.current_player = "X"

    def check_winner(self, x, y):
        def count_consecutive(dx, dy):
            count = 1
            for direction in [1, -1]:
                i, j = x + direction * dx, y + direction * dy
                while 0 <= i < self.board_size and 0 <= j < self.board_size and self.board[i][j]["text"] == self.current_player:
                    count += 1
                    i += direction * dx
                    j += direction * dy
            return count

        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
        for dx, dy in directions:
            if count_consecutive(dx, dy) >= self.win_condition:
                return True

        if all(self.board[i][j]["text"] != " " for i in range(self.board_size) for j in range(self.board_size)):
            if not self.sound_enabled:
                pygame.mixer.music.stop()
            self.play_draw_sound()
            messagebox.showinfo("Kết quả", "Trò chơi hòa!")
            self.reset_game()
            return False

        return False

    def reset_game(self):
        if self.board_frame:
            self.board_frame.destroy()
            self.board_frame = None
            self.win_condition_label.destroy()
            self.exit_button.destroy()
            self.turn_label.destroy()
        self.current_player = "X"
        self.setup_game(self.board_size)

if __name__ == "__main__":
    root = tk.Tk()
    game = CaroGame(root)
    root.mainloop()
