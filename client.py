import requests  

def save_game_data():  
    data = {  
        "player_name": "Your Name",  
        "num_disks": 4,  
        "moves": 10,  
        "time_taken": 30.5  
    }  

    response = requests.post('http://127.0.0.1:5000/save_game', json=data)  

    if response.status_code == 200:  
        print("Game data saved successfully:", response.json())  
    else:  
        print("Failed to save game data:", response.status_code, response.text)  

if __name__ == '__main__':  
    save_game_data()