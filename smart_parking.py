import streamlit as st
import streamlit.components.v1 as components
import sqlite3
import pandas as pd
from datetime import datetime, date

# ==========================================================
# Smart Parking Management System
# Developed by Osamah AL-murisi
# ==========================================================

DB_NAME = "parking_system.db"

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "Osamah2002"

LEFT_CAR_IMAGE = "https://images.unsplash.com/photo-1494976388531-d1058494cdd8?auto=format&fit=crop&w=900&q=80"
RIGHT_CAR_IMAGE = "https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&w=900&q=80"

CAR_TYPES = {
    "Sedan": "https://images.unsplash.com/photo-1552519507-da3b142c6e3d?auto=format&fit=crop&w=900&q=80",
    "SUV": "https://images.unsplash.com/photo-1533473359331-0135ef1b58bf?auto=format&fit=crop&w=900&q=80",
    "Sports Car": "https://images.unsplash.com/photo-1503376780353-7e6692767b70?auto=format&fit=crop&w=900&q=80",
    "Pickup Truck": "https://images.unsplash.com/photo-1549317661-bd32c8ce0db2?auto=format&fit=crop&w=900&q=80",
    "Electric Car": "https://images.unsplash.com/photo-1560958089-b8a1929cea89?auto=format&fit=crop&w=900&q=80",
    "Luxury Car": "https://images.unsplash.com/photo-1542362567-b07e54358753?auto=format&fit=crop&w=900&q=80",
}


# ==========================================================
# Database
# ==========================================================
def get_connection():
    return sqlite3.connect(DB_NAME)


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS parking_slots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            slot_number TEXT UNIQUE NOT NULL,
            status TEXT NOT NULL,
            hourly_rate REAL DEFAULT 3,
            daily_rate REAL DEFAULT 20
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_name TEXT NOT NULL,
            phone_number TEXT,
            car_number TEXT NOT NULL,
            car_type TEXT DEFAULT 'Sedan',
            slot_number TEXT NOT NULL,
            start_date TEXT,
            end_date TEXT,
            days INTEGER DEFAULT 1,
            hours INTEGER DEFAULT 1,
            hourly_rate REAL DEFAULT 3,
            daily_rate REAL DEFAULT 20,
            total_price REAL DEFAULT 3,
            payment_method TEXT DEFAULT 'Cash',
            payment_status TEXT DEFAULT 'Pending',
            online_provider TEXT DEFAULT 'None',
            transaction_id TEXT DEFAULT 'None',
            booking_time TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def fix_old_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("PRAGMA table_info(parking_slots)")
    slot_columns = [col[1] for col in cursor.fetchall()]

    slot_needed = {
        "hourly_rate": "ALTER TABLE parking_slots ADD COLUMN hourly_rate REAL DEFAULT 3",
        "daily_rate": "ALTER TABLE parking_slots ADD COLUMN daily_rate REAL DEFAULT 20",
    }

    for col, sql in slot_needed.items():
        if col not in slot_columns:
            try:
                cursor.execute(sql)
            except sqlite3.OperationalError:
                pass

    cursor.execute("PRAGMA table_info(bookings)")
    booking_columns = [col[1] for col in cursor.fetchall()]

    booking_needed = {
        "phone_number": "ALTER TABLE bookings ADD COLUMN phone_number TEXT",
        "car_type": "ALTER TABLE bookings ADD COLUMN car_type TEXT DEFAULT 'Sedan'",
        "start_date": "ALTER TABLE bookings ADD COLUMN start_date TEXT",
        "end_date": "ALTER TABLE bookings ADD COLUMN end_date TEXT",
        "days": "ALTER TABLE bookings ADD COLUMN days INTEGER DEFAULT 1",
        "hours": "ALTER TABLE bookings ADD COLUMN hours INTEGER DEFAULT 1",
        "hourly_rate": "ALTER TABLE bookings ADD COLUMN hourly_rate REAL DEFAULT 3",
        "daily_rate": "ALTER TABLE bookings ADD COLUMN daily_rate REAL DEFAULT 20",
        "total_price": "ALTER TABLE bookings ADD COLUMN total_price REAL DEFAULT 3",
        "payment_method": "ALTER TABLE bookings ADD COLUMN payment_method TEXT DEFAULT 'Cash'",
        "payment_status": "ALTER TABLE bookings ADD COLUMN payment_status TEXT DEFAULT 'Pending'",
        "online_provider": "ALTER TABLE bookings ADD COLUMN online_provider TEXT DEFAULT 'None'",
        "transaction_id": "ALTER TABLE bookings ADD COLUMN transaction_id TEXT DEFAULT 'None'",
    }

    for col, sql in booking_needed.items():
        if col not in booking_columns:
            try:
                cursor.execute(sql)
            except sqlite3.OperationalError:
                pass

    conn.commit()
    conn.close()


def get_default_rates(slot_number):
    if slot_number.startswith("VIP"):
        return 8.0, 45.0

    section = slot_number[0]

    if section == "A":
        return 2.0, 12.0
    if section == "B":
        return 3.0, 18.0
    if section == "C":
        return 4.0, 24.0
    if section == "D":
        return 5.0, 30.0
    if section == "E":
        return 6.0, 35.0

    return 3.0, 20.0


