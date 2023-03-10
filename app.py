from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file
from flask_mysqldb import MySQL
import hashlib, secrets, binascii
import MySQLdb.cursors
from flask_mail import Mail, Message
import os

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

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'customercare.in2022@gmail.com'
app.config['MAIL_PASSWORD'] = 'rktrsphkqdpltzge'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/offline')
def offline():
    return render_template('404.html')


@app.route('/')
def home():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM builder ORDER BY RAND()')
    account = cursor.fetchall()
    data_list = []
    for row in account:
        id = row['id']
        name = row['username']
        email = row['companyname']
        image_data = row['image']
        my_string = image_data.decode('utf-8')
        my_string_without_prefix = my_string.strip("'")
        # print(my_string_without_prefix)


        # print(image_data)
        # if len(image_data) % 2 != 0:
        #     image_data = "0" + image_data
        # image_base64 = binascii.unhexlify(image_data[2:]).decode('utf-8')
        

        data_list.append((id, name, email, my_string_without_prefix))
    return render_template('home.html', data_list = data_list)
    # print(result)
    # return response
    # return render_template("home.html", name = account)


@app.route('/builderinfo', methods=['GET', 'POST'])
def builderinfo():
    global userid, random

    msg = ''
    name = ''
    if 'register' in request.form:
        if request.method == 'POST' and 'name' in request.form and 'email' in request.form and 'password' in request.form and 'confirm-password' in request.form and 'companyname' in request.form and 'industry' in request.form and 'location' in request.form and 'phone' in request.form  and 'image' in request.files:
            username = request.form['name']
            email = request.form['email']
            password = request.form['password']
            conpassword = request.form['confirm-password']
            companyname = request.form['companyname']
            industry = request.form['industry']
            location = request.form['location']
            phone = request.form['phone']
            randoms = random.randint(0, 10)
            image = request.files['image']
            image.save(os.path.join(app.static_folder, 'images', image.filename))
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
                    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                    cursor.execute('INSERT INTO builder VALUES (NULL, % s, % s, % s, % s, % s, % s, % s, % s, % s, % s)', (username, email, hashed_password, hashed_conpassword, companyname, industry, location, phone, randoms, image.filename))
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

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST' and 'email' in request.form:
        email = request.form['email']

        cursor = mysql.connection.cursor()

        cursor.execute('SELECT * FROM builder WHERE email=%s', (email,))
        account = cursor.fetchone()

        if account:
            otp = random.randint(100000, 999999)
            cursor.execute('UPDATE builder SET reset_otp=%s WHERE email=%s', (otp, email))
            mysql.connection.commit()
            msg = Message('Reset Password OTP', sender = 'customercare.in2022@gmail.com', recipients = [email])
            msg.body = f'Your OTP for resetting password is {otp}'
            mail.send(msg)
            return redirect(url_for('reset_password', email=email))
        else:
            flash('Email does not exist')
            return redirect(url_for('forgot_password'))

    return render_template('forgot_password.html')

@app.route('/reset_password/<string:email>', methods=['GET', 'POST'])
def reset_password(email):
    cursor = mysql.connection.cursor()

    cursor.execute('SELECT * FROM builder WHERE email=%s', (email,))
    account = cursor.fetchone()

    if account:
        if request.method == 'POST':
            otp = request.form['otp']
            password = request.form['password']
            hashpass = hashlib.sha256(password.encode()).hexdigest()
            confirm_password = request.form['confirm_password']
            hashconpass = hashlib.sha256(confirm_password.encode()).hexdigest()

            if str(account[9]) == str(otp):
                if password == confirm_password:
                    cursor.execute('UPDATE builder SET hashed_password =%s, hashed_conpassword =%s, reset_otp=NULL WHERE email=%s', (hashpass, hashconpass, email))
                    mysql.connection.commit()
                    msg = 'Password Reset successfully'
                    return render_template('builderlogin.html',msg = msg)
                else:
                    flash('Passwords do not match')
                    return redirect(url_for('reset_password', email=email))
            else:
                flash('Invalid OTP')
                return redirect(url_for('reset_password', email=email))

        return render_template('reset_password.html', email=email)
    flash('Email does not exist')
    return redirect(url_for('forgot_password'))
    
