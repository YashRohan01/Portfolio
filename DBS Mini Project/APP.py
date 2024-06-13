import tkinter as tk
from tkinter import messagebox
import cx_Oracle
import datetime

# Database connection settings
DB_USERNAME = 'system'
DB_PASSWORD = '1234'
DB_HOST = 'Ash_Machine'
DB_PORT = '1521'
DB_SERVICE = 'XE'

class RegistrationApp:
    def __init__(self, master, login_app):
        self.master = master
        self.master.title("Registration")
        self.login_app = login_app

        self.username_label = tk.Label(self.master, text="Username:")
        self.username_label.grid(row=0, column=0, padx=10, pady=10)

        self.username_entry = tk.Entry(self.master)
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)

        self.password_label = tk.Label(self.master, text="Password:")
        self.password_label.grid(row=1, column=0, padx=10, pady=10)

        self.password_entry = tk.Entry(self.master, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)

        self.contact_label = tk.Label(self.master, text="Contact:")
        self.contact_label.grid(row=2, column=0, padx=10, pady=10)

        self.contact_entry = tk.Entry(self.master)
        self.contact_entry.grid(row=2, column=1, padx=10, pady=10)

        self.address_label = tk.Label(self.master, text="Address:")
        self.address_label.grid(row=3, column=0, padx=10, pady=10)

        self.address_entry = tk.Entry(self.master)
        self.address_entry.grid(row=3, column=1, padx=10, pady=10)

        self.register_button = tk.Button(self.master, text="Register", command=self.register)
        self.register_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    def register(self):
        # Get user input from entry fields
        username = self.username_entry.get()
        password = self.password_entry.get()
        contact = self.contact_entry.get()
        address = self.address_entry.get()

        try:
            # Connect to the database
            connection = cx_Oracle.connect(DB_USERNAME, DB_PASSWORD, f"{DB_HOST}:{DB_PORT}/{DB_SERVICE}")
            cursor = connection.cursor()

            # Get the count of existing customers
            cursor.execute("SELECT COUNT(*) FROM customer")
            customer_count = cursor.fetchone()[0]

            # Generate customer ID by adding 1 to the count
            customer_id = customer_count + 1

            # Insert customer details into the database
            cursor.execute("INSERT INTO customer (customer_id, name, password, contact, address) VALUES (:1, :2, :3, :4, :5)",
                           (customer_id, username, password, contact, address))
            connection.commit()  # Commit the transaction

            # Assuming registration is successful, open the shopping app
            self.open_shopping_app(customer_id)

        except cx_Oracle.Error as error:
            messagebox.showerror("Database Error", f"Error: {error}")
        finally:
            cursor.close()
            connection.close()

    def open_shopping_app(self, customer_id):
        # Close the registration app window
        self.master.destroy()

        # Open the shopping app
        shopping_root = tk.Tk()
        shopping_app = ShoppingApp(shopping_root, customer_id)
        shopping_root.mainloop()

class LoginApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Login")

        self.registration_app = None

        self.username_label = tk.Label(self.master, text="Username:")
        self.username_label.grid(row=0, column=0, padx=10, pady=10)

        self.username_entry = tk.Entry(self.master)
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)

        self.password_label = tk.Label(self.master, text="Password:")
        self.password_label.grid(row=1, column=0, padx=10, pady=10)

        self.password_entry = tk.Entry(self.master, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)

        self.login_button = tk.Button(self.master, text="Login", command=self.login)
        self.login_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        self.register_button = tk.Button(self.master, text="Register", command=self.open_registration)
        self.register_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Connect to the database
        connection = cx_Oracle.connect(DB_USERNAME, DB_PASSWORD, f"{DB_HOST}:{DB_PORT}/{DB_SERVICE}")
        cursor = connection.cursor()

        try:
            cursor.execute("SELECT customer_id FROM customer WHERE name = :username AND password = :password",
                           {"username": username, "password": password})
            result = cursor.fetchone()
            if result:
                self.customer_id = result[0]  # Store customer_id after successful login
                self.master.destroy()  # Close the login window
                self.open_main_window()  # Open the main window
            else:
                messagebox.showerror("Login Failed", "Invalid username or password")
        except cx_Oracle.Error as error:
            messagebox.showerror("Database Error", f"Error: {error}")

    def open_registration(self):
        self.master.destroy()
        root = tk.Tk()
        self.registration_app = RegistrationApp(root, self)
        root.mainloop()
        
    def open_main_window(self):
        root = tk.Tk()
        app = ShoppingApp(root, self.customer_id)
        root.mainloop()

        
class ConfirmationWindow:
    def __init__(self, master, total_price):
        self.master = master
        self.master.title("Confirm Order")

        self.total_price = total_price

        self.confirm_label = tk.Label(self.master, text=f"Total Price: Rs{total_price}")
        self.confirm_label.pack(padx=10, pady=10)

        self.confirm_button = tk.Button(self.master, text="Confirm Order", command=self.confirm_order)
        self.confirm_button.pack(padx=10, pady=10)

    def confirm_order(self):
        # Execute PL/SQL procedure here to confirm the order
        # You can add your PL/SQL procedure call here
        messagebox.showinfo("Order Confirmed", "Your order has been confirmed.")
        self.master.destroy()

