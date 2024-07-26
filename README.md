# goit-core-hw-07
ДЗ 7

*main.py*

```
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
```

*parse.py*

```
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args
```

*action.py*

```
from Class import Record, AddressBook

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return 'Enter [username]'
        except ValueError:
            return 'Give me [name] and [phone] please.'
        except IndexError:
            return'Enter [username]'
        except Exception:
            return 'Something went wrong.'
    return inner

@input_error
def add_contact(args, book: AddressBook):
    if len(args) < 2:
        return 'Invalid arguments. Usage: add [name] [phone]'
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message

@input_error
def change_contact(args, book: AddressBook):
    if len(args) != 3:
        return 'Invalid arguments. Usage: change [name] [oldphone] [newphone]'
    name, old_phone, new_phone = args
    record = book.find(name)
    if record:
        record.edit_phone(old_phone, new_phone)
        return f'Contact {name} phone has been updated.'
    else:
        return 'Contact not found'

@input_error
def show_phone(args, book: AddressBook):
    if len(args) != 1:
        return 'Invalid arguments. Usage: phone [name]'
    name = args[0]
    record = book.find(name)
    if record:
        return str(record)
    else:
        return 'Contact not found'

@input_error
def add_birthday(args, book: AddressBook):
    if len(args) != 2:
        return 'Invalid arguments. Usage: add-birthday [name] [DD.MM.YYYY]'
    name, birthday = args
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return f'Birthday for {name} set to {birthday}.'
    else:
        return 'Contact not found'

@input_error
def show_birthday(args, book: AddressBook):
    if len(args) != 1:
        return 'Invalid arguments. Usage: show-birthday [name]'
    name = args[0]
    record = book.find(name)
    if record:
        days = record.days_to_birthday()
        if days is not None:
            return f'{days} days until {name}\'s birthday.'
        else:
            return f'No birthday set for {name}.'
    else:
        return 'Contact not found'

@input_error
def delete_contact(args, book: AddressBook):
    if len(args) != 1:
        return 'Invalid arguments. Usage: delete [name]'
    name = args[0]
    book.delete(name)
    return f'Contact {name} deleted.'

def get_upcoming_birthdays(book: AddressBook, days):
    upcoming_birthdays = book.get_upcoming_birthdays(days)
    if upcoming_birthdays:
        return '\n'.join(str(record) for record in upcoming_birthdays)
    else:
        return 'No upcoming birthdays found.'
```

*Class.py*

```
import re
from collections import UserDict
from datetime import datetime, timedelta

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        self.validate(value)
        super().__init__(value)
    
    def validate(self, value):
        if not re.fullmatch(r'\d{10}', value):
            raise ValueError(f'Phone number {value} is invalid. It must contain exactly 10 digits.')

class Birthday(Field):
    def __init__(self, value):
        self.validate(value)
        super().__init__(value)

    def validate(self, value):
        try:
            self.date = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Record:
    def __init__(self, name, phones=None, birthday=None):
        self.name = Name(name)
        self.phones = [Phone(phone) for phone in phones] if phones else []
        self.birthday = Birthday(birthday) if birthday else None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        phone_to_remove = self.find_phone(phone)
        if phone_to_remove:
            self.phones.remove(phone_to_remove)
        else:
            raise ValueError(f'Phone number {phone} is not found.')

    def edit_phone(self, old_phone, new_phone):
        self.remove_phone(old_phone)
        self.add_phone(new_phone)

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def days_to_birthday(self):
        if self.birthday:
            today = datetime.now().date()
            birthday_date = self.birthday.date.date()
            next_birthday = birthday_date.replace(year=today.year)
            if next_birthday < today:
                next_birthday = next_birthday.replace(year=today.year + 1)
            return (next_birthday - today).days
        return None

    def __str__(self):
        phones_str = ', '.join(str(phone) for phone in self.phones)
        birthday_str = f", Birthday: {self.birthday}" if self.birthday else ""
        return f"Name: {self.name}, Phones: [{phones_str}]{birthday_str}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name, None)

    def delete(self, name):
        if name in self.data:
            del self.data[name]
        else:
            raise ValueError(f"Record with name {name} not found.")

    def get_upcoming_birthdays(self, days):
        upcoming_birthdays = []
        today = datetime.now().date()
        end_date = today + timedelta(days=days)
        for record in self.data.values():
            if record.birthday:
                birthday_date = record.birthday.date.date()
                next_birthday = birthday_date.replace(year=today.year)
                if today <= next_birthday <= end_date:
                    upcoming_birthdays.append(record)
        return upcoming_birthdays

    def __str__(self):
        records = [str(record) for record in self.data.values()]
        return '\n'.join(records)
```
