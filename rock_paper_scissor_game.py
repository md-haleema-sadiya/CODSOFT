# Rock • Paper • Scissors Game
# A fun terminal-based game where you play against the computer.

import random   # For computer's random choice
import os       # For clearing the terminal screen
import time     # For adding dramatic pauses
 
 
#  CONSTANTS  (things that never change)
 
CHOICES = ["rock", "paper", "scissors"]
 
ICONS = {
    "rock":     "🪨",
    "paper":    "📄",
    "scissors": "✂️ ",
}
 
 # Defines which choice beats which — key for determining the winner

BEATS = {
    "rock":     "scissors",
    "scissors": "paper",
    "paper":    "rock",
}
 
 
#  HELPER FUNCTIONS
 
def clear_screen():
    """Wipes the terminal so each round looks fresh."""
    os.system("cls" if os.name == "nt" else "clear")
 
 
def print_banner():
    """Prints the game title banner."""
    print("\n" + "═" * 54)
    print("   🎮  ROCK • PAPER • SCISSORS  — GAME")
    print("═" * 54)
 
 
def print_scoreboard(player_score: int, computer_score: int, ties: int, round_num: int):
    """Displays the current score in a neat table."""
    print(f"\n  📊  SCOREBOARD  (after {round_num} round(s))")
    print(f"  │  You            │  {player_score:<4}")
    print(f"  │  Computer       │  {computer_score:<4}")
    print(f"  │  Ties           │  {ties:<4}")
 
 
def get_player_choice() -> str:
    """
    Asks the player to pick rock, paper, or scissors.
    Keeps asking until a valid answer is given.
    Returns the choice as a lowercase string.
    """
    print("\n  Choose your weapon:")
    for i, choice in enumerate(CHOICES, start=1):
        print(f"    [{i}]  {ICONS[choice]}  {choice.capitalize()}")
 
    while True:
        user_input = input("\n  ➤  Enter 1, 2, or 3  (or 'q' to quit): ").strip().lower()
 
        if user_input == "q":
            return "quit"
 
        if user_input in ("1", "2", "3"):
            return CHOICES[int(user_input) - 1]   # Convert number → word
 
        print("  ⚠️   Invalid input — please type 1, 2, or 3.")
 
 
def get_computer_choice() -> str:
    """Randomly picks rock, paper, or scissors for the computer."""
    return random.choice(CHOICES)
 
 
def determine_winner(player: str, computer: str) -> str:
    """
    Compares choices and returns:
      'player'   → player wins
      'computer' → computer wins
      'tie'      → it's a draw
    """
    if player == computer:
        return "tie"
    elif BEATS[player] == computer:   # If player's choice beats computer's choice
        return "player"
    else:
        return "computer"
 
 
def display_round_result(player: str, computer: str, winner: str):
    """Shows what both sides picked and who won the round."""
    print("\n" + "─" * 54)
    print(f"  You chose   ▶  {ICONS[player]}  {player.capitalize()}")
 
    # Suspenseful pause before revealing computer choice
    print("  Computer is choosing", end="", flush=True)
    for _ in range(3):
        time.sleep(0.4)
        print(".", end="", flush=True)
    print(f"  {ICONS[computer]}  {computer.capitalize()}")
 
    print("─" * 54)
 
    if winner == "tie":
        print("  🤝  It's a TIE!  Great minds think alike.")
    elif winner == "player":
        print(f"  🎉  YOU WIN!  ({player.capitalize()} beats {computer}.)")
    else:
        print(f"  💻  COMPUTER WINS!  ({computer.capitalize()} beats {player}.)")
 
    print("─" * 54)
 
 
def ask_play_again() -> bool:
    """Asks if the player wants another round. Returns True/False."""
    while True:
        answer = input("\n  🔄  Play another round? (yes (y) / no (n)): ").strip().lower()
        if answer in ("yes", "y"):
            return True
        if answer in ("no", "n"):
            return False
        print("  ⚠️   Please type  yes  or  no.")
 
 
def print_final_summary(player_score: int, computer_score: int, ties: int):
    """Shows the final game summary when the player decides to quit."""
    total = player_score + computer_score + ties
    print("\n" + "═" * 54)
    print("  🏁  GAME OVER — Final Results")
    print("═" * 54)
    print(f"  Total rounds played : {total}")
    print(f"  Your wins           : {player_score}")
    print(f"  Computer wins       : {computer_score}")
    print(f"  Ties                : {ties}")
 
    if total > 0:
        win_rate = (player_score / total) * 100
        print(f"  Your win rate       : {win_rate:.1f}%")
 
    print()
    if player_score > computer_score:
        print("  🏆  YOU ARE THE CHAMPION!  Well played!")
    elif computer_score > player_score:
        print("  🤖  The computer wins this time. Come back stronger!")
    else:
        print("  🤝  It's an overall tie — perfectly balanced!")
 
    print("═" * 54)
    print("  Thanks for playing!  See you next time. 👋\n")
 
 
#  MAIN GAME LOOP
 
def main():
    """Entry point — runs the entire game."""
    clear_screen()
    print_banner()
    print("\n  Welcome!  Beat the computer in Rock • Paper • Scissors.")
 
    # Score counters — start at zero
    player_score   = 0
    computer_score = 0
    ties           = 0
    round_number   = 0
 
    # ── Main loop ──────────────────────────────
    while True:
        round_number += 1
        print(f"\n  ⚡  ROUND {round_number}")
 
        # 1. Get player's choice
        player_choice = get_player_choice()
 
        if player_choice == "quit":
            break   # Exit the loop early if user types 'q'
 
        # 2. Get computer's random choice
        computer_choice = get_computer_choice()
 
        # 3. Decide who won
        result = determine_winner(player_choice, computer_choice)
 
        # 4. Update scores
        if result == "player":
            player_score += 1
        elif result == "computer":
            computer_score += 1
        else:
            ties += 1
 
        # 5. Show round result
        display_round_result(player_choice, computer_choice, result)
 
        # 6. Show updated scoreboard
        print_scoreboard(player_score, computer_score, ties, round_number)
 
        # 7. Ask to play again
        if not ask_play_again():
            break   # Exit loop if player says no
 
    # ── Game over ──────────────────────────────
    print_final_summary(player_score, computer_score, ties)
 
 
#  RUN THE GAME
 
if __name__ == "__main__":
    main()