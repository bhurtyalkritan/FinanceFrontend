import streamlit as st
import requests
import json
import pandas as pd
import pandasql as psql
import graphviz
import re

# Set the base URL for your Portfolio API
BASE_URL = "http://localhost:8080/api"

# Initialize session state
if 'jwt_token' not in st.session_state:
    st.session_state.jwt_token = None
if "df_users" not in st.session_state:
    st.session_state.df_users = pd.DataFrame()
if "df_portfolios" not in st.session_state:
    st.session_state.df_portfolios = pd.DataFrame()
if "df_assets" not in st.session_state:
    st.session_state.df_assets = pd.DataFrame()
if "df_transactions" not in st.session_state:
    st.session_state.df_transactions = pd.DataFrame()

# Function to convert camelCase or PascalCase to snake_case
def camel_to_snake(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

# Function to flatten nested objects and convert keys to snake_case
def flatten_data(data):
    flattened_data = []
    for item in data:
        flattened_item = {}
        for key, value in item.items():
            # Convert key to snake_case
            snake_key = camel_to_snake(key)
            if isinstance(value, dict):
                for sub_key, sub_value in value.items():
                    # Convert sub_key to snake_case
                    snake_sub_key = camel_to_snake(sub_key)
                    flattened_item[f"{snake_key}_{snake_sub_key}"] = sub_value
            elif isinstance(value, list):
                # Convert lists to JSON strings or handle accordingly
                flattened_item[snake_key] = json.dumps(value)
            else:
                flattened_item[snake_key] = value
        flattened_data.append(flattened_item)
    return flattened_data

# Function to preprocess DataFrame for SQL querying
def preprocess_df_for_sql(df):
    # Remove columns with unsupported data types
    df = df.copy()
    for col in df.columns:
        if df[col].apply(lambda x: isinstance(x, (list, dict))).any():
            df[col] = df[col].apply(lambda x: json.dumps(x) if isinstance(x, (list, dict)) else x)
    return df

# Helper function to make API requests with JWT authentication
def make_request(endpoint, method='GET', data=None):
    url = f"{BASE_URL}/{endpoint}"
    headers = {'Content-Type': 'application/json'}
    if st.session_state.jwt_token:
        headers['Authorization'] = f"Bearer {st.session_state.jwt_token}"

    try:
        if method == 'GET':
            response = requests.get(url, headers=headers)
        elif method == 'POST':
            response = requests.post(url, headers=headers, data=json.dumps(data))
        elif method == 'PUT':
            response = requests.put(url, headers=headers, data=json.dumps(data))
        elif method == 'DELETE':
            response = requests.delete(url, headers=headers)
        if response.status_code in [200, 201]:
            return response.json() if response.content else {}
        else:
            st.error(f"API Error [{response.status_code}]: {response.text}")
            return {}
    except Exception as e:
        st.error(f"Request error: {e}")
        return {}

# Function to authenticate user and obtain JWT token
def authenticate_user(username, password):
    url = f"{BASE_URL}/auth/login"
    headers = {'Content-Type': 'application/json'}
    data = {'email': username, 'password': password}

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            token = response.json().get('token')
            return token
        else:
            st.error(f"Authentication failed: {response.json().get('message', 'Unknown error')}")
            return None
    except Exception as e:
        st.error(f"Error during authentication: {e}")
        return None

# Streamlit App
st.title("Fidelity Interview Prep")

# Authentication fields
st.sidebar.header("Authentication")
username = st.sidebar.text_input("Email", value="", type="default")
password = st.sidebar.text_input("Password", value="", type="password")
if st.session_state.jwt_token:
    if st.sidebar.button("Logout"):
        st.session_state.jwt_token = None
        st.success("Logged out successfully!")
else:
    if st.sidebar.button("Login"):
        token = authenticate_user(username, password)
        if token:
            st.session_state.jwt_token = token
            st.success("Logged in successfully!")
        else:
            st.session_state.jwt_token = None

# Tabs for different features
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs([
    "Users", "Portfolios", "Assets", "Transactions", "Health Check", "User Count", "Advanced SQL Query", "OOP", "Docs"
])

# Users Tab
with tab1:
    st.header("User Management")
    if st.session_state.jwt_token:
        page = st.number_input("Page", min_value=0, value=0, step=1)
        size = st.number_input("Size", min_value=1, value=10, step=1)
        sort_by = st.text_input("Sort By", value="id")
        if st.button("Fetch Users"):
            users = make_request(f"users?page={page}&size={size}&sortBy={sort_by}")
            if 'content' in users:
                flattened_users = flatten_data(users['content'])
                st.session_state.df_users = pd.DataFrame(flattened_users)
                st.dataframe(st.session_state.df_users)
            else:
                st.error("Failed to fetch users or invalid data format.")
    else:
        st.warning("Please log in to access this section.")

# Portfolios Tab
with tab2:
    st.header("Portfolio Management")
    if st.session_state.jwt_token:
        user_id = st.number_input("User ID for Portfolio", min_value=0, step=1)
        if st.button("Fetch Portfolio by User ID"):
            portfolios = make_request(f"portfolios/user/{user_id}")
            if isinstance(portfolios, list):
                flattened_portfolios = flatten_data(portfolios)
                st.session_state.df_portfolios = pd.DataFrame(flattened_portfolios)
                st.dataframe(st.session_state.df_portfolios)
            else:
                st.error("Failed to fetch portfolios or invalid data format.")
    else:
        st.warning("Please log in to access this section.")

# Assets Tab
with tab3:
    st.header("Asset Management")
    if st.session_state.jwt_token:
        portfolio_id = st.number_input("Portfolio ID for Assets", min_value=0, step=1)
        if st.button("Fetch Assets by Portfolio ID"):
            assets = make_request(f"assets/portfolio/{portfolio_id}")
            if isinstance(assets, list):
                flattened_assets = flatten_data(assets)
                st.session_state.df_assets = pd.DataFrame(flattened_assets)
                st.dataframe(st.session_state.df_assets)
            else:
                st.error("Failed to fetch assets or invalid data format.")
    else:
        st.warning("Please log in to access this section.")

# Transactions Tab
with tab4:
    st.header("Transaction Management")
    if st.session_state.jwt_token:
        asset_id = st.number_input("Asset ID for Transactions", min_value=0, step=1)
        if st.button("Fetch Transactions by Asset ID"):
            transactions = make_request(f"transactions/asset/{asset_id}")
            if isinstance(transactions, list):
                flattened_transactions = flatten_data(transactions)
                st.session_state.df_transactions = pd.DataFrame(flattened_transactions)
                st.dataframe(st.session_state.df_transactions)
            else:
                st.error("Failed to fetch transactions or invalid data format.")
    else:
        st.warning("Please log in to access this section.")

# Health Check Tab
with tab5:
    st.header("Health Check")
    if st.session_state.jwt_token:
        if st.button("Check Health"):
            url = "http://localhost:8080/health"
            headers = {'Authorization': f"Bearer {st.session_state.jwt_token}"}
            try:
                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    health_status = response.json() if response.content else {"status": "Application is running smoothly!"}
                    st.json(health_status)
                else:
                    st.error(f"Health check failed: {response.text}")
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Please log in to access this section.")

# User Count Tab
with tab6:
    st.header("User Count")
    if st.session_state.jwt_token:
        if st.button("Get User Count"):
            user_count = make_request("users/count")
            if isinstance(user_count, dict) and "count" in user_count:
                st.json(user_count)
            else:
                st.error("Failed to fetch user count or invalid data format.")
    else:
        st.warning("Please log in to access this section.")

# Advanced SQL Query Tab
with tab7:
    st.header("Run Advanced SQL Queries on Loaded Data")

    if st.session_state.jwt_token:
        # Dropdown to select which DataFrames to query
        df_options = {
            "Users": st.session_state.df_users,
            "Portfolios": st.session_state.df_portfolios,
            "Assets": st.session_state.df_assets,
            "Transactions": st.session_state.df_transactions
        }

        # Prepare all DataFrames for SQL querying
        sql_ready_dfs = {name: preprocess_df_for_sql(df) for name, df in df_options.items()}

        # Display available DataFrames
        st.subheader("Available DataFrames")
        for name, df in df_options.items():
            if not df.empty:
                st.write(f"**{name} DataFrame**")
                st.dataframe(df)

        # Debug: Display DataFrame Columns
        st.subheader("Debug: DataFrame Columns")
        for name, df in df_options.items():
            if not df.empty:
                st.write(f"**{name} DataFrame Columns:** {list(df.columns)}")

        # Advanced SQL Query Input
        st.subheader("Write Your Advanced SQL Query")
        st.markdown("""
        You can use the following tables in your SQL query:
        - **Users** (`users`)
        - **Portfolios** (`portfolios`)
        - **Assets** (`assets`)
        - **Transactions** (`transactions`)

        **Example Query with Subquery:**
        ```sql
        SELECT *
        FROM users
        WHERE id IN (SELECT user_id FROM portfolios WHERE portfolio_type = 'Long-term')
        ```
        **Example Corrected Query:**
        ```sql
        SELECT * FROM users WHERE id > 10 LIMIT 10;
        ```
        """)
        query = st.text_area("Enter SQL Query", "SELECT * FROM users WHERE id > 10 LIMIT 10;")

        if st.button("Run Advanced SQL Query"):
            try:
                # Build the locals dictionary for pandasql
                locals_dict = {name.lower(): df for name, df in sql_ready_dfs.items() if not df.empty}
                result_df = psql.sqldf(query, locals_dict)
                st.dataframe(result_df)
            except Exception as e:
                # Enhanced error handling
                error_message = str(e)
                if "no such column" in error_message:
                    st.error("Error: One of the specified columns does not exist. Please verify your column names.")
                    # Optionally, display available columns
                    for name, df in sql_ready_dfs.items():
                        st.write(f"**{name.capitalize()} DataFrame Columns:** {list(df.columns)}")
                else:
                    st.error(f"Error: {e}")

        # Additional Pre-made Advanced Queries
        st.subheader("Pre-made Advanced SQL Queries")
        advanced_query_type = st.selectbox("Select Advanced Query Type", [
            "Users with Most Portfolios",
            "Assets with Highest Total Value",
            "Transactions Summary per Asset",
            "Users with No Portfolios",
            "Portfolios with No Assets",
            "Top 5 Most Traded Assets",
            "Average Asset Value per Portfolio",
            "Users with Portfolios Exceeding a Total Value",
            "Assets Purchased in Last 30 Days",
            "Users by Age Group",
            "Assets Distribution by Type",
            "Transactions Above Average Quantity",
            "Portfolios with Diversified Assets",
            "Inactive Users (No Transactions)",
            "Top Performing Assets by Return Rate",
            "Custom Subquery",
            "Window Functions Example"
        ])

        # Function to execute and display query results
        def execute_query(query, locals_dict):
            try:
                result_df = psql.sqldf(query, locals_dict)
                st.dataframe(result_df)
            except Exception as e:
                error_message = str(e)
                if "no such column" in error_message:
                    st.error("Error: One of the specified columns does not exist. Please verify your column names.")
                    # Optionally, display available columns
                    for name, df in locals_dict.items():
                        st.write(f"**{name.capitalize()} DataFrame Columns:** {list(df.columns)}")
                else:
                    st.error(f"Error: {e}")

        locals_dict = {name.lower(): df for name, df in sql_ready_dfs.items() if not df.empty}

        if advanced_query_type == "Users with Most Portfolios":
            if 'users' in locals_dict and 'portfolios' in locals_dict:
                if st.button("Run 'Users with Most Portfolios' Query"):
                    query = """
                    SELECT u.id, u.name, COUNT(p.id) AS portfolio_count
                    FROM users u
                    JOIN portfolios p ON u.id = p.user_id
                    GROUP BY u.id, u.name
                    ORDER BY portfolio_count DESC
                    """
                    execute_query(query, locals_dict)
            else:
                st.warning("Users and Portfolios data must be loaded.")

        elif advanced_query_type == "Assets with Highest Total Value":
            if 'assets' in locals_dict:
                if st.button("Run 'Assets with Highest Total Value' Query"):
                    query = """
                    SELECT symbol, asset_type, SUM(total_value) AS total_value_sum
                    FROM assets
                    GROUP BY symbol, asset_type
                    ORDER BY total_value_sum DESC
                    LIMIT 10
                    """
                    execute_query(query, locals_dict)
            else:
                st.warning("Assets data must be loaded.")

        elif advanced_query_type == "Transactions Summary per Asset":
            if 'transactions' in locals_dict and 'assets' in locals_dict:
                if st.button("Run 'Transactions Summary per Asset' Query"):
                    query = """
                    SELECT a.symbol, COUNT(t.id) AS transaction_count, SUM(t.quantity) AS total_quantity
                    FROM transactions t
                    JOIN assets a ON t.asset_id = a.id
                    GROUP BY a.symbol
                    ORDER BY transaction_count DESC
                    """
                    execute_query(query, locals_dict)
            else:
                st.warning("Assets and Transactions data must be loaded.")

        elif advanced_query_type == "Users with No Portfolios":
            if 'users' in locals_dict and 'portfolios' in locals_dict:
                if st.button("Run 'Users with No Portfolios' Query"):
                    query = """
                    SELECT u.id, u.name
                    FROM users u
                    LEFT JOIN portfolios p ON u.id = p.user_id
                    WHERE p.id IS NULL
                    """
                    execute_query(query, locals_dict)
            else:
                st.warning("Users and Portfolios data must be loaded.")

        elif advanced_query_type == "Portfolios with No Assets":
            if 'portfolios' in locals_dict and 'assets' in locals_dict:
                if st.button("Run 'Portfolios with No Assets' Query"):
                    query = """
                    SELECT p.id, p.portfolio_name
                    FROM portfolios p
                    LEFT JOIN assets a ON p.id = a.portfolio_id
                    WHERE a.id IS NULL
                    """
                    execute_query(query, locals_dict)
            else:
                st.warning("Portfolios and Assets data must be loaded.")

        elif advanced_query_type == "Top 5 Most Traded Assets":
            if 'transactions' in locals_dict and 'assets' in locals_dict:
                if st.button("Run 'Top 5 Most Traded Assets' Query"):
                    query = """
                    SELECT a.symbol, COUNT(t.id) AS trade_count
                    FROM transactions t
                    JOIN assets a ON t.asset_id = a.id
                    GROUP BY a.symbol
                    ORDER BY trade_count DESC
                    LIMIT 5
                    """
                    execute_query(query, locals_dict)
            else:
                st.warning("Assets and Transactions data must be loaded.")

        elif advanced_query_type == "Average Asset Value per Portfolio":
            if 'assets' in locals_dict and 'portfolios' in locals_dict:
                if st.button("Run 'Average Asset Value per Portfolio' Query"):
                    query = """
                    SELECT p.portfolio_name, AVG(a.total_value) AS average_value
                    FROM assets a
                    JOIN portfolios p ON a.portfolio_id = p.id
                    GROUP BY p.portfolio_name
                    ORDER BY average_value DESC
                    """
                    execute_query(query, locals_dict)
            else:
                st.warning("Assets and Portfolios data must be loaded.")

        elif advanced_query_type == "Users with Portfolios Exceeding a Total Value":
            if 'users' in locals_dict and 'portfolios' in locals_dict and 'assets' in locals_dict:
                if st.button("Run 'Users with Portfolios Exceeding a Total Value' Query"):
                    query = """
                    SELECT u.id, u.name, SUM(a.total_value) AS total_portfolio_value
                    FROM users u
                    JOIN portfolios p ON u.id = p.user_id
                    JOIN assets a ON p.id = a.portfolio_id
                    GROUP BY u.id, u.name
                    HAVING SUM(a.total_value) > 100000
                    ORDER BY total_portfolio_value DESC
                    """
                    execute_query(query, locals_dict)
            else:
                st.warning("Users, Portfolios, and Assets data must be loaded.")

        elif advanced_query_type == "Assets Purchased in Last 30 Days":
            if 'assets' in locals_dict:
                if st.button("Run 'Assets Purchased in Last 30 Days' Query"):
                    query = """
                    SELECT *
                    FROM assets
                    WHERE purchase_date >= DATE('now', '-30 days')
                    """
                    execute_query(query, locals_dict)
            else:
                st.warning("Assets data must be loaded.")

        elif advanced_query_type == "Users by Age Group":
            if 'users' in locals_dict:
                if st.button("Run 'Users by Age Group' Query"):
                    query = """
                    SELECT 
                        CASE 
                            WHEN date_of_birth <= DATE('now', '-60 years') THEN '60+'
                            WHEN date_of_birth <= DATE('now', '-50 years') THEN '50-59'
                            WHEN date_of_birth <= DATE('now', '-40 years') THEN '40-49'
                            WHEN date_of_birth <= DATE('now', '-30 years') THEN '30-39'
                            ELSE 'Under 30'
                        END AS age_group,
                        COUNT(*) AS user_count
                    FROM users
                    GROUP BY age_group
                    ORDER BY 
                        CASE age_group
                            WHEN 'Under 30' THEN 1
                            WHEN '30-39' THEN 2
                            WHEN '40-49' THEN 3
                            WHEN '50-59' THEN 4
                            WHEN '60+' THEN 5
                        END
                    """
                    execute_query(query, locals_dict)
            else:
                st.warning("Users data must be loaded.")

        elif advanced_query_type == "Assets Distribution by Type":
            if 'assets' in locals_dict:
                if st.button("Run 'Assets Distribution by Type' Query"):
                    query = """
                    SELECT asset_type, COUNT(*) AS asset_count
                    FROM assets
                    GROUP BY asset_type
                    ORDER BY asset_count DESC
                    """
                    execute_query(query, locals_dict)
            else:
                st.warning("Assets data must be loaded.")

        elif advanced_query_type == "Transactions Above Average Quantity":
            if 'transactions' in locals_dict:
                if st.button("Run 'Transactions Above Average Quantity' Query"):
                    query = """
                    SELECT *
                    FROM transactions
                    WHERE quantity > (SELECT AVG(quantity) FROM transactions)
                    ORDER BY quantity DESC
                    """
                    execute_query(query, locals_dict)
            else:
                st.warning("Transactions data must be loaded.")

        elif advanced_query_type == "Portfolios with Diversified Assets":
            if 'portfolios' in locals_dict and 'assets' in locals_dict:
                if st.button("Run 'Portfolios with Diversified Assets' Query"):
                    query = """
                    SELECT p.portfolio_name, COUNT(DISTINCT a.asset_type) AS asset_type_count
                    FROM portfolios p
                    JOIN assets a ON p.id = a.portfolio_id
                    GROUP BY p.portfolio_name
                    HAVING COUNT(DISTINCT a.asset_type) >= 3
                    ORDER BY asset_type_count DESC
                    """
                    execute_query(query, locals_dict)
            else:
                st.warning("Portfolios and Assets data must be loaded.")

        elif advanced_query_type == "Inactive Users (No Transactions)":
            if 'users' in locals_dict and 'transactions' in locals_dict:
                if st.button("Run 'Inactive Users (No Transactions)' Query"):
                    query = """
                    SELECT u.id, u.name
                    FROM users u
                    LEFT JOIN portfolios p ON u.id = p.user_id
                    LEFT JOIN assets a ON p.id = a.portfolio_id
                    LEFT JOIN transactions t ON a.id = t.asset_id
                    WHERE t.id IS NULL
                    GROUP BY u.id, u.name
                    """
                    execute_query(query, locals_dict)
            else:
                st.warning("Users, Portfolios, Assets, and Transactions data must be loaded.")

        elif advanced_query_type == "Top Performing Assets by Return Rate":
            if 'assets' in locals_dict:
                if st.button("Run 'Top Performing Assets by Return Rate' Query"):
                    query = """
                    SELECT symbol, ((current_price - purchase_price) / purchase_price) * 100 AS return_rate
                    FROM assets
                    ORDER BY return_rate DESC
                    LIMIT 10
                    """
                    execute_query(query, locals_dict)
            else:
                st.warning("Assets data must be loaded.")

        elif advanced_query_type == "Custom Subquery":
            st.markdown("""
            **Custom Subquery Example:**
            ```sql
            SELECT u.name, p.portfolio_name
            FROM users u
            JOIN portfolios p ON u.id = p.user_id
            WHERE p.id IN (SELECT portfolio_id FROM assets WHERE asset_type = 'Stock')
            ```
            """)
            if st.button("Run 'Custom Subquery' Query"):
                query = """
                SELECT u.name, p.portfolio_name
                FROM users u
                JOIN portfolios p ON u.id = p.user_id
                WHERE p.id IN (SELECT portfolio_id FROM assets WHERE asset_type = 'Stock')
                """
                execute_query(query, locals_dict)

        elif advanced_query_type == "Window Functions Example":
            if 'transactions' in locals_dict:
                if st.button("Run 'Window Functions Example' Query"):
                    query = """
                    SELECT 
                        t.id, 
                        t.transaction_type, 
                        t.quantity, 
                        t.price_per_unit,
                        AVG(t.quantity) OVER (PARTITION BY t.transaction_type) AS avg_quantity
                    FROM transactions t
                    ORDER BY t.transaction_type
                    """
                    execute_query(query, locals_dict)
            else:
                st.warning("Transactions data must be loaded.")

    else:
        st.warning("Please log in to access this section.")

# OOP Tab
with tab8:
    st.header("Object-Oriented Programming (OOP) and the 4 Pillars")

    st.markdown("""
    ## Introduction to OOP

    Object-Oriented Programming (OOP) is a programming paradigm that uses "objects" to design applications and computer programs. It utilizes several key concepts:

    1. **Encapsulation**
    2. **Inheritance**
    3. **Polymorphism**
    4. **Abstraction**

    We'll explore each of these pillars with explanations, code examples, and diagrams.
    """)

    # Encapsulation
    st.subheader("1. Encapsulation")
    st.markdown("""
    **Encapsulation** is the mechanism of hiding the internal state of an object and requiring all interaction to be performed through an object's methods. It protects the integrity of the object's data.

    **Example in Python:**
    """)

    # Encapsulation Code Example
    encapsulation_code = '''
class BankAccount:
    def __init__(self, initial_balance):
        self.__balance = initial_balance  # Private variable

    def deposit(self, amount):
        self.__balance += amount

    def withdraw(self, amount):
        if amount <= self.__balance:
            self.__balance -= amount
            return amount
        else:
            print("Insufficient funds")
            return 0

    def get_balance(self):
        return self.__balance

# Usage
account = BankAccount(1000)
account.deposit(500)
print("Balance:", account.get_balance())
withdrawn = account.withdraw(300)
print("Withdrawn:", withdrawn)
print("Balance:", account.get_balance())
    '''

    st.code(encapsulation_code, language='python')

    st.markdown("""
    In the example, `__balance` is a private variable, and it can only be accessed through the methods provided.

    **Diagram:**
    """)

    # Encapsulation Diagram
    encapsulation_diagram = graphviz.Digraph()
    encapsulation_diagram.node('BankAccount', 'BankAccount\n- __balance')
    encapsulation_diagram.node('Methods', 'Methods\n+ deposit()\n+ withdraw()\n+ get_balance()')
    encapsulation_diagram.edge('BankAccount', 'Methods')
    st.graphviz_chart(encapsulation_diagram)

    # Inheritance
    st.subheader("2. Inheritance")
    st.markdown("""
    **Inheritance** allows a class (child class) to inherit attributes and methods from another class (parent class). It promotes code reusability.

    **Example in Python:**
    """)

    # Inheritance Code Example
    inheritance_code = '''
class Vehicle:
    def __init__(self, make, model):
        self.make = make
        self.model = model

    def drive(self):
        print(f"Driving {self.make} {self.model}")

class Car(Vehicle):  # Inherits from Vehicle
    def __init__(self, make, model, num_doors):
        super().__init__(make, model)
        self.num_doors = num_doors

# Usage
my_car = Car("Toyota", "Camry", 4)
my_car.drive()
    '''

    st.code(inheritance_code, language='python')

    st.markdown("""
    `Car` inherits from `Vehicle`, so it has access to the `drive()` method.

    **Diagram:**
    """)

    # Inheritance Diagram
    inheritance_diagram = graphviz.Digraph()
    inheritance_diagram.node('Vehicle', 'Vehicle\n+ make\n+ model\n+ drive()')
    inheritance_diagram.node('Car', 'Car\n+ num_doors')
    inheritance_diagram.edge('Vehicle', 'Car', label='inherits')
    st.graphviz_chart(inheritance_diagram)

    # Polymorphism
    st.subheader("3. Polymorphism")
    st.markdown("""
    **Polymorphism** allows methods to do different things based on the object it is acting upon, even if they share the same name.

    **Example in Python:**
    """)

    # Polymorphism Code Example
    polymorphism_code = '''
class Shape:
    def area(self):
        pass

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return 3.1416 * self.radius ** 2

# Usage
shapes = [Rectangle(3, 4), Circle(5)]
for shape in shapes:
    print("Area:", shape.area())
    '''

    st.code(polymorphism_code, language='python')

    st.markdown("""
    Both `Rectangle` and `Circle` have an `area()` method, but the implementation differs.

    **Diagram:**
    """)

    # Polymorphism Diagram
    polymorphism_diagram = graphviz.Digraph()
    polymorphism_diagram.node('Shape', 'Shape\n+ area()')
    polymorphism_diagram.node('Rectangle', 'Rectangle\n+ width\n+ height\n+ area()')
    polymorphism_diagram.node('Circle', 'Circle\n+ radius\n+ area()')
    polymorphism_diagram.edge('Shape', 'Rectangle', label='inherits')
    polymorphism_diagram.edge('Shape', 'Circle', label='inherits')
    st.graphviz_chart(polymorphism_diagram)

    # Abstraction
    st.subheader("4. Abstraction")
    st.markdown("""
    **Abstraction** is the concept of hiding the complex reality while exposing only the necessary parts. It focuses on the essential qualities rather than specific characteristics.

    **Example in Python:**
    """)

    # Abstraction Code Example
    abstraction_code = '''
from abc import ABC, abstractmethod

class PaymentProcessor(ABC):
    @abstractmethod
    def process_payment(self, amount):
        pass

class CreditCardProcessor(PaymentProcessor):
    def process_payment(self, amount):
        print(f"Processing credit card payment of ${amount}")

class PayPalProcessor(PaymentProcessor):
    def process_payment(self, amount):
        print(f"Processing PayPal payment of ${amount}")

# Usage
processors = [CreditCardProcessor(), PayPalProcessor()]
for processor in processors:
    processor.process_payment(100)
    '''

    st.code(abstraction_code, language='python')

    st.markdown("""
    `PaymentProcessor` is an abstract base class that defines the `process_payment()` method without implementation.

    **Diagram:**
    """)

    # Abstraction Diagram
    abstraction_diagram = graphviz.Digraph()
    abstraction_diagram.node('PaymentProcessor', 'PaymentProcessor\n+ process_payment()')
    abstraction_diagram.node('CreditCardProcessor', 'CreditCardProcessor\n+ process_payment()')
    abstraction_diagram.node('PayPalProcessor', 'PayPalProcessor\n+ process_payment()')
    abstraction_diagram.edge('PaymentProcessor', 'CreditCardProcessor', label='inherits')
    abstraction_diagram.edge('PaymentProcessor', 'PayPalProcessor', label='inherits')
    st.graphviz_chart(abstraction_diagram)

    st.markdown("""
    ## Conclusion

    Understanding these four pillars of OOP is essential for designing robust, reusable, and maintainable software. They allow developers to model real-world entities and relationships in code.
    """)

# API Documentation Tab
with tab9:
    st.header("API Documentation")

    st.markdown("""
    ## Overview

    This section provides documentation for all the API endpoints available in the Portfolio API.

    The base URL for all endpoints is:

    ```
    http://localhost:8080
    ```

    ---
    """)

    # User Controller Endpoints
    st.subheader("User Controller")
    st.markdown("""
    **Endpoints:**

    - `GET /api/users/{id}`: Retrieve a user by ID.
    - `PUT /api/users/{id}`: Update a user's information.
    - `DELETE /api/users/{id}`: Delete a user.
    - `GET /api/users`: Retrieve a list of users.
    - `POST /api/users`: Create a new user.
    - `GET /api/users/email/{email}`: Retrieve a user by email.
    - `GET /api/users/count`: Get the total number of users.
    - `GET /api/users/account/{accountNumber}`: Retrieve a user by account number.

    ---
    """)

    # Portfolio Controller Endpoints
    st.subheader("Portfolio Controller")
    st.markdown("""
    **Endpoints:**

    - `GET /api/portfolios/user/{userId}`: Retrieve portfolios for a specific user.

    ---
    """)

    # Asset Controller Endpoints
    st.subheader("Asset Controller")
    st.markdown("""
    **Endpoints:**

    - `GET /api/assets/portfolio/{portfolioId}`: Retrieve assets within a specific portfolio.

    ---
    """)

    # Transaction Controller Endpoints
    st.subheader("Transaction Controller")
    st.markdown("""
    **Endpoints:**

    - `GET /api/transactions/asset/{assetId}`: Retrieve transactions for a specific asset.

    ---
    """)

    # Home Controller Endpoints
    st.subheader("Home Controller")
    st.markdown("""
    **Endpoints:**

    - `GET /`: Home endpoint.
    - `GET /health`: Health check endpoint.

    ---
    """)

    # Schemas
    st.subheader("Schemas")
    st.markdown("""
    The following schemas represent the data models used in the API.

    ### User

    ```json
    {
        "id": integer,
        "name": string,
        "email": string,
        "accountNumber": string,
        "dateOfBirth": string (ISO date),
        "phoneNumber": string,
        "address": string,
        "portfolios": [Portfolio]
    }
    ```

    ### Portfolio

    ```json
    {
        "id": integer,
        "portfolioName": string,
        "creationDate": string (ISO date),
        "portfolioType": string,
        "userId": integer,
        "assets": [Asset]
    }
    ```

    ### Asset

    ```json
    {
        "id": integer,
        "symbol": string,
        "assetType": string,
        "quantity": integer,
        "purchasePrice": float,
        "currentPrice": float,
        "totalValue": float,
        "portfolioId": integer,
        "transactions": [Transaction]
    }
    ```

    ### Transaction

    ```json
    {
        "id": integer,
        "transactionType": string,
        "transactionDate": string (ISO datetime),
        "quantity": integer,
        "pricePerUnit": float,
        "assetId": integer
    }
    ```

    ### PageUser

    Represents paginated user data.

    ### PageableObject

    Pagination information for requests.

    ### SortObject

    Sorting information for requests.

    ---
    """)

    st.markdown("""
    ## Swagger UI

    For interactive API documentation and testing, you can access the Swagger UI at:

    ```
    http://localhost:8080/swagger-ui/index.html
    ```

    The Swagger UI provides a web-based interface to interact with the API endpoints, view request and response schemas, and execute API calls directly from your browser.

    ---
    """)

    st.markdown("""
    ## Notes

    - Ensure that the API server is running and accessible at the specified base URL.
    - Authentication is required for certain endpoints; use the authentication fields in the sidebar.
    """)
