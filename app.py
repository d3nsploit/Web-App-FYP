from flask import Flask, render_template, request, url_for, redirect, session, flash, jsonify
from flask_mysqldb import MySQL, MySQLdb
import api_check
from datetime import datetime, date, timedelta
import bcrypt
import numpy as np
import pickle
import string
import random
import feature_extraction
import base64
import smtplib
from itsdangerous import URLSafeTimedSerializer
from email.message import EmailMessage


model = pickle.load(open('url_predict.pkl', 'rb'))

app = Flask(__name__)

app.secret_key = "!@#QWERRRRRRRTY1234"

# Unsort json
app.config['JSON_SORT_KEYS'] = False

s = URLSafeTimedSerializer('Thisissecret!')

# Database connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'scanme_db'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)


ses_created = 0
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def id_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def date_range(start_date):
    number_of_days = 7
    date_list = [(start_date - timedelta(days=day)).isoformat()
            for day in range(number_of_days)]
    return date_list

range_date = date_range(date.today())
range_date.reverse()

# ROute to homepage
@app.route('/')
def index():
    return render_template('index.html')


# Route to result page
@app.route('/result', methods=['POST'])
def result():
    try:
        global count_benign, count_malicious, count, recent_url, recently_scan_dash
        temp = {}

        get_url = request.form['url']

        if get_url.find("://127.0.0.1") != -1 or get_url.find("://localhost") != -1:
            return redirect(url_for('meme'))
        get_result = feature_extraction.load_url(get_url)
        arr = np.array([[get_result[0], get_result[1], get_result[2],
            get_result[3], get_result[4], get_result[5], get_result[6], get_result[7],
            get_result[8], get_result[9], get_result[10], get_result[11], get_result[12]]])

        prediction = model.predict(arr)

        get_url_details = api_check.url_scraper(get_url)
        get_url_domain = get_url_details[0]
        get_url_status = get_url_details[1]
        get_url_content = get_url_details[2]
        get_url_ip = get_url_details[3]
        get_url_redirect = get_result[9]
        get_url_created = get_url_details[4]
        get_url_country = get_url_details[5]
        now = datetime.now()
        get_time = now.strftime("%Y-%m-%d %H:%M:%S")
        get_date = now.strftime("%Y-%m-%d")
        get_screenshot = api_check.screenshot(get_url)
        get_base64_image = api_check.get_as_base64(get_screenshot)
        get_route = feature_extraction.route_redirect(get_url)
        print(get_route)
        # recently_scan
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO recent_scan (urls,status,date) VALUES (%s,%s,%s)",(get_url,prediction[0],get_time,))
        mysql.connection.commit()

        if session.get('email') != None:
            cur.execute("SELECT id from users where email = %s",(session['email'],))
            user = cur.fetchone()
            cur.execute("INSERT INTO url (uid,date,urls,status) VALUES (%s,%s,%s,%s)",
                    (user['id'], get_date, get_url, prediction[0],))
            mysql.connection.commit()
            cur.close()

        return render_template('result.html', data0=get_url, data1=get_time, data2=get_base64_image,
                data3=prediction, data4=get_url_domain, data5=get_url_status, data6=get_url_content,
                data7=get_url_ip, data8=get_url_redirect, data9=get_url_created, data10=get_url_country, data11=get_route)
    except:
        flash("Please enter valid URL including http:// or https://")
        return redirect(url_for('index'))


@app.route('/report/result', methods=["POST"])
def represult():
    report_url = request.form['url-rep']
    report_detail = request.form['detail-rep']
    report_status = "processing"

    cur = mysql.connection.cursor()
    cur.execute("SELECT id from users where email = %s",
            (session['email'],))
    user = cur.fetchone()

    cur.execute("INSERT INTO report (uid,date,url,details,status) VALUES (%s,%s,%s,%s,%s)",
            (user['id'], date.today(), report_url, report_detail,report_status,))

    mysql.connection.commit()

    return redirect(url_for('index'))


