from flask import Flask, render_template, request, url_for, redirect, session, flash
from flask_mysqldb import MySQL, MySQLdb
import api_check
from datetime import datetime
import bcrypt
import numpy as np
import pickle
import feature_extraction

model = pickle.load(open('url_predict.pkl', 'rb'))

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'scanme_db'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

count_benign = 0
count_malicious = 0
count = 0
t = []
k = {}
recently_scan_dash = ()

# Route to homepage
@app.route('/')
def index():
    return render_template('index.html')


# Route to result page
@app.route('/result', methods=['POST'])
def result():
    global count_benign, count_malicious, count, t, k, recently_scan_dash

    get_url = request.form['url']
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
    get_url_redirect = get_result[8]
    get_url_created = get_url_details[4]
    get_url_country = get_url_details[5]
    now = datetime.now()
    get_time = now.strftime("%d/%m/%Y %H:%M:%S")
    get_screenshot = api_check.screenshot(get_url)
    get_base64_image = api_check.get_as_base64(get_screenshot)

    # recently_scan.

    if prediction[0] == 'benign':
        count_benign += 1

    else:
        count_malicious += 1

    if count >= 6:
        t.pop(0)
    k['urls'] = get_url
    k['status'] = prediction
    t.append(k.copy())
    count += 1

    recently_scan_dash = tuple(t)

    if session.get('email') != None:
        cur = mysql.connection.cursor()
        cur.execute("SELECT id from users where email = %s",
                    (session['email'],))
        user = cur.fetchone()
        cur.execute("INSERT INTO url (uid,urls,status) VALUES (%s,%s,%s)",
                    (user['id'], get_url, prediction[0],))
        mysql.connection.commit()
        cur.close()

    return render_template('result.html', data0=get_url, data1=get_time, data2=get_base64_image,
                           data3=prediction, data4=get_url_domain, data5=get_url_status, data6=get_url_content,
                           data7=get_url_ip, data8=get_url_redirect, data9=get_url_created, data10=get_url_country)


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
        hash_password = bcrypt.hashpw(password, bcrypt.gensalt())

        cur = mysql.connection.cursor()
        # print(cur.execute("SELECT * FROM users WHERE email=%s" , (email,))) return 1 if exist in db
        if cur.execute("SELECT * FROM users WHERE email=%s", (email,)) or cur.execute("SELECT * FROM users WHERE username=%s", (username,)):
            flash("The account is already exist!")
            cur.close()
        else:
            cur.execute("INSERT INTO users (fname,lname,email,username,password) VALUES (%s,%s,%s,%s,%s)",
                        (fname, lname, email, username, hash_password,))
            mysql.connection.commit()
            cur.close()
            session['email'] = email
            session['fname'] = fname
            flash("The account created successfully.")
        return render_template('signup.html')


# Route to dashboard page
@app.route('/dashboard')
def dashboard():
    global recently_scan

    if 'email' in session:
        if session['email'] == "dafiq856@gmail.com":

            data = {
                "data0": count_benign+count_malicious,
                "data1": count_benign,
                "data2": count_malicious,
                "data3" : recently_scan_dash
            }
            print(data['data3'])
            return render_template('dashboard.html', data=data)
        else:
            cur = mysql.connection.cursor()
            # print(session['email'])
            cur.execute("SELECT id from users where email = %s",
                        (session['email'],))
            uid = cur.fetchone()
            # print(uid['id'])
            cur.execute(
                "SELECT COUNT(status) from url where status = 'benign' and uid = %s", (uid['id'],))
            total_benign = cur.fetchone()
            # print(total_benign['COUNT(status)'])
            cur.execute(
                "SELECT COUNT(status) from url where status = 'malicious' and uid = %s", (uid['id'],))
            total_malicious = cur.fetchone()
            # print(total_malicious['COUNT(status)'])
            cur.execute(
                "SELECT urls, status from url where uid = %s", (uid['id'],))
            recent_scan = cur.fetchmany(7)

            print(recent_scan)

            data = {
                "data0": total_benign['COUNT(status)']+total_malicious['COUNT(status)'],
                "data1": total_benign['COUNT(status)'],
                "data2": total_malicious['COUNT(status)'],
                "data3": recent_scan
            }
            print(data['data3'])
            return render_template('dashboard.html', data=data)
    else:
        flash("Please sign in")
        return redirect(url_for('signin'))


# Route to 404 page
@app.errorhandler(404)
def error(e):
    return render_template('404.html')

# Route to home page 
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/users')
def users():
    return render_template('users.html')


@app.route('/extension')
def extension():
    return render_template('extension.html')


@app.route('/api')
def api():
    return render_template('api.html')


@app.route('/report')
def report():
    return render_template('report.html')


if __name__ == '__main__':
    app.secret_key = "!@#QWERRRRRRRASDF1234"
    app.run(debug=True)
