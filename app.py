from flask import Flask,render_template,request,redirect,url_for
import sqlite3 as sql

app=Flask(__name__)

@app.route("/")
def read():
    conn=sql.connect("students.db")
    conn.row_factory=sql.Row
    cur=conn.cursor()
    cur.execute("Select * from student")
    data=cur.fetchall()
    return render_template("home.html",d=data)

@app.route("/add_student",methods=["POST","GET"])
def add_student():

    if request.method=="POST":
        name=request.form.get("name")
        age=request.form.get("age")
        rollno=request.form.get("rollno")
        conn=sql.connect("students.db")
        cur=conn.cursor()
        cur.execute("Insert into student(Name, Age, Roll_No) values(?,?,?)",(name,age,rollno))
        conn.commit()
        return redirect(url_for("read"))
    return render_template("add_student.html")

@app.route("/fromAPI",methods=["POST","GET"])
def createFromAPI():
    if request.method=="POST":
        data=request.json
        conn=sql.connect("students.db")
        cur=conn.cursor()
        cur.execute("Insert into student(Name,Age,Roll_No) values(?,?,?)",(data["Name"],data["Age"],data["Roll_No"]))
        conn.commit()
    return render_template("home.html")    


@app.route("/update_student/<string:id>",methods=["GET","POST"])
def update_student(id):
    if request.method=="POST":
        name=request.form.get("name")
        age=request.form.get("age")
        rollno=request.form.get("rollno")
        conn=sql.connect("students.db")
        cur=conn.cursor()
        cur.execute("Update student set Name=?, Age=?, Roll_No=? where ID=?",(name,age,rollno,id))
        conn.commit()
        return redirect(url_for("read"))
    conn=sql.connect("students.db")
    conn.row_factory=sql.Row
    cur=conn.cursor()
    cur.execute("Select * from student where ID=?",(id,))
    data=cur.fetchone()
    return render_template("update_student.html",d=data)
    

@app.route("/delete_student/<string:id>",methods=["POST","GET"])
def delete_student(id):
    conn=sql.connect("students.db")
    cur=conn.cursor()
    cur.execute("Delete from student where ID=?",(id,))
    conn.commit()
    return redirect(url_for("read"))



if __name__=="__main__":
    app.run(debug=True)
