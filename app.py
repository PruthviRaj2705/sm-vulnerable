from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect("secureshop.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE email = ?",
            (email,)
        )

        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user[3], password):
            return redirect(url_for("home"))

        else:
            return "Invalid email or password!"

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        # Check whether passwords match
        if password != confirm_password:
            return "Passwords do not match!"

        # Securely hash the password
        hashed_password = generate_password_hash(password)

        try:
            conn = sqlite3.connect("secureshop.db")
            cursor = conn.cursor()

            cursor.execute(
                "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                (name, email, hashed_password)
            )

            conn.commit()
            conn.close()

            return redirect(url_for("login"))

        except sqlite3.IntegrityError:
            return "An account with this email already exists!"

    return render_template("register.html")


@app.route("/category/<category_name>")
def category(category_name):

    products_data = {

        "electronics": [
            {
                "name": "5G Smartphone",
                "description": "Latest 5G smartphone with high-performance camera.",
                "price": "24,999",
                "image": "electronics.jpg"
            },
            {
                "name": "Performance Laptop",
                "description": "Powerful laptop for work, study and entertainment.",
                "price": "54,999",
                "image": "electronics.jpg"
            },
            {
                "name": "Smart Watch",
                "description": "Fitness smart watch with health tracking.",
                "price": "3,999",
                "image": "electronics.jpg"
            },
            {
                "name": "Wireless Headphones",
                "description": "Bluetooth headphones with clear sound quality.",
                "price": "2,499",
                "image": "electronics.jpg"
            },
            {
                "name": "Wireless Earbuds",
                "description": "Compact earbuds with rich sound and long battery life.",
                "price": "1,999",
                "image": "electronics.jpg"
            },
            {
                "name": "Bluetooth Speaker",
                "description": "Portable speaker with powerful audio output.",
                "price": "2,999",
                "image": "electronics.jpg"
            }
        ],

        "fashion": [
            {
                "name": "Women's Casual Dress",
                "description": "Comfortable and stylish everyday dress.",
                "price": "1,299"
            },
            {
                "name": "Men's Casual Shirt",
                "description": "Premium cotton casual shirt.",
                "price": "899"
            },
            {
                "name": "Women's Kurti",
                "description": "Elegant ethnic wear for everyday occasions.",
                "price": "999"
            },
            {
                "name": "Men's Jeans",
                "description": "Slim-fit comfortable denim jeans.",
                "price": "1,499"
            },
            {
                "name": "Women's Saree",
                "description": "Traditional saree with modern styling.",
                "price": "1,799"
            },
            {
                "name": "Men's T-Shirt",
                "description": "Soft cotton regular-fit T-shirt.",
                "price": "599"
            }
        ],

        "footwear": [
            {
                "name": "Running Shoes",
                "description": "Comfortable sports shoes for running and workouts.",
                "price": "2,499"
            },
            {
                "name": "Casual Sneakers",
                "description": "Stylish sneakers for everyday wear.",
                "price": "1,999"
            },
            {
                "name": "Women's Sandals",
                "description": "Comfortable sandals with modern design.",
                "price": "899"
            },
            {
                "name": "Men's Formal Shoes",
                "description": "Elegant formal shoes for office and occasions.",
                "price": "1,699"
            },
            {
                "name": "Sports Shoes",
                "description": "Lightweight shoes designed for sports activities.",
                "price": "2,799"
            },
            {
                "name": "Women's Flats",
                "description": "Comfortable flats for everyday use.",
                "price": "799"
            }
        ],

        "beauty": [
            {
                "name": "Face Moisturizer",
                "description": "Hydrating moisturizer for soft and healthy-looking skin.",
                "price": "499"
            },
            {
                "name": "Face Serum",
                "description": "Lightweight serum for daily skincare.",
                "price": "699"
            },
            {
                "name": "Sunscreen SPF 50",
                "description": "Broad-spectrum sunscreen for daily protection.",
                "price": "599"
            },
            {
                "name": "Lipstick",
                "description": "Long-lasting lipstick with smooth finish.",
                "price": "399"
            },
            {
                "name": "Shampoo",
                "description": "Gentle shampoo for everyday hair care.",
                "price": "449"
            },
            {
                "name": "Perfume",
                "description": "Fresh long-lasting fragrance for everyday use.",
                "price": "899"
            }
        ],

        "home-kitchen": [
            {
                "name": "Non-Stick Cookware Set",
                "description": "Durable cookware set for everyday cooking.",
                "price": "2,499"
            },
            {
                "name": "Electric Kettle",
                "description": "Fast boiling electric kettle for home and office.",
                "price": "999"
            },
            {
                "name": "Mixer Grinder",
                "description": "Powerful mixer grinder for everyday kitchen needs.",
                "price": "2,999"
            },
            {
                "name": "Dinner Set",
                "description": "Elegant dinner set for family dining.",
                "price": "1,499"
            },
            {
                "name": "Storage Containers",
                "description": "Airtight containers for organized kitchen storage.",
                "price": "699"
            },
            {
                "name": "Table Lamp",
                "description": "Modern decorative lamp for bedroom and study.",
                "price": "799"
            }
        ],

        "grocery": [
            {
                "name": "Basmati Rice",
                "description": "Premium quality long-grain basmati rice.",
                "price": "699"
            },
            {
                "name": "Wheat Flour",
                "description": "Fresh whole wheat flour for everyday cooking.",
                "price": "399"
            },
            {
                "name": "Cooking Oil",
                "description": "High-quality cooking oil for daily use.",
                "price": "179"
            },
            {
                "name": "Toor Dal",
                "description": "Premium quality protein-rich dal.",
                "price": "169"
            },
            {
                "name": "Green Tea",
                "description": "Refreshing green tea for everyday consumption.",
                "price": "249"
            },
            {
                "name": "Dry Fruits",
                "description": "Premium mixed dry fruits and nuts.",
                "price": "599"
            }
        ],

        "books": [
            {
                "name": "Python Programming",
                "description": "Beginner-friendly guide to Python programming.",
                "price": "599"
            },
            {
                "name": "Data Structures and Algorithms",
                "description": "Learn fundamental data structures and algorithms.",
                "price": "699"
            },
            {
                "name": "Web Development",
                "description": "Complete guide to modern web development.",
                "price": "549"
            },
            {
                "name": "Database Management",
                "description": "Learn database concepts and SQL fundamentals.",
                "price": "499"
            },
            {
                "name": "Software Engineering",
                "description": "Concepts and practices for software development.",
                "price": "649"
            },
            {
                "name": "Artificial Intelligence",
                "description": "Introduction to AI concepts and applications.",
                "price": "799"
            }
        ],

        "sports": [
            {
                "name": "Cricket Bat",
                "description": "Professional quality cricket bat.",
                "price": "2,499"
            },
            {
                "name": "Football",
                "description": "Durable football suitable for training and matches.",
                "price": "899"
            },
            {
                "name": "Badminton Racket",
                "description": "Lightweight racket for recreational and professional play.",
                "price": "1,299"
            },
            {
                "name": "Yoga Mat",
                "description": "Non-slip exercise and yoga mat.",
                "price": "699"
            },
            {
                "name": "Skipping Rope",
                "description": "Adjustable skipping rope for fitness workouts.",
                "price": "299"
            },
            {
                "name": "Gym Dumbbells",
                "description": "Durable dumbbells for home workouts.",
                "price": "1,499"
            }
        ],

        "accessories": [
            {
                "name": "Leather Wallet",
                "description": "Premium compact wallet with multiple card slots.",
                "price": "699"
            },
            {
                "name": "Sunglasses",
                "description": "Stylish sunglasses with UV protection.",
                "price": "999"
            },
            {
                "name": "Backpack",
                "description": "Spacious backpack for college, work and travel.",
                "price": "1,299"
            },
            {
                "name": "Wrist Watch",
                "description": "Elegant analog watch for everyday use.",
                "price": "1,799"
            },
            {
                "name": "Travel Bag",
                "description": "Durable travel bag with spacious compartments.",
                "price": "1,499"
            },
            {
                "name": "Belt",
                "description": "Classic adjustable belt for everyday wear.",
                "price": "499"
            }
        ]
    }

    products = products_data.get(category_name.lower(), [])

    return render_template(
        "category.html",
        category=category_name.replace("-", " ").title(),
        products=products
    )


if __name__ == "__main__":
    app.run(debug=True)