def insert_default_slots():
    conn = get_connection()
    cursor = conn.cursor()

    slots = []

    for section in ["A", "B", "C", "D", "E"]:
        for i in range(1, 21):
            slots.append(f"{section}{i}")

    for i in range(1, 11):
        slots.append(f"VIP{i}")

    for slot in slots:
        hourly_rate, daily_rate = get_default_rates(slot)

        cursor.execute("""
            INSERT OR IGNORE INTO parking_slots 
            (slot_number, status, hourly_rate, daily_rate)
            VALUES (?, ?, ?, ?)
        """, (slot, "Available", hourly_rate, daily_rate))

    conn.commit()
    conn.close()


def reset_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM bookings")
    cursor.execute("DELETE FROM parking_slots")

    conn.commit()
    conn.close()

    insert_default_slots()


def get_all_slots():
    conn = get_connection()

    df = pd.read_sql_query("""
        SELECT id, slot_number, status, hourly_rate, daily_rate
        FROM parking_slots
        ORDER BY 
            CASE 
                WHEN slot_number LIKE 'VIP%' THEN 6
                WHEN slot_number LIKE 'A%' THEN 1
                WHEN slot_number LIKE 'B%' THEN 2
                WHEN slot_number LIKE 'C%' THEN 3
                WHEN slot_number LIKE 'D%' THEN 4
                WHEN slot_number LIKE 'E%' THEN 5
                ELSE 7
            END,
            CAST(
                CASE 
                    WHEN slot_number LIKE 'VIP%' THEN REPLACE(slot_number, 'VIP', '')
                    ELSE SUBSTR(slot_number, 2)
                END AS INTEGER
            )
    """, conn)

    conn.close()
    return df


def get_available_slots():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT slot_number
        FROM parking_slots
        WHERE status = 'Available'
        ORDER BY slot_number
    """)

    data = cursor.fetchall()
    conn.close()

    return [x[0] for x in data]


def get_slot_rates(slot_number):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT hourly_rate, daily_rate
        FROM parking_slots
        WHERE slot_number = ?
    """, (slot_number,))

    result = cursor.fetchone()
    conn.close()

    if result:
        return float(result[0]), float(result[1])

    return 3.0, 20.0


def calculate_days(start_date, end_date):
    return max((end_date - start_date).days + 1, 1)


def calculate_total_price(hourly_rate, daily_rate, days, hours):
    one_day_cost = min(hourly_rate * hours, daily_rate)
    return one_day_cost * days


def get_bookings():
    conn = get_connection()

    df = pd.read_sql_query("""
        SELECT 
            id,
            user_name,
            phone_number,
            car_number,
            car_type,
            slot_number,
            start_date,
            end_date,
            days,
            hours,
            hourly_rate,
            daily_rate,
            total_price,
            payment_method,
            payment_status,
            online_provider,
            transaction_id,
            booking_time
        FROM bookings
        ORDER BY booking_time DESC
    """, conn)

    conn.close()
    return df


def book_slot(
    user_name,
    phone_number,
    car_number,
    car_type,
    slot_number,
    start_date,
    end_date,
    days,
    hours,
    payment_method,
    payment_status,
    online_provider,
    transaction_id
):
    conn = get_connection()
    cursor = conn.cursor()

    booking_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    hourly_rate, daily_rate = get_slot_rates(slot_number)
    total_price = calculate_total_price(hourly_rate, daily_rate, days, hours)

    cursor.execute("""
        INSERT INTO bookings 
        (
            user_name, phone_number, car_number, car_type, slot_number,
            start_date, end_date, days, hours,
            hourly_rate, daily_rate, total_price,
            payment_method, payment_status, online_provider, transaction_id, booking_time
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        user_name,
        phone_number,
        car_number,
        car_type,
        slot_number,
        str(start_date),
        str(end_date),
        days,
        hours,
        hourly_rate,
        daily_rate,
        total_price,
        payment_method,
        payment_status,
        online_provider,
        transaction_id,
        booking_time
    ))

    cursor.execute("""
        UPDATE parking_slots
        SET status = 'Booked'
        WHERE slot_number = ?
    """, (slot_number,))

    conn.commit()
    conn.close()

    return {
        "user_name": user_name,
        "phone_number": phone_number,
        "car_number": car_number,
        "car_type": car_type,
        "slot_number": slot_number,
        "start_date": str(start_date),
        "end_date": str(end_date),
        "days": days,
        "hours": hours,
        "hourly_rate": hourly_rate,
        "daily_rate": daily_rate,
        "total_price": total_price,
        "payment_method": payment_method,
        "payment_status": payment_status,
        "online_provider": online_provider,
        "transaction_id": transaction_id,
        "booking_time": booking_time
    }


def cancel_booking(slot_number):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM bookings WHERE slot_number = ?", (slot_number,))
    cursor.execute("UPDATE parking_slots SET status = 'Available' WHERE slot_number = ?", (slot_number,))

    conn.commit()
    conn.close()


def add_parking_slot(slot_number, hourly_rate, daily_rate):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO parking_slots 
        (slot_number, status, hourly_rate, daily_rate)
        VALUES (?, ?, ?, ?)
    """, (slot_number, "Available", hourly_rate, daily_rate))

    conn.commit()
    conn.close()


def update_slot_prices(slot_number, hourly_rate, daily_rate):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE parking_slots
        SET hourly_rate = ?, daily_rate = ?
        WHERE slot_number = ?
    """, (hourly_rate, daily_rate, slot_number))

    conn.commit()
    conn.close()


def delete_parking_slot(slot_number):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM bookings WHERE slot_number = ?", (slot_number,))
    cursor.execute("DELETE FROM parking_slots WHERE slot_number = ?", (slot_number,))

    conn.commit()
    conn.close()


def dataframe_to_csv_bytes(df):
    return df.to_csv(index=False).encode("utf-8-sig")


def create_receipt_text(invoice):
    return f"""
