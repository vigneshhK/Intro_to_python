contacts = {}

while True:
    choice = input("1 add, 2 search, 3 list, 0 quit: ")

    if choice == "1":
        name = input("Name: ")
        phone = input("Phone: ")

        if name not in contacts:
            contacts[name] = []

        contacts[name].append(phone)

    elif choice == "2":
        name = input("Name: ")
        print(contacts.get(name, "Not found"))

    elif choice == "3":
        for name in sorted(contacts):
            print(f"{name:<5} " + ", ".join(contacts[name]))

    elif choice == "0":
        break