@app.route('/userapi', methods=["POST"])
def apiuser():
    try:
        data = request.get_json()

        get_url = data['urls']
        get_apikey = data['apikey']

        cur = mysql.connection.cursor()
        api_exist = cur.execute(
                "SELECT apikey FROM users WHERE apikey=%s", (get_apikey,))
        # print(api_exist)

        if api_exist == 0:
            return jsonify({"Error": "Invalid API Key"})

        if get_url.find("://127.0.0.1") != -1 or get_url.find("://localhost") != -1:
            return jsonify({"Error": "Invalid URL"})

        get_result = feature_extraction.load_url(get_url)
        arr = np.array([[get_result[0], get_result[1], get_result[2],
            get_result[3], get_result[4], get_result[5], get_result[6], get_result[7],
            get_result[8], get_result[9], get_result[10], get_result[11], get_result[12]]])

        prediction = model.predict(arr)

        get_url_details = api_check.url_scraper(get_url)
        get_url_domain = get_url_details[0]
        get_url_status = get_url_details[1]
        get_url_content = str(get_url_details[2])+" bytes"
        get_url_ip = get_url_details[3]
        get_url_redirect = get_result[8]
        get_url_created = get_url_details[4]
        get_url_country = get_url_details[5]
        now = datetime.now()
        get_time = now.strftime("%Y-%m-%d %H:%M:%S")

        cur.execute("SELECT max(date) from api where apikey = %s",
                (get_apikey,))
        date_now = cur.fetchone()['max(date)']

        if date.today() == date_now:
            cur.execute("SELECT count from api where apikey = %s and date = %s",
                    (get_apikey, date.today(),))
            count_api = cur.fetchone()['count']
            count_api += 1
            cur.execute("UPDATE api SET count=%s where apikey = %s and date = %s",
                    (count_api, get_apikey, date.today(),))

        else:
            count_api = 1
            cur.execute("INSERT INTO api (date,apikey,count) VALUES (%s,%s,%s)",
                    (date.today(), get_apikey, count_api,))

            mysql.connection.commit()

        return jsonify({
            "Data": [{
                "Scanned on": get_time,
                "Scanned URL": get_url,
                "Status-Code": get_url_status,
                }],
            "URL Information": [{
                "Main-Domain": get_url_domain,
                "Content-Length": get_url_content,
                "IP-Address": get_url_ip,
                "Date Created": get_url_created,
                "Country": get_url_country,
                "Number of redirections": get_url_redirect
                }],
            "Scanner Result": [{
                "Status Prediction": prediction[0]
                }]
            })

    except:
        return jsonify({"Error": "Invalid URL"})


# Route to sign in page
@app.route('/sign_in', methods=["GET", "POST"])
def signin():
    if request.method == "POST":
        emailusername = request.form['emailusername']
        password = request.form['password'].encode('utf-8')

        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM users WHERE email=%s OR username=%s",
                (emailusername, emailusername,))
        user = cur.fetchone()

        if user != None:
            temp = bcrypt.hashpw(password, user['password'].encode('utf-8'))
            if temp == user['password'].encode('utf-8'):
                session['email'] = user['email']
                session['fname'] = user['fname']
                session['role'] = user['role']
                cur.execute("SELECT num from session")
                ses_created = int(cur.fetchone()['num'])
                ses_created += 1 
                cur.execute("UPDATE session set num=%s",(ses_created,))
                mysql.connection.commit()
                return redirect(url_for('dashboard'))
            else:
                flash("Email or password is incorrect")
                return render_template('signin.html')
        else:
            flash("Email or password is incorrect")
            return render_template('signin.html')
    else:
        return render_template('signin.html')


# Route to sign up page
@app.route('/sign_up', methods=["GET", "POST"])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    else:
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password'].encode('utf-8')
        password1 = request.form['repassword'].encode('utf-8')

        hash_password = bcrypt.hashpw(password, bcrypt.gensalt())


        cur = mysql.connection.cursor()
        # print(cur.execute("SELECT * FROM users WHERE email=%s" , (email,))) return 1 if exist in db
        if cur.execute("SELECT * FROM users WHERE email=%s", (email,)) or cur.execute("SELECT * FROM users WHERE username=%s", (username,)):
            flash("The account is already exist!")
            cur.close()
        else:
            if password != password1:
                flash ("Passwords are not match")
            else:
                role = "user"
                gen_key = 1
                random_key = id_generator()

                while(gen_key):
                    exist_key = cur.execute(
                            "SELECT apikey FROM users WHERE apikey=%s", (random_key,))
                    if exist_key == 1:
                        random_key = id_generator()
                    else:
                        gen_key = 0

                lastseen = datetime.now()
                get_time = lastseen.strftime("%Y-%m-%d %H:%M:%S")
                cur.execute("INSERT INTO users (fname,lname,email,role,username,password,apikey,lastseen) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
                        (fname, lname, email, role, username, hash_password, random_key, get_time,))
                mysql.connection.commit()

                cur.execute("SELECT num from session")
                ses_created = int(cur.fetchone()['num'])
                ses_created += 1
                cur.execute("UPDATE session set num=%s",(ses_created,))
                
                mysql.connection.commit()
                cur.close()
                session['email'] = email
                session['fname'] = fname
                session['role'] = role
                flash("The account created successfully.")
        return render_template('signup.html')


