import sqlite3
import os

def create_database():
    """Create and populate the database"""
    # Remove existing database if it exists
    if os.path.exists("shop.db"):
        os.remove("shop.db")
    
    # Create new database
    conn = sqlite3.connect("shop.db")
    cursor = conn.cursor()
    
    # Read and execute schema
    with open("schema.sql", "r") as f:
        cursor.executescript(f.read())
    
    # Insert sample data
    # Users
    cursor.executemany("""
        INSERT INTO users (client_id, first_name, last_name, email, password)
        VALUES (?, ?, ?, ?, ?)
    """, [
        (15765543, 'Emily', 'Williams', 'emily1@example.com', 'emilyclient'),
        (15765544, 'Emma', 'Johnson', 'emmaj@example.com', 'emmaclient'),
        (15765545, 'Michael', 'Williams', 'michaelw@example.com', 'michaelclient'),
        (15765546, 'Sophia', 'Brown', 'sophiab@example.com', 'sophiaclient'),
        (15765547, 'Christopher', 'Jones', 'chrisj@example.com', 'chrisclient'),
        (15765548, 'Olivia', 'Garcia', 'oliviag@example.com', 'oliviaclient')
    ])
    
    # Categories
    cursor.executemany("""
        INSERT INTO categories (category_id, category_name)
        VALUES (?, ?)
    """, [
        ('01CAT', 'Athletic Clothing'),
        ('02CAT', 'Running Gear'),
        ('03CAT', 'Fitness Equipment'),
        ('04CAT', 'Team Sports'),
        ('05CAT', 'Yoga & Pilates'),
        ('06CAT', 'Cycling Gear'),
        ('07CAT', 'Outdoor Recreation'),
        ('08CAT', 'Gym Accessories'),
        ('09CAT', 'Water Sports Gear'),
        ('10CAT', 'Hiking & Camping Gear')
    ])
    
    # Suppliers
    cursor.executemany("""
        INSERT INTO suppliers (supplier_id, supplier_name, contact_person, email, 
                             phone_number, address, responsible_id)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, [
        ('01SUP', 'Tech Innovations', 'Adam Smith', 'info@techinnov.com', 
         '+14085551234', '123 Tech Street, Silicon Valley, USA', 1010),
        ('02SUP', 'GymFitPro', 'Sarah Johnson', 'sarah@gymfitpro.com', 
         '+13239876543', '456 Fitness Avenue, Los Angeles, USA', 100),
        ('03SUP', 'Sportsworld', 'Mike Davis', 'mike@sportsworld.com', 
         '+15551234567', '789 Sports Plaza, New York, USA', 1010)
    ])
    
    # Products
    cursor.executemany("""
        INSERT INTO products (product_id, product_name, price, category_id, supplier_id)
        VALUES (?, ?, ?, ?, ?)
    """, [
        ('01PROD', 'Treadmill', 1200.00, '03CAT', '02SUP'),
        ('02PROD', 'Running Shoes', 80.00, '12CAT', '15SUP'),
        ('03PROD', 'Yoga Mat', 30.00, '05CAT', '09SUP'),
        ('04PROD', 'Soccer Ball', 25.00, '04CAT', '03SUP'),
        ('05PROD', 'Mountain Bike', 600.00, '10CAT', '08SUP'),
        ('06PROD', 'Protein Powder', 40.00, '18CAT', '14SUP'),
        ('07PROD', 'Swimming Goggles', 15.00, '09CAT', '03SUP'),
        ('08PROD', 'Camping Tent', 150.00, '10CAT', '19SUP'),
        ('09PROD', 'Basketball', 30.00, '04CAT', '03SUP'),
        ('10PROD', 'Winter Jacket', 100.00, '11CAT', '18SUP')
    ])
    
    # Inventory
    cursor.executemany("""
        INSERT INTO inventory (product_id, quantity, reorder_level, reorder_quantity)
        VALUES (?, ?, ?, ?)
    """, [
        ('01PROD', 100, 35, 100),
        ('02PROD', 200, 50, 150),
        ('03PROD', 150, 40, 120),
        ('04PROD', 300, 60, 200),
        ('05PROD', 60, 40, 80),
        ('06PROD', 80, 40, 60),
        ('07PROD', 250, 120, 180),
        ('08PROD', 180, 110, 130),
        ('09PROD', 90, 45, 70),
        ('10PROD', 400, 80, 250)
    ])
    
    # Discounts
    cursor.executemany("""
        INSERT INTO discounts (discount_id, percentage, discount_type, start_date, stop_date)
        VALUES (?, ?, ?, ?, ?)
    """, [
        ('01DIS', 0.5, 'Black Friday', '2023-11-24', '2023-11-26'),
        ('02DIS', 0.25, 'Season Sales', '2023-06-01', '2023-08-31'),
        ('03DIS', 0.1, 'Last Pieces', '2023-10-01', '2023-10-15')
    ])
    
    # Commit changes and close connection
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()
    print("Database created and populated successfully!") 