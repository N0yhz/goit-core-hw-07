from action import (
    add_contact,
    change_contact,
    show_phone,
    add_birthday,
    show_birthday,
    get_upcoming_birthdays,
    delete_contact
)
from Class import AddressBook
from parse import parse_input

def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_contact(args, book))

        elif command == "phone":
            print(show_phone(args, book))

        elif command == "all":
            print(book)

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            if len(args) != 1:
                print("Invalid arguments. Usage: birthdays [days]")
            else:
                try:
                    days = int(args[0])
                    print(get_upcoming_birthdays(book, days))
                except ValueError:
                    print("Invalid number of days.")

        elif command == "delete":
            print(delete_contact(args, book))

        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()
