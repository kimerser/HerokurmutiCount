from datetime import datetime
from typing import Type
from flask import Flask, render_template, redirect, request, url_for, Response, jsonify, flash, session
import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash
app = Flask(__name__)

# mydb = mysql.connector.connect(
#     host="ec2-3-224-125-117.compute-1.amazonaws.com",
#     user="lkpgoucsyezcgn",
#     password="3ddf4e897e1859e61bfffa3bf668acf9633c6dd82c7f03aec8308be5234ecf3e",
#     database="d4pf0p93fbnod2"
# )
mydb = psycopg2.connect(database="d7s6m6ath6ve13"
    , user="zgvqfwsigmwxmz"
    , password="1165a95e7ba1d4c6455d6cab658649c2a5490c8fff39ab89d0be207935eb351c"
    , host="ec2-44-195-169-163.compute-1.amazonaws.com"
    , port="5432")
mycursor = mydb.cursor()

@app.route("/index")
def index():
    # con=mydb.connection.cursor()
    # sql = "SELECT * FROM faculty order by fac_id "
    sql = "select dc.fac_id ,f.fac_name,f.fac_name,dc.num_of_graduates,dc.dateuse,dc.range_count,dc.degree_id ,dc.count_id,dc.count_no from date_counts dc  inner join faculty f on dc.fac_id = f.fac_id inner join degrees d on d.degree_id = dc.degree_id order by dc.dateuse, dc.count_no "
    mycursor.execute(sql)
    res = mycursor.fetchall()

    sql = "select dc.dateuse from date_counts dc  inner join faculty f on dc.fac_id = f.fac_id inner join degrees d on d.degree_id = dc.degree_id group by dc.dateuse order by dc.dateuse"
    mycursor.execute(sql)
    datasert = mycursor.fetchall()

    sql = "select fac_id ,fac_name from faculty f order by fac_id "
    mycursor.execute(sql)
    facdetail = mycursor.fetchall()
    # print(res)
    sql = "SELECT sum(num_of_graduates) FROM date_counts dc"
    mycursor.execute(sql)
    facsum = mycursor.fetchall()

    sql = 'select p."timeDelay"  ,p.left ,p.right,p.timenotify  from parameters p'
    mycursor.execute(sql)
    side = mycursor.fetchall()
    # print(rows)

    
    return render_template("index.html", datas=res,facdetail=facdetail, datasert=datasert, facsum=facsum, side=side)

@app.route("/configparamers")
def configparamers():
    sql = 'select p."timeDelay"  ,p.left ,p.right,p.timenotify,p.dateuse,p.range_count   from parameters p'
    mycursor.execute(sql)
    side = mycursor.fetchall()
    print(side)
    return render_template("admin.html", side=side)

# @app.route("/login")
# def login():
#     # sql = 'select p."timeDelay"  ,p.left ,p.right,p.timenotify,p.dateuse,p.range_count   from parameters p'
#     # mycursor.execute(sql)
#     # side = mycursor.fetchall()
#     # print(side)
#     return render_template("login.html")

@app.route("/monitoring", methods=['GET'])
def monitoring():
    
    print(datetime.now())
    now = datetime.now()
    current_date = now.strftime("%Y-%m-%d")
    startTime = now
    endTime = now
    print(current_date)
    val = [current_date]
    selectDate = "select cp.start_time ,cp.end_time from count_proc cp left join date_counts dc ON cp.count_id  =  dc.count_id  WHERE dc.dateuse  =  %s   and cp.start_time is not null order by  dc.count_no  desc LIMIT 1  "
    mycursor.execute(selectDate,val)
    selectDate = mycursor.fetchall()
    for selectDate in selectDate:
        # dateuse = datamonitor[0]
        startTime = selectDate[0]
        endTime = selectDate[1]
    if startTime is None :
        startTime = now.strftime("%H:%M:%S")
    else:
         startTime = startTime.strftime("%H:%M:%S")
   
    if endTime is None :
        endTime = now.strftime("%H:%M:%S")
    else:
        endTime = endTime.strftime("%H:%M:%S")
    sql = "select dc.dateuse, sum(cp.current_person),sum(dc.num_of_graduates)  from count_proc cp inner join date_counts dc ON cp.count_id = dc.count_id where  dc.dateuse =  %s  group by dc.dateuse"
    mycursor.execute(sql,val)
    datamonitor = mycursor.fetchall()
    print(datamonitor)
    for datamonitor in datamonitor:
        # dateuse = datamonitor[0]
        currentPerson = datamonitor[1]
        numOfGraduates = datamonitor[2]

    print(currentPerson , " currentPerson")
    print(numOfGraduates , " numOfGraduates")
    percen = (currentPerson/numOfGraduates) * 100 
    percen = int(percen)
    print(percen)
    balance = numOfGraduates - currentPerson
    return render_template("monitoring.html",percen = percen, currentPerson = currentPerson, balance = balance ,startTime=startTime , endTime =endTime)





