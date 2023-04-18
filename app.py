from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_mysqldb import MySQL
import hashlib, secrets
import MySQLdb.cursors
from flask_mail import Mail, Message
import os
from datetime import datetime
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
app.config['MAIL_USERNAME'] = 'Futurehaus2022@gmail.com'
app.config['MAIL_PASSWORD'] = 'dgcbdayybzcxdmvk'
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
                return redirect(url_for('builderdash', id = userid))
            else:
                msg = 'Incorrect username / password !'
                return render_template('builderlogin.html', msg = msg, indicator="failure")
        else:
            return render_template("builderlogin.html")

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST' and 'email' in request.form:
        email = request.form['email']

        cursor = mysql.connection.cursor()

        cursor.execute('SELECT * FROM builder WHERE email=%s', (email,))
        account = cursor.fetchone()
        name = account[1]

        if account:
            otp = random.randint(100000, 999999)
            cursor.execute('UPDATE builder SET reset_otp=%s WHERE email=%s', (otp, email))
            mysql.connection.commit()
            html = render_template('otpemail.html', name=name , otp=otp)
            msg = Message('Reset Password OTP for Future Haus', sender = 'futurehaus2022@gmail.com', recipients = [email])
            msg.html = html
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
    
@app.route('/builderdash/<int:id>', methods=["POST","GET"])    
def builderdash(id):
    if 'id' in session:
        uid = session['id']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM builder WHERE id = % s', (uid,))    
        cursor.connection.commit()
        acc = cursor.fetchone()
        image = acc[10]
        my_string = image.decode('utf-8')
        my_string_without_prefix = my_string.strip("'")
        cursor1 = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor2 = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        countuser = cursor2.execute('SELECT * FROM users')
        countproj = cursor1.execute('SELECT * FROM images WHERE uid = % s',(id,))
        cursor1.execute('SELECT * FROM images WHERE uid = % s ORDER BY RAND() LIMIT 6',(id,))
        project = cursor1.fetchall()
        cursor2.execute('SELECT * FROM users ORDER BY RAND() LIMIT 4')
        user = cursor2.fetchall()
        data_list = []
        for row in user:
            id = row['id']
            name = row['username']
            location = row['location']
            image_data = row['image']
            my_string1 = image_data.decode('utf-8')
            my_string_without_prefix1 = my_string1.strip("'")
            data_list.append((id, name, location, my_string_without_prefix1))
        return render_template('navprof.html', user = data_list, project = project, countp = countproj, countu = countuser, name = acc[1], comp=acc[5],location = acc[7], image = my_string_without_prefix, id = uid)

