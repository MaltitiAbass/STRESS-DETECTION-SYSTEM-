import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import streamlit as st
import mysql.connector

@st.cache_data()
def load_data():
    """This function returns the preprocessed data."""
    # Load the Stress dataset into DataFrame
    df = pd.read_csv('Stress.csv')
    # Rename the column names in the DataFrame
    df.rename(columns={"t": "bt"}, inplace=True)
    # Perform feature and target split
    X = df[["sr", "rr", "bt", "lm", "bo", "rem", "sh", "hr"]]
    y = df['sl']
    return df, X, y

@st.cache_data()
def train_model(X, y):
    """This function trains the model and returns the model and model score."""
    model = DecisionTreeClassifier(
        ccp_alpha=0.0, class_weight=None, criterion='entropy',
        max_depth=4, max_features=None, max_leaf_nodes=None,
        min_impurity_decrease=0.0, min_samples_leaf=1,
        min_samples_split=2, min_weight_fraction_leaf=0.0,
        random_state=42, splitter='best'
    )
    model.fit(X, y)
    score = model.score(X, y)
    return model, score

def predict(X, y, features):
    """This function makes predictions based on the trained model."""
    model, score = train_model(X, y)
    prediction = model.predict(np.array(features).reshape(1, -1))
    return prediction, score

def get_db_connection():
    """This function establishes a connection to the database."""
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="stress_detection"
    )

def authenticate_user(username, password):
    """This function authenticates a user based on username and password."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM users WHERE username=%s AND password=%s"
    cursor.execute(query, (username, password))
    user = cursor.fetchone()
    conn.close()
    return user is not None

def authenticate_admin(username, password):
    """This function authenticates an admin user."""
    return username == "admin" and password == "admin12345"

def register_user(first_name, last_name, email, phone_number, username, password):
    """This function registers a new user in the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
    INSERT INTO users (first_name, last_name, email, phone_number, username, password)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    try:
        cursor.execute(query, (first_name, last_name, email, phone_number, username, password))
        conn.commit()
        success = True
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        success = False
    conn.close()
    return success

def get_all_users():
    """This function retrieves all users from the database."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT username, email, first_name, last_name, phone_number FROM users")
    users = cursor.fetchall()
    conn.close()
    return users

def reset_user_password(username, new_password):
    """This function resets the password for a given username."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET password=%s WHERE username=%s", (new_password, username))
    conn.commit()
    conn.close()

def verify_phone_number(username, phone_number):
    """This function verifies if the phone number matches the given username."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username=%s AND phone_number=%s", (username, phone_number))
    user = cursor.fetchone()
    conn.close()
    return user is not None

def send_message(from_user, to_user, content, category="General"):
    """This function sends a message from one user to another."""
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "INSERT INTO messages (from_user, to_user, content, category) VALUES (%s, %s, %s, %s)"
    try:
        cursor.execute(query, (from_user, to_user, content, category))
        conn.commit()
        success = True
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        success = False
    conn.close()
    return success

def get_messages(username, filter_by_sender=None, filter_by_keyword=None, filter_by_category=None):
    """This function retrieves messages for a specific user with optional filters."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT from_user, to_user, content, category FROM messages WHERE to_user=%s OR from_user=%s"
    params = [username, username]
    
    if filter_by_sender:
        query += " AND from_user LIKE %s"
        params.append(f"%{filter_by_sender}%")
    if filter_by_keyword:
        query += " AND content LIKE %s"
        params.append(f"%{filter_by_keyword}%")
    if filter_by_category and filter_by_category != "All":
        query += " AND category=%s"
        params.append(filter_by_category)
    
    cursor.execute(query, params)
    messages = cursor.fetchall()
    conn.close()
    return messages

def reply_to_message(recipient, reply_content):
    """This function allows the admin to reply to user messages."""
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "INSERT INTO messages (from_user, to_user, content, category) VALUES (%s, %s, %s, %s)"
    try:
        cursor.execute(query, ('admin', recipient, reply_content, 'Reply'))
        conn.commit()
        success = True
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        success = False
    conn.close()
    return success

def store_report(title, description):
    """This function stores a report in the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "INSERT INTO reports (title, description) VALUES (%s, %s)"
    try:
        cursor.execute(query, (title, description))
        conn.commit()
        success = True
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        success = False
    conn.close()
    return success

def get_all_reports():
    """This function retrieves all reports from the database."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM reports"
    cursor.execute(query)
    reports = cursor.fetchall()
    conn.close()
    return reports
