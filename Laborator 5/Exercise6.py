class LibraryItem:
    def __init__(self, name, code, num_of_items):
        self.name = name
        self.code = code
        self.num_of_items = num_of_items
        self.checked_out = 0

    def checkout(self, num_to_checkout):
        if num_to_checkout <= self.available_items():
            self.num_of_items -= num_to_checkout
            print(f"Checked out {num_to_checkout} items of {self.name}.")
        else:
            print("Not enough items available for checkout.")

    def return_item(self, num_to_return):
        self.num_of_items += num_to_return
        print(f"Returned {num_to_return} items of {self.name}.")

    def available_items(self):
        return self.num_of_items - self.checked_out

    def __str__(self):
        return f"{self.name} ({self.code}): {self.available_items()} available"


class Book(LibraryItem):
    def __init__(self, name, code, author, publishing_house, num_of_pages, num_of_items=0):
        super().__init__(name, code, num_of_items)
        self.author = author
        self.publishing_house = publishing_house
        self.num_of_pages = num_of_pages

    def display_info(self):
        return f"{self.name} ({self.code}): {self.available_items()} available, Author: {self.author}, Pages: {self.num_of_pages}"


class DVD(LibraryItem):
    def __init__(self, name, code, director, duration, num_of_items=0):
        super().__init__(name, code, num_of_items)
        self.director = director
        self.duration = duration

    def display_info(self):
        return f"{self.name} ({self.code}): {self.available_items()} available, Director: {self.director}, Duration: {self.duration} minutes"


class Magazine(LibraryItem):
    def __init__(self, name, code, issue_date, num_of_items=0):
        super().__init__(name, code, num_of_items)
        self.issue_date = issue_date

    def display_info(self):
        return f"{self.name} ({self.code}): {self.available_items()} available, Issue Date: {self.issue_date}"


def main():
    book = Book("David Copperfield", "#B001", "Charles Dickens", "Random House", 300, num_of_items=20)
    dvd = DVD("The Prestige", "#D012", "Christopher Nolan", 150, num_of_items=15)
    magazine = Magazine("Homes and Gardens", "M300", "2020-06-01", num_of_items=10)

    print(book)
    book.checkout(5)
    print(book)
    book.return_item(2)
    print(book)
    print()

    print(dvd)
    dvd.checkout(10)
    print(dvd)
    dvd.return_item(5)
    print(dvd)
    print()

    print(magazine)
    magazine.checkout(3)
    print(magazine)
    magazine.return_item(2)
    print(magazine)


if __name__ == "__main__":
    main()

