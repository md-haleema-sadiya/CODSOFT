# Contact Book App
# A simple command-line contact manager in Python.

import os       # For clearing the screen
import re       # For validating email format
 
 
#  HELPER / UI FUNCTIONS
 
def clear_screen():
    """Clears the terminal for a fresh look."""
    os.system("cls" if os.name == "nt" else "clear")
 
 
def print_banner():
    """Prints the app title."""
    print("\n" + "═" * 58)
    print("   📒  CONTACT BOOK  —  Your Personal Directory")
    print("═" * 58)
 
 
def print_menu():
    """Displays the main menu options."""
    print("\n  What would you like to do?")
    print("  ┌─────────────────────────────────────┐")
    print("  │  [1]  ➕  Add a new contact          │")
    print("  │  [2]  📋  View all contacts           │")
    print("  │  [3]  🔍  Search for a contact        │")
    print("  │  [4]  ✏️   Update a contact            │")
    print("  │  [5]  🗑️   Delete a contact            │")
    print("  │  [6]  🚪  Quit                        │")
    print("  └─────────────────────────────────────┘")
 
 
def get_menu_choice() -> str:
    """Reads the user's menu choice and validates it."""
    while True:
        choice = input("\n  ➤  Enter your choice (1–6): ").strip()
        if choice in ("1", "2", "3", "4", "5", "6"):
            return choice
        print("  ⚠️   Please enter a number between 1 and 6.")
 
 
def is_valid_phone(phone: str) -> bool:
    """
    Checks if a phone number is valid.
    Allows digits, spaces, +, -, ( )
    Must have at least 7 digits.
    """
    digits_only = re.sub(r"[\s\-\(\)\+]", "", phone)
    return digits_only.isdigit() and len(digits_only) >= 7
 
 
def is_valid_email(email: str) -> bool:
    """
    Basic email format check using regex.
    Checks for: something @ something . something
    """
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
    return re.match(pattern, email) is not None
 
 
def format_contact_card(contact: dict, index: int = None) -> str:
    """
    Returns a neatly formatted string for one contact.
    Used for both viewing and confirming actions.
    """
    prefix = f"  [{index}]  " if index is not None else "  "
    lines = [
        f"\n{prefix}👤  {contact['name']}",
        f"       📞  {contact['phone']}",
        f"       📧  {contact['email']}",
        f"       🏠  {contact['address']}",
    ]
    return "\n".join(lines)
 
 
def find_contacts(contacts: list, query: str) -> list:
    """
    Searches contacts by name or phone number.
    Case-insensitive partial match.
    Returns a list of (original_index, contact) tuples.
    """
    query = query.lower()
    results = []
    for i, c in enumerate(contacts):
        if query in c["name"].lower() or query in c["phone"]:
            results.append((i, c))
    return results
 
 
#  FEATURE FUNCTIONS
 
def add_contact(contacts: list):
    """
    Prompts the user to enter contact details,
    validates each field, then saves the new contact.
    """
    print("\n  ─── ➕ ADD NEW CONTACT ─────────────────────")
 
    # ── Name ──────────────────────────────────
    while True:
        name = input("\n  Full Name      : ").strip()
        if len(name) >= 2:
            break
        print("  ⚠️   Name must be at least 2 characters.")
 
    # Check for duplicate name
    if any(c["name"].lower() == name.lower() for c in contacts):
        print(f"  ⚠️   A contact named '{name}' already exists.")
        overwrite = input("       Continue anyway? (y/n): ").strip().lower()
        if overwrite != "y":
            print("  ℹ️   Cancelled. Returning to menu.")
            return
 
    # ── Phone ──────────────────────────────────
    while True:
        phone = input("  Phone Number   : ").strip()
        if is_valid_phone(phone):
            break
        print("  ⚠️   Invalid phone number. Must have at least 7 digits.")
 
    # ── Email ──────────────────────────────────
    while True:
        email = input("  Email Address  : ").strip()
        if not email:           # Email is optional
            email = "N/A"
            break
        if is_valid_email(email):
            break
        print("  ⚠️   Invalid email format. Try: example@mail.com  (or press Enter to skip)")
 
    # ── Address ────────────────────────────────
    address = input("  Address        : ").strip()
    if not address:
        address = "N/A"
 
    # ── Build & save ───────────────────────────
    new_contact = {
        "name":    name,
        "phone":   phone,
        "email":   email,
        "address": address,
    }
    contacts.append(new_contact)
 
    print(f"\n  ✅  Contact '{name}' added successfully!")
    print(format_contact_card(new_contact))
 
 
def view_contacts(contacts: list):
    """Displays all contacts in a numbered list."""
    print("\n  ─── 📋 ALL CONTACTS ────────────────────────")
 
    if not contacts:
        print("\n  ℹ️   Your contact book is empty.")
        print("       Use option [1] to add your first contact!")
        return
 
    total = len(contacts)
    print(f"\n  {total} contact(s) saved:\n")
    print("  " + "─" * 52)
 
    for i, contact in enumerate(contacts, start=1):
        print(f"  {i:>3}.  {contact['name']:<25}  📞 {contact['phone']}")
 
    print("  " + "─" * 52)
 
 
