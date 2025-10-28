''' 

Basic E-commerce Platform Simulation

Code edits sourced from https://gemini.google.com/

2025

'''
import getpass

# a database of registered users
REGISTERED_USERS = {
    'admin': {'password': 'admin123', 'account_type': 'admin'},
    'seller1': {'password': 'seller123', 'account_type': 'seller'},
    'buyer1': {'password': 'buyer123', 'account_type': 'buyer'},
}

# a database of products
PRODUCT_DB = [
    {
        'id': 1,
        'name': 'Vintage T-Shirt',
        'description': 'A cool old t-shirt',
        'price': 25.00,
        'manufacturer': 'OldNavy',
        'date_of_manufacturer': '2005-01-01',
        'UserOwner': 'seller1'
    },
    {
        'id': 2,
        'name': 'Laptop',
        'description': 'A powerful laptop',
        'price': 1200.00,
        'manufacturer': 'TechCorp',
        'date_of_manufacturer': '2023-05-10',
        'UserOwner': 'seller1'
    }
]

# --- User Class and Permission Management ---

class User:
    #A class to hold user data and permissions.
    def __init__(self, username, account_type):
        self.username = username
        self.account_type = account_type
        self.permissions = {
            'admin': False,
            'seller': False,
            'buyer': False
        }
        self._assign_permissions()

    def _assign_permissions(self):
        if self.account_type == 'admin':
            self.permissions['admin'] = True
            self.permissions['seller'] = True
            self.permissions['buyer'] = True

        elif self.account_type == 'seller':
            self.permissions['seller'] = True
            self.permissions['buyer'] = True
        elif self.account_type == 'buyer':
            self.permissions['buyer'] = True



# --- Login Function ---

def login():
    # Handles the user login process.
    # Check User for Login:
    # PROMPT user for UserName and InputPassword
    print("--- Login ---")
    username = input("Enter UserName: ")
    password = input("Enter Password: ")

    # IF user is in RegisteredUsers THEN
    if username in REGISTERED_USERS:
        user_data = REGISTERED_USERS[username]
        
        # IF InputPassword is equal to the password stored for RegisteredUser
        if password == user_data['password']:
            # PRINT “Access Granted”
            print("\nAccess Granted.")
            # Return account type
            print(f"Account Type: {user_data['account_type']}")
            return User(username, user_data['account_type'])
        else:

            print("\nAccess Denied: Incorrect password.")

    else:
        # PRINT “User not found”
        print("\nAccess Denied: User not found.")


# --- Role-Specific Control Functions ---
def admin_manage_users(user, user_db):
    # Allows admin to list, add, and delete users from REGISTERED_USERS dictionary.
    print(f"\n--- Admin User Management ---")
    print("Available Actions: [list], [add], [delete], [exit]")
    while True:
        action = input("Admin Action: ").lower().strip()
        if action == 'exit':
            break #return to main admin dashboard
        elif action == 'list': #list users
            print("\nRegistered Users:")
            for username, data in user_db.items():
                print(f"  Username: {username}, Account Type: {data['account_type']}")
        elif action == 'add': #add user
            print("Enter new user details:")
            username = input("  New Username: ")
            if username in user_db:
                print("  Error: Username already exists.")
                continue # go back to user action
            password = input("  Password: ")
            account_type = input("  Account Type (admin/seller/buyer): ").lower()
            if account_type not in ['admin', 'seller', 'buyer']:
                print("  Error: Invalid account type.")
                continue
            user_db[username] = {'password': password, 'account_type': account_type}
            print(f"  User '{username}' added successfully as a {account_type}.")
        elif action == 'delete': #delete user
            username = input("Enter Username to delete: ")
            if username not in user_db:
                print("  Error: Username not found.")
                continue
            if username == user.username:
                print("  Error: You cannot delete your own account while logged in.")
                continue
            del user_db[username]
            print(f"  User '{username}' deleted successfully.")
        else: #invalid action
            print("Invalid action. Try [list], [add], [delete], or [exit].")
    print ("--- Exiting User Management ---")
def show_admin_controls(user):

    # IF user has admin privilege
    if not user.permissions['admin']:
        return # Should not happen if called correctly, but good practice

    print(f"\n--- ADMIN DASHBOARD: {user.username} ---")
    print("-----------------------")
    while True:
        print("Admin Actions:")
        print("  [1] Manage Products (Full Access)")
        print("  [2] Manage Users")
        print("  [3] Log Out")
        action = input("Admin Action: ").strip()

        if action == '1':
            show_seller_controls(user, PRODUCT_DB, is_admin_mode=True)
        elif action == '2':
            admin_manage_users(user, REGISTERED_USERS)
        elif action == '3':
            break
        else:
            print("Invalid action. Please try again.")
    print("-----------------------")

