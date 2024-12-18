from datetime import datetime, timedelta
import subprocess

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
        subprocess.run('clear')
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
        input("Press Enter to continue...")
        client.cart.clear()


class Client(User):
    def __init__(self, name, email, password):
        super().__init__(name, email, password)

    def menu(self):
        while True:
            subprocess.run('clear')
            print(f"\n--- Welcome, {self.name}! ---")
            print("1. View Equipment ")
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
                input("Press Enter to continue...")

    def select_or_back(self):
        while True:
            subprocess.run('clear')
            print("\n--- Rent Equipment ---")
            print("1. Select Category")
            print("2. Search Equipment")
            print("0. Back")
            choice = input("Enter your choice: ")

            if choice == "0":
                return
            elif choice == "1":
                self.select_category()
            elif choice == "2":
                self.search_and_rent_equipment()
            else:
                print("Invalid choice. Please try again.")
                input("Press Enter to continue...")

    def select_category(self):
        while True:
            subprocess.run('clear')
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
                input("Press Enter to continue...")
                continue

            self.show_available_equipment(category)

    def show_available_equipment(self, category):
        while True:
            subprocess.run('clear')
            print(f"\n--- {category} Equipment ---")
            available_equipment = [
                equipment for equipment in system.equipment_list if equipment.category == category
            ]

            if not available_equipment:
                print("No equipment available in this category.")
                input("Press Enter to continue...")
                return

            for idx, equipment in enumerate(available_equipment, start=1):
                print(f"{idx}. {equipment.name} (Condition: {'Available' if equipment.quantity > 0 else 'Not Available '}, Daily Fee: ${equipment.daily_fee:.2f})")
            
            print("0. Back")
            choice = input("Enter your choice: ")

            if choice == "0":
                return

            try:
                equipment_index = int(choice) - 1
                selected_equipment = available_equipment[equipment_index]
            except (ValueError, IndexError):
                print("Invalid selection. Please try again.")
                input("Press Enter to continue...")
                continue

            self.add_to_cart(selected_equipment)
            
    def search_and_rent_equipment(self):
        while True:
            subprocess.run('clear')
            print("\n--- Search Equipment ---")
            search_name = input("Enter equipment name to search (or 0 to go back): ").strip().lower()
        
            if search_name == "0":
                return  # Go back to previous menu

            matched_equipment = [
                equipment for equipment in system.equipment_list
                if search_name in equipment.name.lower() and equipment.quantity > 0
            ]

            if not matched_equipment:
                print("No matching equipment found or all out of stock.")
                input("Press Enter to continue...")
                continue    
    
            print("\nMatched Equipment:")
            for idx, equipment in enumerate(matched_equipment, start=1):
                print(f"{idx}. {equipment.name} (Available: {equipment.quantity}, Daily Fee: ${equipment.daily_fee:.2f})")
        
            choice = input("\nEnter the number of equipment to add to cart (or 0 to go back): ")

            if choice == "0":
                return

            try:
                equipment_index = int(choice) - 1
                selected_equipment = matched_equipment[equipment_index]
            except (ValueError, IndexError):
                print("Invalid selection. Please try again.")
                input("Press Enter to continue...")
                continue

            self.add_to_cart(selected_equipment)
                

    def add_to_cart(self, equipment):
        if equipment.quantity > 0:
            self.cart.append(equipment)
            print(f"{equipment.name} has been added to your cart.")
            input("Press Enter to continue...")
        else:
            print("Sorry, this equipment is out of stock.")
            input("Press Enter to continue...")

    def manage_cart(self):
        while True:
            subprocess.run('clear')
            print("\n--- My Cart ---")
            if not self.cart:
                print("Your cart is empty.")
                input("Press Enter to continue...")
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
                input("Press Enter to continue...")

    def remove_from_cart(self):
        subprocess.run('clear')
        print("\n--- Remove Item ---")
        for idx, equipment in enumerate(self.cart, start=1):
            print(f"{idx}. {equipment.name}")

        try:
            choice = int(input("Enter the number of the item to remove: ")) - 1
            removed_item = self.cart.pop(choice)
            print(f"{removed_item.name} has been removed from your cart.")
            input("Press Enter to continue...")
        except (ValueError, IndexError):
            print("Invalid selection. Please try again.")
            input("Press Enter to continue...")

    def proceed_to_payment(self):
        subprocess.run('clear')
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
        subprocess.run('clear')
        print("\n--- My Rents ---")
        if not self.rented_items:
            print("You have not rented any equipment.")
            input("Press Enter to continue...")
            return

        for idx, item in enumerate(self.rented_items, start=1):
            status = "Not Returned" if not item.get("returned", False) else item.get("remark", "Returned")
            extra_charge = (
                "NULL" if not item.get("returned", False)
                else f"${item['extra_charge']:.2f}" if item["extra_charge"] > 0
                else "0"
            )

            print(f"{idx}. {item['name']} (Rented: {item['rental_date']}, Due: {item['return_date']}, "
                  f"Status: {status}, Extra Charge: {extra_charge})")
        input("\nPress Enter to continue...")


