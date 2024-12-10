class Equipment:
    def __init__(self, name, quantity, category, price):
        self.name = name
        self.quantity = quantity
        self.category = category
        self.price = price

    def __str__(self):
        return f"Name: {self.name}, Quantity: {self.quantity}, Category: {self.category}, Price: ${self.price:.2f}"


class User:
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password
        self.cart = []
        self.rented_items = []

    def menu(self):
        pass


class Client(User):
    def __init__(self, name, email, password):
        super().__init__(name, email, password)

    def menu(self):
        while True:
            print(f"\n--- Welcome, {self.name}! ---")
            print("1. Rent Equipment")
            print("2. My Cart")
            print("3. My Rents")
            print("4. Logout")
            choice = input("Enter your choice: ")

            if choice == "1":
                self.select_or_back()
            elif choice == "2":
                self.manage_cart()
            elif choice == "3":
                self.view_my_rents()
            elif choice == "4":
                print("Logging out...")
                break
            else:
                print("Invalid choice. Please try again.")

    def select_or_back(self):
        while True:
            print("\n--- Rent Equipment ---")
            print("1. Select Category")
            print("2. Back to Main Menu")
            choice = input("Enter your choice: ")

            if choice == "2":
                return  # Back to main menu

            if choice == "1":
                self.select_category()
            else:
                print("Invalid choice. Please try again.")

    def select_category(self):
        while True:
            print("\n--- Select Category ---")
            print("1. Camera")
            print("2. Lens")
            print("3. Lighting")
            print("4. Back to Main Menu")
            category_choice = input("Enter your choice: ")

            if category_choice == "4":
                return  # Back to Client's main menu

            categories = {"1": "Camera", "2": "Lens", "3": "Lighting"}
            category = categories.get(category_choice)

            if not category:
                print("Invalid category. Please try again.")
                continue

            self.show_available_equipment(category)

    def show_available_equipment(self, category):
        while True:
            print(f"\n--- {category} Equipment ---")
            available_equipment = [
                equipment for equipment in system.equipment_list if equipment.category == category
            ]

            if not available_equipment:
                print("No equipment available in this category.")
                return  # Back to category selection

            for idx, equipment in enumerate(available_equipment, start=1):
                print(f"{idx}. {equipment.name} (Quantity: {equipment.quantity}, Price: ${equipment.price:.2f})")

            print("0. Back to Category Selection")
            choice = input("Enter your choice: ")

            if choice == "0":
                return  # Back to category selection

            try:
                equipment_index = int(choice) - 1
                selected_equipment = available_equipment[equipment_index]
            except (ValueError, IndexError):
                print("Invalid selection. Please try again.")
                continue

            self.add_to_cart(selected_equipment)

    def add_to_cart(self, equipment):
        if equipment.quantity > 0:
            self.cart.append(equipment)
            print(f"{equipment.name} has been added to your cart.")
        else:
            print("Sorry, this equipment is out of stock.")

    def manage_cart(self):
        while True:
            print("\n--- My Cart ---")
            if not self.cart:
                print("Your cart is empty.")
                return  # Back to main menu

            for idx, equipment in enumerate(self.cart, start=1):
                print(f"{idx}. {equipment.name} (Price: ${equipment.price:.2f})")

            print("\nOptions:")
            print("1. Remove Item")
            print("2. Proceed to Payment")
            print("3. Back to Main Menu")
            choice = input("Enter your choice: ")

            if choice == "3":
                return  # Back to main menu

            if choice == "1":
                self.remove_from_cart()
            elif choice == "2":
                self.proceed_to_payment()
            else:
                print("Invalid choice. Please try again.")

    def remove_from_cart(self):
        print("\n--- Remove Item ---")
        for idx, equipment in enumerate(self.cart, start=1):
            print(f"{idx}. {equipment.name}")

        try:
            choice = int(input("Enter the number of the item to remove: ")) - 1
            removed_item = self.cart.pop(choice)
            print(f"{removed_item.name} has been removed from your cart.")
        except (ValueError, IndexError):
            print("Invalid selection. Please try again.")

    def proceed_to_payment(self):
        total = sum(equipment.price for equipment in self.cart)
        print(f"\nTotal amount: ${total:.2f}")
        confirm = input("Do you want to proceed with the payment? (yes/no): ")

        if confirm.lower() == "yes":
            for item in self.cart:
                item.quantity -= 1  # Deduct quantity from the system
                self.rented_items.append(item.name)  # Add to rented items
            self.cart.clear()  # Clear the cart
            print("Payment successful! Thank you for renting.")
        else:
            print("Payment canceled.")

    def view_my_rents(self):
        print("\n--- My Rents ---")
        if not self.rented_items:
            print("You have not rented any equipment.")
        else:
            print("Your rented equipment:")
            for item in self.rented_items:
                print(f"- {item}")


