from datetime import datetime
from typing import Type
from flask import Flask, render_template, redirect, request, url_for, Response, jsonify, flash
import psycopg2
# from werkzeug.security import generate_password_hash, check_password_hash
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
mydb = psycopg2.connect(database="d7s6m6ath6ve13"
    , user="zgvqfwsigmwxmz"
    , password="1165a95e7ba1d4c6455d6cab658649c2a5490c8fff39ab89d0be207935eb351c"
    , host="ec2-44-195-169-163.compute-1.amazonaws.com"
    , port="5432")
mycursor = mydb.cursor()

@app.route("/index")
def index():
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

    sql = 'select p."timeDelay"  ,p.left ,p.right,p.timenotify , p.range_count  from parameters p'
    mycursor.execute(sql)
    side = mycursor.fetchall()
    # print(rows)
    for side in side:
        # dateuse = datamonitor[0]
        rangeCount = side[4]
    return render_template("index.html", datas=res,facdetail=facdetail, datasert=datasert, facsum=facsum, side=side,rangeCount=rangeCount)

@app.route("/configparamers")
def configparamers():
    sql = 'select p."timeDelay"  ,p.left ,p.right,p.timenotify,p.dateuse,p.range_count   from parameters p'
    mycursor.execute(sql)
    side = mycursor.fetchall()
    print(side)
    return render_template("admin.html", side=side)


