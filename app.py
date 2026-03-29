from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"

def get_db():
    return sqlite3.connect("database.db")

# create table
conn=get_db()
c=conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS complaints (id INTEGER PRIMARY KEY, text TEXT)")
conn.commit()
conn.close()

USER="student"
PASS="1234"
ADMIN="admin"
ADMIN_PASS="admin123"

@app.route("/", methods=["GET","POST"])
def login():
    error=""
    if request.method=="POST":
        if request.form.get("username")==USER and request.form.get("password")==PASS:
            session["user"]="yes"
            return redirect("/home")
        else:
            error="Invalid login"
    return render_template("login.html", error=error)

@app.route("/adminlogin", methods=["GET","POST"])
def adminlogin():
    error=""
    if request.method=="POST":
        if request.form.get("username")==ADMIN and request.form.get("password")==ADMIN_PASS:
            session["admin"]="yes"
            return redirect("/admin")
        else:
            error="Invalid admin login"
    return render_template("adminlogin.html", error=error)

@app.route("/home", methods=["GET","POST"])
def home():
    response="👋 Welcome to College Helpdesk!"
    user_input=""

    if request.method=="POST":
        user_input=request.form.get("question","").lower()

        if "fees" in user_input:
            response="💰 Fees details available in admin office."
        elif "timetable" in user_input:
            response="📅 Timetable available on notice board."
        elif "exam" in user_input:
            response="📝 Exams start next month."
        elif "holiday" in user_input:
            response="🎉 Holiday list available on website."
        elif "admission" in user_input:
            response="🎓 Admission details available on official website."
        elif "library" in user_input:
            response="📚 Library open from 9 AM to 5 PM."
        elif "placement" in user_input:
            response="💼 Placement cell conducts training sessions regularly."
        else:
            response="🤖 Please use options below."

    return render_template("index.html",response=response,user_input=user_input)

@app.route("/complaint", methods=["GET","POST"])
def complaint():
    msg=""
    if request.method=="POST":
        text=request.form.get("complaint","")

        if text.strip()!="":
            conn=get_db()
            c=conn.cursor()
            c.execute("INSERT INTO complaints (text) VALUES (?)",(text,))
            conn.commit()
            conn.close()
            msg="✅ Complaint submitted!"
        else:
            msg="⚠️ Enter something"

    return render_template("complaint.html",msg=msg)

@app.route("/admin")
def admin():
    if "admin" not in session:
        return redirect("/adminlogin")

    conn=get_db()
    c=conn.cursor()
    c.execute("SELECT * FROM complaints")
    data=c.fetchall()
    count=len(data)
    conn.close()

    return render_template("admin.html",data=data,count=count)

@app.route("/delete/<int:id>")
def delete(id):
    conn=get_db()
    c=conn.cursor()
    c.execute("DELETE FROM complaints WHERE id=?",(id,))
    conn.commit()
    conn.close()
    return redirect("/admin")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__=="__main__":
    app.run(debug=True)