========================================
SMART PARKING BOOKING RECEIPT
========================================
Customer Name : {invoice.get("user_name", "")}
Phone Number  : {invoice.get("phone_number", "")}
Car Plate No. : {invoice.get("car_number", "")}
Car Type      : {invoice.get("car_type", "")}
Slot Number   : {invoice.get("slot_number", "")}

Start Date    : {invoice.get("start_date", "")}
End Date      : {invoice.get("end_date", "")}
Days          : {invoice.get("days", "")}
Hours / Day   : {invoice.get("hours", "")}

Hourly Price  : ${float(invoice.get("hourly_rate", 0)):.2f}
Daily Max     : ${float(invoice.get("daily_rate", 0)):.2f}
Total Price   : ${float(invoice.get("total_price", 0)):.2f}

Payment Method : {invoice.get("payment_method", "")}
Payment Status : {invoice.get("payment_status", "")}
Online Provider: {invoice.get("online_provider", "")}
Transaction ID : {invoice.get("transaction_id", "")}

Booking Time  : {invoice.get("booking_time", "")}
========================================
Developed by Osamah AL-murisi
========================================
"""


# ==========================================================
# Style
# ==========================================================
def apply_style():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800;900&display=swap');

        html, body, [class*="css"] {
            font-family: 'Cairo', sans-serif;
        }

        .stApp {
            background: linear-gradient(135deg, #07111f 0%, #0f172a 50%, #102a43 100%);
            color: white;
        }

        header[data-testid="stHeader"],
        div[data-testid="stToolbar"],
        div[data-testid="stDecoration"],
        div[data-testid="stStatusWidget"],
        section[data-testid="stSidebar"] {
            display: none !important;
        }

        #MainMenu, footer {
            visibility: hidden !important;
        }

        .block-container {
            max-width: 1450px !important;
            padding-top: 0rem !important;
            padding-left: 2rem !important;
            padding-right: 2rem !important;
            padding-bottom: 3rem !important;
        }

        .st-key-menu_toggle_btn {
            display: flex !important;
            justify-content: center !important;
        }

        .st-key-menu_toggle_btn button {
            background: transparent !important;
            color: white !important;
            border: none !important;
            width: 115px !important;
            height: 65px !important;
            font-size: 44px !important;
            font-weight: 900 !important;
            box-shadow: none !important;
            margin-top: -155px !important;
            margin-bottom: 25px !important;
            text-shadow: 0 5px 20px rgba(0,0,0,0.55) !important;
            cursor: pointer !important;
        }

        div[data-testid="stExpander"] {
            width: 560px !important;
            max-width: 94% !important;
            margin: -38px auto 30px auto !important;
            background: rgba(255,255,255,0.08) !important;
            border: 1px solid rgba(255,255,255,0.18) !important;
            border-radius: 24px !important;
            box-shadow: 0 22px 50px rgba(0,0,0,0.38) !important;
            overflow: hidden !important;
            padding-bottom: 18px !important;
        }

        div[data-testid="stExpander"] summary {
            min-height: 55px !important;
            padding: 10px 22px !important;
            background: rgba(15,23,42,0.90) !important;
            color: white !important;
            font-size: 22px !important;
            font-weight: 900 !important;
        }

        div[data-testid="stExpander"] summary p {
            color: white !important;
            font-size: 22px !important;
            font-weight: 900 !important;
        }

        .st-key-menu_home,
        .st-key-menu_slots,
        .st-key-menu_book,
        .st-key-menu_receipt,
        .st-key-menu_cancel,
        .st-key-menu_admin {
            width: 100% !important;
            display: flex !important;
            justify-content: center !important;
            align-items: center !important;
        }

        .st-key-menu_home button,
        .st-key-menu_slots button,
        .st-key-menu_book button,
        .st-key-menu_receipt button,
        .st-key-menu_cancel button,
        .st-key-menu_admin button {
            width: 380px !important;
            max-width: 380px !important;
            min-width: 380px !important;
            height: 58px !important;
            background: linear-gradient(135deg, rgba(30,41,59,0.96), rgba(51,65,85,0.96)) !important;
            color: white !important;
            border-radius: 17px !important;
            margin: 7px auto 14px auto !important;
            font-weight: 900 !important;
            font-size: 16px !important;
            border: 1px solid rgba(255,255,255,0.16) !important;
            box-shadow: 0 12px 25px rgba(0,0,0,0.22) !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            text-align: center !important;
            white-space: nowrap !important;
        }

        .st-key-menu_home button:hover,
        .st-key-menu_slots button:hover,
        .st-key-menu_book button:hover,
        .st-key-menu_receipt button:hover,
        .st-key-menu_cancel button:hover,
        .st-key-menu_admin button:hover {
            background: linear-gradient(135deg, rgba(14,165,233,0.38), rgba(20,184,166,0.30)) !important;
            border: 1px solid rgba(56,189,248,0.60) !important;
            transform: scale(1.01) !important;
        }

        .side-dev {
            width: 380px !important;
            max-width: 380px !important;
            min-width: 380px !important;
            margin: 22px auto 0 auto !important;
            padding: 16px 20px !important;
            border-radius: 18px !important;
            background: linear-gradient(135deg, rgba(14,165,233,0.34), rgba(20,184,166,0.26)) !important;
            border: 1px solid rgba(56,189,248,0.45) !important;
            text-align: center !important;
            color: #38bdf8 !important;
            font-weight: 900 !important;
            font-size: 15px !important;
            line-height: 1.8 !important;
            box-shadow: 0 12px 30px rgba(0,0,0,0.25) !important;
            user-select: none !important;
        }

        .section-title {
            font-size: 34px;
            font-weight: 900;
            color: white;
            margin: 0 0 15px 0;
            text-shadow: 0 4px 15px rgba(0,0,0,0.7);
        }

        .note {
            color: #cbd5e1;
            font-size: 18px;
            margin-bottom: 22px;
            line-height: 1.8;
            font-weight: 600;
        }

        div[data-testid="stMetric"] {
            background: rgba(255,255,255,0.08);
            padding: 22px;
            border-radius: 22px;
            border: 1px solid rgba(255,255,255,0.14);
            box-shadow: 0 15px 35px rgba(0,0,0,0.22);
        }

        div[data-testid="stMetric"] label {
            color: #cbd5e1 !important;
            font-size: 16px !important;
            font-weight: 800 !important;
        }

        div[data-testid="stMetricValue"] {
            color: white !important;
            font-size: 34px !important;
            font-weight: 900 !important;
        }

        .feature-card {
            background: rgba(56,189,248,0.12);
            border: 1px solid rgba(56,189,248,0.35);
            border-radius: 22px;
            padding: 28px;
            min-height: 210px;
            text-align: center;
            margin-bottom: 22px;
            box-shadow: 0 16px 35px rgba(0,0,0,0.25);
            transition: 0.3s ease-in-out;
        }

        .feature-card:hover {
            transform: translateY(-6px);
            background: rgba(56,189,248,0.18);
            border: 1px solid rgba(56,189,248,0.60);
        }

        .feature-icon {
            font-size: 44px;
            margin-bottom: 12px;
        }

        .feature-title {
            font-size: 20px;
            font-weight: 900;
            color: white;
            margin-bottom: 10px;
        }

        .feature-text {
            font-size: 15px;
            color: #cbd5e1;
            line-height: 1.7;
            font-weight: 700;
        }

        .parking-card {
            padding: 18px;
            border-radius: 22px;
            text-align: center;
            font-size: 15px;
            font-weight: 900;
            margin-bottom: 17px;
            box-shadow: 0 14px 30px rgba(0,0,0,0.22);
        }

        .available {
            background: linear-gradient(135deg, #dcfce7, #86efac);
            color: #14532d;
            border: 2px solid #22c55e;
        }

        .booked {
            background: linear-gradient(135deg, #fee2e2, #fca5a5);
            color: #7f1d1d;
            border: 2px solid #ef4444;
        }

        .vip {
            background: linear-gradient(135deg, #fef3c7, #fbbf24);
            color: #78350f;
            border: 2px solid #f59e0b;
        }

        .price-box, .receipt-box, .car-preview, .payment-box {
            background: rgba(56,189,248,0.12);
            border: 1px solid rgba(56,189,248,0.35);
            border-radius: 18px;
            padding: 18px;
            color: #e0f2fe;
            font-size: 17px;
            font-weight: 900;
            margin: 18px 0;
            text-align: center;
            box-shadow: 0 12px 30px rgba(0,0,0,0.20);
        }

        .receipt-box {
            text-align: left;
            line-height: 1.8;
        }

        .car-img {
            width: 100%;
            max-width: 520px;
            height: 260px;
            object-fit: cover;
            border-radius: 22px;
            border: 2px solid rgba(56,189,248,0.55);
            box-shadow: 0 15px 35px rgba(0,0,0,0.35);
            margin-top: 10px;
        }

        .stButton>button {
            background: linear-gradient(135deg, #0ea5e9, #14b8a6);
            color: white;
            border-radius: 14px;
            min-height: 48px;
            font-size: 17px;
            font-weight: 900;
            border: none;
            padding: 0 26px;
        }

        input, textarea, select {
            border-radius: 14px !important;
        }

        .stAlert {
            border-radius: 16px;
        }

        div[data-testid="stDataFrame"] {
            border-radius: 18px;
            overflow: hidden;
        }

        .footer {
            margin-top: 40px;
            padding: 20px;
            text-align: center;
            color: #cbd5e1;
            background: rgba(255,255,255,0.06);
            border-radius: 18px;
            border: 1px solid rgba(255,255,255,0.12);
        }
        </style>
    """, unsafe_allow_html=True)