@app.route('/builderdash', methods=["POST","GET"])    
def builderdash():
    if 'id' in session:
        uid = session['id']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM builder WHERE id = % s', (uid,))    
        cursor.connection.commit()
        acc = cursor.fetchone()
        image = acc[10]
        my_string = image.decode('utf-8')
        my_string_without_prefix = my_string.strip("'")
        return render_template('builderprofile.html',name = acc[1], comp=acc[5],location = acc[7], image = my_string_without_prefix)


@app.route('/userinfo', methods=['GET', 'POST'])
def userinfo():
    global random
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
            random1 = random.randint(0, 100)
            image = request.files['image']
            image.save(os.path.join(app.static_folder, 'images', image.filename))
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
                    cursor.execute('INSERT INTO users VALUES (NULL, % s, % s, % s, % s, % s, % s, % s, % s)', (username, email, hashed_password, hashed_conpassword, location, phone, random1, image.filename))
                    mysql.connection.commit()
                    msg = 'Dear %s You have successfully registered !'%(username)
                else:
                    msg = 'Passwords does not match. Re-enter password'
        elif request.method == 'POST':
            msg = 'Please fill out the form !'
        return render_template('userlogin.html', msg=msg)
    else:
        if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
            username = request.form['email']
            password = request.form['password']
            hashpass = hashlib.sha256(password.encode()).hexdigest()
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM users WHERE email = %s AND hashed_password = % s', (username, hashpass))
            account = cursor.fetchone()
            if account:
                session['id'] = account['id']
                userid =  account['id']
                session['username'] = account['username']
                return redirect(url_for('userdash'))
            else:
                msg = "Invalid Credentials"
        return render_template('userlogin.html',msg = msg)
    
@app.route('/forgotuser', methods=['GET', 'POST'])
def forgotuser():
    if request.method == 'POST' and 'email' in request.form:
        email = request.form['email']

        cursor = mysql.connection.cursor()

        cursor.execute('SELECT * FROM users WHERE email=%s', (email,))
        account = cursor.fetchone()

        if account:
            otp = random.randint(100000, 999999)
            cursor.execute('UPDATE users SET reset_otp=%s WHERE email=%s', (otp, email))
            mysql.connection.commit()
            msg = Message('Reset Password OTP', sender = 'customercare.in2022@gmail.com', recipients = [email])
            msg.body = f'Your OTP for resetting password is {otp}'
            mail.send(msg)
            return redirect(url_for('resetuser', email=email))
        else:
            flash('Email does not exist')
            return redirect(url_for('forgotuser'))

    return render_template('forgot.html')

@app.route('/resetuser/<string:email>', methods=['GET', 'POST'])
def resetuser(email):
    cursor = mysql.connection.cursor()

    cursor.execute('SELECT * FROM users WHERE email=%s', (email,))
    account = cursor.fetchone()

    if account:
        if request.method == 'POST':
            otp = request.form['otp']
            password = request.form['password']
            hashpass = hashlib.sha256(password.encode()).hexdigest()
            confirm_password = request.form['confirm_password']
            hashconpass = hashlib.sha256(confirm_password.encode()).hexdigest()

            if str(account[7]) == str(otp):
                if password == confirm_password:
                    cursor.execute('UPDATE users SET hashed_password =%s, hashed_conpassword =%s, reset_otp=NULL WHERE email=%s', (hashpass, hashconpass, email))
                    mysql.connection.commit()
                    msg = 'Password Reset successfully'
                    return render_template('userlogin.html',msg = msg)
                else:
                    flash('Passwords do not match')
                    return redirect(url_for('resetuser', email=email))
            else:
                flash('Invalid OTP')
                return redirect(url_for('resetuser', email=email))

        return render_template('reset.html', email=email)
    flash('Email does not exist')
    return redirect(url_for('forgotuser'))

@app.route('/userdash', methods=["POST","GET"])    
def userdash():
    if 'id' in session:
        uid = session['id']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE id = % s', (uid,))    
        cursor.connection.commit()
        acc = cursor.fetchone()
        image = acc[8]
        my_string = image.decode('utf-8')
        my_string_without_prefix = my_string.strip("'")
        return render_template('userprofile.html',name = acc[1], email=acc[2], location = acc[5], image = my_string_without_prefix)
        

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
