@app.route("/configparamers")
# def index():
#     # con=mydb.connection.cursor()
#     sql = "SELECT * FROM faculty order by fac_id "
#     mycursor.execute(sql)
#     res = mycursor.fetchall()
#     # print(res)
#     sql = "SELECT sum(num_of_graduates) FROM faculty"
#     mycursor.execute(sql)
#     facsum = mycursor.fetchall()

#     sql = 'select p."timeDelay"  ,p.left ,p.right  from parameters p'
#     mycursor.execute(sql)
#     side = mycursor.fetchall()
#     return render_template("index.html", datas=res, facsum=facsum, side=side)