@ app.route('/update', methods=['POST'])
def update():
    print("update")
    countNo = request.form["countNo"]
    facId = request.form["facId"]
    countId = request.form["countId"]
    # fac = request.form["fac"]
    # department = request.form["department"]
    num = request.form["num"]
    dateuse = request.form["dateuse"]
    range = request.form["range"]
    dregree = request.form["dregree"]
    sql = "UPDATE date_counts SET  dateuse=%s, range_count=%s, degree_id=%s, num_of_graduates=%s ,count_no=%s,fac_id=%s  WHERE count_id=%s"
    val = [dateuse,range,dregree, num,countNo,facId, countId]
    print(val)
    mycursor.execute(sql, val)
    mydb.commit()
    return redirect(url_for("index"))


@ app.route("/update_left", methods=['GET', 'POST'])
def left():
    left = request.form["left"]
    sql = 'UPDATE parameters SET "left"= %s'
    val = [left]
    mycursor.execute(sql, val)
    mydb.commit()
    return redirect(url_for("configparamers"))

@ app.route("/update_dateuse", methods=['GET', 'POST'])
def updateDateuse():
    print("update_dateuse")
    dateuse = request.form["dateuse"]
    print(dateuse)
    sql = 'UPDATE parameters SET dateuse= %s'
    val = [dateuse]
    mycursor.execute(sql, val)
    mydb.commit()
    return redirect(url_for("index"))


@ app.route("/update_range_count", methods=['GET', 'POST'])
def updateRangeCount():
    print("update_dateuse")
    rangecount = request.form["rangecount"]
    print(rangecount)
    sql = 'UPDATE parameters SET range_count    = %s'
    val = [rangecount]
    mycursor.execute(sql, val)
    mydb.commit()
    return redirect(url_for("index"))


@ app.route("/index", methods=['GET', 'POST'])
def find_fac():
    print("index")
        # con=mydb.connection.cursor()
    # sql = "SELECT * FROM faculty  where dateuse=%s order by fac_id"
    sql = "select dc.fac_id ,f.fac_name,f.fac_name,dc.num_of_graduates,dc.dateuse,dc.range_count,dc.degree_id ,dc.count_id ,dc.count_no from date_counts dc  inner join faculty f on dc.fac_id = f.fac_id inner join degrees d on d.degree_id = dc.degree_id where dc.dateuse like %s order by dc.count_id "
    dateuse = request.form["dateuse"]
    # range = request.form["range"]
    val =[dateuse]
    print(val)
    mycursor.execute(sql,val)
    res = mycursor.fetchall()

    sql = "select fac_id ,fac_name from faculty f order by fac_id"
    mycursor.execute(sql)
    facdetail = mycursor.fetchall()

    sql = "select dateuse from date_counts dc"
    mycursor.execute(sql)
    res2 = mycursor.fetchall()

    sql = "select dc.dateuse from date_counts dc  inner join faculty f on dc.fac_id = f.fac_id inner join degrees d on d.degree_id = dc.degree_id group by dc.dateuse order by dc.dateuse"
    mycursor.execute(sql)
    datasert = mycursor.fetchall()
    # # print(res)
    # sql = "SELECT sum(num_of_graduates) FROM faculty"
    # mycursor.execute(sql)
    # facsum = mycursor.fetchall()

    # sql = 'select p."timeDelay"  ,p.left ,p.right  from parameters p'
    # mycursor.execute(sql)
    # side = mycursor.fetchall()
    # # print(rows)
    return render_template("index.html", datas=res,facdetail=facdetail,datasert=datasert)


@ app.route("/update_right", methods=['GET', 'POST'])
def right():
    right = request.form["right"]
    # sql = "UPDATE `parameter` SET `right`= %s"
    sql = 'UPDATE parameters SET "right"= %s'
    val = [right]
    mycursor.execute(sql, val)
    mydb.commit()
    return redirect(url_for("configparamers"))