def show_seller_controls(user, product_db, is_admin_mode=False):
    # the Seller dashboard.
    # Seller Access:
    # IF user has seller privilege
    if not user.permissions['seller']:
        return

    if user.permissions['admin']:
        print(f"\n--- ADMIN PRODUCT MANAGEMENT: {user.username} ---")
    else:
        print(f"\n--- SELLER DASHBOARD: {user.username} ---")
    # ALLOW access to Seller_Page and Pricing_Controls
    print("Available actions: [list], [add], [update], [delete], [exit]")
    
    while True:
        action = input("Seller Action: ").lower().strip()

        if action == 'exit':
            break

        # DISPLAY existing product list from PRODUCT_DB
        elif action == 'list':
            print("\nYour Products:")
            found_products = False
            for item in product_db:
                if item['UserOwner'] == user.username or is_admin_mode:
                    print(f"  ID {item['id']}: {item['name']} - ${item['price']:.2f}")
                    found_products = True
            if not found_products:
                print("  You have no products listed.")

        # IF product selected for deletion,
        elif action == 'delete':
            try:
                prod_id = int(input("Enter Product ID to delete: "))
                product_to_delete = None
                for item in product_db:
                    if item['id'] == prod_id:
                        product_to_delete = item
                        break
                
                if product_to_delete:
                    # Check User == UserOwner in PRODUCT_DB
                    # IF CheckUser is True
                    if product_to_delete['UserOwner'] == user.username or is_admin_mode:
                        # Delete Product
                        product_db.remove(product_to_delete)
                        print(f"Product ID {prod_id} deleted.")
                    else:
                        print("Error: You do not own this product.")
                else:
                    print("Error: Product ID not found.")
            except ValueError:
                print("Error: Invalid ID.")

        # IF product selected for price adjustment
        elif action == 'update':
            try:
                prod_id = int(input("Enter Product ID to update price: "))
                product_to_update = None
                for item in product_db:
                    if item['id'] == prod_id:
                        product_to_update = item
                        break
                
                if product_to_update:
                    # CheckUser == UserOwner in PRODUCT_DB
                    # IF CheckUser is True
                    if product_to_update['UserOwner'] == user.username or is_admin_mode:
                        # setPrice = input price
                        new_price = float(input("Enter new price: "))
                        product_to_update['price'] = new_price
                        print(f"Product ID {prod_id} price updated to ${new_price:.2f}.")
                    else:
                        print("Error: You do not own this product.")
                else:
                    print("Error: Product ID not found.")
            except ValueError:
                print("Error: Invalid ID or price.")

        # IF new product
        elif action == 'add':
            print("Enter new product details:")
            # New product = PROMPT user for ProductName
            # Input Title, description, price, manufacturer, date of manufacturer.
            name = input("  Name/Title: ")
            desc = input("  Description: ")
            price = float(input("  Price: "))
            manu = input("  Manufacturer: ")
            date_manu = input("  Date of Manufacturer (YYYY-MM-DD): ")
            
            # Improvement: Generate a new unique ID
            new_id = max(item['id'] for item in product_db) + 1
            
            if is_admin_mode:
                owner = input(" Enter Owner Username: ")
            else:
                owner = user.username
            new_product = {
                'id': new_id,
                'name': name,
                'description': desc,
                'price': price,
                'manufacturer': manu,
                'date_of_manufacturer': date_manu,
                # APPEND UserOwner to ProductNameDescription
                'UserOwner': owner
            }
            
            # APPEND New_product to PRODUCT_DB
            product_db.append(new_product)
            print(f"New product '{name}' (ID: {new_id}) added successfully.")
        
        else:
            print("Invalid action. Try [list], [add], [update], [delete], or [exit].")
    
    print("--------------------------------------")


