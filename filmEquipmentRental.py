from datetime import datetime, timedelta

class Equipment:
    def __init__(self, name, quantity, category, daily_fee):
        self.name = name
        self.quantity = quantity
        self.category = category
        self.daily_fee = daily_fee

    def __str__(self):
        return f"Name: {self.name}, Quantity: {self.quantity}, Category: {self.category}, Daily Fee: ${self.daily_fee:.2f}"


class User:
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password
        self.cart = []
        self.rented_items = []

    def menu(self):
        pass


class Rental:
    def __init__(self, equipment, rental_date, return_date):
        self.equipment = equipment
        self.rental_date = rental_date
        self.return_date = return_date
        self.rental_days = (return_date - rental_date).days

    def calculate_total(self):
        return self.equipment.daily_fee * self.rental_days


class Payment:
    @staticmethod
    def process_payment(client, cart, rental_date, return_date):
        rental_days = (return_date - rental_date).days
        total = sum(item.daily_fee * rental_days for item in cart)

        print("\n--- Payment Receipt ---")
        print(f"Client Name: {client.name}")
        print(f"Rental Date: {rental_date}")
        print(f"Return Date: {return_date}")
        print(f"Rental Period: {rental_days} days")
        print("\nRented Equipment:")
        for item in cart:
            print(f"- {item.name} (Daily Fee: ${item.daily_fee:.2f}, Total: ${item.daily_fee * rental_days:.2f})")
            item.quantity -= 1
            client.rented_items.append(
                {"name": item.name, "rental_date": rental_date, "return_date": return_date}
            )
        print(f"\nGrand Total: ${total:.2f}")
        print("Payment successful! Thank you for renting.")
        client.cart.clear()


class Client(User):
    def __init__(self, name, email, password):
        super().__init__(name, email, password)

    def menu(self):
        while True:
            print(f"\n--- Welcome, {self.name}! ---")
            print("1. Rent Equipment")
            print("2. My Cart")
            print("3. My Rents")
            print("0. Logout")
            choice = input("Enter your choice: ")

            if choice == "1":
                self.select_or_back()
            elif choice == "2":
                self.manage_cart()
            elif choice == "3":
                self.view_my_rents()
            elif choice == "0":
                print("Logging out...")
                break
            else:
                print("Invalid choice. Please try again.")

    def select_or_back(self):
        while True:
            print("\n--- Rent Equipment ---")
            print("1. Select Category")
            print("0. Back")
            choice = input("Enter your choice: ")

            if choice == "0":
                return

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
            print("0. Back")
            category_choice = input("Enter your choice: ")

            if category_choice == "0":
                return

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
                return

            for idx, equipment in enumerate(available_equipment, start=1):
                print(f"{idx}. {equipment.name} (Quantity: {equipment.quantity}, Daily Fee: ${equipment.daily_fee:.2f})")
            
            print("0. Back")
            choice = input("Enter your choice: ")

            if choice == "0":
                return

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
                return
                
            total_fee = sum(item.daily_fee for item in self.cart)
            
            for idx, equipment in enumerate(self.cart, start=1):
                print(f"{idx}. {equipment.name} (Daily Fee: ${equipment.daily_fee:.2f})")
            
            print(f"\nTotal Daily Fee: ${total_fee:.2f}")
            print("\nOptions:")
            print("1. Remove Item")
            print("2. Proceed to Payment")
            print("0. Back")
            choice = input("Enter your choice: ")

            if choice == "0":
                return

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
        print("\nChoose Rental Date:")
        rental_date = self.get_valid_date("Rental Date (YYYY-MM-DD): ")

        print("\nChoose Return Date:")
        return_date = self.get_valid_date("Return Date (YYYY-MM-DD): ", rental_date)

        Payment.process_payment(self, self.cart, rental_date, return_date)

    def get_valid_date(self, prompt, min_date=None):
        while True:
            date_str = input(prompt)
            try:
                date = datetime.strptime(date_str, "%Y-%m-%d").date()
                today = datetime.today().date()
                if min_date is None:
                    min_date = today
                if date < min_date:
                    print(f"Date cannot be earlier than {min_date}. Please try again.")
                    continue
                return date
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD.")

    def view_my_rents(self):
        print("\n--- My Rents ---")
        if not self.rented_items:
            print("You have not rented any equipment.")
        else:
            print("Your rented equipment:")
            for item in self.rented_items:
                print(
                    f"- {item['name']} (Rented: {item['rental_date']}, Return: {item['return_date']})"
                )


class Admin(User):
    def __init__(self, email, password):
        super().__init__("Admin", email, password)

    def menu(self):
        while True:
            print("\n--- Admin Menu ---")
            print("1. View Users")
            print("2. View Equipment")
            print("3. Add Equipment")
            print("0. Logout")
            choice = input("Enter your choice: ")

            if choice == "1":
                self.view_users()
            elif choice == "2":
                self.select_category()
            elif choice == "3":
                self.add_equipment()
            elif choice == "0":
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
            print("0. Back")
            category_choice = input("Enter your choice: ")

            if category_choice == "0":
                return

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
            return

        for equipment in available_equipment:
            print(equipment)

    def add_equipment(self):
        print("\n--- Add Equipment ---")
        name = input("Enter equipment name: ")
        quantity = int(input("Enter equipment quantity: "))
        price = float(input("Enter daily fee: "))
        print("Select a category:")
        print("1. Camera")
        print("2. Lens")
        print("3. Lighting")
        category_choice = input("Enter your choice: ")

        categories = {"1": "Camera", "2": "Lens", "3": "Lighting"}
        category = categories.get(category_choice)

        if not category:
            print("Invalid category. Equipment not added.")
            return

        new_equipment = Equipment(name, quantity, category, price)
        system.equipment_list.append(new_equipment)
        print(f"{new_equipment.name} has been added to {category}.")


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
            print("0. Exit")
            choice = input("Enter your choice: ")

            if choice == "1":
                self.login()
            elif choice == "2":
                self.create_account()
            elif choice == "0":
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")

system = System()
system.run()
        