@ app.route("/update_linetoken", methods=['GET', 'POST'])
def linetoken():
    linetoken = request.form["linetoken"]
    # sql = "UPDATE `parameter` SET `right`= %s"
    sql = 'UPDATE parameters SET "linetoken"= %s'
    val = [linetoken]
    mycursor.execute(sql, val)
    mydb.commit()
    return redirect(url_for("configparamers"))

@ app.route("/delaytime", methods=['GET', 'POST'])
def delaytime():
    delaytime = request.form["delaytime"]
    # sql = "UPDATE `parameter` SET `timeDelay`= %s"
    sql = 'UPDATE parameters SET "timeDelay"= %s'
    val = [delaytime]
    mycursor.execute(sql, val)
    mydb.commit()
    return redirect(url_for("configparamers"))

@ app.route("/update_timenotify", methods=['GET', 'POST'])
def timenotify():
    timenotify = request.form["timenotify"]
    # sql = "UPDATE `parameter` SET `timeDelay`= %s"
    sql = 'UPDATE parameters SET "timenotify"= %s'
    val = [timenotify]
    mycursor.execute(sql, val)
    mydb.commit()
    return redirect(url_for("configparamers"))

@ app.route("/insert_fac", methods=['GET', 'POST'])
def insert_fac():
    try:
        if request.method == "POST":
            facId = request.form["facId"]
            fac = request.form["fac"]
            # department = request.form["department"]
            # num = request.form["num"]
            # dateuser = request.form["dateuser"]
            # range = request.form["range"]
            # dregree = request.form["dregree"]
            # countNo = request.form["countNo"]
            sql = "INSERT INTO faculty (fac_id, fac_name) VALUES (%s,%s)"
            # sql = "INSERT INTO faculty (fac_id, fac_name, department, num_of_graduates, dateuse, range_count, degrees_id,count_no) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
            val = [facId, fac]
            # val = [facId, fac, department, num ,dateuser,range,dregree,countNo]
            # print(val)    
            mycursor.execute(sql, val)
            mydb.commit()
            print(mycursor.rowcount, "record inserted.")
        else:
            print("NOT SUCCESS")
    except Exception as e:
        return jsonify({'error': 'Missing data!'})
    return redirect(url_for("index"))

@ app.route("/insert_count_no", methods=['GET', 'POST'])
def insert_count_no():
    try:
        if request.method == "POST":
            print("hi")
            facId = request.form["facId"]
            print(facId)
            # fac = request.form["fac"]
            # department = request.form["department"]
            num = request.form["num"]
            print(num)
            dateuse = request.form["dateuse"]
            print(dateuse)
            range = request.form["range"]
            print(range)
            dregree = request.form["dregree"]
            print(dregree)
            countNo = request.form["countNo"]
            print(countNo)
            currentperson = 0;

            sql = "INSERT INTO count_proc (fac_id, start_time, end_time, date_stamp, current_person, time_per_person ) VALUES( NULL, NULL, NULL, NULL, 0, NULL)"
            # val = [facId,dateuse,currentperson]
            mycursor.execute(sql)
            mydb.commit()
            sql = "(select  max(count_id)::text from count_proc cp)"
            mycursor.execute(sql)
            mydb.commit()
            setcountid = mycursor.fetchall()
            for getcountid in setcountid:
                print(getcountid)
                getcountid = setcountid[0]

            sql = "INSERT INTO date_counts (fac_id, dateuse, range_count, count_id, degree_id, num_of_graduates,count_no) VALUES( %s, %s, %s, %s, %s, %s,%s)"
            # sql = "INSERT INTO faculty (fac_id, fac_name, department, num_of_graduates, dateuse, range_count, degrees_id,count_no) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
            # val = [facId, fac]
            val = [facId,dateuse, range, getcountid, dregree , num ,countNo]
            print("insert_count_no")
            print(val)
            print(sql)
            mycursor.execute(sql, val)
            mydb.commit()
            print(mycursor.rowcount, "record inserted.")
        else:
            print("NOT SUCCESS")
    except Exception as e:
        print(e)
        return jsonify({'error': 'Missing data!'})
    return redirect(url_for("index"))

# @ app.route("/testdate", methods=['GET', 'POST'])
# def testdate():
#     try:
#         if request.method == "POST":
#             datetestinput = request.form["datetestinput"]
#             print(datetestinput)
#         else:
#             print("NOT SUCCESS")
#     except Exception as e:
#         return jsonify({'error': 'Missing data!'})
#     return redirect(url_for("index"))
# @ app.route('/process', methods=['POST'])
# def process():

