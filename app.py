from flask import Flask, render_template, request, redirect, url_for,flash
from flask_mysqldb import MySQL

app = Flask(__name__)

# Mysql Connection
app.config['MYSQL_HOST'] = 'localhost' 
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_DB'] = 'database'
mysql = MySQL(app)

# settigs
app.secret_key = "mysecretkey"

@app.route("/")
def Index():
	cursor = mysql.connection.cursor()
	cursor.execute("SELECT * FROM contacts")
	date = cursor.fetchall()
	return render_template("index.html", contacts = date)

@app.route("/add_contacts", methods=["POST"])
def add_contacts():
	if request.method == "POST":
		fullname = request.form["fullname"]
		phone = request.form["phone"]
		email = request.form["email"]
		cursor = mysql.connection.cursor()
		cursor.execute("INSERT INTO contacts (fullname,phone,email) VALUES(%s,%s,%s)",(fullname,phone,email))
		cursor.connection.commit()
		cursor.connection.close()
		flash("Contact added successfully")
		return redirect(url_for("Index"))

@app.route("/edit/<string:id>")
def select_contact(id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM contacts WHERE id = {}".format(id))
    date = cursor.fetchall()
    return render_template("/edit_contacts.html", contacts = date[0])

@app.route("/update/<string:id>", methods = ["POST"])
def update_contacts(id):
    if request.method == "POST":
        fullname = request.form["fullname"]
        phone = request.form["phone"]
        email = request.form["email"]
        cursor = mysql.connection.cursor()
        cursor.execute("""UPDATE contacts SET fullname = %s,
                       phone = %s,
                       email = %s WHERE id = %s
                       """, (fullname, phone, email, id))
        cursor.connection.commit()
        flash("Contact updated successfully")
        return redirect(url_for("Index"))
  
@app.route("/delete/<string:id>")
def delete_contact(id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM contacts WHERE id = {}".format(id))
    cursor.connection.commit()
    cursor.connection.close()
    flash("contact remove successfully")
    return redirect(url_for("Index"))
    
if __name__ == "__main__":
	app.run(port=3000, debug=True)