class Admin(User):
    def __init__(self, email, password):
        super().__init__("Admin", email, password)

    def menu(self):
        while True:
            print("\n--- Admin Menu ---")
            print("1. View Users")
            print("2. View Equipment")
            print("3. Add Equipment")
            print("4. Logout")
            choice = input("Enter your choice: ")

            if choice == "1":
                self.view_users()
            elif choice == "2":
                self.select_category()
            elif choice == "3":
                self.add_equipment()
            elif choice == "4":
                print("Logging out...")
                break
            else:
                print("Invalid choice. Please try again.")

    def select_category(self):
        while True:
            print("\n--- View Equipment ---")
            print("Select a category:")
            print("1. Camera")
            print("2. Lens")
            print("3. Lighting")
            print("4. Back to Main Menu")
            category_choice = input("Enter your choice: ")

            if category_choice == "4":
                return  # Back to Admin's main menu

            categories = {"1": "Camera", "2": "Lens", "3": "Lighting"}
            category = categories.get(category_choice)

            if not category:
                print("Invalid category. Please try again.")
                continue

            self.show_available_equipment(category)

    def show_available_equipment(self, category):
        print(f"\n--- {category} Equipment ---")
        available_equipment = [
            equipment for equipment in system.equipment_list if equipment.category == category
        ]

        if not available_equipment:
            print("No equipment available in this category.")
            return  # Back to category selection

        for equipment in available_equipment:
            print(equipment)

    def add_equipment(self):
        print("\n--- Add Equipment ---")
        name = input("Enter equipment name: ")
        quantity = int(input("Enter equipment quantity: "))
        price = float(input("Enter equipment price: "))
        print("Select a category:")
        print("1. Camera")
        print("2. Lens")
        print("3. Lighting")
        category_choice = input("Enter category: ")

        categories = {"1": "Camera", "2": "Lens", "3": "Lighting"}
        category = categories.get(category_choice)

        if not category:
            print("Invalid category. Please try again.")
            return

        new_equipment = Equipment(name, quantity, category, price)
        system.equipment_list.append(new_equipment)
        print(f"Equipment '{name}' added successfully!")


class System:
    def __init__(self):
        self.users = []
        self.equipment_list = []
        self.admin_email = "admin"
        self.admin_password = "admin"

        # Predefined equipment
        self.add_default_equipment()

    def add_default_equipment(self):
        self.equipment_list = [
            Equipment("Canon EOS R5", 5, "Camera", 200.0),
            Equipment("Sony A7 III", 3, "Camera", 180.0),
            Equipment("Fujifilm X-T4", 4, "Camera", 150.0),
            Equipment("Canon 50mm f/1.2", 2, "Lens", 50.0),
            Equipment("Sony 24-70mm f/2.8", 2, "Lens", 70.0),
            Equipment("Profoto B10 Lighting Kit", 3, "Lighting", 100.0),
            Equipment("Godox SL60W", 5, "Lighting", 80.0),
        ]

    def create_account(self):
        print("\n--- Create Account ---")
        name = input("Enter your name: ")
        email = input("Enter your email: ")
        password = input("Enter your password: ")

        for user in self.users:
            if user.email == email:
                print("This email is already registered. Please try again.")
                return

        new_user = Client(name, email, password)
        self.users.append(new_user)
        print("Account created successfully! Please log in.")

    def login(self):
        print("\n--- Login ---")
        email = input("Enter your email: ")
        password = input("Enter your password: ")

        if email == self.admin_email and password == self.admin_password:
            admin = Admin(email, password)
            admin.menu()
        else:
            for user in self.users:
                if user.email == email and user.password == password:
                    user.menu()
                    return
            print("Invalid credentials. Please try again.")

    def run(self):
        while True:
            print("\n--- Welcome to the System ---")
            print("1. Login")
            print("2. Create Account")
            print("3. Exit")
            choice = input("Enter your choice: ")

            if choice == "1":
                self.login()
            elif choice == "2":
                self.create_account()
            elif choice == "3":
                print("Exiting the system. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")


# Create and run the system
system = System()
system.run()
