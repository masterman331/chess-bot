# Chess Automation Bot (Stockfish + Selenium)  
**⚠️ ETHICAL USE ONLY ⚠️**  
This bot is for educational purposes and testing **only**. Do not use it to violate terms of service or cheat in competitive play.  

---

## Table of Contents  
1. [Overview](#overview)  
2. [Features](#features)  
3. [Prerequisites](#prerequisites)  
4. [Installation](#installation)  
5. [Usage](#usage)  
6. [Configuration](#configuration)  
7. [Troubleshooting](#troubleshooting)  
8. [Legal Compliance](#legal-compliance)  

---

## Overview  
This bot automates chess moves on Chess.com using the **Stockfish engine** for analysis and **Selenium/PyAutoGUI** for browser interaction. It is designed for learning AI-driven gameplay strategies and should **not** be used in real competitions.  

---

## Features  
- **Stockfish Analysis**: Calculates optimal moves with depth control.  
- **Browser Automation**: Navigates Chess.com and interacts with the board.  
- **Mouse Control**: Simulates clicks/drag-and-drop for piece movement.  
- **Error Handling**: Detects game over states and opponent moves.  
- **Calibration**: Adjusts screen coordinates for accurate interactions.  

---

## Prerequisites  
1. **Python 3.8+**: [Download Python](https://www.python.org/downloads/)  
2. **Dependencies**:  
   ```bash  
   pip install selenium pyautogui pygetwindow opencv-python  
   ```  
3. **Stockfish Engine**:  
   - Download from [Stockfish Official](https://stockfishchess.org/download/).  
   - Example path: `C:\stockfish\stockfish.exe` (update in `STOCKFISH_PATH`).  
4. **ChromeDriver**:  
   - Download [here](https://sites.google.com/chromium.org/driver/).  

---

## Installation  
1. **Clone Repository**:  
   ```bash  
   git clone https://github.com/masterman331/chess-bot
   cd chess-bot  
   ```  
2. **Set Stockfish Path**:  
   Open `main.py` and update:  
   ```python  
   STOCKFISH_PATH = r"YOUR_STOCKFISH_PATH"  # e.g., r"C:\stockfish\stockfish.exe"  
   ```  
3. **Configure ChromeDriver**:  
   Add to `PATH` or specify in `main.py`:  
   ```python  
   service = Service(executable_path="path/to/chromedriver.exe")  
   ```  

---

## Usage  
1. **Start a New Game**:  
   Open Chess.com and navigate to `https://www.chess.com/play/computer`.  
2. **Run the Bot**:  
   ```bash  
   python main.py  
   ```  
3. **Calibration**:  
   - The bot will prompt you to click squares `e2` and `e4`.  
   - Adjust `VERTICAL_OFFSET` in `main.py` if clicks are misaligned.  
4. **Monitor**:  
   Watch the terminal for move suggestions and game status.  

---

## Configuration  
### Key Settings  
- **Stockfish Path**:  
  ```python  
  STOCKFISH_PATH = r"YOUR_STOCKFISH_PATH"  
  ```  
- **Vertical Offset**:  
  ```python  
  VERTICAL_OFFSET = 120  # Adjust for screen positioning (negative values move up)  
  ```  
- **Analysis Depth**:  
  Modify `depth=15` in `get_best_move()` for accuracy vs. speed tradeoff.  

---

## Troubleshooting  
- **PyAutoGUI Errors**:  
  - Ensure Chrome is visible and not minimized.  
  - Disable screen scaling or adjust offsets.  
- **Stockfish Not Responding**:  
  - Verify `STOCKFISH_PATH` is correct.  
  - Increase `time_limit` in `get_best_move()`.  
- **Browser Popups**:  
  Manually close ads or notifications during execution.  

---

## Legal Compliance  
- **Chess.com Terms of Service**:  
  This bot must **not** be used in rated games, tournaments, or against human players.  
- **Ethical Use**:  
  This project is for testing automation logic and AI strategies. Misuse may result in account suspension.  

> **Disclaimer:**  
> This project has been vibe-coded please use it cautiously. - masterman331
