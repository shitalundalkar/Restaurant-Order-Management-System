import streamlit as st
from functions import *

st.set_page_config(page_title="🍽️ Restaurant Order Management", layout="wide")
st.title("🍽️ Restaurant Order Management System")

# Sidebar for role selection
role = st.sidebar.selectbox("Choose Role", ["Customer", "Admin"])

# ==========================
# 👤 CUSTOMER SECTION
# ==========================
if role == "Customer":
    st.subheader("🧑‍🍳 Welcome, Customer!")
    menu = get_menu()

    if not menu:
        st.warning("No menu items available.")
    else:
        st.markdown("### 📝 Browse Menu & Place Order")
        selected_items = {}
        for item_id, name, category, price, available in menu:
            qty = st.number_input(f"{name} ({category}) - ₹{price}", min_value=0, max_value=10, key=item_id)
            if qty > 0:
                selected_items[item_id] = qty

        customer_name = st.text_input("Enter your name")
        if st.button("Place Order") and selected_items and customer_name:
            items = list(selected_items.items())
            order_id = place_order(customer_name, items)
            st.success(f"✅ Order placed successfully! Your Order ID is {order_id}")

    st.markdown("---")
    st.markdown("### 🔎 Track Your Order")
    track_id = st.number_input("Enter Order ID", step=1)
    if st.button("Track"):
        status = get_order_status(track_id)
        st.info(f"📦 Order Status: **{status}**")

# ==========================
# 👨‍🍳 ADMIN SECTION (with password)
# ==========================
elif role == "Admin":
    st.subheader("🔐 Admin Login")

    admin_password = st.text_input("Enter Admin Password", type="password")
    if st.button("Login"):
        if admin_password == "admin123":
            st.success("🔓 Access granted. Welcome, Admin!")

            st.markdown("### 📋 Add New Menu Item")
            with st.form("add_menu_form"):
                name = st.text_input("Dish Name")
                category = st.text_input("Category")
                price = st.number_input("Price", min_value=1.0)
                submitted = st.form_submit_button("Add Item")
                if submitted and name:
                    add_menu_item(name, category, price)
                    st.success("✅ Item added to menu!")

            st.markdown("---")
            st.markdown("### 📦 View & Update Orders")

            orders = get_all_orders()
            if not orders:
                st.warning("No orders yet.")
            else:
                for order in orders:
                    order_id, customer, status, timestamp, items = order
                    with st.expander(f"Order #{order_id} by {customer} ({status})"):
                        st.write(f"🕒 Time: {timestamp}")
                        st.write(f"🧾 Items: {items}")
                        new_status = st.selectbox("Update Status", ["Pending", "In Progress", "Completed"],
                                                  index=["Pending", "In Progress", "Completed"].index(status),
                                                  key=order_id)
                        if st.button("Update", key=f"update_{order_id}"):
                            update_order_status(order_id, new_status)
                            st.success(f"✅ Order #{order_id} status updated to {new_status}")
        else:
            st.error("❌ Incorrect password. Access denied.")
