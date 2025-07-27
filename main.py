from datetime import datetime, timedelta
from collections import UserDict
import pickle


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number must be 10 digits.")
        super().__init__(value)


class Birthday(Field):
    def __init__(self, value):
        try:
            datetime.strptime(value, "%d.%m.%Y")
            super().__init__(value)
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")



class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def remove_phone(self, phone):
        p = self.find_phone(phone)
        if p:
            self.phones.remove(p)
        else:
            raise ValueError("Phone not found.")

    def edit_phone(self, old_phone, new_phone):
        self.remove_phone(old_phone)
        self.add_phone(new_phone)

    def add_birthday(self, birthday_str):
        self.birthday = Birthday(birthday_str)

    def __str__(self):
        phones = ', '.join(p.value for p in self.phones)
        bday = f", Birthday: {self.birthday.value}" if self.birthday else ""
        return f"{self.name.value}: {phones}{bday}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self):
        today = datetime.today().date()
        result = []

        for record in self.data.values():
            if record.birthday:
                bday_date = datetime.strptime(record.birthday.value, "%d.%m.%Y").date()
                bday = bday_date.replace(year=today.year)
                if bday < today:
                    bday = bday.replace(year=today.year + 1)

                delta = (bday - today).days
                if 0 <= delta <= 7:
                    congrat_day = bday
                    if bday.weekday() >= 5:
                        days_ahead = 7 - bday.weekday()
                        congrat_day += timedelta(days=days_ahead)

                    result.append({
                        "name": record.name.value,
                        "birthday": congrat_day.strftime("%d.%m.%Y")
                    })

        return result



    def __str__(self):
        return '\n'.join(str(record) for record in self.data.values())

def save_data(book, filename="addressbook.pkl"):
        with open(filename, "wb") as f:
            pickle.dump(book, f)

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
             return pickle.load(f)
    except FileNotFoundError:
            return AddressBook()


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return str(e) or "Give me name and phone please."
        except KeyError:
            return "Contact not found."
        except IndexError:
            return "Enter user name please."
        except AttributeError:
            return "Contact not found."
    return inner


def parse_input(user_input):
    cmd, *args = user_input.strip().lower().split()
    return cmd, args


@input_error
def add_contact(args, book: AddressBook):
    name, phone, *rest = args
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
def change_contact(args, book):
    name, old_phone, new_phone = args
    record = book.find(name)
    record.edit_phone(old_phone, new_phone)
    return "Phone updated."



@input_error
def get_phone(args, book):
    name = args[0]
    record = book.find(name)
    return ', '.join(p.value for p in record.phones)


@input_error
def get_all(args, book):
    if args:
        raise ValueError("This command doesn't take arguments.")
    return str(book) if book.data else "No contacts saved."


@input_error
def add_birthday(args, book):
    name, bday = args
    record = book.find(name)
    record.add_birthday(bday)
    return "Birthday added."



@input_error
def show_birthday(args, book):
    name = args[0]
    record = book.find(name)
    if record.birthday:
        return f"{name}'s birthday is {record.birthday.value}"

    return "Birthday not set."



@input_error
def birthdays(args, book):
    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return "No upcoming birthdays."
    return '\n'.join([f"{r['name']}: {r['birthday']}" for r in upcoming])


def main():
    book = load_data()
    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ").strip()
        if not user_input:
            print("Please enter a command.")
            continue

        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            save_data(book)
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(get_phone(args, book))
        elif command == "all":
            print(get_all(args, book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(args, book))
        else:
            print("Invalid command.")



if __name__ == "__main__":
    main()
