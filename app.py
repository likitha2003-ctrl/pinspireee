from flask import Flask, render_template, request, redirect
import sqlite3
app = Flask(__name__)

# Create connection to SQLite database
def create_connection():
    conn = sqlite3.connect("users.db")
    return conn

# Create table to sre users
def create_table():
    conn = create_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()




@app.route("/")
def home():
    return render_template("index.html")



# Login route
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        # Check if the user exists
        conn = create_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
        user = cur.fetchone()

        if user:
            return render_template("thankyou.html")
        else:
            return "Invalid credentials! <a href='/login'>Try again</a>"

    return render_template("login.html")



# Registration route
@app.route("/registration", methods=["GET", "POST"])
def registration():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        full_name = request.form["full_name"]
        confirm_password = request.form["Confirm_password"]
        if password != confirm_password:
            return "Passwords do not match. Please <a href'/registration'>Try again</a>."

        # Insert data into the database
        conn = create_connection()
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO users ( full_name,email, password) VALUES (?, ?,?)", ( full_name,email, password))
            conn.commit()
            conn.close()
            return redirect('/login')
        except sqlite3.IntegrityError:
            conn.close()
            return redirect("/login")

    return render_template("registration.html")



if __name__ == "__main__":
    create_table()
    app.run(debug=True)