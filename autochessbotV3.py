#This was made by masterman331
import time
import subprocess
import re
import pyautogui
import pygetwindow as gw
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Path to Stockfish executable - modify this to your actual path
STOCKFISH_PATH = r"C:\path\to\stockfish.exe"

# Vertical offset correction (adjust if needed)
VERTICAL_OFFSET = 120  # Negative means move up

def get_chess_board(driver):
    """
    Extract the current chess board state from chess.com
    Returns a 2D array representing the board, the FEN string, and board screen location info.
    """
    # Wait for the board to load
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "wc-chess-board")))
    
    # Get the chess board element
    chess_board = driver.find_element(By.TAG_NAME, "wc-chess-board")
    
    # Initialize empty board
    board = [[' ' for _ in range(8)] for _ in range(8)]
    
    # Get the board position and size
    board_rect = chess_board.rect
    
    # Get browser window position to calculate absolute coordinates
    chrome_window = find_chrome_window()
    if not chrome_window:
        print("Warning: Could not find Chrome window. Coordinates may be incorrect.")
        window_x, window_y = 0, 0
    else:
        window_x, window_y = chrome_window.left, chrome_window.top
    
    # Adjust for browser window position and apply vertical offset
    board_location = {
        'x': window_x + board_rect['x'],
        'y': window_y + board_rect['y'] + VERTICAL_OFFSET,  # Apply vertical offset
        'width': board_rect['width'],
        'height': board_rect['height']
    }
    
    # Try to get FEN from the board's data attribute
    try:
        board_position = chess_board.get_attribute("data-position")
        if board_position:
            # If we can get the position directly, use it
            fen = board_position.split(" ")[0]  # Just get the piece placement part
            
            # Fill our visual board for display
            for rank_idx, rank in enumerate(fen.split("/")):
                file_idx = 0
                for char in rank:
                    if char.isdigit():
                        file_idx += int(char)
                    else:
                        piece_map = {
                            'P': '♙', 'R': '♖', 'N': '♘', 'B': '♗', 'Q': '♕', 'K': '♔',
                            'p': '♟', 'r': '♜', 'n': '♞', 'b': '♝', 'q': '♛', 'k': '♚'
                        }
                        board[rank_idx][file_idx] = piece_map.get(char, '?')
                        file_idx += 1
            
            # For now, assume it's white's turn (we'll refine this later)
            complete_fen = fen + " w KQkq - 0 1"
            return board, complete_fen, board_location
    except Exception as e:
        print(f"Error extracting FEN: {e}")
    
    # If we couldn't get the FEN directly, try analyzing the board based on piece elements
    try:
        pieces = driver.find_elements(By.CSS_SELECTOR, ".piece")
        
        # Map piece class to symbol and FEN character
        piece_symbols = {
            'wp': ('♙', 'P'), 'wr': ('♖', 'R'), 'wn': ('♘', 'N'), 'wb': ('♗', 'B'), 'wq': ('♕', 'Q'), 'wk': ('♔', 'K'),
            'bp': ('♟', 'p'), 'br': ('♜', 'r'), 'bn': ('♞', 'n'), 'bb': ('♝', 'b'), 'bq': ('♛', 'q'), 'bk': ('♚', 'k')
        }
        
        # Fill the board with pieces
        fen_board = [[''] * 8 for _ in range(8)]
        
        for piece in pieces:
            classes = piece.get_attribute("class").split()
            
            # Find piece type
            piece_type = None
            for cls in classes:
                if cls in piece_symbols:
                    piece_type = cls
                    break
            
            # Find square position
            square = None
            for cls in classes:
                if cls.startswith("square-"):
                    square = cls[7:]  # Remove "square-" prefix
                    break
            
            if piece_type and square and len(square) == 2:
                file_idx = int(square[0]) - 1  # Convert from 1-8 to 0-7
                rank_idx = 8 - int(square[1])  # Convert from 1-8 to 0-7 (inverted)
                
                if 0 <= file_idx < 8 and 0 <= rank_idx < 8:
                    board[rank_idx][file_idx] = piece_symbols.get(piece_type, ('?', '?'))[0]
                    fen_board[rank_idx][file_idx] = piece_symbols.get(piece_type, ('?', '?'))[1]
        
        # Generate FEN string
        fen_rows = []
        for rank in fen_board:
            empty_count = 0
            row = ""
            for square in rank:
                if square:
                    if empty_count > 0:
                        row += str(empty_count)
                        empty_count = 0
                    row += square
                else:
                    empty_count += 1
            if empty_count > 0:
                row += str(empty_count)
            fen_rows.append(row)
        
        fen = "/".join(fen_rows)
        complete_fen = fen + " w KQkq - 0 1"  # Assume white's turn
        
        return board, complete_fen, board_location
    except Exception as e:
        print(f"Error analyzing pieces: {e}")
    
    # If all else fails, return default starting position
    print("Couldn't extract board state. Using default starting position.")
    default_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    return board, default_fen, board_location

