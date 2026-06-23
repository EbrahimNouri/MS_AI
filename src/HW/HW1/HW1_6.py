from pathlib import Path
import json
from typing import Optional

FILE_PATH = Path("products.txt")
product_local: list[Product] = []


class Product:

  def __init__(self, name: str, count: int, saved: bool = False) -> None:
    self.name = name
    self.count = count
    self.saved = saved

  def __str__(self) -> str:
    return f"name: {self.name:<12} | count: {self.count:<5} | saved: {self.saved}"

  def obj_to_dict(self) -> dict:
    return {"name": self.name, "count": self.count}

  @staticmethod
  def dict_to_obj(dic: dict, saved: bool = False) -> Product:
    return Product(dic["name"], dic["count"], saved)


def search(name: str, include_file: bool = True, include_memory: bool = True) -> Optional[Product]:
  if include_memory:
    for product in product_local:
      if name.lower() in product.name.lower():
        return product

  if include_file:
    products_file = get_all_products(include_file=True, include_memory=False)
    for product in products_file:
      if name.lower() in product.name.lower():
        return product

  return None


def save() -> None:
  for product in product_local:
    existing = search(product.name, include_file=True, include_memory=False)
    if existing is not None:
      existing.count += product.count
      existing.saved = True
      write_to_file(existing)
    else:
      product.saved = True
      write_to_file(product)
  product_local.clear()
  print("Saved successfully.")


def add(product_input: Product) -> None:
  for product in product_local:
    if product_input.name.lower() in product.name.lower():
      product.count += product_input.count
      return
  product_local.append(product_input)


def delete_from_file(product: Product) -> bool:
  products = get_all_products(include_file=True, include_memory=False)

  for i, p in enumerate(products):
    if p.name.lower() == product.name.lower():
      products.pop(i)
      products_dict = [p.obj_to_dict() for p in products]
      FILE_PATH.write_text(json.dumps(products_dict, indent=4))
      return True

  return False


def sell(product: Product) -> None:
  found = search(product.name)

  if found is None:
    print("Product not found!")
    return

  if found.count < product.count:
    print("Not enough product in stock")
    return

  found.count -= product.count

  if found.count == 0:
    delete_from_file(found)
    print(f"Product '{found.name}' sold out and removed from file.")
  else:
    write_to_file(found)
    print("Sold successfully.")


def write_to_file(product: Product):
  products = get_all_products(include_file=True, include_memory=False)

  for i, p in enumerate(products):
    if p.name.lower() == product.name.lower():
      products[i] = product
      products_dict = [p.obj_to_dict() for p in products]
      FILE_PATH.write_text(json.dumps(products_dict, indent=4))
      return

  products.append(product)
  products_dict = [p.obj_to_dict() for p in products]
  FILE_PATH.write_text(json.dumps(products_dict, indent=4))


def get_all_products(include_file: bool = True, include_memory: bool = True) -> list[Product]:
  products = []
  if include_file:
    products_dict = json.loads(FILE_PATH.read_text())
    get_all_from_file = [Product.dict_to_obj(p, True) for p in products_dict]
    products.extend(get_all_from_file)
  if include_memory:
    products.extend(product_local)
  return products


def report() -> dict[str, float]:
  products = get_all_products(include_file=True, include_memory=False)
  if not products:
    return {
      "count_of_saved": 0,
      "total_count": 0,
      "max_count": 0,
      "min_count": 0,
    }

  return {
    "count_of_saved": sum(p.count for p in products if p.saved),
    "total_count": sum(p.count for p in products),
    "max_count": max(p.count for p in products),
    "min_count": min(p.count for p in products),
  }


def menu():
  menu_print = """
    1. Add
    2. Sell
    3. Search
    4. Show
    5. Save
    6. Report
    7. Exit

    Enter your choice:
    ~ """

  choice = input(menu_print)
  match choice:

    case "1":  # Add
      product = get_product_from_input()
      add(product)

    case "2":  # sell
      product = get_product_from_input()
      sell(product)

    case "3":  # Search
      name = input("Enter product name: ")
      product = search(name)
      if product:
        print(product)
      else:
        print("Product not found.")

    case "4":  # Show
      products = get_all_products(include_file=True, include_memory=True)
      if products:
        for product in products:
          print(product)
      else:
        print("List of products is empty.")

    case "5":  # Save
      save()

    case "6":  # report
      report_data = report()
      for key, value in report_data.items():
        print(f"{key}: {value}")

    case "7":  # Exit
      print("Goodbye!")
      exit()

    case _:
      print("Invalid choice.")


def get_product_from_input():
  name = input("Enter product name: ")
  count = input("Enter product count: ")
  if not count.isdigit():
    print("Invalid count")
    return get_product_from_input()
  return Product(name, int(count), False)


def check_file():
  if not FILE_PATH.exists() or FILE_PATH.stat().st_size == 0:
    FILE_PATH.write_text(json.dumps([]))


def main():
  check_file()
  while True:
    menu()


if __name__ == "__main__":
  try:
    main()
  except Exception as e:
    print("unexpected error:", e)
