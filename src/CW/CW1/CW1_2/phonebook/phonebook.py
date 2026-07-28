phonebook = {}


def add_contact(name="", phone=""):
    phonebook[name] = phone


def delete_contact(name=""):
    phonebook.pop(name)


def update_contact(name="", phone=""):
    phonebook[name] = phone


def print_contacts():
    for key, value in phonebook.items():
        print(f"{key}: {value}")


def find_contact(name=""):
    return phonebook.get(name)


def get_name() -> str:
    return input("Enter the name: ")


def get_phonenumber() -> str:
    return input("Enter the phone: ")


def show_menu():
    global menu
    print("1. Add contact")
    print("2. Delete contact")
    print("3. Update contact")
    print("4. Print contacts")
    print("5. Find contact")
    print("6. Exit")
    menu = input("Enter your choice: ")
    return menu


while True:
    menu = show_menu()
    match menu:
        case "1":
            name = get_name()
            phone = get_phonenumber()
            add_contact(name, phone)
        case "2":
            name = input("Enter the name: ")
            delete_contact(name)
        case "3":
            name = input("Enter the name: ")
            phone = input("Enter the phone: ")
            update_contact(name, phone)
        case "4":
            print_contacts()
        case "5":
            name = input("Enter the name: ")
            find_contact(name)
        case _:
            print("Invalid input")
            break

    # if menu == "1":
    #     name = get_name()
    #     phone = get_phonenumber()
    #     add_contact(name, phone)
    # elif menu == "2":
    #     name = input("Enter the name: ")
    #     delete_contact(name)
    # elif menu == "3":
    #     name = input("Enter the name: ")
    #     phone = input("Enter the phone: ")
    #     update_contact(name, phone)
    # elif menu == "4":
    #     print_contacts()
    # elif menu == "5":
    #     name = input("Enter the name: ")
    #     find_contact(name)
    # else:
    #     break