class Staff(User):
    def __init__(self, email, password):
        super().__init__("Staff", email, password)

    def menu(self):
        while True:
            subprocess.run('clear')
            print("\n--- Staff Menu ---")
            print("1. View All Users")
            print("2. Search User")
            print("3. View Equipment")
            print("0. Logout")
            choice = input("Enter your choice: ")

            if choice == "1":
                self.view_users()
            elif choice == "2":
                self.search_user()
            elif choice == "0":
                print("Logging out...")
                break
            else:
                print("Invalid choice. Please try again.")
                input("Press Enter to continue...")

    def view_users(self):
        subprocess.run('clear')
        print("\n--- User List ---")
        if not system.users:
            print("No users found.")
            input("Press Enter to return...")
            return

        for idx, user in enumerate(system.users, start=1):
            print(f"{idx}. {user.name} ({user.email})")

        try:
            choice = int(input("\nEnter user number to manage rentals (or 0 to go back): ")) - 1
            if choice == -1:
                return
            if 0 <= choice < len(system.users):
                self.manage_user_rentals(system.users[choice])
            else:
                print("Invalid selection. Try again.")
                input("Press Enter to continue...")
        except ValueError:
            print("Invalid input. Please enter a valid number.")
            input("Press Enter to continue...")

    def search_user(self):
        subprocess.run('clear')
        print("\n--- Search User ---")
        search_query = input("Enter user name or email to search: ").strip().lower()

        matched_users = [
            user for user in system.users
            if search_query in user.name.lower() or search_query in user.email.lower()
        ]

        if not matched_users:
            print("No users found.")
            input("Press Enter to return...")
            return

        for idx, user in enumerate(matched_users, start=1):
            print(f"{idx}. {user.name} ({user.email})")

        try:
            choice = int(input("\nEnter user number to manage rentals (or 0 to go back): ")) - 1
            if choice == -1:
                return
            if 0 <= choice < len(matched_users):
                self.manage_user_rentals(matched_users[choice])
            else:
                print("Invalid selection. Try again.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")
        input("Press Enter to continue...")

    def manage_user_rentals(self, user):
        while True:
            subprocess.run('clear')
            print(f"\n--- Manage Rentals for {user.name} ---")
            not_returned_items = [item for item in user.rented_items if not item.get("returned", False)]

            if not not_returned_items:
                print("No rentals to return for this user.")
                input("Press Enter to go back...")
                return

            for idx, item in enumerate(not_returned_items, start=1):
                print(f"{idx}. {item['name']} (Rented: {item['rental_date']}, Due: {item['return_date']})")

            try:
                choice = int(input("\nEnter rental number to process return (or 0 to go back): ")) - 1
                if choice == -1:
                    return
                if 0 <= choice < len(not_returned_items):
                    self.process_return(not_returned_items[choice], user)
                else:
                    print("Invalid selection. Try again.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")
                input("Press Enter to continue...")

    def process_return(self, item, user):
        subprocess.run('clear')
        print("\n--- Returning Equipment ---")
        print(f"Equipment: {item['name']}")
        print(f"Rental Date: {item['rental_date']}")
        print(f"Due Date: {item['return_date']}")

        return_date = self.get_valid_date("Enter the actual return date (YYYY-MM-DD): ")
    
        # Ensure return_date is a string before comparison
        if isinstance(item["return_date"], str):
            due_date = datetime.strptime(item["return_date"], "%Y-%m-%d").date()
        else:
            due_date = item["return_date"]

        extra_charge = 0
        if return_date > due_date:
            late_days = (return_date - due_date).days
            daily_fee = next(
                equipment.daily_fee for equipment in system.equipment_list if equipment.name == item["name"]
            )
            extra_charge = late_days * daily_fee * 0.05  # Adjust late fee rate as needed
            item["remark"] = "Returned Late"
        elif return_date < due_date:
            item["remark"] = "Returned Early"
        else:
            item["remark"] = "Returned On Time"

        item["returned"] = True
        item["extra_charge"] = extra_charge
        subprocess.run('clear')
        print("\n--- Return Receipt ---")
        print(f"Client: {user.name}")
        print(f"Equipment: {item['name']}")
        print(f"Return Date: {return_date}")
        print(f"Extra Charge: ${extra_charge:.2f}")
        
        print("\nThank you for returning equipment!")
        input("Press Enter to return...")


    def get_valid_date(self, prompt):
        while True:
            date_str = input(prompt)
            try:
                return datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD.")
                


        