def search_contact(contacts: list):
    """Searches contacts by name or phone and shows full details."""
    print("\n  ─── 🔍 SEARCH CONTACT ──────────────────────")
 
    if not contacts:
        print("\n  ℹ️   No contacts to search. Add some first!")
        return
 
    query = input("\n  Search by name or phone: ").strip()
    if not query:
        print("  ⚠️   Please enter a search term.")
        return
 
    results = find_contacts(contacts, query)
 
    if not results:
        print(f"\n  ❌  No contacts found matching '{query}'.")
        return
 
    print(f"\n  ✅  Found {len(results)} result(s):\n")
    for orig_index, contact in results:
        print(format_contact_card(contact, index=orig_index + 1))
        print()
 
 
def update_contact(contacts: list):
    """
    Lets the user search for a contact, then update
    any or all of its fields (press Enter to keep existing).
    """
    print("\n  ─── ✏️  UPDATE CONTACT ─────────────────────")
 
    if not contacts:
        print("\n  ℹ️   No contacts to update.")
        return
 
    query = input("\n  Search contact to update: ").strip()
    results = find_contacts(contacts, query)
 
    if not results:
        print(f"\n  ❌  No contacts found matching '{query}'.")
        return
 
    # If multiple results, let user pick one
    if len(results) == 1:
        orig_index, contact = results[0]
    else:
        print(f"\n  Found {len(results)} matches:")
        for i, (orig_idx, c) in enumerate(results, start=1):
            print(f"    [{i}]  {c['name']}  —  {c['phone']}")
        while True:
            pick = input("\n  ➤  Which contact to update? (enter number): ").strip()
            if pick.isdigit() and 1 <= int(pick) <= len(results):
                orig_index, contact = results[int(pick) - 1]
                break
            print("  ⚠️   Invalid choice.")
 
    print("\n  Current details:")
    print(format_contact_card(contact))
    print("\n  (Press Enter to keep the existing value)\n")
 
    # ── Update each field ──────────────────────
    new_name = input(f"  New Name     [{contact['name']}]: ").strip()
    if new_name and len(new_name) >= 2:
        contact["name"] = new_name
    elif new_name:
        print("  ⚠️   Name too short — kept original.")
 
    while True:
        new_phone = input(f"  New Phone    [{contact['phone']}]: ").strip()
        if not new_phone:
            break   # Keep original
        if is_valid_phone(new_phone):
            contact["phone"] = new_phone
            break
        print("  ⚠️   Invalid phone. Try again or press Enter to skip.")
 
    while True:
        new_email = input(f"  New Email    [{contact['email']}]: ").strip()
        if not new_email:
            break   # Keep original
        if is_valid_email(new_email) or new_email == "N/A":
            contact["email"] = new_email
            break
        print("  ⚠️   Invalid email format. Try again or press Enter to skip.")
 
    new_address = input(f"  New Address  [{contact['address']}]: ").strip()
    if new_address:
        contact["address"] = new_address
 
    # Update the contact in the list
    contacts[orig_index] = contact
 
    print(f"\n  ✅  Contact updated successfully!")
    print(format_contact_card(contact))
 
 
def delete_contact(contacts: list):
    """
    Searches for a contact and deletes it after confirmation.
    """
    print("\n  ─── 🗑️  DELETE CONTACT ─────────────────────")
 
    if not contacts:
        print("\n  ℹ️   No contacts to delete.")
        return
 
    query = input("\n  Search contact to delete: ").strip()
    results = find_contacts(contacts, query)
 
    if not results:
        print(f"\n  ❌  No contacts found matching '{query}'.")
        return
 
    # Pick one if multiple found
    if len(results) == 1:
        orig_index, contact = results[0]
    else:
        print(f"\n  Found {len(results)} matches:")
        for i, (orig_idx, c) in enumerate(results, start=1):
            print(f"    [{i}]  {c['name']}  —  {c['phone']}")
        while True:
            pick = input("\n  ➤  Which contact to delete? (enter number): ").strip()
            if pick.isdigit() and 1 <= int(pick) <= len(results):
                orig_index, contact = results[int(pick) - 1]
                break
            print("  ⚠️   Invalid choice.")
 
    # Confirm before deleting
    print(f"\n  About to delete:")
    print(format_contact_card(contact))
    confirm = input("\n  ⚠️   Are you sure? This cannot be undone. (yes/no): ").strip().lower()
 
    if confirm in ("yes", "y"):
        contacts.pop(orig_index)
        print(f"\n  ✅  '{contact['name']}' has been deleted.")
    else:
        print("  ℹ️   Deletion cancelled.")
 
 
#  MAIN PROGRAM
 
def main():
    """Entry point — runs the contact book app."""
    clear_screen()
    print_banner()
 
    # Start with an empty list — contacts live in memory only
    contacts = []
    print(f"\n  Welcome!  Contacts are stored for this session only.")
 
    while True:
        print_menu()
        choice = get_menu_choice()
 
        if   choice == "1": add_contact(contacts)
        elif choice == "2": view_contacts(contacts)
        elif choice == "3": search_contact(contacts)
        elif choice == "4": update_contact(contacts)
        elif choice == "5": delete_contact(contacts)
        elif choice == "6":
            print("\n" + "═" * 58)
            print(f"  👋  Goodbye!  {len(contacts)} contact(s) will be cleared.")
            print("═" * 58 + "\n")
            break
 
        input("\n  Press Enter to return to the menu...")
        clear_screen()
        print_banner()
 
 
#  RUN THE PROGRAM
 
if __name__ == "__main__":
    main()