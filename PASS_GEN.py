#  PASS_GEN.py
#  A simple yet powerful password generator.
#  Create strong, random passwords with customizable options.

import random      # For random character selection
import string      # Provides ready-made character sets
import os          # For clearing the screen


#  CHARACTER POOLS  (building blocks of passwords)

UPPERCASE   = string.ascii_uppercase   # A-Z
LOWERCASE   = string.ascii_lowercase   # a-z
DIGITS      = string.digits            # 0-9
SYMBOLS     = "!@#$%^&*()_+-=[]{}|;:,.<>?"

# Combine everything for a "full strength" pool
ALL_CHARS   = UPPERCASE + LOWERCASE + DIGITS + SYMBOLS


#  HELPER FUNCTIONS

def clear_screen():
    """Wipes the terminal for a clean look."""
    os.system("cls" if os.name == "nt" else "clear")


def print_banner():
    """Prints the app title banner."""
    print("\n" + "═" * 56)
    print("   🔐  PASSWORD GENERATOR  —  Stay Safe, Stay Strong")
    print("═" * 56)


def get_password_length() -> int:
    """
    Asks the user for a password length between 6 and 128.
    Keeps asking until a valid number is entered.
    Returns an integer.
    """
    print("\n  📏  How long should your password be?")
    print("      (Recommended: 12–20 characters)")

    while True:
        user_input = input("\n  ➤  Enter length (6 – 128): ").strip()

        # Make sure it's actually a number
        if not user_input.isdigit():
            print("  ⚠️   Please enter a whole number (e.g. 16).")
            continue

        length = int(user_input)

        if length < 6:
            print("  ⚠️   Too short! Minimum is 6 characters.")
        elif length > 128:
            print("  ⚠️   Too long! Maximum is 128 characters.")
        else:
            return length   # Valid — return it


def get_complexity_choice() -> dict:
    """
    Lets the user choose which character types to include.
    Returns a dictionary of booleans, e.g.:
      { 'uppercase': True, 'lowercase': True, 'digits': True, 'symbols': False }
    """
    print("\n  🛠️   Customize your password (press Enter to include, 'n' to skip):")

    options = {
        "uppercase": ("A – Z  (Uppercase letters)", True),
        "lowercase": ("a – z  (Lowercase letters)", True),
        "digits":    ("0 – 9  (Numbers)",            True),
        "symbols":   ("!@#$%  (Special symbols)",    True),
    }

    choices = {}
    for key, (label, _) in options.items():
        answer = input(f"    Include  {label}?  [Y/n]: ").strip().lower()
        choices[key] = (answer != "n")   # Include unless user types 'n'

    # Make sure at least one type is selected
    if not any(choices.values()):
        print("  ⚠️   You must include at least one character type.")
        print("        Defaulting to all character types.")
        choices = {k: True for k in choices}

    return choices


def build_character_pool(choices: dict) -> str:
    """
    Builds the pool of characters to pick from,
    based on what the user chose.
    Returns a single string of all allowed characters.
    """
    pool = ""
    if choices["uppercase"]: pool += UPPERCASE
    if choices["lowercase"]: pool += LOWERCASE
    if choices["digits"]:    pool += DIGITS
    if choices["symbols"]:   pool += SYMBOLS
    return pool


def generate_password(length: int, pool: str, choices: dict) -> str:
    """
    Generates a truly random password of the given length.

    SMART TRICK: Guarantees at least one character from each
    selected type — so the password always passes complexity rules.
    """

    # Step 1: Pick at least one character from each selected type
    guaranteed = []
    if choices["uppercase"]: guaranteed.append(random.choice(UPPERCASE))
    if choices["lowercase"]: guaranteed.append(random.choice(LOWERCASE))
    if choices["digits"]:    guaranteed.append(random.choice(DIGITS))
    if choices["symbols"]:   guaranteed.append(random.choice(SYMBOLS))

    # Step 2: Fill the rest randomly from the full pool
    remaining_length = length - len(guaranteed)
    rest = [random.choice(pool) for _ in range(remaining_length)]

    # Step 3: Shuffle everything so guaranteed chars aren't always at the front
    all_chars = guaranteed + rest
    random.shuffle(all_chars)

    return "".join(all_chars)   # Convert list → string


