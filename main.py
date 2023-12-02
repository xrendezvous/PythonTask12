from collections import UserDict
import json

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def validate(self, value):
        if len(value) > 30:
            raise ValueError(f"Name should be no more than 30 symbols")
        if not value.isalpha():
            raise ValueError("Name should consist of letters")

    def __str__(self):
        return f"Name: {self.value}"

    def __init__(self, value):
        self.validate(value)
        super().__init__(value)


class Phone(Field):
    def validate(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError('Phone number should be a 10-digit number')

    def __str__(self):
        return f"Phone: {self.value}"

    def __init__(self, value):
        self.validate(value)
        super().__init__(value)



class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def __str__(self):
        result = f"{self.name}"
        if self.phones:
            result += f" Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"
        return result

    def add_phone(self, phone_number):
        phone = Phone(phone_number)
        phone.validate(phone_number)
        if phone not in self.phones:
            self.phones.append(phone)

    def find_phone(self, phone_number: str):
        for phone in self.phones:
            if phone.value == phone_number:
                return phone

        return None

    def edit_phone(self, old_phone, new_phone):
        for i, phone in enumerate(self.phones):
            if phone.value == old_phone:
                self.phones[i] = Phone(new_phone)
                self.phones[i].validate(new_phone)
                return f"Phone number {old_phone} updated to {new_phone}"

        raise ValueError(f"No phone number {old_phone} found")

    def remove_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                self.phones.remove(phone)
                return f"Phone number {phone_number} removed"

        return f"No phone number {phone_number} found"


class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name):
        if name in self.data:
            return self.data[name]
        else:
            return None

    def delete(self, name):
        if name in self.data:
            del self.data[name]
            return f"Record {name} deleted"
        else:
            return f"No record found with name {name}"

    def save_to_file(self, filename):
        with open(filename, 'w') as file:
            json.dump(self.data, file)

    def load_from_file(self, filename):
        try:
            with open(filename, 'r') as file:
                self.data = json.load(file)
        except FileNotFoundError:
            pass

    def search(self, query):
        results = []
        for record_data in self.data.values():
            record = Record(record_data['name'])
            for phone_number in record_data.get('phones', []):
                record.add_phone(phone_number)
            if query.lower() in record.name.value.lower() or any(query in phone.value for phone in record.phones):
                results.append(record)
        return results

if __name__ == "__main__":
    address_book = AddressBook()
    address_book.load_from_file('address_book.json')
    address_book.save_to_file('address_book.json')
    search_query = input('Enter search query: ')
    search_results = address_book.search(search_query)

    if search_results:
        print('Search results: ')
        for result in search_results:
            print(result)
    else:
        print('No results found')
