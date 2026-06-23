import json
from pathlib import Path

FILE_PATH = Path("books.txt")


class Book:
  def __init__(self, name, author):
    self.name = name
    self.author = author

  @classmethod
  def dic_to_obj(cls, book_dict):
    return cls(book_dict.get("name"), book_dict.get("author"))

  def obj_to_dic(self):
    return {
      "name": self.name,
      "author": self.author
    }

  def __str__(self):
    return f"{self.name:<15} : {self.author:<15}"


def add_to_file(book: Book) -> None:
  if FILE_PATH.exists() and FILE_PATH.stat().st_size > 0:
    books_data = json.loads(FILE_PATH.read_text())
  else:
    books_data = []

  books_data.append(book.obj_to_dic())
  FILE_PATH.write_text(json.dumps(books_data, indent=4))


def search_by_name(name: str) -> Book | None:
  return next((Book(b["name"], b["author"]) for b in json.loads(FILE_PATH.read_text()) if
               name.lower() in b["name"].lower()), None)
  # books_data = json.loads(FILE_PATH.read_text())
  # for book in books_data:
  #     if name.lower() in book["name"].lower():
  #         return Book(book["name"], book["author"])
  # return None


def show_all():
  return list(map(lambda b: Book(b["name"], b["author"]), json.loads(FILE_PATH.read_text())))
  # books_data = json.loads(FILE_PATH.read_text())
  # res = []
  # for book in books_data:
  #     res.append(Book(book["name"], book["author"])
  # return res


def menu():
  menu_print = '''
    What do you want to do?
    1. Add a book
    2. Search by name
    3. Show all
    4. Exit
    ~ '''

  input_menu = input(menu_print)

  match input_menu:
    case "1":
      name = input("Enter book name: ")
      author = input("Enter book author: ")
      add_to_file(Book(name, author))
    case "2":
      name = input("Enter book name: ")
      book = search_by_name(name)
      if book:
        print(book)
      else:
        print("Book not found.")
    case "3":
      books = show_all()
      [print(book) for book in books]
    case "4":
      print("Exiting...")
      exit()
    case _:
      print("Invalid input.")
      menu()


while True:
  menu()
