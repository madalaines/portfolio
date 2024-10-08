from flask import Blueprint, render_template, request, redirect, url_for, flash
from .draw import generate_random_artwork
from .models import get_user_by_email, verify_password, create_user, insert_artwork, get_db_connection, add_to_cart, get_cart, remove_from_cart, admin_required, login_user, add_favorites, remove_favorites, get_favorites
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from ..app import login_manager  # Import login_manager from main app

# Create the blueprint for Artstractaguiar
artstractaguiar_app = Blueprint('artstractaguiar', __name__, template_folder='templates')

artstractaguiar_app.secret_key = 'sdsjfoe0wu4adj*!fk'


@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect(url_for('register'))

class User(UserMixin):
    def __init__(self, id, username, is_admin=False):
        self.id = id
        self.username = username
        self.is_admin = is_admin

    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

@login_manager.user_loader
def load_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM User WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    if user:
        return User(id=user['id'], username=user['username'], is_admin=user['is_admin'] == 1)
    return None

@artstractaguiar_app.route('/print_admins')
def print_admins():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM User WHERE is_admin = 1')
    admins = cursor.fetchall()
    conn.close()
    admin_emails = [admin['email'] for admin in admins]
    return "Admins: " + ", ".join(admin_emails)

@artstractaguiar_app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = get_user_by_email(email)
        if user and verify_password(user['password_hash'], password):
            login_user(User(id=user['id'], username=user['username'], is_admin=user['is_admin'] == 1))
            return redirect(url_for('home'))
        flash('Invalid credentials')
    return render_template('login.html')

@artstractaguiar_app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        if get_user_by_email(email):
            flash('Email already registered')
        else:
            create_user(username, email, password)
            flash('User registered successfully')
            return redirect(url_for('login'))
    return render_template('register.html')

@artstractaguiar_app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Route to display artwork (including pending and approved)
@artstractaguiar_app.route('/validate_artwork')
@admin_required
@login_required
def validate_artwork():
    conn = get_db_connection()
    pending_artworks = conn.execute('SELECT * FROM Artwork WHERE status = "pending"').fetchall()
    conn.close()
    return render_template('validate_artwork.html', artworks=pending_artworks)

@artstractaguiar_app.route('/approve/<int:artwork_id>', methods=['POST'])
@login_required
@admin_required
def approve_artwork(artwork_id):
    conn = get_db_connection()
    name = request.form['name']
    price = request.form['price']
    conn.execute('UPDATE Artwork SET status = "approved", name = ?, price = ? WHERE id = ?', (name, price, artwork_id))
    conn.commit()
    conn.close()
    return redirect(url_for('validate_artwork'))

@artstractaguiar_app.route('/reject/<int:artwork_id>', methods=['POST'])
@admin_required
@login_required
def reject_artwork(artwork_id):
    conn = get_db_connection()
    conn.execute('UPDATE Artwork SET status = "rejected" WHERE id = ?', (artwork_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('validate_artwork'))

# Route to generate new artwork
@artstractaguiar_app.route('/generate_artwork')
@admin_required
@login_required
def generate_artwork():
    filename = generate_random_artwork("static/artwork")
    insert_artwork("artshop.db", filename, "pending")
    return redirect(url_for('validate_artwork'))

@artstractaguiar_app.route('/')
def home():
    conn = get_db_connection()
    approved_artworks = conn.execute('SELECT * FROM Artwork WHERE status = "approved"').fetchall()
    conn.close()
    return render_template('home.html', artworks=approved_artworks)

@artstractaguiar_app.route('/favorites')
@login_required
def favorites():
    user_id = current_user.id
    favorites = get_favorites(user_id)
    return render_template('favorites.html', favorites=favorites)

@artstractaguiar_app.route('/add_to_favorites/<int:artwork_id>', methods=['POST'])
@login_required
def add_to_favorites(artwork_id):
    add_favorites(current_user.id, artwork_id)
    return '', 204

@artstractaguiar_app.route('/remove_from_favorites/<int:artwork_id>', methods=['POST'])
@login_required
def remove_from_favorites(artwork_id):
    remove_favorites(current_user.id, artwork_id)
    return redirect(request.referrer or url_for('home'))

@artstractaguiar_app.route('/faq')
def faq():
    return render_template('faq.html')

@artstractaguiar_app.route('/directions')
def directions():
    return render_template('directions.html')

@artstractaguiar_app.route('/add_to_cart/<int:artwork_id>', methods=['POST'])
@login_required
def add_artwork_to_cart(artwork_id):
    add_to_cart(current_user.id, artwork_id)
    return '', 204

@artstractaguiar_app.route('/cart')
@login_required
def cart():
    cart_items = get_cart(current_user.id)
    return render_template('cart.html', cart_items=cart_items)

@artstractaguiar_app.route('/remove_from_cart/<int:artwork_id>', methods=['POST'])
@login_required
def remove_artwork_from_cart(artwork_id):
    remove_from_cart(current_user.id, artwork_id)
    return redirect(url_for('cart'))

if __name__ == '__main__':
    artstractaguiar_app.run(debug=False)
