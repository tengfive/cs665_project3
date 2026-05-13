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
logs = db.relationship("InventoryLog", backref="product", lazy=True)

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

@app.route("/delete_product/<int:product_id>")
def delete_product(product_id):

    product = Product.query.get_or_404(product_id)

    db.session.delete(product)
    db.session.commit()

    return redirect("/products")

@app.route("/restock/<int:product_id>", methods=["POST"])
def restock_product(product_id):

    product = Product.query.get_or_404(product_id)

    amount = int(request.form["amount"])

    if amount > 0:

        try:

            product.quantity += amount

            new_log = InventoryLog(
                product_id=product.product_id,
                change_amount=amount,
                note="Product restocked"
            )

            db.session.add(new_log)

            db.session.commit()

        except:

            db.session.rollback()

    return redirect("/products")

@app.route("/edit_product/<int:product_id>", methods=["GET", "POST"])
def edit_product(product_id):

    product = Product.query.get_or_404(product_id)

    categories = Category.query.all()

    if request.method == "POST":

        product.product_name = request.form["product_name"]

        product.price = float(request.form["price"])

        product.quantity = int(request.form["quantity"])

        product.category_id = int(request.form["category_id"])

        db.session.commit()

        return redirect("/products")

    return render_template(
        "edit_product.html",
        product=product,
        categories=categories
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

@app.route("/delete_category/<int:category_id>")
def delete_category(category_id):

    category = Category.query.get_or_404(category_id)

    db.session.delete(category)
    db.session.commit()

    return redirect("/categories")

@app.route("/dashboard")
def dashboard():

    total_products = Product.query.count()

    total_categories = Category.query.count()

    total_inventory = db.session.query(
        db.func.sum(Product.quantity)
    ).scalar()

    average_price = db.session.query(
        db.func.avg(Product.price)
    ).scalar()

    if total_inventory is None:
        total_inventory = 0

    if average_price is None:
        average_price = 0

    return render_template(
        "dashboard.html",
        total_products=total_products,
        total_categories=total_categories,
        total_inventory=total_inventory,
        average_price=round(average_price, 2)
    )

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