# Forgot Pass
@app.route('/forgot', methods=['GET','POST'])
def forgot():
    if request.method == 'POST':
        email = request.form['email']
        cur = mysql.connection.cursor()
        res_email = cur.execute("SELECT email from users where email = %s",(email,))
        if res_email > 0:
            token = s.dumps(email, salt='email-confirm')

            gmail_user = 'scanme.urlscan@gmail.com'
            gmail_password = 'Scanme123@'

            msg = EmailMessage()
            msg.set_content('\nScanMe Password Reset\n\n\nWe heard that you lost your ScanMe password. Sorry about that!\n\nThis is the link to reset your password. https://www.scan4me.xyz/confirm'+token+'. \n\nThis link will be expired within 1 hour\n\n\nIf you are not request this link please ignore this email.\n\n\nThank You.')

            msg['Subject'] = 'Reset Password For ScanMe Account'
            msg['From'] = "d3nsploit@gmail.com"
            msg['To'] = email

            try:
                server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                server.ehlo()
                server.login(gmail_user, gmail_password)
                server.send_message(msg)
                server.close()
            except:
                print ('Something went wrong...')

        flash("You will receive an reset password link if your email is exists")
    return render_template('forgot.html')

@app.route('/confirm/<token>', methods=['GET','POST'])
def confirm_email(token):
    try:
        email = s.loads(token, salt='email-confirm',max_age=3600)
        print(email)
        if request.method == "POST":
            passwd = request.form['password'].encode('utf-8')
            passwd1 = request.form['password1'].encode('utf-8')
            if passwd == passwd1:
                cur = mysql.connection.cursor()
                hash_password = bcrypt.hashpw(passwd1, bcrypt.gensalt())
                cur.execute("UPDATE users SET password = %s WHERE email = %s",(hash_password,email,))
                mysql.connection.commit()
                flash("Your password change successfully")
                return render_template('reset.html')

            else:
                flash("Your password not match")
                return render_template('reset.html')

        return render_template('reset.html')

    except:
        return '<h1>Token is expired</h1>'




# Route to dashboard page
@app.route('/dashboard')
def dashboard():

    if 'email' in session:
        cur = mysql.connection.cursor()
        if session['role'] == "admin":
            cur.execute("SELECT urls,status,date from recent_scan order by id DESC limit 6")
            recently_scan_url = cur.fetchall()

            cur.execute("SELECT count(id) from recent_scan")
            count_total = cur.fetchone()['count(id)']

            cur.execute("SELECT count(id) from recent_scan where status = 'benign'")
            count_benign = cur.fetchone()['count(id)']

            cur.execute("SELECT count(id) from recent_scan where status = 'malicious'")
            count_malicious = cur.fetchone()['count(id)']


            data = {
                    "data0": count_total,
                    "data1": count_benign,
                    "data2": count_malicious,
                    "data3": recently_scan_url,
                    "data4": '',
                    "data5": '',
                    "data6": ''
                    }
            return render_template('dashboard.html', data=data)
        else:
            # print(session['email'])

            ben_rec = []
            mal_rec = []

            cur.execute("SELECT id from users where email = %s",
                    (session['email'],))
            id_user = cur.fetchone()['id']

            for i in range_date:
                cur.execute(
                        "SELECT COUNT(id) as num_scan from url where date = %s and uid=%s and status='benign'", (i,id_user,))
                x = cur.fetchone()

                cur.execute(
                        "SELECT COUNT(id) as num_scan from url where date = %s and uid=%s and status='malicious'", (i,id_user,))
                y = cur.fetchone()
                if x == None:
                    x = 0
                    ben_rec.append(x)
                elif y == None:
                    y=0
                    mal_rec.append(y)
                else:
                    ben_rec.append(x['num_scan'])
                    mal_rec.append(y['num_scan'])

            cur.execute(
                    "SELECT COUNT(status) from url where status = 'benign' and uid = %s", (id_user,))
            total_benign = cur.fetchone()
            # print(total_benign['COUNT(status)'])
            cur.execute(
                    "SELECT COUNT(status) from url where status = 'malicious' and uid = %s", (id_user,))
            total_malicious = cur.fetchone()
            # print(total_malicious['COUNT(status)'])
            cur.execute(
                    "SELECT urls, status, date from url  where uid = %s order by date desc", (id_user,))
            recent_scan = cur.fetchmany(6)

            if not recent_scan:
                recent_scan = "No data available in table"

            data = {
                    "data0": total_benign['COUNT(status)']+total_malicious['COUNT(status)'],
                    "data1": total_benign['COUNT(status)'],
                    "data2": total_malicious['COUNT(status)'],
                    "data3": recent_scan,
                    "data4": range_date,
                    "data5": ben_rec,
                    "data6": mal_rec
                    }
            # print(data['data3'])
            return render_template('dashboard.html', data=data)
    else:
        flash("Please sign in")
        return redirect(url_for('signin'))


