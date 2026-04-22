from flask import Flask, render_template, request, redirect, session

app = Flask(__name__)
app.secret_key = "secret123"

#  USERS (ROLE BASED) 
users = {
    "vignesh.k1918@gmail.com": ("vk123", "admin"),
    "nithin2324@gmail.com": ("nithin123", "user")
}

#  PRODUCTS 
products = [
    {"id": 1, "name": "Laptop", "price": 50000},
    {"id": 2, "name": "Phone", "price": 20000},
    {"id": 3, "name": "Headphones", "price": 3000}
]

#  CART 
cart = {}

#  HOME 
@app.route('/')
def index():
    return render_template('index.html', products=products)

#  LOGIN 
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if email in users and users[email][0] == password:
            session['user'] = email
            session['role'] = users[email][1]
            return redirect('/dashboard')
        else:
            return "Invalid Login ❌"

    return render_template('login.html')

#  DASHBOARD 
@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/login')

    return render_template('dashboard.html', products=products)

#  ADD TO CART 
@app.route('/add/<int:pid>')
def add(pid):
    if 'user' not in session:
        return redirect('/login')

    cart.setdefault(session['user'], [])
    cart[session['user']].append(pid)

    return redirect('/dashboard')

#  CHECKOUT 
@app.route('/checkout')
def checkout():
    if 'user' not in session:
        return redirect('/login')

    user_cart = cart.get(session['user'], [])

    total = 0
    for pid in user_cart:
        for p in products:
            if p["id"] == pid:
                total += p["price"]

    # ✅ TUPLE USED
    order = (session['user'], tuple(user_cart), total)

    return f"""
    <h2>Order Confirmed ✅</h2>
    <p>User: {order[0]}</p>
    <p>Items: {order[1]}</p>
    <p>Total: ₹{order[2]}</p>
    <a href='/dashboard'>Back</a>
    """

#  ADMIN 
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if session.get('role') != 'admin':
        return "Access Denied ❌"

    if request.method == 'POST':
        name = request.form['name']
        price = int(request.form['price'])

        new_id = len(products) + 1
        products.append({"id": new_id, "name": name, "price": price})

    return render_template('admin.html', products=products)

#  LOGOUT 
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

#  RUN 
if __name__ == '__main__':
    app.run(debug=True)