def show_buyer_controls(user, product_db):
    # the Buyer marketplace and purchase flow.
    # Buyer Access:
    # IF user has buyer privileges
    if not user.permissions['buyer']:
        return

    print(f"\n--- MARKETPLACE: Welcome, {user.username} ---")
    # ALLOW access to product list,
    # DISPLAY Marketplace
    # DISPLAY only applied items
    for item in product_db:
        print(f"  ID {item['id']}: {item['name']} - ${item['price']:.2f} (Sold by: {item['UserOwner']})")
    
    # ALLOW access to purchase button
    # IF PurchaseButton Clicked
    if input("\nDo you want to purchase an item? (yes/no): ").lower() == 'yes':
        try:
            prod_id = int(input("Enter Product ID to purchase: "))
            product_to_buy = None
            for item in product_db:
                if item['id'] == prod_id:
                    product_to_buy = item
                    break
            
            if not product_to_buy:
                print("Invalid product ID.")
                return

            print(f"Purchasing '{product_to_buy['name']}' for ${product_to_buy['price']:.2f}.")
            
            # PROMPT input for address and personal information
            
            # INPUT PaymentType: CreditCard/DebitCard/paypal
            payment_type = input("Enter Payment Type (CreditCard/DebitCard/paypal): ")
            payment_successful = False
            # Process payment ( CARD #, Expieration , CVV)
            # (Simulated by the process_payment function)
            payment_successful = process_payment(payment_type)

            # IF PaymentSuccessful == TRUE
            if payment_successful:
                # SET PaymentSuccessful = TRUE
                print("\nPayment Successful.")
                # PROMPT User for ShippingDetails
                print("Please enter shipping details:")
                # User INPUT City
                city = input("  City: ")
                # User INPUT Address
                address = input("  Address: ")
                # User INPUT PostalCode
                postal_code = input("  Postal Code: ")

                # If AddressValid == TRUE (Simulating as always true)
                address_valid = True 
                if address_valid:
                    # PRINT “Order Placed. Confirmation: [###]”
                    print("\nOrder Placed. Confirmation: #123456789")
                    # SendShippingInfoTo(City,Address,ID,PostalCode)
                    print(f"Shipping info sent for: {address}, {city}, {postal_code}")
                # ELSE
                else:
                    # PRINT “Order Failed. Please try again.”
                    print("Order Failed: Invalid address.")
            # ELSE
            else:
                # PRINT “Payment Failed. Please try again.”
                print("\nPayment Failed. Please try again.")

        except ValueError:
            print("Invalid input.")
    
    print("-----------------------------------")


def process_payment(payment_type):
    #Simulated payment processing function.
    # IF PaymentType == CreditCard
    if payment_type.lower() == 'creditcard':
        # PROMPT User For:
        # Card Number
        while True: 
            credit_card_num = input(" 16-digit Card Number: ")
            if len(credit_card_num) != 16 or not credit_card_num.isdigit():
                print("  Invalid Card Number. Please ensure you have entered your 16-digit card number correctly.")
            else:
                break
        # Card Expiration
        while True:
            expiry = input(" Enter 4-digit expiry (MM/YY): ")
            if len(expiry) == 4 and expiry.isdigit():
                month = int(expiry[:2])
                if month < 1 or month > 12:
                    print("  Invalid Expiration Month.")
                else:
                    break
            else:
                print("  Expiration must be exactly 4 digits.")
        # Card CVV
        cvv = input(" Enter 3-digit Card CVV: ")
        if len(cvv) == 3 and cvv.isdigit():
            pass  # CVV valid
        else:
            print("  Invalid CVV.")
            return False

    # IF PaymentType == DebitCard
    elif payment_type.lower() == 'debitcard':
        # PROMPT User For
        # Card Number
        while True:
            debit_card_num = input(" 16-digit Card Number: ")
            if len(debit_card_num) != 16 or not debit_card_num.isdigit():
                print("  Invalid Card Number. Please ensure you have entered your 16-digit card number correctly.")
            else:
                break
        # AccountType (Chequing/Savings)
        input("  Account Type (Chequing/Savings): ")
        # PIN
        getpass.getpass("  PIN: ")
    # IF PaymentType == paypal
    elif payment_type.lower() == 'paypal':
        # REDIRECT User to
        # Paypal Portal
        print("  ...Redirecting to PayPal portal (simulated)...")
    else:
        print("  Invalid payment type.")
        return False
    
    print("  ...Processing payment...")
    # IF paymentProcess returns TRUE then
    # (Simulating a successful payment)
    return True
    # ELSE
    # (This mock function always succeeds for demo purposes)


# --- Main Application ---

def main():
    while True:
        current_user = None
        
        # Loop until a successful login
        while not current_user:
            current_user = login()
            # Else: (DENY USER FROM WEBSITE ACCESS)
            # Return to login
            if not current_user:
                print("Please try again.")

        # Show GUI/controls based on user account:
        
        # Admin Access:
        if current_user.account_type == 'admin':
            show_admin_controls(current_user)

        # Seller Access:
        elif current_user.account_type == 'seller':
            show_seller_controls(current_user, PRODUCT_DB)

        # Buyer Access:
        elif current_user.account_type == 'buyer':
            show_buyer_controls(current_user, PRODUCT_DB)
        
        print(f"\nUser {current_user.username} logged out.")

        if input("Exit ordering system? (yes/no): ").lower() == 'yes':
            print("Exiting system. Goodbye!")
            break

main()