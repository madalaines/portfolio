import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from flask import abort
from flask_login import current_user

def get_db_connection():
    conn = sqlite3.connect('artshop.db')
    conn.row_factory = sqlite3.Row
    return conn

def insert_artwork(database, filename, status, name=None, price=None):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO Artwork (filename, status, name, price) VALUES (?, ?, ?, ?)', 
                    (filename, status, name, price))
    conn.commit()
    conn.close()

def get_user_by_email(email):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM User WHERE email = ?', (email,)).fetchone()
    conn.close()
    return user

def verify_password(stored_password, provided_password):
    return check_password_hash(stored_password, provided_password)

def create_user(username, email, password):
    password_hash = generate_password_hash(password)
    conn = get_db_connection()
    conn.execute('INSERT INTO User (username, email, password_hash) VALUES (?, ?, ?)', 
                    (username, email, password_hash))
    conn.commit()
    conn.close()

def register_user(username, email, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    password_hash = generate_password_hash(password)
    try:
        cursor.execute('INSERT INTO User (username, email, password_hash) VALUES (?, ?, ?)', (username, email, password_hash))
        conn.commit()
        user_id = cursor.lastrowid
    except sqlite3.IntegrityError:
        user_id = None
    conn.close()
    return user_id

def login_user(email, password):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM User WHERE email = ?', (email,))
    user = cursor.fetchone()
    conn.close()
    if user and check_password_hash(user['password_hash'], password):
        return user['id']
    else:
        return None

def get_cart(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT Artwork.id, Artwork.filename, Artwork.name, Artwork.price, CartItem.quantity 
        FROM CartItem 
        JOIN Artwork ON CartItem.artwork_id = Artwork.id 
        JOIN Cart ON CartItem.cart_id = Cart.id 
        WHERE Cart.user_id = ?
    ''', (user_id,))
    
    cart_items = cursor.fetchall()
    conn.close()
    return cart_items

def remove_from_cart(user_id, artwork_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Find the user's cart
    cursor.execute('SELECT id FROM Cart WHERE user_id = ?', (user_id,))
    cart = cursor.fetchone()
    
    if cart:
        # Remove the item from the cart
        cursor.execute('DELETE FROM CartItem WHERE cart_id = ? AND artwork_id = ?', (cart['id'], artwork_id))
    
    conn.commit()
    conn.close()

def add_to_cart(user_id, artwork_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    # Find the user's cart or create one if it doesn't exist
    cursor.execute('SELECT id FROM Cart WHERE user_id = ?', (user_id,))
    cart = cursor.fetchone()
    if not cart:
        cursor.execute('INSERT INTO Cart (user_id) VALUES (?)', (user_id,))
        cart_id = cursor.lastrowid
    else:
        cart_id = cart['id']
    # Check if the artwork is already in the cart
    cursor.execute('SELECT id FROM CartItem WHERE cart_id = ? AND artwork_id = ?', (cart_id, artwork_id))
    cart_item = cursor.fetchone()
    if cart_item:
        # If the artwork is already in the cart, increase the quantity
        cursor.execute('UPDATE CartItem SET quantity = quantity + 1 WHERE id = ?', (cart_item['id'],))
    else:
        # Otherwise, add the artwork to the cart
        cursor.execute('INSERT INTO CartItem (cart_id, artwork_id) VALUES (?, ?)', (cart_id, artwork_id))
    conn.commit()
    conn.close()

def add_favorites(user_id, artwork_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM Favorites WHERE user_id = ? AND artwork_id = ?', (user_id, artwork_id))
    favorite = cursor.fetchone()
    if not favorite:
        cursor.execute('INSERT INTO Favorites (user_id, artwork_id) VALUES (?, ?)', (user_id, artwork_id))
        conn.commit()
    conn.close()

def remove_favorites(user_id, artwork_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Favorites WHERE user_id = ? AND artwork_id = ?', (user_id, artwork_id))
    conn.commit()
    conn.close()

def get_favorites(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT Artwork.id, Artwork.filename, Artwork.name, Artwork.price 
        FROM Favorites
        JOIN Artwork ON Favorites.artwork_id = Artwork.id 
        WHERE Favorites.user_id = ?
    ''', (user_id,))
    favorites = cursor.fetchall()
    conn.close()
    return favorites

def init_db():
    conn = sqlite3.connect('artshop.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS User (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        email TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        is_admin INTEGER DEFAULT 0
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Artwork (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename TEXT NOT NULL,
        status TEXT NOT NULL,
        name TEXT,
        price REAL
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Cart (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        FOREIGN KEY (user_id) REFERENCES User (id)
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS CartItem (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cart_id INTEGER NOT NULL,
        artwork_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL DEFAULT 1,
        FOREIGN KEY (cart_id) REFERENCES Cart (id),
        FOREIGN KEY (artwork_id) REFERENCES Artwork (id)
    );
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Favorites (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    artwork_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES User (id),
    FOREIGN KEY (artwork_id) REFERENCES Artwork (id)
    );
    ''')

    conn.commit()
    conn.close()
    print("Database initialized successfully.")

if __name__ == '__main__':
    init_db()

def make_user_admin(email):
    conn = sqlite3.connect('artshop.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE User SET is_admin = 1 WHERE email = ?', (email,))
    conn.commit()
    conn.close()

def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            abort(403)  # HTTP status code for Forbidden
        return func(*args, **kwargs)
    return decorated_view