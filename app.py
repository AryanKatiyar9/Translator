# use this before pip install flask
from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask import request, redirect, url_for,session
app = Flask(__name__)

# Product Data
products = [
    {"id": 1, "name": "Electronics", "description": "Latest gadgets and tech"},
    {"id": 2, "name": "Clothing", "description": "Trendy fashion"},
    {"id": 3, "name": "Home & Kitchen", "description": "Living space upgrades"},
]

@app.route("/")
def home():
    return render_template("index.html")  # Frontend HTML file

@app.route("/products", methods=["GET"])
def get_products():
    return jsonify(products)

if __name__ == "__main__":
    app.run(debug=True)

#update

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///marketplace.db"
db = SQLAlchemy(app)
class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    user = db.relationship('User', backref=db.backref('cart_items', lazy=True))
    product = db.relationship('Product', backref=db.backref('cart_items', lazy=True))
        
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    price = db.Column(db.Float, nullable=False)
    seller_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    seller = db.relationship('User', backref=db.backref('products', lazy=True))
    with app.app_context():
        db.create_all()
##next

@app.route("/add_product", methods=["GET", "POST"])
def add_product():
    if "user" not in session:
        return redirect(url_for("login"))
    if request.method == "POST":
        name = request.form["name"]
        description = request.form.get("description", "")
        price = float(request.form["price"])
        seller = User.query.filter_by(username=session["user"]).first()
        new_product = Product(name=name, description=description, price=price, seller=seller)
        db.session.add(new_product)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("add_product.html")

@app.route("/products")
def products():
    all_products = Product.query.all()
    return render_template("products.html", products=all_products)
##next
@app.route("/add_to_cart/<int:product_id>")
def add_to_cart(product_id):
    if "user" not in session:
        return redirect(url_for("login"))
    user = User.query.filter_by(username=session["user"]).first()
    cart_item = Cart.query.filter_by(user_id=user.id, product_id=product_id).first()
    if cart_item:
        cart_item.quantity += 1
    else:
        new_cart_item = Cart(user_id=user.id, product_id=product_id, quantity=1)
        db.session.add(new_cart_item)
    db.session.commit()
    return redirect(url_for("view_cart"))

@app.route("/view_cart")
def view_cart():
    if "user" not in session:
        return redirect(url_for("login"))
    user = User.query.filter_by(username=session["user"]).first()
    cart_items = Cart.query.filter_by(user_id=user.id).all()
    return render_template("cart.html", cart_items=cart_items)
import stripe

stripe.api_key = "your_stripe_secret_key"

@app.route("/checkout", methods=["POST"])
def checkout():
    if "user" not in session:
        return redirect(url_for("login"))
    user = User.query.filter_by(username=session["user"]).first()
    cart_items = Cart.query.filter_by(user_id=user.id).all()

    # Calculate total amount
    total_amount = sum(item.product.price * item.quantity for item in cart_items)

    # Create a Stripe Checkout Session
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": item.product.name,
                    },
                    "unit_amount": int(item.product.price * 100),  # Stripe amount is in cents
                },
                "quantity": item.quantity,
            } for item in cart_items
        ],
        mode="payment",
        success_url=url_for("checkout_success", _external=True),
        cancel_url=url_for("view_cart", _external=True),
    )
    return redirect(session.url, code=303)

@app.route("/checkout/success")
def checkout_success():
    return "Payment successful!"
if __name__ == "__main__":
        app.run(debug=True, port=5001)  # Changing port to 5001
        