# ==========================================================
# Header
# ==========================================================
def car_header():
    components.html(f"""
    <html>
    <head>
    <style>
        body {{
            margin: 0;
            padding: 0;
            background: transparent;
        }}

        .purple-menu-bar {{
            width: 100%;
            height: 185px;
            background: linear-gradient(135deg, #8b00ff, #6a00d4);
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 70px;
            box-sizing: border-box;
            overflow: hidden;
        }}

        .car-box {{
            width: 245px;
            height: 140px;
            border-radius: 25px;
            overflow: hidden;
            border: 3px solid rgba(255,255,255,0.45);
            box-shadow: 0 15px 35px rgba(0,0,0,0.45);
            background: rgba(255,255,255,0.12);
        }}

        .car-box img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
            display: block;
        }}

        .center-space {{
            width: 160px;
            height: 80px;
        }}
    </style>
    </head>
    <body>
        <div class="purple-menu-bar">
            <div class="car-box">
                <img src="{LEFT_CAR_IMAGE}">
            </div>
            <div class="center-space"></div>
            <div class="car-box">
                <img src="{RIGHT_CAR_IMAGE}">
            </div>
        </div>
    </body>
    </html>
    """, height=190)


# ==========================================================
# Pages
# ==========================================================
def home_page():
    slots_df = get_all_slots()

    total_slots = len(slots_df)
    available_slots = len(slots_df[slots_df["status"] == "Available"])
    booked_slots = len(slots_df[slots_df["status"] == "Booked"])
    total_hourly_capacity = slots_df["hourly_rate"].sum()
    total_daily_capacity = slots_df["daily_rate"].sum()

    st.markdown('<div class="section-title">🚗 Smart Parking Management System</div>', unsafe_allow_html=True)

    st.markdown("""
        <div class="note">
            A professional digital system for managing parking spaces, reservations,
            car types, online payments, invoices, search, and admin operations.
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric("Total Slots", total_slots)

    with col2:
        st.metric("Available", available_slots)

    with col3:
        st.metric("Booked", booked_slots)

    with col4:
        st.metric("Hourly Capacity", f"${total_hourly_capacity:.2f}")

    with col5:
        st.metric("Daily Capacity", f"${total_daily_capacity:.2f}")

    st.markdown('<div class="section-title" style="margin-top:40px;">✨ Project Features</div>', unsafe_allow_html=True)

    f1, f2, f3 = st.columns(3)

    with f1:
        st.markdown("""
            <div class="feature-card">
                <div class="feature-icon">🅿️</div>
                <div class="feature-title">Parking Slot Management</div>
                <div class="feature-text">
                    View all parking slots, check availability, and manage booked or available spaces easily.
                </div>
            </div>
        """, unsafe_allow_html=True)

    with f2:
        st.markdown("""
            <div class="feature-card">
                <div class="feature-icon">📌</div>
                <div class="feature-title">Smart Booking</div>
                <div class="feature-text">
                    Customers can book a parking slot by entering their information, car plate number, date, and time.
                </div>
            </div>
        """, unsafe_allow_html=True)

    with f3:
        st.markdown("""
            <div class="feature-card">
                <div class="feature-icon">💵</div>
                <div class="feature-title">Automatic Price Calculation</div>
                <div class="feature-text">
                    The system calculates the total price automatically using hourly and daily parking rates.
                </div>
            </div>
        """, unsafe_allow_html=True)

    f4, f5, f6 = st.columns(3)

    with f4:
        st.markdown("""
            <div class="feature-card">
                <div class="feature-icon">💳</div>
                <div class="feature-title">Online Payment Options</div>
                <div class="feature-text">
                    Supports Cash, Credit Card, and Online Payment with provider name and transaction ID.
                </div>
            </div>
        """, unsafe_allow_html=True)

    with f5:
        st.markdown("""
            <div class="feature-card">
                <div class="feature-icon">🧾</div>
                <div class="feature-title">Booking Receipt</div>
                <div class="feature-text">
                    Generates a professional receipt after booking with customer, car, slot, price, and payment details.
                </div>
            </div>
        """, unsafe_allow_html=True)

    with f6:
        st.markdown("""
            <div class="feature-card">
                <div class="feature-icon">🔐</div>
                <div class="feature-title">Admin Dashboard</div>
                <div class="feature-text">
                    Admin can add, delete, update slots, export CSV files, search bookings, and track income.
                </div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="section-title" style="margin-top:40px;">🚘 Car Types Supported</div>', unsafe_allow_html=True)

    cols = st.columns(3)
    for index, (car_type, image_url) in enumerate(CAR_TYPES.items()):
        with cols[index % 3]:
            st.markdown(
                f"""
                <div class="car-preview">
                    <b>{car_type}</b><br>
                    <img class="car-img" src="{image_url}">
                </div>
                """,
                unsafe_allow_html=True
            )


def slots_page():
    st.markdown('<div class="section-title">🅿️ Parking Slots Status & Prices</div>', unsafe_allow_html=True)

    slots_df = get_all_slots()
    cols = st.columns(5)

    for index, row in slots_df.iterrows():
        col = cols[index % 5]
        slot_number = row["slot_number"]
        status = row["status"]
        hourly_rate = float(row["hourly_rate"])
        daily_rate = float(row["daily_rate"])

        if status == "Booked":
            card_class = "booked"
            icon = "🔴"
            label = "Booked"
        elif slot_number.startswith("VIP"):
            card_class = "vip"
            icon = "⭐"
            label = "VIP Available"
        else:
            card_class = "available"
            icon = "🟢"
            label = "Available"

        col.markdown(
            f"""
            <div class="parking-card {card_class}">
                {icon}<br>
                {slot_number}<br>
                {label}<br>
                💵 ${hourly_rate:.2f} / hour<br>
                📅 ${daily_rate:.2f} / day
            </div>
            """,
            unsafe_allow_html=True
        )


def book_page():
    st.markdown('<div class="section-title">📌 Book Parking Slot</div>', unsafe_allow_html=True)

    available_slots = get_available_slots()

    if len(available_slots) == 0:
        st.warning("No available parking slots right now.")
        return

    col1, col2 = st.columns(2)

    with col1:
        user_name = st.text_input("Customer Name", key="book_customer_name")

    with col2:
        phone_number = st.text_input("Phone Number", key="book_phone_number")

    car_number = st.text_input("Car Plate Number", key="book_car_number")

    car_type = st.selectbox(
        "Choose Car Type",
        list(CAR_TYPES.keys()),
        key="book_car_type"
    )

    st.markdown(
        f"""
        <div class="car-preview">
            <b>Selected Car Type: {car_type}</b><br>
            <img class="car-img" src="{CAR_TYPES[car_type]}">
        </div>
        """,
        unsafe_allow_html=True
    )

    selected_slot = st.selectbox(
        "Choose Available Slot",
        available_slots,
        key="book_selected_slot"
    )

    hourly_rate, daily_rate = get_slot_rates(selected_slot)

    col_start, col_end = st.columns(2)

    with col_start:
        start_date = st.date_input("Start Date", value=date.today(), key="book_start_date")

    with col_end:
        end_date = st.date_input("End Date", value=date.today(), key="book_end_date")

    if end_date < start_date:
        st.error("End date must be after or equal to start date.")
        return

    days = calculate_days(start_date, end_date)

    hours = st.number_input(
        "Hours per Day",
        min_value=1,
        max_value=24,
        value=1,
        step=1,
        key="book_hours"
    )

    payment_method = st.selectbox(
        "Payment Method",
        ["Cash", "Credit Card", "Online Payment"],
        key="book_payment_method"
    )

    online_provider = "None"
    transaction_id = "None"

    if payment_method == "Online Payment":
        st.markdown(
            """
            <div class="payment-box">
                Online payment is simulated for the project.
                No real card or bank information is required.
            </div>
            """,
            unsafe_allow_html=True
        )

        col_online1, col_online2 = st.columns(2)

        with col_online1:
            online_provider = st.selectbox(
                "Online Payment Provider",
                ["PayPal", "Stripe", "Apple Pay", "Google Pay", "Bank Transfer"],
                key="book_online_provider"
            )

        with col_online2:
            transaction_id = st.text_input(
                "Transaction ID",
                value=f"TXN-{datetime.now().strftime('%Y%m%d%H%M%S')}",
                key="book_transaction_id"
            )

        payment_status = st.selectbox(
            "Payment Status",
            ["Paid", "Pending", "Failed"],
            index=0,
            key="book_payment_status_online"
        )

    else:
        payment_status = st.selectbox(
            "Payment Status",
            ["Paid", "Pending"],
            key="book_payment_status_normal"
        )

    day_cost = min(hourly_rate * hours, daily_rate)
    total_price = calculate_total_price(hourly_rate, daily_rate, days, int(hours))

    st.markdown(
        f"""
        <div class="price-box">
            Slot: {selected_slot}<br>
            Car Type: {car_type}<br>
            Hourly Price: ${hourly_rate:.2f}<br>
            Daily Max Price: ${daily_rate:.2f}<br>
            Start Date: {start_date} | End Date: {end_date}<br>
            Days: {days} | Hours per Day: {hours}<br>
            Payment Method: {payment_method}<br>
            Payment Status: {payment_status}<br>
            Online Provider: {online_provider}<br>
            Transaction ID: {transaction_id}<br>
            One Day Cost: ${day_cost:.2f}<br>
            Total Price: ${total_price:.2f}
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button("Book Now", key="book_now_button"):
        missing_fields = []

        if not user_name.strip():
            missing_fields.append("Customer Name")

        if not phone_number.strip():
            missing_fields.append("Phone Number")

        if not car_number.strip():
            missing_fields.append("Car Plate Number")

        if payment_method == "Online Payment" and not transaction_id.strip():
            missing_fields.append("Transaction ID")

        if missing_fields:
            st.warning("Please fill these fields: " + ", ".join(missing_fields))
            return

        invoice = book_slot(
            user_name.strip(),
            phone_number.strip(),
            car_number.strip(),
            car_type,
            selected_slot,
            start_date,
            end_date,
            days,
            int(hours),
            payment_method,
            payment_status,
            online_provider,
            transaction_id.strip()
        )

        st.session_state.last_invoice = invoice
        st.session_state.page = "🧾 Receipt"
        st.success(f"Slot {selected_slot} booked successfully! Total price: ${total_price:.2f}")
        st.balloons()
        st.rerun()


def receipt_page():
    st.markdown('<div class="section-title">🧾 Booking Receipt</div>', unsafe_allow_html=True)

    invoice = st.session_state.get("last_invoice", None)

    if not invoice:
        st.warning("No receipt available yet. Please make a booking first.")
        return

    car_type = invoice.get("car_type", "Sedan")
    car_image = CAR_TYPES.get(car_type, CAR_TYPES["Sedan"])

    st.markdown(
        f"""
        <div class="receipt-box">
            <b>Customer Name:</b> {invoice["user_name"]}<br>
            <b>Phone Number:</b> {invoice["phone_number"]}<br>
            <b>Car Plate Number:</b> {invoice["car_number"]}<br>
            <b>Car Type:</b> {car_type}<br>
            <img class="car-img" src="{car_image}"><br><br>

            <b>Slot Number:</b> {invoice["slot_number"]}<br>
            <b>Start Date:</b> {invoice["start_date"]}<br>
            <b>End Date:</b> {invoice["end_date"]}<br>
            <b>Days:</b> {invoice["days"]}<br>
            <b>Hours per Day:</b> {invoice["hours"]}<br><br>

            <b>Hourly Price:</b> ${invoice["hourly_rate"]:.2f}<br>
            <b>Daily Max Price:</b> ${invoice["daily_rate"]:.2f}<br>
            <b>Total Price:</b> ${invoice["total_price"]:.2f}<br>
            <b>Payment Method:</b> {invoice["payment_method"]}<br>
            <b>Payment Status:</b> {invoice["payment_status"]}<br>
            <b>Online Provider:</b> {invoice["online_provider"]}<br>
            <b>Transaction ID:</b> {invoice["transaction_id"]}<br>
            <b>Booking Time:</b> {invoice["booking_time"]}<br>
        </div>
        """,
        unsafe_allow_html=True
    )

    receipt_text = create_receipt_text(invoice)

    st.download_button(
        label="Download Receipt TXT",
        data=receipt_text,
        file_name=f"receipt_{invoice['slot_number']}.txt",
        mime="text/plain"
    )


def cancel_page():
    st.markdown('<div class="section-title">❌ Cancel Booking</div>', unsafe_allow_html=True)

    bookings_df = get_bookings()

    if bookings_df.empty:
        st.warning("No bookings found.")
        return

    search_text = st.text_input("Search by name, phone, car plate, slot, payment, or transaction")

    filtered_df = bookings_df.copy()

    if search_text.strip():
        keyword = search_text.strip().lower()
        filtered_df = filtered_df[
            filtered_df["user_name"].astype(str).str.lower().str.contains(keyword) |
            filtered_df["phone_number"].astype(str).str.lower().str.contains(keyword) |
            filtered_df["car_number"].astype(str).str.lower().str.contains(keyword) |
            filtered_df["car_type"].astype(str).str.lower().str.contains(keyword) |
            filtered_df["slot_number"].astype(str).str.lower().str.contains(keyword) |
            filtered_df["payment_method"].astype(str).str.lower().str.contains(keyword) |
            filtered_df["payment_status"].astype(str).str.lower().str.contains(keyword) |
            filtered_df["transaction_id"].astype(str).str.lower().str.contains(keyword)
        ]

    if filtered_df.empty:
        st.warning("No matching booking found.")
        return

    booked_slots = filtered_df["slot_number"].tolist()
    selected_slot = st.selectbox("Choose Slot to Cancel", booked_slots)

    booking_info = filtered_df[filtered_df["slot_number"] == selected_slot].iloc[0]

    st.markdown(
        f"""
        <div class="price-box">
            Customer: {booking_info["user_name"]}<br>
            Phone: {booking_info["phone_number"]}<br>
            Car Plate: {booking_info["car_number"]}<br>
            Car Type: {booking_info["car_type"]}<br>
            Slot: {booking_info["slot_number"]}<br>
            Payment: {booking_info["payment_method"]} - {booking_info["payment_status"]}<br>
            Provider: {booking_info["online_provider"]}<br>
            Transaction ID: {booking_info["transaction_id"]}<br>
            Total Price: ${float(booking_info["total_price"]):.2f}
        </div>
        """,
        unsafe_allow_html=True
    )

    confirm_cancel = st.checkbox("I confirm cancelling this booking")

    if st.button("Cancel Booking", disabled=not confirm_cancel):
        cancel_booking(selected_slot)
        st.success(f"Booking for slot {selected_slot} cancelled successfully!")
        st.rerun()


def admin_page():
    st.markdown('<div class="section-title">🔐 Admin Dashboard</div>', unsafe_allow_html=True)

    admin_username = st.text_input("Admin Username")
    admin_password = st.text_input("Admin Password", type="password")

    if admin_username == ADMIN_USERNAME and admin_password == ADMIN_PASSWORD:
        st.success("Admin login successful.")

        slots_df = get_all_slots()
        bookings_df = get_bookings()

        paid_income = bookings_df[bookings_df["payment_status"] == "Paid"]["total_price"].sum() if not bookings_df.empty else 0
        online_income = bookings_df[bookings_df["payment_method"] == "Online Payment"]["total_price"].sum() if not bookings_df.empty else 0

        c1, c2, c3, c4, c5 = st.columns(5)

        with c1:
            st.metric("Total Slots", len(slots_df))

        with c2:
            st.metric("Available", len(slots_df[slots_df["status"] == "Available"]))

        with c3:
            st.metric("Booked", len(slots_df[slots_df["status"] == "Booked"]))

        with c4:
            st.metric("Paid Income", f"${paid_income:.2f}")

        with c5:
            st.metric("Online Income", f"${online_income:.2f}")

        st.markdown('<div class="section-title" style="margin-top:30px;">Search Bookings</div>', unsafe_allow_html=True)

        search_text = st.text_input("Search by name, phone, car plate, payment, provider, or transaction ID")

        filtered_bookings = bookings_df.copy()

        if search_text.strip():
            keyword = search_text.strip().lower()
            filtered_bookings = filtered_bookings[
                filtered_bookings["user_name"].astype(str).str.lower().str.contains(keyword) |
                filtered_bookings["phone_number"].astype(str).str.lower().str.contains(keyword) |
                filtered_bookings["car_number"].astype(str).str.lower().str.contains(keyword) |
                filtered_bookings["car_type"].astype(str).str.lower().str.contains(keyword) |
                filtered_bookings["slot_number"].astype(str).str.lower().str.contains(keyword) |
                filtered_bookings["payment_method"].astype(str).str.lower().str.contains(keyword) |
                filtered_bookings["payment_status"].astype(str).str.lower().str.contains(keyword) |
                filtered_bookings["online_provider"].astype(str).str.lower().str.contains(keyword) |
                filtered_bookings["transaction_id"].astype(str).str.lower().str.contains(keyword)
            ]

        st.markdown('<div class="section-title" style="margin-top:30px;">Parking Slots Table</div>', unsafe_allow_html=True)
        st.dataframe(slots_df, use_container_width=True, hide_index=True)

        st.download_button(
            label="Download Parking Slots CSV",
            data=dataframe_to_csv_bytes(slots_df),
            file_name="parking_slots.csv",
            mime="text/csv"
        )

        st.markdown('<div class="section-title" style="margin-top:30px;">Bookings Table</div>', unsafe_allow_html=True)
        st.dataframe(filtered_bookings, use_container_width=True, hide_index=True)

        st.download_button(
            label="Download Bookings CSV",
            data=dataframe_to_csv_bytes(filtered_bookings),
            file_name="bookings.csv",
            mime="text/csv"
        )

        st.markdown('<div class="section-title" style="margin-top:30px;">Manage Parking Slots & Prices</div>', unsafe_allow_html=True)

        col_add, col_update, col_delete = st.columns(3)

        with col_add:
            new_slot = st.text_input("New Slot Number, example: F1 or VIP11")
            new_hourly_rate = st.number_input("New Slot Hourly Price $", min_value=0.5, max_value=100.0, value=3.0, step=0.5)
            new_daily_rate = st.number_input("New Slot Daily Max Price $", min_value=1.0, max_value=500.0, value=20.0, step=1.0)

            if st.button("Add New Slot"):
                if new_slot.strip() == "":
                    st.warning("Please enter slot number.")
                else:
                    add_parking_slot(new_slot.upper(), float(new_hourly_rate), float(new_daily_rate))
                    st.success(f"Slot {new_slot.upper()} added successfully.")
                    st.rerun()

        with col_update:
            all_slots_for_price = slots_df["slot_number"].tolist()

            if len(all_slots_for_price) > 0:
                price_slot = st.selectbox("Choose Slot to Update Prices", all_slots_for_price)
                current_hourly_rate, current_daily_rate = get_slot_rates(price_slot)

                updated_hourly_rate = st.number_input(
                    "Updated Hourly Price $",
                    min_value=0.5,
                    max_value=100.0,
                    value=float(current_hourly_rate),
                    step=0.5
                )

                updated_daily_rate = st.number_input(
                    "Updated Daily Max Price $",
                    min_value=1.0,
                    max_value=500.0,
                    value=float(current_daily_rate),
                    step=1.0
                )

                if st.button("Update Prices"):
                    update_slot_prices(price_slot, float(updated_hourly_rate), float(updated_daily_rate))
                    st.success(f"Prices for {price_slot} updated successfully.")
                    st.rerun()

        with col_delete:
            all_slots = slots_df["slot_number"].tolist()

            if len(all_slots) > 0:
                delete_slot = st.selectbox("Choose Slot to Delete", all_slots)
                confirm_delete = st.checkbox("I confirm deleting this slot")

                if st.button("Delete Slot", disabled=not confirm_delete):
                    delete_parking_slot(delete_slot)
                    st.success(f"Slot {delete_slot} deleted successfully!")
                    st.rerun()

        st.markdown("---")
        st.warning("Reset System will delete all bookings and restore default slots and prices.")

        confirm_reset = st.checkbox("I confirm resetting the whole system")

        if st.button("Reset System", disabled=not confirm_reset):
            reset_database()
            st.success("System reset successfully.")
            st.rerun()

    elif admin_username != "" or admin_password != "":
        st.error("Wrong admin username or password.")


# ==========================================================
# Main
# ==========================================================
def go_to_page(page_name):
    st.session_state.page = page_name
    st.session_state.show_menu = False
    st.rerun()


def main():
    st.set_page_config(
        page_title="Smart Parking System",
        page_icon="🚗",
        layout="wide"
    )

    create_tables()
    fix_old_database()
    insert_default_slots()
    apply_style()

    if "page" not in st.session_state:
        st.session_state.page = "🏠 Home"

    if "show_menu" not in st.session_state:
        st.session_state.show_menu = False

    car_header()

    if st.button("☰", key="menu_toggle_btn"):
        st.session_state.show_menu = not st.session_state.show_menu
        st.rerun()

    if st.session_state.show_menu:
        with st.expander("☰ Menu", expanded=True):

            if st.button("🏠 Home", key="menu_home"):
                go_to_page("🏠 Home")

            if st.button("🅿️ Parking Slots", key="menu_slots"):
                go_to_page("🅿️ Parking Slots")

            if st.button("📌 Book Slot", key="menu_book"):
                go_to_page("📌 Book Slot")

            if st.button("🧾 Receipt", key="menu_receipt"):
                go_to_page("🧾 Receipt")

            if st.button("❌ Cancel Booking", key="menu_cancel"):
                go_to_page("❌ Cancel Booking")

            if st.button("🔐 Admin Dashboard", key="menu_admin"):
                go_to_page("🔐 Admin Dashboard")

            st.markdown(
                """
                <div class="side-dev">
                    <div>Developed by</div>
                    <div>Osamah AL-murisi</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    if st.session_state.page == "🏠 Home":
        home_page()

    elif st.session_state.page == "🅿️ Parking Slots":
        slots_page()

    elif st.session_state.page == "📌 Book Slot":
        book_page()

    elif st.session_state.page == "🧾 Receipt":
        receipt_page()

    elif st.session_state.page == "❌ Cancel Booking":
        cancel_page()

    elif st.session_state.page == "🔐 Admin Dashboard":
        admin_page()

    st.markdown("""
        <div class="footer">
            Smart Parking Management System | Python • Streamlit • SQLite | Developed by Osamah AL-murisi
        </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()