import tkinter as tk  
from tkinter import simpledialog, messagebox  
import time  
from flask import Flask, render_template  

app = Flask(__name__)  

@app.route('/')  
def home():  
    return render_template('tower_of_hanoi.html')  

if __name__ == '__main__':  
    app.run(debug=True)
class TowerOfHanoiApp:  
    def __init__(self, master):  
        self.master = master  
        self.master.configure(bg="#e0f7fa")  # Light cyan background  
        self.create_database()  
        self.start_game()  

    def create_database(self):  
        # Placeholder for database creation logic  
        pass  

    def start_game(self):  
        self.player_name = simpledialog.askstring("Player Name", "Enter your name:")  
        if not self.player_name:  
            messagebox.showerror("Error", "Player name is required!")  
            self.master.destroy()  
            return  

        num_disks = simpledialog.askinteger("Number of Disks", "Enter the number of disks (3-10):", minvalue=3, maxvalue=10)  
        if num_disks is None:  
            messagebox.showerror("Error", "Number of disks is required!")  
            self.master.destroy()  
            return  

        self.num_disks = num_disks  
        self.moves = 0  
        self.start_time = time.time()  

        self.pegs = {'A': list(range(self.num_disks, 0, -1)), 'B': [], 'C': []}  
        self.create_widgets()  

    def create_widgets(self):  
        title_label = tk.Label(self.master, text="Tower of Hanoi", font=("Arial", 24, "bold"), bg="#e0f7fa")  
        title_label.pack(pady=20)  

        self.peg_frames = []  
        for peg in ['A', 'B', 'C']:  
            peg_frame = tk.Frame(self.master, width=200, height=400, bg="#f5f5f5", borderwidth=2, relief=tk.RAISED)  
            peg_frame.pack(side=tk.LEFT, padx=20, pady=20)  
            self.peg_frames.append(peg_frame)  
            peg_label = tk.Label(peg_frame, text=peg, font=("Arial", 16, "bold"), bg="#e0f7fa")  
            peg_label.pack(side=tk.TOP)  

        self.update_disk_positions()  

    def update_disk_positions(self):  
        for peg, disks in self.pegs.items():  
            peg_index = ['A', 'B', 'C'].index(peg)  
            for i, disk in enumerate(disks):  
                disk_label = tk.Label(self.peg_frames[peg_index], text=str(disk), font=("Arial", 16, "bold"),  
                                      bg=self.get_disk_color(disk), fg="white", width=6, height=2)  
                disk_label.place(x=50 - i * 10, y=350 - i * 30)  
                disk_label.bind("<Button-1>", self.start_drag)  
                disk_label.bind("<B1-Motion>", self.on_drag)  
                disk_label.bind("<ButtonRelease-1>", self.stop_drag)  

    def get_disk_color(self, disk):  
        colors = ['#FF5733', '#33FF57', '#3357FF', '#F3FF33', '#FF33A1', '#33FFF5', '#FF8333']  
        return colors[disk - 1] if disk - 1 < len(colors) else '#000'  

    def start_drag(self, event):  
        widget = event.widget  
        self.drag_data = {"disk": widget, "start_peg": self.find_peg(widget)}  

    def on_drag(self, event):  
        x = event.x_root - self.master.winfo_rootx() - event.widget.winfo_width() // 2  
        y = event.y_root - self.master.winfo_rooty() - event.widget.winfo_height() // 2  
        event.widget.place(x=x, y=y)  

    def stop_drag(self, event):  
        x, y = event.widget.winfo_x(), event.widget.winfo_y()  
        peg_index = self.get_target_peg(x, y)  

        if peg_index is not None:  
            target_peg = ["A", "B", "C"][peg_index]  
            disk = int(event.widget["text"])  
            self.move_disk(self.drag_data["start_peg"], target_peg, disk)  

        self.update_disk_positions()  

    def find_peg(self, widget):  
        for peg, disks in self.pegs.items():  
            if int(widget["text"]) in disks:  
                return peg  
        return None  

    def get_target_peg(self, x, y):  
        for i, peg_frame in enumerate(self.peg_frames):  
            peg_x, peg_y = peg_frame.winfo_x(), peg_frame.winfo_y()  
            peg_width, peg_height = peg_frame.winfo_width(), peg_frame.winfo_height()  
            if peg_x < x < peg_x + peg_width and peg_y < y < peg_y + peg_height:  
                return i  
        return None  

    def move_disk(self, start_peg, target_peg, disk):  
        if not self.pegs[target_peg] or self.pegs[target_peg][-1] > disk:  
            self.pegs[start_peg].remove(disk)  
            self.pegs[target_peg].append(disk)  
            self.moves += 1  
            self.update_disk_positions()  
            self.check_win()  

    def check_win(self):  
        if len(self.pegs['C']) == self.num_disks:  
            end_time = time.time()  
            time_taken = end_time - self.start_time  
            self.save_game_data(self.player_name, self.num_disks, self.moves, time_taken)  
            messagebox.showinfo("Game Over", f"Congratulations, {self.player_name}! You completed the game in {time_taken:.2f} seconds.")  
            self.master.destroy()  

    def save_game_data(self, player_name, num_disks, moves, time_taken):  
        # Placeholder for saving game data logic  
        pass  

if __name__ == "__main__":  
    root = tk.Tk()  
    app = TowerOfHanoiApp(root)  
    root.mainloop()