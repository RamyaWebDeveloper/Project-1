from flask import Flask, render_template, redirect, url_for, request, flash
import sqlite3
import datetime

app=Flask(__name__)
app.secret_key = 'Ramyarey'
con=sqlite3.connect("todo.db", check_same_thread=False)
cur=con.cursor()

@app.route("/", methods=["GET","POST"])
def new():
    if request.method == "POST":
        title=request.form.get('title')
        content=request.form.get('content')
        datetimes=datetime.datetime.now()
        dates= datetimes.strftime("%x")
        times= datetimes.strftime("%X")

        con.execute("create table if not exists Lists(S_No integer primary key autoincrement, Title varchar(60), Content text, Date date, Time time)")
        con.execute("insert into Lists(Title, Content, Date, Time) values(?,?,?,?)", (title, content,dates,times))
        con.commit()
        cur.execute("select * from Lists")
        data=cur.fetchall()
        return render_template("new.html", datas=data)
    cur.execute("select * from Lists")
    data=cur.fetchall()
    return render_template("new.html", datas=data)

@app.route("/update/<int:id>", methods=["GET","POST"])
def update(id):
    cur.execute("select * from Lists where S_No = ?", (id,))
    data = cur.fetchall()
    if request.method == "POST":
        title=request.form.get('title')
        content=request.form.get('content')
        datetimes=datetime.datetime.now()
        dates= datetimes.strftime("%x")
        times= datetimes.strftime("%X")

        cur.execute("update Lists set Title = ?, Content = ?, Date = ?, Time = ? where S_No = ?", (title, content, dates, times,id))
        con.commit()
        flash("Successfully Updated!", "info")
        return redirect('/')
    return render_template("new.html", data=data)

@app.route("/delete/<int:id>")
def delete(id):
    cur.execute("delete from Lists where S_No = ?", (id,))
    con.commit()
    cur.execute("select * from Lists")
    data= cur.fetchall()
    flash("Successfully Deleted", "danger")
    return render_template("new.html", datas=data)

if __name__ == ("__main__"):
    app.run(debug=True)
