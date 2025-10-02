import json

FILENAME = "contacts.json"   # JSON file to store all contact data


# ---------- Storage Functions ----------

def load_contacts():
    """
    Load contacts from the JSON file.
    Returns a list of contacts. If the file does not exist, 
    or is empty/corrupted, returns an empty list.
    """
    try:
        with open(FILENAME, "r") as f:
            data = json.load(f)
            return data.get("contacts", [])
    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        return []


def save_contacts(people):
    """
    Save all contacts back to the JSON file.
    Stores data as a dictionary with key 'contacts' for structure.
    """
    with open(FILENAME, "w") as f:
        json.dump({"contacts": people}, f, indent=2)


# ---------- Core Contact Actions ----------

def add_person():
    """
    Add a new person by asking for name, age, and email.
    Returns a dictionary representing the person.
    """
    name = input("Name: ").strip().title()      # Auto-format names
    age = input("Age: ").strip()
    email = input("Email: ").strip().lower()    # Emails in lowercase

    # Each contact is a dictionary (JSON-friendly)
    person = {"name": name, "age": age, "email": email, "favorite": False}
    return person


def display_people(people):
    """
    Display a list of people in a table-like format.
    Shows index, name, age, email, and favorite status.
    """
    if not people:
        print("(No contacts to show)")
        return

    # Print table header
    print("\n# | Name                 | Age | Email                  | Fav")
    print("-" * 55)

    # Print each contact with formatting
    for i, person in enumerate(people, start=1):
        fav = "★" if person.get("favorite") else ""
        print(f"{i:<2}| {person['name']:<20}| {person['age']:<4}| {person['email']:<22}| {fav}")
    print()


def delete_contact(people):
    """
    Delete a contact by its number.
    Shows all contacts first, asks for a number, and requires confirmation.
    """
    if not people:
        print("No contacts to delete.")
        return

    display_people(people)

    while True:
        number = input("Enter a number to delete (or Enter to cancel): ").strip()
        if number == "":
            print("Canceled.")
            return
        try:
            number = int(number)
            if number <= 0 or number > len(people):
                print("Invalid number, out of range.")
            else:
                # Confirm deletion for safety
                confirm = input(f"Type {number} again to confirm delete: ").strip()
                if confirm == str(number):
                    people.pop(number - 1)
                    print("Person deleted!")
                else:
                    print("Delete canceled.")
                break
        except ValueError:
            print("Invalid number.")


def search(people):
    """
    Search for contacts by name or email.
    Displays all matches in table format.
    """
    if not people:
        print("(No contacts to search)")
        return

    search_text = input("Search for a name/email: ").lower().strip()
    result = [p for p in people
              if search_text in p["name"].lower() or search_text in p["email"].lower()]

    display_people(result)


def toggle_favorite(people):
    """
    Toggle the 'favorite' status of a contact.
    Shows all contacts first, asks for a number, and flips favorite on/off.
    """
    if not people:
        print("No contacts to update.")
        return

    display_people(people)
    number = input("Enter contact number to toggle favorite: ").strip()

    try:
        idx = int(number) - 1
        if 0 <= idx < len(people):
            people[idx]["favorite"] = not people[idx].get("favorite", False)
            status = "★ Added to favorites!" if people[idx]["favorite"] else "☆ Removed from favorites."
            print(status)
        else:
            print("Invalid number.")
    except ValueError:
        print("Not a valid number.")


# ---------- Extra Features ----------

def help_menu():
    """
    Display a help menu showing all available commands.
    """
    print("""
Available commands:
  add      - Add a new contact
  delete   - Delete a contact (with confirmation)
  search   - Search contacts by name/email
  fav      - Toggle favorite for a contact
  list     - Show all contacts
  help     - Show this menu
  q        - Quit program
""")


# ---------- Main Program ----------

print("Hi, welcome to the contact management system.\n")

# Load contacts at startup
people = load_contacts()

# Main loop
while True:
    print("Contact list size:", len(people))
    command = input("Command (type 'help' for options): ").strip().lower()

    if command == "add":
        person = add_person()
        people.append(person)
        save_contacts(people)
        print("Person added!")

    elif command == "delete":
        delete_contact(people)
        save_contacts(people)

    elif command == "search":
        search(people)

    elif command == "fav":
        toggle_favorite(people)
        save_contacts(people)

    elif command == "list":
        display_people(people)

    elif command == "help":
        help_menu()

    elif command == "q":
        break

    else:
        print("Invalid command!")

# Save all contacts before exiting
save_contacts(people)
print("Goodbye!")