@app.route('/builderprofile/<int:id>', methods=['GET','POST'])
def builderprofile(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM builder WHERE id = %s", (id, ))
    row = cursor.fetchone()
    name1 = row['username']
    comp = row['companyname']
    image = row['image']
    my_string = image.decode('utf-8')
    my_string_without_prefix = my_string.strip("'")
    return render_template('builderprofile.html', user = name1, name = name1, comp = comp, image = my_string_without_prefix, id = id)

@app.route('/showuser/<int:id>', methods=['GET','POST'])
def showuser(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM builder WHERE id = %s", (id, ))
    row = cursor.fetchone()
    name1 = row['username']
    comp = row['companyname']
    image = row['image']
    my_string = image.decode('utf-8')
    my_string_without_prefix = my_string.strip("'")
    cursor.execute('SELECT * FROM users')
    user = cursor.fetchall()
    return render_template('seeall.html', user = user, name = name1, comp = comp, image = my_string_without_prefix, id = id)

@app.route('/showproject/<int:id>', methods=['GET','POST'])
def showproject(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM images WHERE uid = % s',(id,))
    project = cursor.fetchall()
    return render_template('seeproject.html', project = project, id = id)

@app.route('/buildergallery/<int:id>', methods=["GET","POST"])
def buildergallery(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM builder WHERE id = %s", (id, ))
    row = cursor.fetchone()
    name1 = row['username']
    comp = row['companyname']
    image = row['image']
    my_string = image.decode('utf-8')
    my_string_without_prefix = my_string.strip("'")
    msg = ''
    if request.method=='POST' and 'location' in request.form and 'sqft' in request.form and 'build_type' in request.form and 'budget' in request.form and 'room' in request.form and 'image' in request.files and 'status' in request.form:
        if 'id' in session:
            uid = session['id']
            location = request.form['location']
            sqft = request.form['sqft']
            build_type = request.form['build_type']
            budget = request.form['budget']
            room = request.form['room']
            image2 = request.files['image']
            status = request.form['status']
            image2.save(os.path.join(app.static_folder, 'image', image2.filename))
            if not image2:
                msg = 'Image not Inserted'
                return render_template('buildergallery.html', a = msg, id = id)    
            else:
                cursor = mysql.connection.cursor()
                cursor.execute('INSERT INTO images VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, % s)', (uid, location, sqft, build_type, budget, room, image2.filename, status))
                mysql.connection.commit()
                msg = 'Image Added Successfully!'
                return redirect(url_for('buildergallery',  id = id))
    return render_template('buildergallery.html', name = name1, comp = comp, image = my_string_without_prefix, id = id, msg = msg)

@app.route('/viewgallery/<int:id>', methods = ['GET', 'POST'])
def viewgallery(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM builder WHERE id = %s", (id, ))
    row = cursor.fetchone()
    name1 = row['username']
    comp = row['companyname']
    image = row['image']
    my_string = image.decode('utf-8')
    my_string_without_prefix = my_string.strip("'")
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM images WHERE uid = %s', (id, ))
    mysql.connection.commit()
    account = cursor.fetchall()
    data_list = []
    for row in account:
        location = row['location']
        sqft = row['sqft']
        build_type = row['build_type']
        budget = row['budget']
        room = row['room']
        image_data = row['image']
        my_string1 = image_data.decode('utf-8')
        my_string_without_prefix1 = my_string1.strip("'")
        data_list.append((location, sqft, build_type, budget, room, my_string_without_prefix1))
    if account:
        return render_template('viewgallery.html', data = data_list, name = name1, comp = comp, image = my_string_without_prefix, id = id)
    else:
        msg = 'No Image is uploaded'
        return render_template('viewgallery.html', name = name1, comp = comp, image = my_string_without_prefix, id = id, msg = msg)


@app.route('/material/<int:id>', methods=['GET','POST'])
def material(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM builder WHERE id = %s", (id, ))
    row = cursor.fetchone()
    name1 = row['username']
    comp = row['companyname']
    image = row['image']
    my_string = image.decode('utf-8')
    my_string_without_prefix = my_string.strip("'")
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM material WHERE uid = % s', (id, ))
    acc = cursor.fetchone()
    return render_template('showmater.html', acc = acc, name = name1, comp = comp, image = my_string_without_prefix, id = id)

@app.route('/editmaterial/<int:id>', methods=['POST','GET'])
def editmaterial(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM builder WHERE id = %s", (id, ))
    row = cursor.fetchone()
    name1 = row['username']
    comp = row['companyname']
    image = row['image']
    my_string = image.decode('utf-8')
    my_string_without_prefix = my_string.strip("'")
    msg = ''
    if request.method == 'POST' and 'cement' in request.form and 'steel' in request.form and 'wood' in request.form and 'bricks' in request.form and 'tiles' in request.form and 'paint' in request.form and 'glass' in request.form:
        if 'id' in session:
            uid=session['id']
            cement = request.form['cement']
            steel = request.form['steel']
            wood = request.form['wood']
            bricks = request.form['bricks']
            tiles = request.form['tiles']
            paint = request.form['paint']
            glass = request.form['glass']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM material WHERE uid = % s', (id, ))
            account = cursor.fetchone()
            if not account:
                cursor = mysql.connection.cursor()
                cursor.execute('INSERT INTO material VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', (uid, cement, steel, wood, bricks, tiles, paint, glass))
                mysql.connection.commit()
                msg = 'Added Successfully!'
                return redirect(url_for('material',  id = id, a = msg))
            else:
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('UPDATE material SET uid = % s, cement = % s, steel = % s, wood = % s, bricks = % s, tiles = % s, paint = % s, glass = % s WHERE uid = % s', (uid, cement, steel, wood, bricks, tiles, paint, glass, id))
                mysql.connection.commit()
                msg = 'Updated Successfully!'
                return redirect(url_for('material', id = id, a = msg))
        else:
            msg = 'Please fill the form!'
            return render_template('buildermater.html', name = name1, comp = comp, image = my_string_without_prefix, id = id, a = msg)  
    return render_template('buildermater.html', name = name1, comp = comp, image = my_string_without_prefix, id = id, a = msg)

# @app.route('/buildermessage/<int:id>', methods=['GET','POST'])
# def buildermessage(id):
#     cursor = mysql.connection.cursor()
#     cursor.execute('SELECT * FROM users')
#     acc = cursor.fetchall()
#     data_list = []
#     for row in acc:
#         id = row[0]
#         name = row[1]
#         image_data = row[8]
#         my_string1 = image_data.decode('utf-8')
#         my_string_without_prefix1 = my_string1.strip("'")
#         data_list.append((id, name, my_string_without_prefix1))
#     print(data_list)
#     return render_template('chat.html', acc = data_list, id = id)


@app.route('/messages/<int:id>', methods = ['GET','POST'])
def messages(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM users')
    user = cur.fetchone()
    users = user[0]
    cur.execute("SELECT * FROM messages WHERE sender_id = %s AND receiver_id = %s",(id, users, ))
    messages = cur.fetchall()
    if not id and not users:
        msg = 'No Message'
        return render_template('chatbuilder.html', id = id)
    else:
        msg = []
        for row in messages:
            sender_id = row[1]
            receiver_id = row[2]
            message = row[3]
            timestamp = row[4]
            msg.append((sender_id, receiver_id, message, timestamp))
        return render_template("chatbuilder.html", messages=msg, id = id)

@app.route("/send-message/<int:id>", methods=["GET", "POST"])
def send_message(id):
    if 'id' in session:
        uid = session['id']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM users')
        user = cursor.fetchall()
        cursor.execute('SELECT * FROM builder WHERE id = %s', (id, ))
        builder = cursor.fetchone()
        builderid = builder[0]
        if request.method == "POST" and 'message' in request.form:
            sender_id = builderid
            receiver_id = uid
            message = request.form["message"]
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor = mysql.connection.cursor()
            cursor.execute('INSERT INTO messages (sender_id, receiver_id, message, timestamp) VALUES (%s, %s, %s, %s)', (sender_id, receiver_id, message, timestamp))
            mysql.connection.commit()
            return redirect(url_for("messages", id=id))
    return render_template("chatb.html", id = id, acc = user)

@app.route('/userinfo', methods=['GET', 'POST'])
def userinfo():
    global random
    msg = ''
    name = ''
    if 'register' in request.form:
        if request.method == 'POST' and 'name' in request.form and 'email' in request.form and 'password' in request.form and 'confirm-password' in request.form and 'location' in request.form and 'phone' in request.form and 'image' in request.files:
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
        name = account[1]
        if account:
            otp = random.randint(100000, 999999)
            cursor.execute('UPDATE users SET reset_otp=%s WHERE email=%s', (otp, email))
            mysql.connection.commit()
            html = render_template('otpemail.html', name=name , otp=otp)
            msg = Message('Reset Password OTP for Future Haus', sender = 'futurehaus2022@gmail.com', recipients = [email])
            msg.html = html
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
        id = acc[0]
        image = acc[8]
        my_string = image.decode('utf-8')
        my_string_without_prefix = my_string.strip("'")
        return render_template('navuser.html',name = acc[1], email=acc[2], location = acc[5], image = my_string_without_prefix, id = id)
    
@app.route('/userprofile/<int:id>', methods = ['GET','POST'])
def userprofile(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM users WHERE id = %s", (id, ))
    row = cursor.fetchone()
    name1 = row['username']
    email1 = row['email']
    location = row['location']
    image = row['image']
    my_string = image.decode('utf-8')
    my_string_without_prefix = my_string.strip("'")
    return render_template('userprofile.html', id = id,location = location,  name = name1, email = email1, image = my_string_without_prefix)
        
    
@app.route('/userbit/<int:id>', methods=["GET","POST"])
def userbit(id):  
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM users WHERE id = %s", (id, ))
    row = cursor.fetchone()
    name1 = row['username']
    email1 = row['email']
    image = row['image']
    my_string = image.decode('utf-8')
    my_string_without_prefix = my_string.strip("'")

    if request.method == 'POST' and 'name' in request.form and 'email' in request.form and 'location' in request.form and 'address' in request.form and 'phone' in request.form and 'approval_status' in request.form and 'timeline' in request.form and 'sqft' in request.form and 'build_type' in request.form and 'budget' in request.form and 'wood' in request.form and 'room' in request.form and 'additional' in request.form:
        if 'id' in session:
            msg = ''
            uid=session['id']
            name = request.form['name']
            email = request.form['email']
            location = request.form['location']
            address = request.form['address']
            phone = request.form['phone']
            approval_status = request.form['approval_status']
            timeline = request.form['timeline']
            sqft = request.form['sqft']
            build_type = request.form['build_type']
            budget = request.form['budget']
            wood = request.form['wood']
            room = request.form['room']
            additional = request.form['additional']
            cursor = mysql.connection.cursor()
            cursor.execute('INSERT INTO bit VALUES (NULL, % s, % s, % s, % s, % s, % s, % s, % s, % s, % s, % s, % s, % s, % s)', (uid, name, email, location, address, phone, approval_status, timeline, sqft, build_type, budget, wood, room, additional))
            mysql.connection.commit()
            html = render_template('quationmail.html', name = name, email = email, location = location, phone = phone, approval_status = approval_status, timeline = timeline, sqft = sqft, budget = budget, wood = wood, room = room, additional = additional)
            msg = 'You have successfully registered your Quotation'
            TEXT = Message('Hello, Mail form Future Haus', sender = 'futurehaus2022@gmail.com', recipients = [email])
            TEXT.html = html
            mail.send(TEXT)
            cursor.execute('SELECT email FROM builder')
            emails = cursor.fetchall()
            for emails in emails:
                html1 = render_template('quotationengin.html', name = name, email = email, location = location, phone = phone, approval_status = approval_status, timeline = timeline, sqft = sqft, budget = budget, wood = wood, room = room, additional = additional)
                TEXT1 = Message('Hello, Mail from Future Haus', sender = 'futurehaus2022@gmail.com', recipients = [emails[0]])
                TEXT1.html = html1
                mail.send(TEXT1)
            return render_template('userbit.html', msg = msg, name = name1, email = email1, image = my_string_without_prefix, id = id)
    return render_template('userbit.html', name = name1, email = email1, image = my_string_without_prefix, id = id)

@app.route('/viewquotation/<int:id>', methods=["GET","POST"])
def viewquotation(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM users WHERE id = %s", (id, ))
    row = cursor.fetchone()
    name1 = row['username']
    email1 = row['email']
    image = row['image']
    my_string = image.decode('utf-8')
    my_string_without_prefix = my_string.strip("'")
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM bit WHERE uid = %s", (id, ))
    cursor.connection.commit()
    acc = cursor.fetchall()
    if not acc:
        msg = 'No Data is Found'
        return render_template('userview.html', acc = acc, name = name1, email = email1, image = my_string_without_prefix, id = id, msg = msg)
    else:
        return render_template('userview.html',acc = acc, name = name1, email = email1, image = my_string_without_prefix, id = id)

@app.route('/usermessage/<int:id>', methods=['GET','POST'])
def usermessage(id):
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM builder')
    acc = cursor.fetchall()
    data_list = []
    for row in acc:
        id = row[0]
        name = row[1]
        image_data = row[10]
        my_string1 = image_data.decode('utf-8')
        my_string_without_prefix1 = my_string1.strip("'")
        data_list.append((id, name, my_string_without_prefix1))
    print(data_list)
    return render_template('chatb.html', acc = data_list, id = id)

@app.route("/userchat/<string:name>", methods = ['GET', 'POST'])
def userchat(name):
    if 'id' in session:
        uid = session['id']
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE id = %s', (uid, ))
        users = cursor.fetchone()
        usern = users[1]
        userid = ''
        if request.method =='POST' and 'message' in request.form:
            now = datetime.now()
            timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
            builderna = name
            userid = usern
            message = request.form['message']
            print(message)
            cursor1 = mysql.connection.cursor1(MySQLdb.cursors.DictCursor)
            cursor1.execute('INSERT INTO message VALUES (%s, %s, %s, %s)', (timestamp, builderna, userid, message))
            mysql.connection.commit()
            return render_template('chatuser.html', user = name)
        else:
            cursor1 = mysql.connection.cursor()
            cursor1.execute('SELECT * FROM users WHERE id = % s' ,(uid, ))
            users = cursor1.fetchone()
            builderid = name
            userid = users[1]
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM message')
            messages = cursor.fetchall()
            data_list = []
            for row in messages:
                timestamp = row['timestamp']
                sender = row['sendid']
                receive = row['receiveid']
                message = row['message']
                data_list.append((timestamp, sender, receive, message))
            return render_template('chatuser.html', user = name, messages = data_list)
    return render_template('chatuser.html', user = name,)
    
@app.route('/assigned/<int:id>', methods=["GET","POST"])
def assigned(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM users WHERE id = %s", (id, ))
    row = cursor.fetchone()
    name1 = row['username']
    email1 = row['email']
    image = row['image']
    my_string = image.decode('utf-8')
    my_string_without_prefix = my_string.strip("'")
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id FROM bit")
    ids = cursor.fetchone()
    cursor.execute("UPDATE bit SET status = % s WHERE id = % s",('Assigned', ids))
    cursor.connection.commit()
    return redirect(url_for('viewquotation', id=id, name = name1, email = email1, image = my_string_without_prefix))


@app.route('/usergallery/<int:id>', methods=["GET","POST"])
def usergallery(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM users WHERE id = %s", (id, ))
    row = cursor.fetchone()
    name1 = row['username']
    email1 = row['email']
    image = row['image']
    my_string = image.decode('utf-8')
    my_string_without_prefix = my_string.strip("'")
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM images')
    mysql.connection.commit()
    acc = cursor.fetchall()
    data_list = []
    for row in acc:
        location = row[2]
        sqft = row[3]
        build_type = row[4]
        budget = row[5]
        room = row[6]
        image_data = row[7]
        my_string1 = image_data.decode('utf-8')
        my_string_without_prefix1 = my_string1.strip("'")
        data_list.append((location, sqft, build_type, budget, room, my_string_without_prefix1))
    return render_template('usergallery.html', data = data_list, name = name1, email = email1, image = my_string_without_prefix, id = id)

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
