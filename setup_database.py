from sqlalchemy.engine import URL
from sqlalchemy import create_engine, inspect, text, engine
import requests
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

#-----------------------------------------------SETUP TABLES-----------------------------------------------#
users_table_exist = inspect(engine).has_table("users") # if table exists return True, if not return False
users_info_table_exist = inspect(engine).has_table("users_info")
products_table_exist = inspect(engine).has_table("products")

print("Verifiyng if tables exist...")
try:
    if users_info_table_exist: # if table exists drop the table
        run_query(engine, "DROP TABLE users_info;")
        print("Table users_info deleted.")
    else:
        print("Table users_info don't exist.")
    if users_table_exist:
        run_query(engine, "DROP TABLE users;")
        print("Table users deleted.")
    else:
        print("Table users don't exist.")
    if products_table_exist:
        run_query(engine, "DROP TABLE products;")
        print("Table products deleted.\n")
    else:
        print("Table products don't exist.\n")
except:
    print("Something went wrong.")
    return_error()


# All fields must have values (NOT NULL)
# Columns "login" in table "users", "email" in table "users_info" and "name" in table "products" must be all distinct values (UNIQUE)
create_tables = \
"""
CREATE TABLE users (
    id_user SERIAL,
    login VARCHAR(255) NOT NULL UNIQUE,
    "password" VARCHAR(255) NOT NULL,
    PRIMARY KEY (id_user)
);

CREATE TABLE users_info (
    id_user SERIAL,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    FOREIGN KEY (id_user) REFERENCES users(id_user)
);

CREATE TABLE products (
    id_product SERIAL,
    "name" VARCHAR(255) NOT NULL UNIQUE,
    price FLOAT NOT NULL,
    score INT NOT NULL,
    image VARCHAR(255),
    PRIMARY KEY (id_product)
);
"""
print("Creating tables...")
try:
    run_query(engine, create_tables)
    print("Tables created.\n")
except:
    print("Error creating tables.")
    return_error()

#-----------------------------------------------PRODUCTS DATA-----------------------------------------------#
print("Getting products data...")
try:
    url = "https://raw.githubusercontent.com/Supera-Inovacao-Tecnologia/PS-Python-React/master/products.json"
    response = requests.get(url)
    products = response.json()
    print(f"{len(products)} products read.\n")
except:
    print("Error getting products data.")
    return_error()

load_products_data = \
f"""
INSERT INTO products ("name", price, score, image)
VALUES 
"""

print("Inserting products into database table...")
try:
    for p in products:
        if p != products[-1]:
            load_products_data += f"('{p['name']}', {p['price']}, {p['score']}, '{p['image']}'),\n" # concatenating string for insert all products
        else:
            load_products_data += f"('{p['name']}', {p['price']}, {p['score']}, '{p['image']}');"
    
    run_query(engine, load_products_data)
    print("Products inserted:\n")

    result = run_query(engine, "SELECT * FROM products;") # get all rows in products table
    for row in result: # showing products
        print(row)
except:
    print("Error inserting products.")
    return_error()