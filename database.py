import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

def create_database():
    conn = sqlite3.connect('hanoi.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS games (
                  id INTEGER PRIMARY KEY,
                  player_name TEXT,
                  num_disks INTEGER,
                  moves INTEGER,
                  time_taken REAL)''')
    conn.commit()
    conn.close()

def save_game_data(player_name, num_disks, moves, time_taken):
    conn = sqlite3.connect('hanoi.db')
    c = conn.cursor()
    c.execute("INSERT INTO games (player_name, num_disks, moves, time_taken) VALUES (?, ?, ?, ?)",
              (player_name, num_disks, moves, time_taken))
    conn.commit()
    conn.close()

@app.route('/save_game', methods=['POST'])
def save_game():
    data = request.get_json()
    player_name = data['player_name']
    num_disks = data['num_disks']
    moves = data['moves']
    time_taken = data['time_taken']
    save_game_data(player_name, num_disks, moves, time_taken)
    return jsonify({"status": "success"})

create_database()

if __name__ == '__main__':
    app.run(debug=True)