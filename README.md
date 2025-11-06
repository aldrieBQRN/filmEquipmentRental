# Film Equipment Rental System (CLI)

A command-line interface (CLI) application for managing the rental of film equipment, built with Python. This system allows clients to register, browse equipment, rent items, and manage returns. It also provides an admin panel for user management and equipment inventory control.

The entire application is contained within a single Python script: `filmEquipmentRental.py`.

## Key Features

### Client Features
* **Account Management:** Clients can create a new account and log in.
* **Browse & Rent:** Browse equipment by category (Camera, Lens, Lighting) and add available items to a shopping cart.
* **Cart Management:** View all items in the cart, see the total daily fee, and remove items.
* **Payment & Checkout:** Proceed to payment, select rental and return dates (in YYYY-MM-DD format), and receive a complete receipt. Inventory quantity is automatically updated upon rental.
* **View Rentals:** Check a personal history of all rented items, including their due dates and return status.
* **Return Equipment:** Process the return of an item. The system calculates and displays extra charges for late returns (based on a 0.5% daily fee penalty).

### Admin Features
* **Secure Login:** Access a separate admin dashboard with a unique login.
* **View Users:** List all registered clients.
* **View User History:** Select a specific user to see their complete rental history, including return status and any extra charges.
* **View Equipment:** View all available equipment, sorted by category.
* **Add Equipment:** Add new equipment to the system's inventory by providing a name, quantity, daily fee, and category.

## Technology Stack
* **Language:** Python 3
* **Standard Libraries:**
    * `datetime` (for handling rental and return dates)
    * `subprocess` (for clearing the console screen)

## How to Run

1.  **Prerequisites:** Ensure you have [Python 3](https://www.python.org/downloads/) installed on your system.
2.  **Save the File:** Save the code as `filmEquipmentRental.py`.
3.  **Run from Terminal:** Open your terminal or command prompt, navigate to the directory where you saved the file, and run the following command:
    ```bash
    python filmEquipmentRental.py
    ```
4.  **Follow Prompts:** The application will start, presenting you with the main menu to log in or create an account.

## Default Logins

The system is pre-populated with one admin account and several client accounts for testing.

### Admin
* **Email:** `admin`
* **Password:** `admin`

### Default Clients
You can also log in as any of the pre-defined clients:
* **Email:** `drei` | **Password:** `drei123`
* **Email:** `bob17@gmail.com` | **Password:** `bob17`
* **Email:** `charlie03@gmail.com` | **Password:** `charlie3`
* (and 2 others as defined in the `add_default_users` function)