def find_chrome_window():
    """
    Find the Chrome window containing chess.com
    """
    chrome_windows = gw.getWindowsWithTitle('Chrome')
    for window in chrome_windows:
        if 'chess.com' in window.title.lower():
            return window
    # If no specific window found, get any Chrome window
    if chrome_windows:
        return chrome_windows[0]
    return None

def focus_chrome_window():
    """
    Find and focus the Chrome window
    """
    window = find_chrome_window()
    if window:
        window.activate()
        time.sleep(0.5)  # Give time for window to come to front
        return True
    return False

def print_chess_board(board):
    """
    Print the chess board in the terminal.
    """
    print("  +---+---+---+---+---+---+---+---+")
    for i, row in enumerate(board):
        print(f"{8-i} | {' | '.join(row)} |")
        print("  +---+---+---+---+---+---+---+---+")
    print("    a   b   c   d   e   f   g   h  ")

def get_best_move(fen, depth=15, time_limit=3000):
    """
    Get the best move from Stockfish for the given FEN position.
    """
    # Start Stockfish process
    stockfish = subprocess.Popen(
        STOCKFISH_PATH,
        universal_newlines=True,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Configure Stockfish
    commands = [
        "uci",
        "setoption name Threads value 4",
        "setoption name Hash value 128",
        f"position fen {fen}",
        f"go depth {depth} movetime {time_limit}"
    ]
    
    for cmd in commands:
        stockfish.stdin.write(cmd + "\n")
        stockfish.stdin.flush()
    
    # Parse output to find best move
    best_move = None
    while True:
        line = stockfish.stdout.readline().strip()
        if line.startswith("bestmove"):
            best_move = line.split()[1]
            break
    
    # Close Stockfish
    stockfish.terminate()
    
    return best_move

def calculate_square_position(board_location, square):
    """
    Calculate the screen position of a chess square.
    The square format is like 'e2' (file + rank).
    """
    file_to_index = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
    file_idx = file_to_index[square[0].lower()]
    rank_idx = 8 - int(square[1])
    square_width = board_location['width'] / 8
    square_height = board_location['height'] / 8
    x = board_location['x'] + (file_idx * square_width) + (square_width / 2)
    y = board_location['y'] + (rank_idx * square_height) + (square_height / 2)
    return int(x), int(y)

def make_move_with_mouse(board_location, move):
    """
    Make a move using pyautogui to control the mouse.
    The move format is like 'e2e4'.
    """
    # Focus the browser window
    focus_chrome_window()
    
    # Convert chess notation to screen coordinates
    from_square = move[0:2]
    to_square = move[2:4]
    from_x, from_y = calculate_square_position(board_location, from_square)
    to_x, to_y = calculate_square_position(board_location, to_square)
    
    print(f"Moving from coordinates ({from_x}, {from_y}) to ({to_x}, {to_y})")
    
    pyautogui.moveTo(from_x, from_y, duration=0.3)
    time.sleep(0.2)
    pyautogui.mouseDown()
    time.sleep(0.2)
    pyautogui.moveTo(to_x, to_y, duration=0.5)
    time.sleep(0.2)
    pyautogui.mouseUp()
    time.sleep(1)

def wait_for_board_change(driver, current_fen):
    """
    Wait for the board to change, indicating opponent has moved.
    If a timeout occurs, prompt the user whether to continue waiting or break.
    """
    print("Waiting for opponent's move...")
    max_attempts = 60  # Maximum number of checks (60 * 2 seconds = 2 minutes max)
    attempts = 0
    while attempts < max_attempts:
        try:
            new_board, new_fen, _ = get_chess_board(driver)
            if new_fen != current_fen:
                print("Opponent has moved!")
                return new_board, new_fen
        except Exception as e:
            print(f"Error checking for opponent move: {e}")
        time.sleep(2)
        attempts += 1

    # If timeout occurred, ask the user what to do
    choice = input("No opponent move detected after waiting a fuckin' long time. Continue waiting? (y/n): ")
    if choice.lower() == 'y':
        return wait_for_board_change(driver, current_fen)
    else:
        raise TimeoutError("Opponent did not move within the time limit. Exiting move wait.")

def check_game_over(driver):
    """Check if the game is over."""
    try:
        game_over_modal = driver.find_elements(By.CSS_SELECTOR, ".modal-game-over-buttons-component")
        if game_over_modal:
            return True
        result_texts = driver.find_elements(By.CSS_SELECTOR, ".result-text")
        for text in result_texts:
            if "checkmate" in text.text.lower() or "stalemate" in text.text.lower():
                return True
    except Exception as e:
        print(f"Error checking game over: {e}")
    return False

def test_square_click(driver, board_location):
    """
    Test the board position calibration by clicking on e2 and e4.
    """
    print("Testing board position calibration...")
    focus_chrome_window()
    e2_x, e2_y = calculate_square_position(board_location, 'e2')
    print(f"Clicking on e2: ({e2_x}, {e2_y})")
    pyautogui.click(e2_x, e2_y)
    time.sleep(1)
    e4_x, e4_y = calculate_square_position(board_location, 'e4')
    print(f"Clicking on e4: ({e4_x}, {e4_y})")
    pyautogui.click(e4_x, e4_y)
    time.sleep(1)
    print("Calibration test complete. Was the e2 pawn selected and e4 highlighted?")
    adjust = input("Do you need to adjust the vertical offset? (y/n): ")
    if adjust.lower() == 'y':
        try:
            offset = int(input("Enter vertical offset (negative = up, positive = down): "))
            return offset
        except ValueError:
            print("Invalid offset value. Using default.")
    return 0

def setup_game(driver):
    """
    Navigate to chess.com and set up a new game with a computer opponent.
    """
    print("Navigating to chess.com/play/computer...")
    driver.get("https://www.chess.com/play/computer")
    time.sleep(5)
    try:
        popups = driver.find_elements(By.CSS_SELECTOR, ".modal-close-button, .close-button")
        for popup in popups:
            popup.click()
            time.sleep(1)
    except Exception as e:
        print(f"Error closing popups: {e}")
    time.sleep(3)
    print("Game is ready to start")

def run_game(driver):
    """
    Run a single game loop.
    """
    global VERTICAL_OFFSET
    # Allow some time for the user to set difficulty or adjust settings on chess.com
    print("\n===== Chess.com Bot Automation with Stockfish =====")
    print("Please ensure the chess board is fully visible.")
    print("Set your difficulty level on chess.com now.")
    
    board, fen, board_location = get_chess_board(driver)
    
    print("\n===== Board Position Calibration =====")
    offset_adjustment = test_square_click(driver, board_location)
    if offset_adjustment != 0:
        VERTICAL_OFFSET += offset_adjustment
        print(f"Vertical offset adjusted to: {VERTICAL_OFFSET}")
        board_location['y'] = board_location['y'] - offset_adjustment
    
    print("\nInitial Chess Board:\n")
    print_chess_board(board)
    
    confirm = input("\nEverything configured? Ready to start playing? (y/n): ")
    if confirm.lower() != 'y':
        print("Exiting game loop.")
        return
    
    move_counter = 1
    while not check_game_over(driver):
        print(f"\nMove {move_counter}:")
        print("Getting best move from Stockfish...")
        try:
            best_move = get_best_move(fen)
            print(f"Stockfish recommends: {best_move}")
        except Exception as e:
            print(f"Error getting best move: {e}")
            break
        
        print(f"Making move {best_move}...")
        try:
            make_move_with_mouse(board_location, best_move)
        except Exception as e:
            print(f"Error making move with mouse: {e}")
            break

        board, fen, board_location = get_chess_board(driver)
        print("\nBoard after our move:\n")
        print_chess_board(board)
        
        if check_game_over(driver):
            print("Game over!")
            break
        
        try:
            board, fen = wait_for_board_change(driver, fen)
            # Refresh board location after opponent move
            _, _, board_location = get_chess_board(driver)
            print("\nBoard after opponent's move:\n")
            print_chess_board(board)
        except TimeoutError as te:
            print(te)
            break
        
        move_counter += 1
    print("Game completed!")

def main():
    """
    Main function to manage sessions so you can run the bot multiple times without restarting the program.
    """
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1200x800")
    
    driver = webdriver.Chrome(options=chrome_options)
    try:
        while True:
            setup_game(driver)
            run_game(driver)
            restart_choice = input("Do you want to play another game? (y/n): ")
            if restart_choice.lower() != 'y':
                print("Exiting bot. Fuck yeah, we did it!")
                break
            else:
                print("Restarting game...")
                driver.delete_all_cookies()  # Clean up before the next game
                time.sleep(2)
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()
    finally:
        input("Press Enter to close the browser and exit...")
        driver.quit()

if __name__ == "__main__":
    main()
