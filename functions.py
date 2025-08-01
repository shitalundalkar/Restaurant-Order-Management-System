
# Connect to Database

import sqlite3

DB_NAME = 'restaurant.db'

def connect():
    return sqlite3.connect(DB_NAME)


# ------------------Menu Management----------------------------------

def add_menu_item(name, category, price):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO menu (name, category, price) VALUES (?, ?, ?)",
                   (name, category, price))
    conn.commit()
    conn.close()

def get_menu():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT item_id, name, category, price, available FROM menu WHERE available = 1")
    rows = cursor.fetchall()
    conn.close()
    return rows


# ---------------Place and View Orders-----------------

def place_order(customer_name, items):  # items = [(item_id, quantity)]
    conn = connect()
    cursor = conn.cursor()
    
    # Insert into orders
    cursor.execute("INSERT INTO orders (customer_name) VALUES (?)", (customer_name,))
    order_id = cursor.lastrowid

    # Insert into order_items
    for item_id, qty in items:
        cursor.execute("INSERT INTO order_items (order_id, item_id, quantity) VALUES (?, ?, ?)",
                       (order_id, item_id, qty))

    conn.commit()
    conn.close()
    return order_id


# -----------Admin: View & Update Orders--------------

def get_all_orders():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT o.order_id, o.customer_name, o.status, o.timestamp,
               GROUP_CONCAT(m.name || ' x' || oi.quantity, ', ')
        FROM orders o
        JOIN order_items oi ON o.order_id = oi.order_id
        JOIN menu m ON oi.item_id = m.item_id
        GROUP BY o.order_id
        ORDER BY o.timestamp DESC
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows

def update_order_status(order_id, new_status):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("UPDATE orders SET status = ? WHERE order_id = ?", (new_status, order_id))
    conn.commit()
    conn.close()

#-----------------------Customer: Track Order---------------------------

def get_order_status(order_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT status FROM orders WHERE order_id = ?", (order_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else "Invalid Order ID"