#     email = request.form['email']
#     name = request.form['name']

#     if name and email:
#         newName = name[::-1]

#         return jsonify({'name': newName})

#     return jsonify({'error': 'Missing data!'})
# @app.route("/insert", methods=['GET', 'POST'])
# def insert():
#     if request.method == "POST":
#         Time = request.form["Time"]
#         if Time == '':
#             print("hi")
#         else:
#             left = request.form["left"]
#             right = request.form["right"]
#             sql = "UPDATE `timedelay` SET `TimeDelay`=(%s),`left`=(%s),`right`=(%s) WHERE 1"
#             val = [Time, left, right]
#             mycursor.execute(sql, val)
#             mydb.commit()
#             print(mycursor.rowcount, "record inserted.")
#     else:
#         print("NOT SUCCESS")

#     return redirect(url_for("index"))


@ app.route('/delete/<string:id_data>', methods=['GET'])
def delelte(id_data):
    mycursor.execute("DELETE FROM date_counts WHERE  count_id = " + (id_data))
    mydb.commit()
    return redirect(url_for("index"))


# @ app.route('/video_feed')
# def video_feed():
#     return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


    # Video streaming route. Put this in the src attribute of an img tag
# camera = cv2.VideoCapture(0)
# switch = 1
# selectcamera = 1


# def gen_frames():
#     sql = 'select p."timeDelay" ,p."left" ,p."right"  from "parameter" p'
#     mycursor.execute(sql)
#     myresult = mycursor.fetchall()
#     left = 0
#     right = 0
#     for parameter in myresult:
#         left = parameter[0]
#         right = parameter[1]
#         print(left, right)
#     while True:
#         success, frame = camera.read()  # read the camera frame
#         frameHeight = frame.shape[0]
#         frameWidth = frame.shape[1]
#         cv2.line(frame, (frameWidth//2 - left, 0),
#                  (frameWidth//2 - left, frameHeight), (0, 255, 255), 2)
#         cv2.line(frame, (frameWidth//2 + right, 0),
#                  (frameWidth//2 + right, frameHeight), (0, 255, 255), 2)
#         if not success:
#             break
#         else:
#             ret, buffer = cv2.imencode('.jpg', frame)
#             frame = buffer.tobytes()
#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


# @ app.route('/requests', methods=['POST', 'GET'])
# def tasks():
#     global switch, camera, selectcamera
#     print(left, " ", right)
#     if request.method == 'POST':
#         if request.form.get('stop') == 'Start/Stop':
#             if(switch == 1):
#                 switch = 0
#                 camera.release()
#                 cv2.destroyAllWindows()
#             else:
#                 camera = cv2.VideoCapture(0)
#                 switch = 1
#             return redirect(url_for("index"))
#         elif request.form.get('camera') == 'camera':
#             if(selectcamera == 1):
#                 camera = cv2.VideoCapture(selectcamera)
#                 selectcamera = 0
#             else:
#                 camera = cv2.VideoCapture(selectcamera)
#                 selectcamera = 1
#             return redirect(url_for("index"))
#         return redirect(url_for("index"))

@app.route('/')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('login.html', username=session['username'])
        #  User is not loggedin redirect to login page
    return redirect(url_for('login'))

from datetime import datetime
@ app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text']
    processed_text = text.upper()
    return processed_text

@app.route('/login', methods=['GET', 'POST'])
def login():
    print("login")
#     cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        print("method")
        username = request.form['username']
        password = request.form['password']
        print(password)

        # Check if account exists using MySQL
        # mycursor.execute("DELETE FROM date_counts WHERE  count_id = " + (id_data))
        mycursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        # Fetch one record and return result
        account = mycursor.fetchone()
        print(account)
        if account:
            password_rs = account[3]
            print(password_rs, password)
            # If account exists in users table in out database
            if (password_rs == password):
                print("before session")
                # Create session data, we can access this data in other routes
                # session['loggedin'] = True
                # session['id'] = account['id']
                # session['username'] = account['username']
                # Redirect to home page
                print("Redirect to index")
                if(username == 'admin'):
                    return redirect(url_for('configparamers'))
                else:
                    return redirect(url_for('index'))
            else:
                # Account doesnt exist or username/password incorrect
                flash('Incorrect username/password')
        else:
            # Account doesnt exist or username/password incorrect
            flash('Incorrect username/password')

    return render_template('login.html')


if __name__ == "__main__":
    app.run(debug=True)


# {{ url_for('video_feed') }}
# {{ url_for('tasks') }}