# # Route to 404 page
@app.errorhandler(404)
def error(e):
    return render_template('404.html')


@app.route('/error')
def meme():
    return render_template('400.html')


# Route to home page
@app.route('/logout')
def logout():
    global ses_created
    lastseen = datetime.now()
    get_time = lastseen.strftime("%Y-%m-%d %H:%M:%S")
    cur = mysql.connection.cursor()
    # print(session['email'])
    cur.execute("UPDATE users SET lastseen = %s where email = %s",
            (get_time, session['email'],))
    mysql.connection.commit()

    cur.execute("SELECT num from session")
    ses_created = int(cur.fetchone()['num'])
    ses_created -= 1 
    cur.execute("UPDATE session set num=%s",(ses_created,))
    mysql.connection.commit()
    
    cur.close()
    session.clear()

    return redirect(url_for('index'))


@app.route('/users')
def users():
    cur = mysql.connection.cursor()
    cur.execute(
            "SELECT users.id, username, email, role , COUNT(report.uid) AS number_of_report, lastseen FROM users left join report on users.id = report.uid GROUP BY username order by users.id")
    total_users = cur.fetchall()

    cur.execute("SELECT COUNT(id) from users")
    num_user = cur.fetchone()

    cur.execute("SELECT COUNT(id) from users where role = 'admin'")
    num_admin = cur.fetchone()

    cur.execute("SELECT num from session")
    ses_created = cur.fetchone()['num']

    data = {
            "data0": total_users,
            "data1": num_user['COUNT(id)'],
            "data2": num_admin['COUNT(id)'],
            "data3": ses_created,
            }
    return render_template('users.html', data=data)


@app.route('/extension')
def extension():
    return render_template('extension.html')


@app.route('/api')
def api():
    data_api = []

    cur = mysql.connection.cursor()

    cur.execute("SELECT apikey from users where email = %s",
            (session['email'],))
    api_key = cur.fetchone()['apikey']

    for i in range_date:
        cur.execute(
                "SELECT count from api where date = %s and apikey=%s", (i,api_key,))
        x = cur.fetchone()
        if x == None:
            x = 0
            data_api.append(x)
        else:
            data_api.append(x['count'])

    return render_template('api.html', data=api_key, data2=range_date, data3=data_api)


@app.route('/report')
def report():
    if session['role'] == "admin":
        cur = mysql.connection.cursor()
        # print(session['email'])

        cur.execute(
                "SELECT report.id, url, status, date , details, users.username AS username FROM report left join users on users.id = report.uid")

        recent_scan = cur.fetchall()

        cur.execute("SELECT COUNT(uid) from report ")
        total_report = cur.fetchone()

        cur.execute(
                "SELECT COUNT(uid) from report where status ='valid'")
        valid_report = cur.fetchone()

        cur.execute(
                "SELECT COUNT(uid) from report where status ='invalid'")
        invalid_report = cur.fetchone()

        # print(recent_scan)

    else:
        cur = mysql.connection.cursor()
        # print(session['email'])
        cur.execute("SELECT id from users where email = %s",
                (session['email'],))
        uid = cur.fetchone()
        # print(uid['id'])

        cur.execute(
                "SELECT url, status, date,details from report where uid = %s ORDER by date DESC", (uid['id'],))
        recent_scan = cur.fetchall()

        cur.execute(
                "SELECT COUNT(uid) from report where uid = %s", (uid['id'],))
        total_report = cur.fetchone()

        cur.execute(
                "SELECT COUNT(uid) from report where uid = %s and status ='valid'", (uid['id'],))
        valid_report = cur.fetchone()

        cur.execute(
                "SELECT COUNT(uid) from report where uid = %s and status ='invalid'", (uid['id'],))
        invalid_report = cur.fetchone()

        # print(recent_scan)
    data = {
            "data0": total_report['COUNT(uid)'],
            "data1": valid_report['COUNT(uid)'],
            "data2": invalid_report['COUNT(uid)'],
            "data3": total_report['COUNT(uid)']-valid_report['COUNT(uid)']-invalid_report['COUNT(uid)'],
            "data4": recent_scan
            }
    return render_template('report.html', data=data)


