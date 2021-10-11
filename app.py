from flask import Flask, render_template, request, url_for, redirect, session, flash, jsonify
from flask_mysqldb import MySQL, MySQLdb
from requests.api import get
import api_check
from datetime import datetime, date, timedelta
import bcrypt
import numpy as np
import pickle
import string
import random
import feature_extraction

model = pickle.load(open('url_predict.pkl', 'rb'))

app = Flask(__name__)

# Unsort json
app.config['JSON_SORT_KEYS'] = False


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'scanme_db'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

count_benign, count, count_malicious, ses_created = 0,0,0,0
recent_url = []
recently_scan_dash = ()
# Route to homepage





def id_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def date_range(start_date):
    number_of_days = 7
    date_list = [(start_date - timedelta(days=day)).isoformat()
                 for day in range(number_of_days)]
    return date_list


range_date = date_range(date.today())
range_date.reverse()

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
        get_url_redirect = get_result[8]
        get_url_created = get_url_details[4]
        get_url_country = get_url_details[5]
        now = datetime.now()
        get_time = now.strftime("%Y-%m-%d %H:%M:%S")
        get_date = now.strftime("%Y-%m-%d")
        get_screenshot = api_check.screenshot(get_url)
        get_base64_image = api_check.get_as_base64(get_screenshot)

        # recently_scan
        if prediction[0] == 'benign':
            count_benign += 1

        else:
            count_malicious += 1

        if count >= 6:
            recent_url.pop(0)
        temp['urls'] = get_url
        temp['status'] = prediction[0]
        recent_url.append(temp.copy())
        count += 1
        recently_scan_dash = tuple(recent_url)

        if session.get('email') != None:
            cur = mysql.connection.cursor()
            cur.execute("SELECT id from users where email = %s",
                        (session['email'],))
            user = cur.fetchone()
            cur.execute("INSERT INTO url (uid,date,urls,status) VALUES (%s,%s,%s,%s)",
                        (user['id'], get_date, get_url, prediction[0],))
            mysql.connection.commit()
            cur.close()

        return render_template('result.html', data0=get_url, data1=get_time, data2=get_base64_image,
                               data3=prediction, data4=get_url_domain, data5=get_url_status, data6=get_url_content,
                               data7=get_url_ip, data8=get_url_redirect, data9=get_url_created, data10=get_url_country)
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
    global ses_created
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
                ses_created += 1
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
            global ses_created
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
            cur.close()
            session['email'] = email
            session['fname'] = fname
            ses_created += 1
            flash("The account created successfully.")
        return render_template('signup.html')

# Route to dashboard page


@app.route('/dashboard')
def dashboard():

    if 'email' in session:

        if session['role'] == "admin":

            data = {
                "data0": count_benign+count_malicious,
                "data1": count_benign,
                "data2": count_malicious,
                "data3": recently_scan_dash[::-1],
                "data4": '',
                "data5": '',
                "data6": ''
            }

            return render_template('dashboard.html', data=data)
        else:
            # print(session['email'])
            cur = mysql.connection.cursor()

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
                "SELECT urls, status from url  where uid = %s order by date desc", (id_user,))
            recent_scan = cur.fetchmany(6)

            # print(recent_scan)

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
    ses_created -= 1
    session.clear()
    return redirect(url_for('index'))


@app.route('/users')
def users():
    global ses_created
    cur = mysql.connection.cursor()
    cur.execute(
        "SELECT username, email, role , COUNT(report.uid) AS number_of_report, lastseen FROM users left join report on users.id = report.uid GROUP BY username order by users.id")
    total_users = cur.fetchall()

    cur.execute("SELECT COUNT(id) from users")
    num_user = cur.fetchone()

    cur.execute("SELECT COUNT(id) from users where role = 'admin'")
    num_admin = cur.fetchone()

    data = {
        "data0": total_users,
        "data1": num_user['COUNT(id)'],
        "data2": num_admin['COUNT(id)'],
        "data3": ses_created
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
        "data0": valid_report['COUNT(uid)']+invalid_report['COUNT(uid)'],
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


if __name__ == '__main__':
    app.secret_key = "!@#QWERRRRRRRASDF1234"
    app.run(debug=True)
