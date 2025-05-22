-- Create tables for the shop system
CREATE TABLE IF NOT EXISTS users (
    client_id INTEGER PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    email TEXT,
    password TEXT
);

CREATE TABLE IF NOT EXISTS categories (
    category_id TEXT PRIMARY KEY,
    category_name TEXT
);

CREATE TABLE IF NOT EXISTS suppliers (
    supplier_id TEXT PRIMARY KEY,
    supplier_name TEXT,
    contact_person TEXT,
    email TEXT,
    phone_number TEXT,
    address TEXT,
    responsible_id INTEGER
);

CREATE TABLE IF NOT EXISTS products (
    product_id TEXT PRIMARY KEY,
    product_name TEXT,
    price REAL,
    category_id TEXT,
    supplier_id TEXT,
    FOREIGN KEY (category_id) REFERENCES categories(category_id),
    FOREIGN KEY (supplier_id) REFERENCES suppliers(supplier_id)
);

CREATE TABLE IF NOT EXISTS inventory (
    product_id TEXT PRIMARY KEY,
    quantity INTEGER,
    reorder_level INTEGER,
    reorder_quantity INTEGER,
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- Create cart table
CREATE TABLE IF NOT EXISTS cart (
    cart_id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id INTEGER,
    product_id TEXT,
    quantity INTEGER DEFAULT 1,
    added_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (client_id) REFERENCES users(client_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id),
    UNIQUE(client_id, product_id) -- Ensures only one type of product per cart
);

-- Create orders table
CREATE TABLE IF NOT EXISTS orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id INTEGER,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total REAL,
    FOREIGN KEY (client_id) REFERENCES users(client_id)
);

-- Create order details table
CREATE TABLE IF NOT EXISTS order_details (
    order_id INTEGER,
    product_id TEXT,
    quantity INTEGER,
    price_at_time REAL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- Create discounts table
CREATE TABLE IF NOT EXISTS discounts (
    discount_id TEXT PRIMARY KEY,
    percentage REAL,
    discount_type TEXT,
    start_date TEXT,
    stop_date TEXT
); 