class Admin(User):
    def __init__(self, email, password):
        super().__init__("Admin", email, password)

    def menu(self):
        while True:
            subprocess.run('clear')
            print("\n--- Admin Menu ---")
            print("1. View Users")
            print("2. Manage Equipment")
            print("0. Logout")
            choice = input("Enter your choice: ")

            if choice == "1":
                self.view_users()
            elif choice == "2":
                self.manage_equipment()
            elif choice == "0":
                print("Logging out...")
                break
            else:
                print("Invalid choice. Please try again.")
                input("Press Enter to continue...")
                
    def view_users(self):
        while True:
            subprocess.run('clear')
            print("\n--- Registered Users ---")
            if not system.users:
                print("No users registered.")
                input("Press Enter to continue...")
                return

            for idx, user in enumerate(system.users, start=1):
                print(f"{idx}. {user.name} ({user.email})")

            try:
                choice = int(input("\nEnter the number of the user to view details (or 0 to go back): ")) - 1
                if choice == -1:
                    return

                if 0 <= choice < len(system.users):
                    self.view_user_rental_history(system.users[choice])
                else:
                    print("Invalid selection. Please try again.")
                    input("Press Enter to continue...")
            except ValueError:
                print("Invalid input. Please enter a valid number.")
                input("Press Enter to continue...")

    def view_user_rental_history(self, user):
        subprocess.run('clear')
        print(f"\n--- Rental History for {user.name} ---")
        if not user.rented_items:
            print("No rental history available for this user.")
            input("Press Enter to continue...")
            return

        for idx, item in enumerate(user.rented_items, start=1):
            status = "Not Returned" if not item.get("returned", False) else item.get("remark", "Returned")
            extra_charge = (
                "NULL" if not item.get("returned", False)
                else f"${item['extra_charge']:.2f}" if item["extra_charge"] > 0
                else "0"
            )

            print(
                f"{idx}. {item['name']} (Rented: {item['rental_date']}, Due: {item['return_date']}, "
                f"Status: {status}, Extra Charge: {extra_charge})"
            )

        input("\nPress Enter to return to the user list.")
                

    def manage_equipment(self):
        while True:
            subprocess.run('clear')
            print("\n--- Manage Equipment ---")
            print("1. Select Category")
            print("2. Search Equipment")
            print("0. Back")
            choice = input("Enter your choice: ")

            if choice == "1":
                self.select_category()
            elif choice == "2":
                self.search_equipment()
            elif choice == "0":
                return
            else:
                print("Invalid choice. Please try again.")
                input("Press Enter to continue...")

    def select_category(self):
        categories = {"1": "Camera", "2": "Lens", "3": "Lighting"}
        while True:
            subprocess.run('clear')
            print("\n--- Select Category ---")
            print("1. Camera")
            print("2. Lens")
            print("3. Lighting")
            print("0. Back")
            choice = input("Enter your choice: ")

            if choice == "0":
                return
            category = categories.get(choice)
            if category:
                self.show_and_manage_equipment(category)
            else:
                print("Invalid category. Please try again.")
                input("Press Enter to continue...")
                
    def show_and_manage_equipment(self, category):
        while True:
            subprocess.run('clear')
            print(f"\n--- {category} Equipment ---")
            available_equipment = [
                equipment for equipment in system.equipment_list if equipment.category == category
            ]

            if not available_equipment:
                print("No equipment available in this category.")
            else:
                for idx, equipment in enumerate(available_equipment, start=1):
                    print(f"{idx}. {equipment}")

            print("\nOptions:")
            print("1. Add Equipment")
            print("2. Delete Equipment")
            print("3. Update Equipment")
            print("0. Back")

            choice = input("Enter your choice: ")

            if choice == "0":
                return
            elif choice == "1":
                self.add_equipment(category)
            elif choice == "2":
                self.delete_equipment(category)
            elif choice == "3":
                self.update_equipment(category)
            else:
                print("Invalid choice. Please try again.")
                input("Press Enter to continue...")

    def add_equipment(self, category):
        subprocess.run('clear')
        print("\n--- Add Equipment ---")
        name = input("Enter equipment name: ")
        try:
            quantity = int(input("Enter equipment quantity: "))
            daily_fee = float(input("Enter daily fee: "))
        except ValueError:
            print("Invalid input. Quantity and daily fee must be numbers.")
            input("Press Enter to continue...")
            return

        new_equipment = Equipment(name, quantity, category, daily_fee)
        system.equipment_list.append(new_equipment)
        print(f"{new_equipment.name} has been added to {category}.")
        input("Press Enter to continue...")

    def delete_equipment(self, category):
        subprocess.run('clear')
        print("\n--- Delete Equipment ---")
        filtered_equipment = [
            equipment for equipment in system.equipment_list if equipment.category == category
        ]

        if not filtered_equipment:
            print("No equipment available to delete.")
            input("Press Enter to continue...")
            return

        for idx, equipment in enumerate(filtered_equipment, start=1):
            print(f"{idx}. {equipment}")

        try:
            choice = int(input("Enter the number of the equipment to delete: ")) - 1
            if 0 <= choice < len(filtered_equipment):
                removed_equipment = filtered_equipment[choice]
                system.equipment_list.remove(removed_equipment)
                print(f"{removed_equipment.name} has been deleted.")
            else:
                print("Invalid selection.")
        except ValueError:
            print("Invalid input.")
        input("Press Enter to continue...")

    def update_equipment(self, category):
        subprocess.run('clear')
        print("\n--- Update Equipment ---")
        filtered_equipment = [
            equipment for equipment in system.equipment_list if equipment.category == category
        ]

        if not filtered_equipment:
            print("No equipment available to update.")
            input("Press Enter to continue...")
            return

        for idx, equipment in enumerate(filtered_equipment, start=1):
            print(f"{idx}. {equipment}")

        try:
            choice = int(input("Enter the number of the equipment to update: ")) - 1
            if 0 <= choice < len(filtered_equipment):
                equipment_to_update = filtered_equipment[choice]
                print(f"\nUpdating {equipment_to_update.name}:")

                name = input("Enter new name (leave blank to keep current): ") or equipment_to_update.name
                quantity_input = input("Enter new quantity (leave blank to keep current): ")
                daily_fee_input = input("Enter new daily fee (leave blank to keep current): ")

                quantity = int(quantity_input) if quantity_input else equipment_to_update.quantity
                daily_fee = float(daily_fee_input) if daily_fee_input else equipment_to_update.daily_fee

                equipment_to_update.name = name
                equipment_to_update.quantity = quantity
                equipment_to_update.daily_fee = daily_fee

                print(f"{equipment_to_update.name} has been updated.")
            else:
                print("Invalid selection.")
        except ValueError:
            print("Invalid input.")
        input("Press Enter to continue...")            

    def search_equipment(self):
        while True:
            subprocess.run('clear')
            print("\n--- Search Equipment ---")
            search_name = input("Enter equipment name to search (or 0 to go back): ").strip().lower()
        
            if search_name == "0":
                return  # Go back to previous menu

            matched_equipment = [
                equipment for equipment in system.equipment_list
                if search_name in equipment.name.lower() and equipment.quantity > 0
            ]

            if not matched_equipment:
                print("No matching equipment found or all out of stock.")
                input("Press Enter to continue...")
                continue    
    
            print("\nMatched Equipment:")
            for idx, equipment in enumerate(matched_equipment, start=1):
                print(f"{idx}. {equipment.name} (Available: {equipment.quantity}, Daily Fee: ${equipment.daily_fee:.2f})")
        
            
            choice = input("\nEnter the number of equipment to add to cart (or 0 to go back): ")

            if choice == "0":
                return

            try:
                equipment_index = int(choice) - 1
                selected_equipment = matched_equipment[equipment_index]
            except (ValueError, IndexError):
                print("Invalid selection. Please try again.")
                input("Press Enter to continue...")
                continue

            self.update_or_delete_equipment(selected_equipment)
    
    def update_or_delete_equipment(self, equipment):
        while True:
            subprocess.run('clear')
            print(f"\n--- Manage Equipment: {equipment.name} ---")
            print("1. Update Equipment")
            print("2. Delete Equipment")
            print("0. Back")
            choice = input("Enter your choice: ")

            if choice == "1":
                self.update_equipment_details(equipment)
                return
            elif choice == "2":
                self.delete_selected_equipment(equipment, system.equipment_list)
                return  
            elif choice == "0":
                return 
            else:
                print("Invalid choice. Please try again.")
                input("Press Enter to continue...")

    def update_equipment_details(self, equipment):
        subprocess.run('clear')
        print(f"\nUpdating {equipment.name}:")
        name = input("Enter new name (leave blank to keep current): ") or equipment.name
        try:
            quantity_input = input("Enter new quantity (leave blank to keep current): ")
            quantity = int(quantity_input) if quantity_input else equipment.quantity

            fee_input = input("Enter new daily fee (leave blank to keep current): ")
            daily_fee = float(fee_input) if fee_input else equipment.daily_fee
        except ValueError:
            print("Invalid input. Quantity and daily fee must be numbers.")
            input("Press Enter to continue...")
            return

        equipment.name = name
        equipment.quantity = quantity
        equipment.daily_fee = daily_fee
        print(f"{equipment.name} has been updated.")
        input("Press Enter to continue...")
        return

    def delete_selected_equipment(self, equipment, equipment_list):
        subprocess.run('clear')
        confirmation = input(f"Are you sure you want to delete {equipment.name}? (y/n): ").lower()

        if confirmation == "y":
            system.equipment_list.remove(equipment)
            print(f"{equipment.name} has been deleted.")
            input("Press Enter to continue...")  
        else:
            print("Delete operation canceled.")
            input("Press Enter to continue...")