@app.route("/monitoring", methods=['GET'])
def monitoring():
    currentPerson = 0
    numOfGraduates = 0
    percen = 0
    balance = 0
    print(datetime.now())
    now = datetime.now()
    current_date = now.strftime("%Y-%m-%d")
    startTime = now
    endTime = now
    print(current_date)
    val = [current_date]
    selectDate = "select cp.start_time ,cp.end_time from count_proc cp left join date_counts dc ON cp.count_id  =  dc.count_id  WHERE dc.dateuse  =  %s   and cp.start_time is not null  and dc.range_count  = '1'   order by  dc.count_no  desc LIMIT 1  "
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
    sql = "select dc.dateuse, sum(cp.current_person),sum(dc.num_of_graduates)  from count_proc cp inner join date_counts dc ON cp.count_id = dc.count_id where  dc.dateuse =  %s  and dc.range_count  = '1'  group by dc.dateuse"
    mycursor.execute(sql,val)
    datamonitor = mycursor.fetchall()
    print(datamonitor)
    for datamonitor in datamonitor:
        # dateuse = datamonitor[0]
        currentPerson = datamonitor[1]
        numOfGraduates = datamonitor[2]

    print(currentPerson , " currentPerson")
    print(numOfGraduates , " numOfGraduates")
    if(currentPerson != 0 and numOfGraduates != 0):
        percen = (currentPerson/numOfGraduates) * 100 
        percen = int(percen)
        print(percen)
        balance = numOfGraduates - currentPerson

    currentPerson2 = 0
    numOfGraduates2 = 0
    percen2 = 0
    balance2 = 0
    current_date2 = now.strftime("%Y-%m-%d")
    startTime2 = now
    endTime2 = now
    print(current_date2)
    val = [current_date]
    selectDate2 = "select cp.start_time ,cp.end_time from count_proc cp left join date_counts dc ON cp.count_id  =  dc.count_id  WHERE dc.dateuse  =  %s   and cp.start_time is not null  and dc.range_count  = '2'   order by  dc.count_no  desc LIMIT 1  "
    mycursor.execute(selectDate2,val)
    selectDate2 = mycursor.fetchall()
    for selectDate2 in selectDate2:
        # dateuse = datamonitor[0]
        startTime2 = selectDate2[0]
        endTime2 = selectDate2[1]
    if startTime2 is None :
        startTime2 = now.strftime("%H:%M:%S")
    else:
         startTime2 = startTime2.strftime("%H:%M:%S")
   
    if endTime2 is None :
        endTime2 = now.strftime("%H:%M:%S")
    else:
        endTime2 = endTime2.strftime("%H:%M:%S")
    sql = "select dc.dateuse, sum(cp.current_person),sum(dc.num_of_graduates)  from count_proc cp inner join date_counts dc ON cp.count_id = dc.count_id where  dc.dateuse =  %s  and dc.range_count  = '2'  group by dc.dateuse"
    mycursor.execute(sql,val)
    datamonitor2 = mycursor.fetchall()
    print(datamonitor2)
    for datamonitor2 in datamonitor2:
        # dateuse = datamonitor[0]
        currentPerson2 = datamonitor2[1]
        numOfGraduates2 = datamonitor2[2]
    if(currentPerson2 != 0 or numOfGraduates2 != 0):
        print(currentPerson2 , " currentPerson2")
        print(numOfGraduates2 , " numOfGraduates2")
        percen2 = (currentPerson2/numOfGraduates2) * 100 
        percen2 = int(percen2)
        print(percen2)
        balance2 = numOfGraduates2 - currentPerson2

    currentPerson3 = 0
    numOfGraduates3 = 0
    percen3 = 0
    balance3 = 0
    current_date3 = now.strftime("%Y-%m-%d")
    startTime3 = now
    endTime3 = now
    print(current_date3)
    val = [current_date]
    selectDate3 = "select cp.start_time ,cp.end_time from count_proc cp left join date_counts dc ON cp.count_id  =  dc.count_id  WHERE dc.dateuse  =  %s   and cp.start_time is not null  and dc.range_count  = '3'   order by  dc.count_no  desc LIMIT 1  "
    mycursor.execute(selectDate3,val)
    selectDate3 = mycursor.fetchall()
    for selectDate3 in selectDate3:
        # dateuse = datamonitor[0]
        startTime3 = selectDate3[0]
        endTime3 = selectDate3[1]
    if startTime3 is None :
        startTime3 = now.strftime("%H:%M:%S")
    else:
         startTime3 = startTime3.strftime("%H:%M:%S")
   
    if endTime3 is None :
        endTime3 = now.strftime("%H:%M:%S")
    else:
        endTime3 = endTime3.strftime("%H:%M:%S")
    sql = "select dc.dateuse, sum(cp.current_person),sum(dc.num_of_graduates)  from count_proc cp inner join date_counts dc ON cp.count_id = dc.count_id where  dc.dateuse =  %s  and dc.range_count  = '3'  group by dc.dateuse"
    mycursor.execute(sql,val)
    datamonitor3 = mycursor.fetchall()
    print(datamonitor3)
    for datamonitor3 in datamonitor3:
        # dateuse = datamonitor[0]
        currentPerson3 = datamonitor3[1]
        numOfGraduates3 = datamonitor3[2]
    if(currentPerson3 != 0 or numOfGraduates3 != 0):
        print(currentPerson3 , " currentPerson3")
        print(currentPerson3 , " numOfGraduates3")
        percen3 = (currentPerson3/numOfGraduates3) * 100 
        percen3 = int(percen3)
        print(percen3)
        balance3 = numOfGraduates3 - currentPerson3


    currentPerson4 = 0
    numOfGraduates4 = 0
    percen4 = 0
    balance4 = 0
    current_date4 = now.strftime("%Y-%m-%d")
    startTime4 = now
    endTime4 = now
    print(current_date4)
    val = [current_date]
    selectDate4 = "select cp.start_time ,cp.end_time from count_proc cp left join date_counts dc ON cp.count_id  =  dc.count_id  WHERE dc.dateuse  =  %s   and cp.start_time is not null  and dc.range_count  = '4'   order by  dc.count_no  desc LIMIT 1  "
    mycursor.execute(selectDate4,val)
    selectDate4 = mycursor.fetchall()
    for selectDate4 in selectDate4:
        # dateuse = datamonitor[0]
        startTime4 = selectDate4[0]
        endTime4 = selectDate4[1]
    if startTime4 is None :
        startTime4 = now.strftime("%H:%M:%S")
    else:
         startTime4 = startTime4.strftime("%H:%M:%S")
   
    if endTime4 is None :
        endTime4 = now.strftime("%H:%M:%S")
    else:
        endTime4 = endTime4.strftime("%H:%M:%S")
    sql = "select dc.dateuse, sum(cp.current_person),sum(dc.num_of_graduates)  from count_proc cp inner join date_counts dc ON cp.count_id = dc.count_id where  dc.dateuse =  %s  and dc.range_count  = '4'  group by dc.dateuse"
    mycursor.execute(sql,val)
    datamonitor4 = mycursor.fetchall()
    print(datamonitor4)
    for datamonitor4 in datamonitor4:
        # dateuse = datamonitor[0]
        currentPerson4 = datamonitor4[1]
        numOfGraduates4 = datamonitor4[2]
    if(currentPerson4 != 0 or numOfGraduates4 != 0):
        print(currentPerson4 , " currentPerson4")
        print(currentPerson4 , " numOfGraduates4")
        percen4 = (currentPerson4/numOfGraduates4) * 100 
        percen4 = int(percen4)
        print(percen4)
        balance4 = numOfGraduates4 - currentPerson4
    
    currentPersonall = 0
    numOfGraduatesall = 0
    percenall = 0
    balanceall = 0
    current_dateall = now.strftime("%Y-%m-%d")
    startTimeall = now
    endTimeall = now
    print(current_dateall)
    val = [current_date]
    selectDateall = "select cp.start_time ,cp.end_time from count_proc cp left join date_counts dc ON cp.count_id  =  dc.count_id  WHERE dc.dateuse  =  %s   and cp.start_time is not null   order by  dc.count_no  desc LIMIT 1  "
    mycursor.execute(selectDateall,val)
    selectDateall = mycursor.fetchall()
    for selectDateall in selectDateall:
        # dateuse = datamonitor[0]
        startTimeall = selectDateall[0]
        endTimeall = selectDateall[1]
    if startTimeall is None :
        startTimeall = now.strftime("%H:%M:%S")
    else:
         startTimeall = startTimeall.strftime("%H:%M:%S")
   
    if endTimeall is None :
        endTimeall = now.strftime("%H:%M:%S")
    else:
        endTimeall = endTimeall.strftime("%H:%M:%S")
    sql = "select dc.dateuse, sum(cp.current_person),sum(dc.num_of_graduates)  from count_proc cp inner join date_counts dc ON cp.count_id = dc.count_id where  dc.dateuse =  %s    group by dc.dateuse"
    mycursor.execute(sql,val)
    datamonitorall = mycursor.fetchall()
    print(datamonitorall)
    for datamonitorall in datamonitorall:
        # dateuse = datamonitor[0]
        currentPersonall = datamonitorall[1]
        numOfGraduatesall = datamonitorall[2]
    if(currentPersonall != 0 or numOfGraduatesall != 0):
        print(currentPersonall , " currentPerson4")
        print(currentPersonall , " numOfGraduates4")
        percenall = (currentPersonall/numOfGraduatesall) * 100 
        percenall = int(percenall)
        print(percenall)
        balanceall = numOfGraduatesall - currentPersonall

    return render_template("monitoring.html",percen = percen, currentPerson = currentPerson, balance = balance ,startTime=startTime , endTime =endTime ,
    percen2 = percen2, currentPerson2 = currentPerson2, balance2 = balance2 ,startTime2=startTime2 , endTime2 =endTime2,
    percen3 = percen3, currentPerson3 = currentPerson3, balance3 = balance3 ,startTime3=startTime3 , endTime3 =endTime3,
    percen4 = percen4, currentPerson4 = currentPerson4, balance4 = balance4 ,startTime4=startTime4, endTime4 =endTime4,
    percenall = percenall, currentPersonall = currentPersonall, balanceall = balanceall ,startTimeall=startTimeall, endTimeall =endTimeall)





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
    

    sql = "SELECT sum(num_of_graduates) FROM date_counts dc where dc.dateuse like %s "
    val =[dateuse]
    mycursor.execute(sql,val)
    facsum = mycursor.fetchall()


    sql = 'select p."timeDelay"  ,p.left ,p.right,p.timenotify , p.range_count  from parameters p'
    mycursor.execute(sql)
    side = mycursor.fetchall()
    # print(rows)
    for side in side:
        # dateuse = datamonitor[0]
        rangeCount = side[4]
    # # print(res)
    # sql = "SELECT sum(num_of_graduates) FROM faculty"
    # mycursor.execute(sql)
    # facsum = mycursor.fetchall()

    # sql = 'select p."timeDelay"  ,p.left ,p.right  from parameters p'
    # mycursor.execute(sql)
    # side = mycursor.fetchall()
    # # print(rows)
    return render_template("index.html", datas=res,facdetail=facdetail,datasert=datasert,facsum= facsum,rangeCount =rangeCount)


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
    if(delaytime is None or delaytime == '' ):
        if(type(delaytime) == str):
            print("delaytime")
            flash('ค่าเวลาที่กำหนด ไม่ถูกต้อง')
        else:
            print("delaytime")
            flash('ค่าเวลาที่กำหนดไม่ใช่ตัวเลข')
        return redirect(url_for("configparamers"))
    else:
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
    # # Check if user is loggedin
    # if 'loggedin' in session:
    #     # User is loggedin show them the home page
    #     return render_template('login.html', username=session['username'])
    #     #  User is not loggedin redirect to login page
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
                flash('username หรือ password ไม่ถูกต้อง')
        else:
            # Account doesnt exist or username/password incorrect
            flash('username หรือ password ไม่ถูกต้อง')

    return render_template('login.html')


if __name__ == "__main__":
    app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
    app.run(debug=True)


# {{ url_for('video_feed') }}
# {{ url_for('tasks') }}