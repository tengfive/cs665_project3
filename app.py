from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project3.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Category(db.Model):
    __tablename__ = "categories"

    category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(100), nullable=False, unique=True)

    products = db.relationship("Product", backref="category", lazy=True)


class Product(db.Model):
    __tablename__ = "products"

    product_id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    category_id = db.Column(db.Integer, 
db.ForeignKey("categories.category_id"), nullable=False)


class InventoryLog(db.Model):
    __tablename__ = "inventory_logs"

    log_id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, 
db.ForeignKey("products.product_id"), nullable=False)
    change_amount = db.Column(db.Integer, nullable=False)
    note = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/products", methods=["GET", "POST"])
def products():

    if request.method == "POST":

        product_name = request.form["product_name"]
        price = request.form["price"]
        quantity = request.form["quantity"]
        category_id = request.form["category_id"]

        if (
            product_name.strip() != ""
            and float(price) >= 0
            and int(quantity) >= 0
        ):

            new_product = Product(
                product_name=product_name,
                price=float(price),
                quantity=int(quantity),
                category_id=int(category_id)
            )

            db.session.add(new_product)
            db.session.commit()

        return redirect("/products")

    all_products = Product.query.all()
    all_categories = Category.query.all()

    return render_template(
        "products.html",
        products=all_products,
        categories=all_categories
    )

@app.route("/categories", methods=["GET", "POST"])
def categories():

    if request.method == "POST":

        category_name = request.form["category_name"]

        if category_name.strip() != "":

            new_category = Category(category_name=category_name)

            db.session.add(new_category)
            db.session.commit()

        return redirect("/categories")

    all_categories = Category.query.all()

    return render_template(
        "categories.html",
        categories=all_categories
    )


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
