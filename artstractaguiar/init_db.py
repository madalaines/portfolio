import sqlite3

def init_db():
    conn = sqlite3.connect('artshop.db')
    cursor = conn.cursor()
    
    # Create User table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS User (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    password_hash TEXT NOT NULL
    );
    ''')

    # Create Artwork table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Artwork (
    id INTEGER PRIMARY KEY,
    filename TEXT NOT NULL,
    status TEXT NOT NULL,
    name TEXT,
    price REAL
    );
    ''')
    
    # Create Cart table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Cart (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES User (id)
    );
    ''')

    # Create CartItem table
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
    
    conn.commit()
    conn.close()
    print("Database initialized successfully.")

if __name__ == '__main__':
    init_db()
