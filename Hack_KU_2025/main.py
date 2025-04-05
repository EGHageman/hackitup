from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Connect to SQLite Database
def get_db_connection():
    conn = sqlite3.connect('data.db')  # 'data.db' is the name of the SQLite database
    conn.row_factory = sqlite3.Row  # This allows us to access rows as dictionaries
    return conn

# Builds the contidtions data base (only one so far) 
def init_db():
    conn = get_db_connection()

    #The sql data base column build
    #IMPORTANT: Remeber to delete or manually add onto database if a new entry is introduced, EG
    conn.execute('''CREATE TABLE IF NOT EXISTS items (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        value INTEGER NOT NULL,
                        date_time TEXT NOT NULL
                    )''')

    conn.commit()
    conn.close()

@app.route('/')
def home():
    return render_template('index.html')  # The homepage that links to `/patient`

@app.route('/sign-in', methods=['GET', 'POST'])
def sign_in():
    # Mock sign-in (no actual login functionality)
    if request.method == 'POST':
        # Normally, you would check the credentials here, but we will just mock the process, EG.
        return redirect(url_for('patient'))  # Redirect to patient page after submitting

    return render_template('sign_in.html')  # Render sign-in page when accessed by GET request

@app.route('/patient')
def patient():
    conn = get_db_connection()
    items = conn.execute('SELECT * FROM items').fetchall()  # Fetch all items from DB
    conn.close()
    return render_template('patient.html', items=items)

@app.route('/doctor-sign-in', methods=['GET', 'POST'])
def doctor_sign_in():
    # Mock sign-in (no actual login functionality)
    if request.method == 'POST':
        # Normally, you would check the credentials here, but we will just mock the process.
        return redirect(url_for('doctor'))  # Redirect to doctor page after submitting

    return render_template('doctor_sign_in.html')  # Render doctor sign-in page when accessed by GET request

@app.route('/add', methods=['POST'])
def add_item():
    item_name = request.form['item_name'] #User can input the condition name
    item_value = request.form['item_value']  # Get the value of the slider from the form
    date_time = request.form['date_time']  # Get the date and time from the form

    if item_name and item_value and date_time:  # Make sure all fields are filled
        conn = get_db_connection()
        conn.execute('INSERT INTO items (name, value, date_time) VALUES (?, ?, ?)', 
                     (item_name, item_value, date_time))
        conn.commit()
        conn.close()
    return redirect(url_for('patient'))  # Redirect to patient page after adding item

@app.route('/delete/<int:item_id>', methods=['GET'])
def delete_item(item_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM items WHERE id = ?', (item_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('patient'))  # Redirect to patient page after deleting item

@app.route('/doctor', methods=['GET'])
def doctor():
    severity_filter = request.args.get('severity')  # Get the severity filter from the URL
    conn = get_db_connection()

    if severity_filter:
        # Filter conditions based on the selected severity
        items = conn.execute('SELECT * FROM items WHERE value = ?', (severity_filter,)).fetchall()
    else:
        # Show all items if no severity filter is selected
        items = conn.execute('SELECT * FROM items').fetchall()

    conn.close()
    return render_template('doctor.html', items=items)


if __name__ == '__main__':
    init_db()  # Initialize the database
    app.run(debug=True, host="0.0.0.0", port=5000)
    #for opening to local public wifi, EG