from flask import Flask, render_template, request
from werkzeug.security import generate_password_hash
from sqlalchemy.engine import URL
from sqlalchemy import create_engine, text, engine
import traceback
import sys

#-----------------------------------------------DATABASE VARIABLES-----------------------------------------------#
DATABASE = "desafio_ecommerce_db"
USERNAME = "postgres"
PASSWORD = "mickael_desafio_python"
DRIVERNAME = "postgresql+psycopg2"
HOST = "desafio-desenvolvedor-python.cgmf4txisda9.sa-east-1.rds.amazonaws.com"
PORT = "5432"

#-----------------------------------------------FUNCTIONS-----------------------------------------------#
def return_error():
    """Show error exception and exit the script."""
    traceback.print_exc() # print the error
    print("Exiting...\n\n")
    sys.exit() # encerra o programa

def run_query(engine: engine, query: str) -> engine.cursor.CursorResult:
    """
    Receive the engine connection and a string for the query and return the query result.
    """
    with engine.begin() as conn: # start the engine
        return conn.execute(text(query)) # execute the query

def get_rows(result: engine.cursor.CursorResult) -> list:
    """
    Get the result from query and return in list type.
    """
    rows = []
    for row in result:
        rows.append(row)
    return rows

def rows_to_dict(result: engine.cursor.CursorResult) -> list[dict]:
    """
    Get the resolt from query all products and return a list of dict.
    """
    products = []
    for row in result:
        products.append({
            "id_product": row[0],
            "name": row[1],
            "price": row[2],
            "score": row[3],
            "image": row[4]
        })
    return products

#-----------------------------------------------POSTGRESQL DATABASE CONNECTION-----------------------------------------------#
print("Connecting to database...")
try:
    url_connection = URL.create( # create the url for database connection
        drivername = DRIVERNAME,
        username = USERNAME,
        password = PASSWORD,
        host = HOST,
        port = PORT,
        database = DATABASE
    )
    engine = create_engine(url_connection) # create engine connection
    print("Database connected.\n")
except:
    print("Error connecting to database.")
    return_error()

#-----------------------------------------------FLASK APPLICATION-----------------------------------------------#
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html") # main page

@app.route("/products") # return all products
def products():
    result = run_query(engine, "SELECT * FROM products;")
    return rows_to_dict(result)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        login = request.form.get("login").lower()
        password = request.form.get("password")
        hash_password = generate_password_hash(password, method="plain")
        
        if len(login) != 0 and len(password) != 0: # if all fields are filled in
            result = run_query(engine, f"SELECT id_user, login, password FROM users WHERE login='{login}' AND password='{hash_password}'")
            rows = get_rows(result)
            if len(rows) == 1: # if there's a row matching login and username, means that is registered
                result = run_query(engine, f"SELECT first_name, last_name FROM users_info WHERE id_user={rows[0][0]}")# getting hte first name and last name for that id_user
                rows = get_rows(result) 
                return "Welcome " + rows[0][0] + " " + rows[0][1]
            else:
                return "Try again."
        else: # if not all fields are filled in
            return "Fill in all fields!"
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        first_name = request.form.get("first_name").title()
        last_name = request.form.get("last_name").title()
        email = request.form.get("email").lower()
        login = request.form.get("login").lower()
        password = request.form.get("password")
        hash_password = generate_password_hash(password, method="plain")

        # if all fields are filled in
        if len(first_name) != 0 and len(last_name) != 0 and len(email) != 0 and len(login) != 0 and len(password) != 0:
            result_login = run_query(engine, f"SELECT login FROM users WHERE login = '{login}'") # getting a matching login
            rows_login = get_rows(result_login)
            
            result_email = run_query(engine, f"SELECT email FROM users_info WHERE email = '{email}'") # getting a matching login
            rows_email = get_rows(result_email)

            not_unique_login = ""
            if len(rows_login) == 1: # if there is a matching login
                not_unique_login += "Login already registered."

            not_unique_email = ""
            if len(rows_email) == 1: # if there is a matching email
                not_unique_email += "Email already registered."

            if len(not_unique_login) == 0 and len(not_unique_email) == 0: # if there is no matching login and email
                run_query(engine, f"INSERT INTO users (login, password) VALUES('{login}', '{hash_password}')")
                run_query(engine, f"INSERT INTO users_info (first_name, last_name, email) VALUES ('{first_name}', '{last_name}', '{email}')")
                return "Welcome " + first_name + " " + last_name
            else: # if there is matching login and email
                return not_unique_login + "\n" + not_unique_email
        else: # if not all fields are filled in
            return "Fill in all fields!"
    return render_template("register.html")

if __name__ == "__main__":
    app.run(debug=True)