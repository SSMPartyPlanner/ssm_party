import os
import uuid
import qrcode

from dotenv import load_dotenv
load_dotenv()

from flask import Flask, render_template, request, redirect, session
from werkzeug.utils import secure_filename

import mysql.connector

app = Flask(__name__)
app.secret_key = "ssm_secret_key"


def get_db_connection():

    print("HOST =", os.getenv("MYSQLHOST"))
    print("PORT =", os.getenv("MYSQLPORT"))
    print("USER =", os.getenv("MYSQLUSER"))
    print("DB =", os.getenv("MYSQLDATABASE"))

    conn = mysql.connector.connect(
        host=os.getenv("MYSQLHOST"),
        user=os.getenv("MYSQLUSER"),
        password=os.getenv("MYSQLPASSWORD"),
        database=os.getenv("MYSQLDATABASE"),
        port=int(os.getenv("MYSQLPORT"))
    )

    return conn


@app.route('/')
def home():
    try:
        return render_template('index.html')
    except Exception as e:
        return str(e)


@app.route('/admin')
def admin():
    return render_template('admin_login.html')


# Admin Login Check
@app.route('/admin/login', methods=['POST'])
def admin_login():
    username = request.form['username']
    password = request.form['password']

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM admin WHERE username=%s AND password=%s",
            (username, password)
        )
        admin_user = cursor.fetchone()

        cursor.close()
        conn.close()

        if admin_user:
            session['admin'] = True
            return redirect('/dashboard')

        return "Invalid Login"

    except Exception as e:
        print("DB Error in admin_login:", e)
        return "Something went wrong. Please try again.", 500


# Dashboard
@app.route('/dashboard')
def dashboard():
    if not session.get('admin'):
        return redirect('/admin')

    status = request.args.get('status')
    event_type = request.args.get('event_type')
    from_date = request.args.get('from_date')
    to_date = request.args.get('to_date')

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        query = "SELECT * FROM bookings WHERE 1=1"
        values = []

        if status:
            query += " AND status=%s"
            values.append(status)

        if event_type:
            query += " AND event_type=%s"
            values.append(event_type)

        if from_date:
            query += " AND event_date >= %s"
            values.append(from_date)

        if to_date:
            query += " AND event_date <= %s"
            values.append(to_date)

        query += " ORDER BY id DESC"

        cursor.execute(query, values)
        bookings = cursor.fetchall()

        cursor.execute("SELECT COUNT(*) AS total FROM bookings")
        total_count = cursor.fetchone()['total']

        cursor.execute("SELECT COUNT(*) AS total FROM bookings WHERE status='Pending'")
        pending_count = cursor.fetchone()['total']

        cursor.execute("SELECT COUNT(*) AS total FROM bookings WHERE status='Confirmed'")
        confirmed_count = cursor.fetchone()['total']

        cursor.execute("SELECT COUNT(*) AS total FROM bookings WHERE status='Completed'")
        completed_count = cursor.fetchone()['total']

        cursor.close()
        conn.close()

        return render_template(
            'dashboard.html',
            bookings=bookings,
            total_count=total_count,
            pending_count=pending_count,
            confirmed_count=confirmed_count,
            completed_count=completed_count
        )

    except Exception as e:
        print("DB Error in dashboard:", e)
        return "Something went wrong loading the dashboard.", 500


# Save Booking
@app.route('/booking', methods=['POST'])
def booking():
    name = request.form['name']
    phone = request.form['phone']
    event_type = request.form['event_type']
    package_name = request.form['package_name']
    event_date = request.form['event_date']
    message = request.form['message']

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        sql = """
            INSERT INTO bookings
            (name, phone, event_type, package_name, event_date, message)
            VALUES (%s,%s,%s,%s,%s,%s)
        """

        values = (
            name,
            phone,
            event_type,
            package_name,
            event_date,
            message
        )

        cursor.execute(sql, values)
        conn.commit()

        cursor.close()
        conn.close()

        return redirect('/?booked=1')

    except Exception as e:
        print("DB Error in booking:", e)
        return "Something went wrong saving your booking. Please try again.", 500


@app.route('/update_status/<int:id>', methods=['POST'])
def update_status(id):
    if not session.get('admin'):
        return redirect('/admin')

    status = request.form['status']

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE bookings
            SET status=%s
            WHERE id=%s
            """,
            (status, id)
        )

        conn.commit()

        cursor.close()
        conn.close()

        return redirect('/dashboard')

    except Exception as e:
        print("DB Error in update_status:", e)
        return "Something went wrong updating the status.", 500


# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/admin')


@app.route("/photobooth")
def photobooth():

    if "admin" not in session:
        return redirect("/admin")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM photobooth_events
        ORDER BY id DESC
    """)

    events = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "photobooth.html",
        events=events
    )

print(app.url_map)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)