class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

class ShoppingCart:
    def __init__(self):
        self.items = []

    def add_item(self, product):
        self.items.append(product)

    def remove_item(self, index):
        del self.items[index]
        
class ShoppingApp:
    def __init__(self, master, customer_id):
        self.master = master
        self.master.title("Online Shopping Platform")
        self.name = ""
        
        self.customer_id = customer_id

        self.total_cost = 0  # Initialize total cost attribute

        self.criteria_var = tk.StringVar()
        self.criteria_var.set("Genre")

        self.search_label = tk.Label(self.master, text="Search:")
        self.search_label.grid(row=0, column=0, padx=10, pady=10)

        self.criteria_dropdown = tk.OptionMenu(self.master, self.criteria_var, "Genre", "Company", "Price")
        self.criteria_dropdown.grid(row=0, column=1, padx=10, pady=10)

        self.search_entry = tk.Entry(self.master, width=30)
        self.search_entry.grid(row=0, column=2, padx=10, pady=10)

        self.search_button = tk.Button(self.master, text="Search", command=self.search_products)
        self.search_button.grid(row=0, column=3, padx=10, pady=10)

        self.product_listbox = tk.Listbox(self.master, width=50)
        self.product_listbox.grid(row=1, column=0, padx=10, pady=10, columnspan=4)

        self.shopping_cart = ShoppingCart()

        self.add_to_cart_button = tk.Button(self.master, text="Add to Cart", command=self.add_to_cart)
        self.add_to_cart_button.grid(row=2, column=1, padx=10, pady=10)

        self.shopping_cart_label = tk.Label(self.master, text="Shopping Cart:")
        self.shopping_cart_label.grid(row=3, column=1)

        self.shopping_cart_listbox = tk.Listbox(self.master, width=50)
        self.shopping_cart_listbox.grid(row=4, column=0, padx=10, pady=10, columnspan=4)

        self.checkout_button = tk.Button(self.master, text="Checkout", command=self.checkout)
        self.checkout_button.grid(row=7, column=1, padx=10, pady=10)
        
        self.total_price_label = tk.Label(self.master, text="Total Price: Rs. 0.00")
        self.total_price_label.grid(row=6, column=1, padx=10, pady=10)

        # Populate the product listbox
        self.populate_product_listbox()

    def populate_product_listbox(self):
        # Connect to the database
        connection = cx_Oracle.connect(DB_USERNAME, DB_PASSWORD, f"{DB_HOST}:{DB_PORT}/{DB_SERVICE}")
        cursor = connection.cursor()

        try:
            # Execute SQL query to select all product names and prices
            cursor.execute("SELECT name, price FROM product")

            # Fetch and display product names and prices
            for result in cursor:
                product_info = f"{result[0]} - Rs {result[1]}"
                self.product_listbox.insert(tk.END, product_info)
        except cx_Oracle.Error as error:
            messagebox.showerror("Database Error", f"Error: {error}")
        finally:
            cursor.close()
            connection.close()

    def search_products(self):
        search_term = self.search_entry.get().lower()
        search_criteria = self.criteria_var.get().lower()

        # Connect to the database
        connection = cx_Oracle.connect(DB_USERNAME, DB_PASSWORD, f"{DB_HOST}:{DB_PORT}/{DB_SERVICE}")
        cursor = connection.cursor()

        try:
            # Execute SQL query based on selected search criteria
            if search_criteria == "genre":
                cursor.execute("SELECT name, price FROM product WHERE LOWER(genre) LIKE '%' || :search_term || '%'", {"search_term": search_term})
            elif search_criteria == "company":
                cursor.execute("SELECT name, price FROM product WHERE LOWER(company) LIKE '%' || :search_term || '%'", {"search_term": search_term})
            elif search_criteria == "price":
                cursor.execute("SELECT name, price FROM product WHERE price = :search_term", {"search_term": float(search_term)})

            # Fetch and display search results
            self.product_listbox.delete(0, tk.END)
            for result in cursor:
                product_info = f"{result[0]} - Rs {result[1]}"
                self.product_listbox.insert(tk.END, product_info)
        except cx_Oracle.Error as error:
            messagebox.showerror("Database Error", f"Error: {error}")
        finally:
            cursor.close()
            connection.close()

    def add_to_cart(self):
        selected_index = self.product_listbox.curselection()
        if selected_index:
            # Add the newly selected product to the shopping cart
            selected_product_info = self.product_listbox.get(selected_index[0])  # Get the selected product info
            selected_product_name = selected_product_info.split(' - ')[0]  # Extract product name
            selected_product_price = selected_product_info.split(' - ')[1]  # Extract product price
            # Remove any non-numeric characters from the price string before converting to float
            selected_product_price = float(''.join(filter(str.isdigit, selected_product_price)))
            selected_product = Product(selected_product_name, selected_product_price)
            self.shopping_cart.add_item(selected_product)
        
            # Update the name attribute of the class with concatenated names of all products in the shopping cart
            self.name = ", ".join([product.name for product in self.shopping_cart.items])
        
            # Clear and re-populate the shopping cart listbox
            self.shopping_cart_listbox.delete(0, tk.END)
            for item in self.shopping_cart.items:
                self.shopping_cart_listbox.insert(tk.END, item.name)
        
            self.update_total_price()
    
    def update_total_price(self):
        total_price = sum(product.price for product in self.shopping_cart.items)
        self.total_price_label.config(text=f"Total Price: Rs. {total_price:.2f}")

    def checkout(self):
        # Calculate total cost
        total_cost = sum(self.fetch_product_price(product.name) for product in self.shopping_cart.items)

        # Open confirmation window
        self.open_confirmation(total_cost)
        
    def fetch_product_price(self, product_name):
        # Connect to the database
        connection = cx_Oracle.connect(DB_USERNAME, DB_PASSWORD, f"{DB_HOST}:{DB_PORT}/{DB_SERVICE}")
        cursor = connection.cursor()

        try:
            # Execute SQL query to fetch the price of the product
            cursor.execute("SELECT price FROM product WHERE name = :product_name", {"product_name": product_name})
            result = cursor.fetchone()
            if result:
                return result[0]
            else:
                return 0  # If price is not found, return 0
        except cx_Oracle.Error as error:
            messagebox.showerror("Database Error", f"Error: {error}")
            return 0
        finally:
            cursor.close()
            connection.close()
            
    def open_confirmation(self, total_cost):
        confirmation_window = tk.Toplevel(self.master)
        confirmation_window.title("Confirmation")

        confirmation_label = tk.Label(confirmation_window, text="Are you sure you want to checkout?")
        confirmation_label.pack()

        confirm_button = tk.Button(confirmation_window, text="Confirm", command=lambda: self.process_checkout(total_cost))
        confirm_button.pack()
    
    def process_checkout(self, total_cost):
        # Prepare the product IDs string
        product_ids = [str(self.fetch_product_id(product.name)) for product in self.shopping_cart.items]
        product_ids_str = ','.join(product_ids)

        # Prepare the products string
        products = ', '.join([product.name for product in self.shopping_cart.items])

        try:
            with cx_Oracle.connect(DB_USERNAME, DB_PASSWORD, f"{DB_HOST}:{DB_PORT}/{DB_SERVICE}") as connection:
                with connection.cursor() as cursor:
                    # Call the process_checkout procedure and pass the required parameters
                    cursor.callproc("process_checkout", [self.customer_id, total_cost, product_ids_str, products])
                    messagebox.showinfo("Checkout Successful", "Your order has been placed successfully!")
                    self.master.destroy()  # Close the shopping app window after checkout

                    # Get the last order ID
                    cursor.execute("SELECT MAX(order_id) FROM orders")
                    last_order_id = cursor.fetchone()[0]

                    # Execute the SQL query after the procedure call
                    cursor.execute("""
                    DECLARE 
                    v_shipping_id shipping_info.shipping_id%TYPE;
                    v_products shipping_info.products%TYPE;
                    v_address shipping_info.shipping_address%TYPE;
                    v_shipping_date DATE := SYSDATE; -- Set shipping date to current date
                    BEGIN
                    SELECT COUNT(*) + 1 INTO v_shipping_id FROM shipping_info;
                    SELECT products INTO v_products FROM orders WHERE order_id = :last_order_id;
                    SELECT address INTO v_address FROM customer WHERE customer_id = :customer_id;
                    INSERT INTO shipping_info VALUES (v_shipping_id, v_products, v_address, v_shipping_date, v_shipping_date + 7);
                    COMMIT; -- Commit the transaction
                    END;
                    """, last_order_id=last_order_id, customer_id=self.customer_id)
                    # Delete the window and show order completion message
                    self.show_order_completion_message(total_cost)
        except cx_Oracle.Error as error:
            # Handle exceptions
            messagebox.showerror("Database Error", f"Error: {error}")


    def show_order_completion_message(self, total_cost):
        try:
            # Calculate delivery date (1 week after the current date)
            delivery_date = datetime.datetime.now() + datetime.timedelta(days=7)
            delivery_date_str = delivery_date.strftime("%Y-%m-%d")  # Convert delivery date to string format

            # Display the message box with delivery date and total cost
            messagebox.showinfo("Order Completed", f"Your order has been completed successfully!\nDelivery Date: {delivery_date_str}\nTotal Cost: Rs. {total_cost:.2f}")
        except Exception as e:
            # Handle exceptions
            messagebox.showerror("Error", f"An error occurred: {e}")
    
    def fetch_product_id(self, product_name):
        # Connect to the database and fetch the product ID
        try:
            with cx_Oracle.connect(DB_USERNAME, DB_PASSWORD, f"{DB_HOST}:{DB_PORT}/{DB_SERVICE}") as connection:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT product_id FROM product WHERE name = :product_name", {"product_name": product_name})
                    result = cursor.fetchone()
                    if result:
                        return result[0]
                    else:
                        return None
        except cx_Oracle.Error as error:
            messagebox.showerror("Database Error", f"Error: {error}")
            return None


def main():
    root = tk.Tk()
    login_app = LoginApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