def calculate_strength(length: int, choices: dict) -> tuple:
    """
    Calculates a password strength score (0–100) and label.
    Returns (score, label, bar_string).

    Scoring:
      - Length contributes up to 60 points
      - Each character type adds 10 points (max 40)
    """
    # Points for length
    if   length >= 20: length_score = 60
    elif length >= 16: length_score = 50
    elif length >= 12: length_score = 40
    elif length >= 8:  length_score = 25
    else:              length_score = 10

    # Points for character variety
    variety_score = sum(10 for v in choices.values() if v)

    total = length_score + variety_score   # Max = 100

    # Label
    if   total >= 90: label, color = "EXCELLENT 🟢", "🟢"
    elif total >= 70: label, color = "STRONG    🟡", "🟡"
    elif total >= 50: label, color = "MODERATE  🟠", "🟠"
    else:             label, color = "WEAK      🔴", "🔴"

    # Visual bar (20 segments)
    filled = round((total / 100) * 20)
    bar = "█" * filled + "░" * (20 - filled)

    return total, label, bar


def display_password(password: str, length: int, choices: dict):
    """Displays the generated password with strength info."""
    score, label, bar = calculate_strength(length, choices)

    print("\n" + "─" * 56)
    print("  ✅  YOUR PASSWORD IS READY!\n")
    print(f"  🔑  {password}")
    print("\n" + "─" * 56)
    print(f"  📊  Strength : {label}")
    print(f"  📈  Score    : {score}/100")
    print(f"  [{bar}]")
    print("─" * 56)

    # Handy tips based on score
    if score < 50:
        print("  💡  Tip: Use 12+ characters with symbols for better security.")
    elif score < 80:
        print("  💡  Tip: Add symbols or increase length to make it stronger.")
    else:
        print("  💡  Tip: Store this in a password manager to remember it safely.")


def display_history(history: list):
    """Prints all passwords generated in this session."""
    if not history:
        print("  ℹ️   No passwords generated yet.")
        return

    print("\n  📋  PASSWORD HISTORY (this session)")
    print("  " + "─" * 46)
    for i, (pwd, length, score) in enumerate(history, start=1):
        print(f"  {i:>2}.  {pwd:<30}  len={length}  score={score}")
    print("  " + "─" * 46)


def ask_what_next() -> str:
    """
    Asks user what they want to do next.
    Returns: 'new', 'history', or 'quit'
    """
    print("\n  What would you like to do?")
    print("    [1]  Generate another password")
    print("    [2]  View password history")
    print("    [3]  Quit")

    while True:
        choice = input("\n  ➤  Enter 1, 2, or 3: ").strip()
        if choice == "1": return "new"
        if choice == "2": return "history"
        if choice == "3": return "quit"
        print("  ⚠️   Please enter 1, 2, or 3.")


def print_goodbye(total_generated: int):
    """Prints a closing message."""
    print("\n" + "═" * 56)
    print(f"  🔒  Session complete!  Passwords generated: {total_generated}")
    print("  Stay secure — never reuse passwords. 👋")
    print("═" * 56 + "\n")


#  MAIN PROGRAM

def main():
    """Entry point — runs the password generator."""
    clear_screen()
    print_banner()
    print("\n  Welcome!  Let's create strong, random passwords for you.")

    history = []   # Stores (password, length, score) for this session

    while True:
        # ── Step 1: Get length ──────────────────
        length = get_password_length()

        # ── Step 2: Get complexity ──────────────
        choices = get_complexity_choice()

        # ── Step 3: Build pool & generate ───────
        pool     = build_character_pool(choices)

        print("\n  ⚙️   Generating password...")

        password = generate_password(length, pool, choices)
        score, _, _ = calculate_strength(length, choices)

        # ── Step 4: Display result ───────────────
        display_password(password, length, choices)

        # ── Step 5: Save to history ──────────────
        history.append((password, length, score))

        # ── Step 6: What next? ───────────────────
        while True:
            action = ask_what_next()
            if action == "history":
                display_history(history)
            else:
                break   # 'new' or 'quit' — exit inner loop

        if action == "quit":
            break   # Exit main loop

    print_goodbye(len(history))


#  RUN THE PROGRAM

if __name__ == "__main__":
    main()