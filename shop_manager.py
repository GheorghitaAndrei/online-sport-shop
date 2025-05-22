import sqlite3
from datetime import datetime
import os

class ShopManager:
    def __init__(self, db_name="shop.db"):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.current_user = None
        
    def connect(self):
        """Connect to the SQLite database"""
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        
    def close(self):
        """Close the database connection"""
        if self.conn:
            self.conn.close()
            
    def login(self, email, password):
        """Login a user"""
        self.connect()
        self.cursor.execute("""
            SELECT client_id, first_name, last_name 
            FROM users 
            WHERE email = ? AND password = ?
        """, (email, password))
        user = self.cursor.fetchone()
        if user:
            self.current_user = {
                'client_id': user[0],
                'first_name': user[1],
                'last_name': user[2]
            }
            return True
        return False
    
    def get_products(self):
        """Get all available products with their categories"""
        self.connect()
        self.cursor.execute("""
            SELECT p.product_id, p.product_name, p.price, c.category_name, i.quantity
            FROM products p
            JOIN categories c ON p.category_id = c.category_id
            JOIN inventory i ON p.product_id = i.product_id
            WHERE i.quantity > 0
            ORDER BY c.category_name, p.product_name
        """)
        return self.cursor.fetchall()
    
    def add_to_cart(self, product_id, quantity=1):
        """Add a product to cart"""
        if not self.current_user:
            return False, "User not logged in"
            
        self.connect()
        try:
            # Check if product exists and has enough quantity
            self.cursor.execute("""
                SELECT quantity FROM inventory 
                WHERE product_id = ?
            """, (product_id,))
            available = self.cursor.fetchone()
            
            if not available:
                return False, "Product not found"
            if available[0] < quantity:
                return False, "Not enough quantity available"
                
            # Try to insert or update cart
            self.cursor.execute("""
                INSERT INTO cart (client_id, product_id, quantity)
                VALUES (?, ?, ?)
                ON CONFLICT(client_id, product_id) 
                DO UPDATE SET quantity = quantity + ?
            """, (self.current_user['client_id'], product_id, quantity, quantity))
            
            self.conn.commit()
            return True, "Product added to cart"
            
        except sqlite3.Error as e:
            return False, f"Error: {str(e)}"
    
    def update_cart_quantity(self, product_id, new_quantity):
        """Update quantity of a product in cart"""
        if not self.current_user:
            return False, "User not logged in"
            
        self.connect()
        try:
            # Check if product exists in cart
            self.cursor.execute("""
                SELECT quantity FROM cart 
                WHERE client_id = ? AND product_id = ?
            """, (self.current_user['client_id'], product_id))
            cart_item = self.cursor.fetchone()
            
            if not cart_item:
                return False, "Product not in cart"
                
            # Check if enough quantity available
            self.cursor.execute("""
                SELECT quantity FROM inventory 
                WHERE product_id = ?
            """, (product_id,))
            available = self.cursor.fetchone()
            
            if available[0] < new_quantity:
                return False, "Not enough quantity available"
                
            if new_quantity <= 0:
                # Remove item from cart if quantity is 0 or negative
                self.cursor.execute("""
                    DELETE FROM cart 
                    WHERE client_id = ? AND product_id = ?
                """, (self.current_user['client_id'], product_id))
            else:
                # Update quantity
                self.cursor.execute("""
                    UPDATE cart 
                    SET quantity = ? 
                    WHERE client_id = ? AND product_id = ?
                """, (new_quantity, self.current_user['client_id'], product_id))
                
            self.conn.commit()
            return True, "Cart updated successfully"
            
        except sqlite3.Error as e:
            return False, f"Error: {str(e)}"
    
    def remove_from_cart(self, product_id):
        """Remove a product from cart"""
        if not self.current_user:
            return False, "User not logged in"
            
        self.connect()
        try:
            self.cursor.execute("""
                DELETE FROM cart 
                WHERE client_id = ? AND product_id = ?
            """, (self.current_user['client_id'], product_id))
            self.conn.commit()
            return True, "Product removed from cart"
        except sqlite3.Error as e:
            return False, f"Error: {str(e)}"
    
    def view_cart(self):
        """View current cart contents"""
        if not self.current_user:
            return None, "User not logged in"
            
        self.connect()
        try:
            self.cursor.execute("""
                SELECT p.product_id, p.product_name, p.price, c.quantity, 
                       (p.price * c.quantity) as total
                FROM cart c
                JOIN products p ON c.product_id = p.product_id
                WHERE c.client_id = ?
                ORDER BY c.added_date
            """, (self.current_user['client_id'],))
            return self.cursor.fetchall(), None
        except sqlite3.Error as e:
            return None, f"Error: {str(e)}"

# Example usage
if __name__ == "__main__":
    # Initialize the shop manager
    shop = ShopManager()
    
    # Example login
    if shop.login("emily1@example.com", "emilyclient"):
        print(f"Welcome {shop.current_user['first_name']}!")
        
        # View available products
        print("\nAvailable Products:")
        products = shop.get_products()
        for product in products:
            print(f"ID: {product[0]}, Name: {product[1]}, Price: ${product[2]}, "
                  f"Category: {product[3]}, Available: {product[4]}")
        
        # Example cart operations
        print("\nAdding product to cart...")
        success, message = shop.add_to_cart("01PROD", 1)
        print(message)
        
        print("\nViewing cart...")
        cart_items, error = shop.view_cart()
        if cart_items:
            for item in cart_items:
                print(f"Product: {item[1]}, Quantity: {item[3]}, "
                      f"Price: ${item[2]}, Total: ${item[4]}")
        
        print("\nUpdating cart quantity...")
        success, message = shop.update_cart_quantity("01PROD", 2)
        print(message)
        
        print("\nViewing updated cart...")
        cart_items, error = shop.view_cart()
        if cart_items:
            for item in cart_items:
                print(f"Product: {item[1]}, Quantity: {item[3]}, "
                      f"Price: ${item[2]}, Total: ${item[4]}")
        
        print("\nRemoving product from cart...")
        success, message = shop.remove_from_cart("01PROD")
        print(message)
    else:
        print("Login failed")
    
    shop.close() 