class System:
    def __init__(self):
        self.users = []
        self.equipment_list = []
        self.admin_email = "admin"
        self.admin_password = "admin"
        self.staff_email = "staff"
        self.staff_password = "staff"
        self.add_default_equipment()
        self.add_default_users()

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

    def add_default_users(self):
        # Predefined users
        user1 = Client("Aldrie Baquiran", "drei", "drei123")
        user1.rented_items = [
            {"name": "Canon EOS R5", "rental_date": datetime(2024, 12, 1).date(), "return_date": datetime(2024, 12, 5).date(), "remark": "Returned On Time", "returned": True, "extra_charge": 0},
            {"name": "Sony A7 III", "rental_date": datetime(2024, 12, 7).date(), "return_date": datetime(2024, 12, 10).date()},
        ]

        user2 = Client("Bob Mendoza", "bob17@gmail.com", "bob17")
        user2.rented_items = [
            {"name": "Fujifilm X-T4", "rental_date": datetime(2024, 12, 3).date(), "return_date": datetime(2024, 12, 6).date(), "remark": "Returned Late", "returned": True, "extra_charge": 20},
        ]

        user3 = Client("Charlie Pot", "charlie03@gmail.com", "charlie3")
        user3.rented_items = []

        user4 = Client("Claire Cabral", "claire09@gmail.com", "claire09")
        user4.rented_items = [
            {"name": "Canon 50mm f/1.2", "rental_date": datetime(2024, 12, 2).date(), "return_date": datetime(2024, 12, 4).date(), "remark": "Returned Early", "returned": True, "extra_charge": 0},
        ]

        user5 = Client("Clarisse Cabral", "clarisse15@gmail.com", "clarisse15")
        user5.rented_items = [
            {"name": "Sony 24-70mm f/2.8", "rental_date": datetime(2024, 12, 5).date(), "return_date": datetime(2024, 12, 9).date()},
        ]

        self.users.extend([user1, user2, user3, user4, user5])

    def create_account(self):
        subprocess.run('clear')
        print("\n--- Create Account ---")
        name = input("Enter your name: ")
        email = input("Enter your email: ")
        password = input("Enter your password: ")

        for user in self.users:
            if user.email == email:
                print("This email is already registered. Please try again.")
                input("Press Enter to continue...")
                return

        new_user = Client(name, email, password)
        self.users.append(new_user)
        print("Account created successfully! Please log in.")
        input("Press Enter to continue...")

    def login(self):
        subprocess.run('clear')
        print("\n--- Login ---")
        email = input("Enter your email: ")
        password = input("Enter your password: ")

        if email == self.admin_email and password == self.admin_password:
            admin = Admin(email, password)
            admin.menu()
        elif email == self.staff_email and password == self.staff_password:
            staff = Staff(email, password)
            staff.menu()
        else:
            for user in self.users:
                if user.email == email and user.password == password:
                    user.menu()
                    return
            print("Invalid credentials. Please try again.")
            input("Press Enter to continue...")

    def run(self):
        while True:
            subprocess.run('clear')
            print("--- Online Film Equipment Reservation ---\n")
            print("1. Login")
            print("2. Create Account")
            print("0. Exit")
            choice = input("Enter your choice: ")

            if choice == "1":
                self.login()
            elif choice == "2":
                self.create_account()
            elif choice == "0":
                print("Existing...")
                break
            else:
                print("Invalid choice. Please try again.")
                input("Press Enter to continue...")


system = System()
system.run()
    