@app.route('/report/del', methods=['POST'])
def delreport():
    cur = mysql.connection.cursor()
    url = request.form['url']
    date = request.form['date']
    cur.execute("SELECT id FROM users WHERE email=%s",(session['email'],))
    id = cur.fetchone()['id']
    cur.execute("DELETE FROM report WHERE uid=%s and url=%s and date=%s",(id,url,date,))
    mysql.connection.commit()
    flash("Report deleted successfully")
    return redirect(url_for('report'))


@app.route('/report/val', methods=['POST'])
def valreport():
    cur = mysql.connection.cursor()
    if request.form['validate'] == "valid":
        validate = "valid"
    else:
        validate = "invalid"

    rep_id = request.form['id']

    cur.execute("UPDATE report SET status = %s WHERE id=%s",(validate,rep_id,))
    mysql.connection.commit()
    return redirect(url_for('report'))


@app.route('/edit/pass', methods=['POST'])
def editpass():
    cur = mysql.connection.cursor()
    old_pass = request.form['old-pass'].encode('utf-8')
    new_pass = request.form['new-pass'].encode('utf-8')
    new_pass2 = request.form['new-pass2'].encode('utf-8')
    cur.execute("SELECT password from users where email = %s",(session['email'],))
    password = cur.fetchone()['password']
    temp = bcrypt.hashpw(old_pass, password.encode('utf-8'))
    # print(temp)
    if temp == password.encode('utf-8'):
        # print("haaa")
        if new_pass == new_pass2:
            hash_password = bcrypt.hashpw(new_pass2, bcrypt.gensalt())
            cur.execute("UPDATE users SET password = %s WHERE email = %s",(hash_password,session['email'],))
            mysql.connection.commit()
            flash("Your password change successfully")
            return redirect(url_for('dashboard'))
        else:
            flash("Your new password is not match")
            return redirect(url_for('dashboard'))
    else:
        flash("Your old password appears to be incorrect")
        return redirect(url_for('dashboard'))
    

@app.route('/edit/role', methods=['POST'])
def editrole():
    cur = mysql.connection.cursor()
    username = request.form['info-username']
    role = request.form['info-role']
    if role == "admin":
        cur.execute("UPDATE users SET role = %s WHERE username = %s",(role,username,))
        mysql.connection.commit()    
        flash("User information updated")
    else:
        flash("User information failed")
    return redirect(url_for('users'))
    

@app.route('/edit/pic', methods=['POST'])
def editpic():
    if 'user-img' not in request.files:
        flash("Upload image failed")
        return redirect(url_for('dashboard'))

    img_user = request.files['user-img']
    pic_byte = request.files['user-img'].read()
    
    if img_user and allowed_file(img_user.filename):
        cur = mysql.connection.cursor()
        pic_bs64 = base64.b64encode(pic_byte)
        cur.execute("UPDATE users SET image = %s WHERE email = %s",(pic_bs64,session['email'],))
        mysql.connection.commit()    
        flash("User image updated")
        return redirect(url_for('dashboard'))

    flash("Upload image failed")
    return redirect(url_for('dashboard'))
    

@app.route('/scan/extension', methods=['POST'])
def scanextension():
    get_url = request.form['url']
    get_result = feature_extraction.load_url(get_url)
    arr = np.array([[get_result[0], get_result[1], get_result[2],
        get_result[3], get_result[4], get_result[5], get_result[6], get_result[7],
        get_result[8], get_result[9], get_result[10], get_result[11], get_result[12]]])

    prediction = model.predict(arr)

    return jsonify(prediction[0])

@app.context_processor
def context_processor():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT fname, lname, email, username, image from users where email = %s",(session['email'],))
        user_info = cur.fetchone()
        cur.execute("SELECT image from users where email = %s",(session['email'],))
        user_info_img = cur.fetchone()
        user_info_img = user_info_img['image'].decode('UTF-8')
        user_info['image'] = user_info_img
        return dict(uinfo=user_info)
    except:
        return dict(info='')


if __name__ == '__main__':
    app.run(debug=True)
