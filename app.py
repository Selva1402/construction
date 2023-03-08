from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import hashlib, secrets
import MySQLdb.cursors
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random

import re

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)


app.secret_key = 'a'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'selva2002'
app.config['MYSQL_DB'] = 'haus'
mysql = MySQL(app)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/offline')
def offline():
    return render_template('404.html')


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/builderinfo', methods=['GET', 'POST'])
def builderinfo():
    global userid
    msg = ''
    name = ''
    if 'register' in request.form:
        if request.method == 'POST' and 'name' in request.form and 'email' in request.form and 'password' in request.form and 'confirm-password' in request.form and 'companyname' in request.form and 'industry' in request.form and 'location' in request.form and 'phone' in request.form:
            username = request.form['name']
            email = request.form['email']
            password = request.form['password']
            conpassword = request.form['confirm-password']
            companyname = request.form['companyname']
            industry = request.form['industry']
            location = request.form['location']
            phone = request.form['phone']
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            hashed_conpassword = hashlib.sha256(conpassword.encode()).hexdigest()
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM builder WHERE username = % s', (username, ))
            account = cursor.fetchone()
            if account:
                msg = 'Account already exists !'
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                msg = 'Invalid email address !'
            elif not re.match(r'[A-Za-z0-9]+', username):
                msg = 'Username must contain only characters and numbers !'
            elif not username or not password or not email:
                msg = 'Please fill out the form !'
            else:
                if (password == conpassword):
                    cursor.execute('INSERT INTO builder VALUES (NULL, % s, % s, % s, % s, % s, % s, % s, %s)', (username, email, hashed_password, hashed_conpassword, companyname, industry, location, phone))
                    mysql.connection.commit()
                    msg = 'Dear %s You have successfully registered !'%(username)
                else:
                    msg = 'Passwords does not match.Re-enter password'
        elif request.method == 'POST':
            msg = 'Please fill out the form !'
        return render_template('builderlogin.html', msg=msg)
    else:
        if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
            username = request.form['email']
            password = request.form['password']
            hashpass = hashlib.sha256(password.encode()).hexdigest()
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM builder WHERE email = %s AND hashed_password = % s', (username, hashpass))
            account = cursor.fetchone()
            if account:
                session['id'] = account['id']
                userid =  account['id']
                session['username'] = account['username']
                return redirect(url_for('builderdash'))
            else:
                msg = 'Incorrect username / password !'
                return render_template('builderlogin.html', msg = msg,indicator="failure")
        else:
            return render_template("builderlogin.html")

@app.route("/forgot", methods = ['GET', 'POST'])
def forgot_password():
    if request.method == 'POST' and 'email' in request.form:
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM builder WHERE email = %s", (email,))
        user = cursor.fetchone()
        if user:
            otp = generate_otp()
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("UPDATE builder SET reset_otp = %s WHERE id = %s", (otp, user['id']))
            mysql.connection.commit()
            send_reset_email(email, otp)
            return render_template('reset.html', message='An OTP has been sent to your email with instructions to reset your password.')
        else:
            return render_template('forgot.html', message='No user with that email address was found.')
    return render_template('forgot.html')

def generate_otp():
    return random.randint(100000, 999999)

def send_reset_email(email, otp):
    msg = MIMEMultipart()
    msg['From'] = 'customercare.in2022@gmail.com'
    msg['To'] = email
    msg['Subject'] = 'Reset Password OTP'
    body = f"Your OTP to reset your password is: {otp}"
    msg.attach(MIMEText(body, 'plain'))
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('customercare.in2022@gmail.com', 'rktrsphkqdpltzge')
    text = msg.as_string()
    server.sendmail(msg['From'], msg['To'], text)
    server.quit()

@app.route("/reset_password", methods = ['GET', 'POST'])
def reset_password():
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM builder WHERE id = %s", (id,))
        mysql.connection.commit()
        user = cursor.fetchone()
        # otp = user[9]
        # user1 = user['reset_otp']
        # print(user1)
        # return render_template("reset.html")
        # if not user:
        #     return render_template('reset.html',message = "Invalid or expired reset link.")
        if request.method == 'POST':
            otp = request.form['otp']
            password = request.form['password']
            conpassword = request.form['conpassword']
            hashpass = hashlib.sha256(password.encode()).hexdigest()
            hashconpassword = hashlib.sha256(conpassword.encode()).hexdigest()
            if otp != str(otp):
                return render_template('reset.html', message='Incorrect OTP. Please try again.')
            cursor = mysql.connection.cursor()
            cursor.execute("UPDATE builder SET hashed_password = %s, hashed_conpassword = %s WHERE id = %s", (hashpass, hashconpassword, id))
            mysql.connection.commit()
        return render_template('builderlogin.html', msg='Your password has been reset.')
    # return render_template('builderlogin.html')

    
@app.route('/builderdash', methods=["POST","GET"])    
def builderdash():
    if 'id' in session:
        uid = session['id']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM builder WHERE id = % s', (uid,))    
        cursor.connection.commit()
        acc = cursor.fetchone()
        return render_template('builderdash.html',name = acc[1], comp=acc[5])


@app.route('/userinfo', methods=['GET', 'POST'])
def userinfo():
    msg = ''
    name = ''
    if 'register' in request.form:
        if request.method == 'POST' and 'name' in request.form and 'email' in request.form and 'password' in request.form and 'confirm-password' in request.form and 'location' in request.form and 'phone' in request.form:
            username = request.form['name']
            email = request.form['email']
            password = request.form['password']
            conpassword = request.form['confirm-password']
            location = request.form['location']
            phone = request.form['phone']
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            hashed_conpassword = hashlib.sha256(conpassword.encode()).hexdigest()
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM users WHERE username = % s', (username, ))
            account = cursor.fetchone()
            if account:
                msg = 'Account already exists !'
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                msg = 'Invalid email address !'
            elif not re.match(r'[A-Za-z0-9]+', username):
                msg = 'Username must contain only characters and numbers !'
            elif not username or not password or not email:
                msg = 'Please fill out the form !'
            else:
                if (password == conpassword):
                    cursor.execute('INSERT INTO users VALUES (NULL, % s, % s, % s, % s, % s, %s)', (username, email, hashed_password, hashed_conpassword, location, phone))
                    mysql.connection.commit()
                    msg = 'Dear %s You have successfully registered !'%(username)
                else:
                    msg = 'Passwords does not match.Re-enter password'
        elif request.method == 'POST':
            msg = 'Please fill out the form !'
        return render_template('builderlogin.html', msg=msg)
    else:
        if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
            username = request.form['email']
            password = request.form['password']
            hashpass = hashlib.sha256(password.encode()).hexdigest()
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM users WHERE email = %s AND hashed_password = % s', (username, hashpass))
            account = cursor.fetchone()
            if account:
                session['loggedin'] = True
                session['username'] = username
                msg = "Login successful"
                return render_template('dashboard.html',name = username)
            else:
                msg = "Invalid Credentials"
        return render_template('userlogin.html',msg = msg)
        

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('builderinfo'))

@app.route('/loggout')
def loggout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('userinfo'))

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8080)
