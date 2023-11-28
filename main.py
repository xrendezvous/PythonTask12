import json
import cmd

class AddressBook:
    def dump(self):
        with open(self.file, 'wb') as file:
            json.dump((self.record_id, self.record), file)

    def load(self):
        if not self.file.exists():
            return
        with open(self.file, 'rb') as file:
            self.record_id, self.record = json.load(file)


class Controller(cmd.Cmd):
    def exit(self):
        self.book.dump()
        return True