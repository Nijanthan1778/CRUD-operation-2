from flask import Flask,render_template,request,redirect,url_for
import sqlite3

app=Flask(__name__)

@app.route("/")
def func():
    conn=sqlite3.connect("userList.db")
    conn.row_factory=sqlite3.Row
    cur=conn.cursor()
    cur.execute("Select * from users")
    data=cur.fetchall()
    print(data)
    conn.commit()
    return render_template("home.html",d=data)

@app.route("/addUser",methods=["GET","POST"])
def addUser():
    if request.method=="POST":
        name=request.form.get("name")
        age=request.form.get("age")
        rollno=request.form.get("rollno")
        conn=sqlite3.connect("userList.db")
        cur=conn.cursor()
        cur.execute("Insert Into users(Name,Age,Roll_No) values(?,?,?)",(name,age,rollno))
        conn.commit()
        return redirect(url_for("func"))
    return render_template("add_user.html")

@app.route("/editUser/<string:id>",methods=["GET","POST"])
def editUser(id):
    if request.method=="POST":
        name=request.form.get("name")
        age=request.form.get("age")
        rollno=request.form.get("rollno")
        conn=sqlite3.connect("userList.db")
        cur=conn.cursor()
        cur.execute("Update users set Name=?, Age=?, Roll_No=?  where Roll_No=?",(name,age,rollno,id))
        conn.commit()
        return redirect(url_for("func"))
    conn=sqlite3.connect("userList.db")
    conn.row_factory=sqlite3.Row
    cur=conn.cursor()
    cur.execute("Select * from users where ROll_No=?",(id,))
    data=cur.fetchone()
    return render_template("edit.html",d=data)    

@app.route("/deleteUser/<string:id>")
def deleteUser(id):
    conn=sqlite3.connect("userList.db")
    cur=conn.cursor()
    cur.execute("Delete from users where Roll_No=?",(id,))
    conn.commit()
    return redirect(url_for("func"))
if __name__=="__main__":
    app.run(debug=True)
