import tkinter as tk  
from tkinter import ttk, messagebox, simpledialog  
import sqlite3  
import time  

# Database functions  
def create_database():  
    conn = sqlite3.connect('hanoi.db')  
    c = conn.cursor()  
    c.execute('''CREATE TABLE IF NOT EXISTS games (  
                  player_name TEXT,  
                  num_disks INTEGER,  
                  moves INTEGER,  
             
                  time_taken REAL)''')  
    conn.commit()  
    conn.close()  

def next_move(self, from_peg, to_peg):  
    if not self.pegs[to_peg] or self.pegs[to_peg][-1] > self.pegs[from_peg][-1]:  
        disk = self.pegs[from_peg].pop()  
        self.pegs[to_peg].append(disk)  
        self.moves += 1  
        self.update_disk_positions()  
        if len(self.pegs['C']) == self.num_disks:  
            end_time = time.time()  
            time_taken = end_time - self.start_time  
            self.save_game_data(self.player_name, self.num_disks, self.moves, time_taken)  
            messagebox.showinfo("Game Over", f"Congratulations, {self.player_name}! You completed the game in {time_taken:.2f} seconds.")  
            self.master.destroy()  
    else:  
        messagebox.showerror("Invalid Move", "Cannot move a larger disk onto a smaller disk.")  

import sqlite3

def save_game_data(player_name, num_disks, time_taken, moves):
    conn = sqlite3.connect('hanoi.db')
    c = conn.cursor()

    
    c.execute("INSERT INTO games (player_name, num_disks, time_taken, moves) VALUES (?, ?, ?, ?)", 
              (player_name, num_disks, time_taken, moves))

    conn.commit()
    conn.close()

  

class TowerOfHanoiApp:  
    def __init__(self, master):  
        self.master = master  
        self.master.title("Tower of Hanoi")  
        self.master.geometry("800x600")  
        self.master.configure(bg="#e0f7fa")   
        create_database()  
        self.start_game()  

    def start_game(self):  
        self.player_name = simpledialog.askstring("Player Name", "Enter your name:")  
        if not self.player_name:  
            messagebox.showerror("Error", "Player name is required!")  
            self.master.destroy()  
            return  

        num_disks = simpledialog.askinteger("Number of Disks", "Enter the number of disks (1-10):", minvalue=1, maxvalue=10)  
        if num_disks is None:  
            messagebox.showerror("Error", "Number of disks is required!")  
            self.master.destroy()  
            return  

        self.num_disks = num_disks  
        self.moves = 0  
        self.start_time = time.time()  

        self.pegs = {'A': [], 'B': [], 'C': []}  
        for i in range(self.num_disks, 0, -1):  
            self.pegs['A'].append(i)  

        self.create_widgets()  

    def create_widgets(self):  
        # Title  
        title_label = ttk.Label(self.master, text="Tower of Hanoi", font=("Arial", 24, "bold"), background="#e0f7fa")  
        title_label.pack(pady=20)  

        # Pegs  
        self.peg_frames = []  
        peg_colors = ['#ffcc80', '#80deea', '#ffab91']  # Light orange, cyan, and coral colors for the pegs  
        for peg, color in zip(['A', 'B', 'C'], peg_colors):  
            peg_frame = ttk.Frame(self.master, width=200, height=400, relief=tk.RAISED, borderwidth=2, style='Peg.TFrame')  
            peg_frame.pack(side=tk.LEFT, padx=20, pady=20)  
            self.peg_frames.append(peg_frame)  
            peg_label = ttk.Label(peg_frame, text=peg, font=("Arial", 16, "bold"), background=color)  
            peg_label.pack(side=tk.TOP)  

        # Disks  
        self.disk_labels = {}  
   
        for i in range(self.num_disks):  
            disk_size = i + 1  
            disk_label = ttk.Label(self.peg_frames[0], text=str(disk_size), font=("Arial", 16, "bold"),  
                                   background=f"#{i+1:02x}{i+1:02x}{i+1:02x}",   
                                   foreground="white", padding=5)  
            disk_label.place(x=50 - i * 10, y=350 - i * 30)  
            disk_label.bind("<Button-1>", self.start_drag)  
            disk_label.bind("<B1-Motion>", self.on_drag)  
            disk_label.bind("<ButtonRelease-1>", self.stop_drag)  
            self.disk_labels[disk_size] = disk_label  

        self.drag_data = {"disk": None, "start_peg": None}  

    def start_drag(self, event):  
        widget = event.widget  
        self.drag_data["disk"] = widget  
        for peg, disks in self.pegs.items():  
            if int(widget["text"]) in disks:  
                self.drag_data["start_peg"] = peg  
                break  

    def on_drag(self, event):  
        x = event.x_root - self.master.winfo_rootx() - event.widget.winfo_width() // 2  
        y = event.y_root - self.master.winfo_rooty() - event.widget.winfo_height() // 2  
        event.widget.place(x=x, y=y)  

    def stop_drag(self, event):  
        x, y = event.widget.winfo_x(), event.widget.winfo_y()  
        peg_index = self.get_target_peg(x, y)  

        if peg_index is not None:  
            target_peg = ["A", "B", "C"][peg_index]  
            self.move_disk(self.drag_data["start_peg"], target_peg, int(event.widget["text"]))  

        # Reset disk position if drag is cancelled  
        self.drag_data["disk"].place(x=50 - len(self.pegs[self.drag_data["start_peg"]]) * 10,  
                                     y=350 - len(self.pegs[self.drag_data["start_peg"]]) * 30,  
                                     in_=self.peg_frames[["A", "B", "C"].index(self.drag_data["start_peg"])])  
        self.drag_data = {"disk": None, "start_peg": None}  

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

    def update_disk_positions(self):  
        for peg, disks in self.pegs.items():  
            peg_index = ["A", "B", "C"].index(peg)  
            for i, disk in enumerate(disks):  
                disk_label = self.disk_labels[disk]  
                disk_label.place(x=50 - i * 10, y=350 - i * 30, in_=self.peg_frames[peg_index])  

    def check_win(self):  
        if len(self.pegs['C']) == self.num_disks:  # Check if all disks are on peg 'C'  
            end_time = time.time()  
            time_taken = end_time - self.start_time  
            save_game_data(self.player_name, self.num_disks, self.moves, time_taken)  
            messagebox.showinfo("Game Over", f"Congratulations, {self.player_name}! You completed the game in {time_taken:.2f} seconds.")  
            self.master.destroy()  

def isValidMove(startTower, targetTower, diskSize):
    return 
    (
        towers[targetTower].length == 0 or
        towers[targetTower][towers[targetTower].length - 1].dataset.size > diskSize
    );

if __name__ == "__main__":  
    root = tk.Tk()  
    app = TowerOfHanoiApp(root)  
    root.mainloop() 
