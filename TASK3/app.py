from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "secret123"

# PRODUCTS
products = [
    {
        "id": 1,
        "name": "Laptop",
        "price": 50000,
        "image": "laptop.jpg"
    },
    {
        "id": 2,
        "name": "Phone",
        "price": 20000,
        "image": "phone.jpg"
    },
    {
        "id": 3,
        "name": "Headphones",
        "price": 2000,
        "image": "headphones.jpg"
    }
]


# LOGIN PAGE
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        if username == "admin" and password == "123":

            session['user'] = username

            if 'cart' not in session:
                session['cart'] = []

            return redirect(url_for('home'))

        else:
            return "Invalid Username or Password"

    return render_template('login.html')


# HOME PAGE
@app.route('/')
def home():

    if 'user' not in session:
        return redirect(url_for('login'))

    return render_template(
        'index.html',
        products=products
    )


# ADD TO CART
@app.route('/add_to_cart/<int:id>')
def add_to_cart(id):

    if 'cart' not in session:
        session['cart'] = []

    for product in products:
        if product['id'] == id:
            session['cart'].append(product)

    session.modified = True

    return redirect(url_for('home'))


# VIEW CART
@app.route('/cart')
def cart():

    cart_items = session.get('cart', [])

    total = 0

    for item in cart_items:
        total += item['price']

    return render_template(
        'cart.html',
        cart_items=cart_items,
        total=total
    )


# REMOVE ITEM
@app.route('/remove/<int:id>')
def remove_from_cart(id):

    cart = session.get('cart', [])

    for item in cart:
        if item['id'] == id:
            cart.remove(item)
            break

    session['cart'] = cart
    session.modified = True

    return redirect(url_for('cart'))


# CHECKOUT
@app.route('/checkout')
def checkout():

    return render_template('checkout.html')


# SUCCESS PAGE
@app.route('/success', methods=['POST'])
def success():

    session.pop('cart', None)

    return render_template('success.html')


# LOGOUT
@app.route('/logout')
def logout():

    session.clear()

    return redirect(url_for('login'))


# RUN
if __name__ == '__main__':
    app.run(debug=True)