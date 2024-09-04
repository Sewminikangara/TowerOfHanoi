import time
from database import save_game_data

def hanoi(n, source, target, auxiliary):
    if n == 1:
        print(f"Move disk 1 from rod {source} to rod {target}")
        return [(source, target)]
    moves = hanoi(n - 1, source, auxiliary, target)
    moves.append((source, target))
    print(f"Move disk {n} from rod {source} to rod {target}")
    moves += hanoi(n - 1, auxiliary, target, source)
    return moves

def get_user_moves(n):
    moves = []
    print(f"Enter your {n} moves as pairs of rods (e.g., A B):")
    for i in range(n):
        move = input(f"Move {i+1}: ").split()
        moves.append((move[0], move[1]))
    return moves

def main():
    player_name = input("Enter your name: ")
    n = int(input("Enter the number of disks: "))
    
    start_time = time.time()
    
    correct_moves = hanoi(n, 'A', 'C', 'B')
    user_moves = get_user_moves(len(correct_moves))
    
    end_time = time.time()
    time_taken = end_time - start_time
    
    if correct_moves == user_moves:
        print("Congratulations! You've solved the Tower of Hanoi.")
        save_game_data(player_name, n, time_taken)
    else:
        print("Incorrect solution. Try again.")

if __name__ == "__main__":
    main()
