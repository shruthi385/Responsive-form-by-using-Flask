from flask import Flask, render_template,request,flash,redirect,url_for,session
import sqlite3
import os
app2 = Flask(__name__)
app2.secret_key="123"

con=sqlite3.connect("database3.db")
con.execute("create table if not exists students(pid integer primary key,name text,password text,address text,dept text,contact integer,mail text)")
con.close()

picFolder=os.path.join('static','image')
app2.config['UPLOAD_FOLDER']=picFolder



@app2.route('/')
def index():
    ach=os.path.join(app2.config['UPLOAD_FOLDER'],'ach.jpg')
    return render_template('indexes.html',user_image=ach)        


@app2.route('/login',methods=["GET","POST"])
def login():
    if request.method=='POST':
        name=request.form['name']
        password=request.form['password']
        con=sqlite3.connect("database3.db")
        con.row_factory=sqlite3.Row
        cur=con.cursor()
        cur.execute("select * from students where name=? and Password=?",(name,password))
        data=cur.fetchone()

        if data:
            session["name"]=data["name"]
            session["mail"]=data["mail"]
            return redirect("customer")
        else:
            flash("Username and Password Mismatch","danger")
    return redirect(url_for("index"))


@app2.route('/customer',methods=["GET","POST"])
def customer():
     ach=os.path.join(app2.config['UPLOAD_FOLDER'],'ach.jpg')
     return render_template('customers.html',user_image=ach)       
   

@app2.route('/register',methods=["GET","POST"])
def register():
    if request.method=='POST':
        try:
            name=request.form['name']
            password=request.form['password']
            address=request.form['address']
            dept=request.form['dept']
            contact=request.form['contact']
            mail=request.form['mail']
            con=sqlite3.connect("database3.db")
            cur=con.cursor()
            cur.execute("insert into students(name,password,address,dept,contact,mail)values(?,?,?,?,?,?)",(name,password,address,dept,contact,mail))
            con.commit()
            flash("Record Added  Successfully","success")
        except:
            flash("Error in Insert Operation","danger")
        finally:
            return redirect(url_for("index"))
            con.close()
    ach=os.path.join(app2.config['UPLOAD_FOLDER'],'ach.jpg')
    return render_template('registersss.html',user_image=ach)        

    

@app2.route('/logout')
def logout():

    session.clear()
    return redirect(url_for("index"))

if __name__ == '__main__':
    app2.run(debug=True,port=5500)