import flask
from flask import Flask,render_template,redirect,request,session
from flask_session import Session
import sqlite3

con = sqlite3.connect("bookmanagement.db",check_same_thread=False)
cursor = con.cursor()

listOfTables = con.execute("SELECT name from sqlite_master WHERE type='table' AND name='BOOKSELF' ").fetchall()
listOfTables1 = con.execute("SELECT name from sqlite_master WHERE type='table' AND name='USER'").fetchall()

if listOfTables!=[]:
    print("Table Already Exists ! ")

else:
    con.execute('''CREATE TABLE BOOKSELF(
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                bookname TEXT,author TEXT,category TEXT,
                price INTEGER,publisher TEXT);  ''')

print("Table has Created")

if listOfTables1!=[]:
    print("Table Already Exists !")

else:
    con.execute(''' CREATE TABLE USER(
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                 name TEXT,address TEXT,email TEXT,
                 mobileno TEXT,password TEXT);''')


app = Flask(__name__)
app.config["SESSION_PERMANENT"]=False
app.config["SESSION_TYPE"]="filesystem"
Session(app)
@app.route("/")
def hello():

    return render_template("/index.html")



@app.route("/adminlogin",methods=['GET','POST'])
def adminlogin():
    if request.method == 'POST':
        getname = request.form["name"]
        getpass = request.form["pass"]

    try:
        if getname =='admin' and getpass=='1234':
            return redirect("/bookentry")
        else:
            print("Invalid username and password")
    except Exception as e:
        print(e)
    return render_template("/adminlogin.html")


@app.route("/userlogin", methods=['GET','POST'])
def userlogin():
    if request.method == 'POST':
        getemail = request.form['email']
        getpass = request.form['pass']
        print(getemail)
        print(getpass)

    try:
        querry= "SELECT * FROM USER WHERE email='"+getemail+"' AND password='"+getpass+"'"
        cursor.execute(querry)
        result= cursor.fetchall()
        print(result)
        if len(result)>0:
            for i in result:
                getname =i[1]
                getid = i[0]

            session["name"] = getname
            session["id"] = getid

            return redirect("/dashboard")
    except Exception as e:
        print(e)

    return render_template("/userlogin.html")
@app.route("/dashboard",methods =['GET','POST'])
def dashboard():
    if not session.get("name"):
        return redirect("/userlogin")
    else:
        return render_template("/dashboard.html")


@app.route("/register",methods=['GET','POST'])
def register():

    if request.method == 'POST':
        getname = request.form['name']
        getaddress = request.form['address']
        getemail = request.form['email']
        getmobilno = request.form['mobileno']
        getpass = request.form['pass']

        print(getname)
        print(getaddress)
        print(getemail)
        print(getmobilno)
        print(getpass)

    try:
        querry = cursor.execute("INSERT INTO USER(name,address,email,mobileno,password) VALUES('"+getname+"','"+getaddress+"','"+getemail+"',"+getmobilno+",'"+getpass+"')")
        print(querry)
        con.commit()
        return redirect("/userlogin")
    except Exception as e:
        print(e)

    return render_template("/register.html")

@app.route("/bookentry",methods = ['GET','POST'])
def Addbook():
    if request.method == 'POST':
        getname = request.form['bookname']
        getauthor = request.form['author']
        getcategory = request.form['category']
        getprice = request.form['price']
        getpublisher = request.form['publisher']

        print(getname)
        print(getauthor)
        print(getcategory)
        print(getprice)
        print(getpublisher)

        try:
            query = cursor.execute("INSERT INTO BOOKSELF(bookname,author,category,price,publisher)VALUES('" + getname + "','" + getauthor + "','" + getcategory + "','" + getprice + "','" + getpublisher + "')")
            print(query)
            print("SUCCESSFULLY INSERTED ")
            con.commit()
            return redirect("/viewall")
        except Exception as e:
            print(e)

    return render_template("bookentry.html")



@app.route("/search",methods=['GET','POST'])
def search():
    if request.method == "POST":
        getname = request.form["name"]
        print(getname)
        try:
            query = "SELECT * FROM BOOKSELF WHERE bookname='" + getname + "'"
            print(query)
            cursor.execute(query)
            print("SUCCESSFULLY SELECTED!")
            result = cursor.fetchall()
            print(result)
            if len(result) == 0:
                print("Invalid Book Name")
            else:
                return render_template("search.html", book=result, status=True)
        except Exception as e:
            print(e)

    return render_template("search.html",book=[],status=False)

@app.route("/usersearch",methods=['GET','POST'])
def usersearch():
    if not session.get("name"):
        return redirect("/userlogin")
    else:
        if request.method == "POST":
            getname = request.form["name"]
            print(getname)
            try:
                querry = "SELECT * FROM BOOKSELF WHERE bookname='" + getname + "'"
                print(querry)
                cursor.execute(querry)
                print("SUCCESSFULLY SELECTED!")
                result = cursor.fetchall()
                print(result)
                if len(result) == 0:
                    print("Invalid Book Name")
                else:
                    return render_template("usersearch.html", books=result, status=True)

            except Exception as e:
                print(e)
        return render_template("usersearch.html", books=[], status = False)

@app.route("/viewall")
def viewall():
    cursor=con.cursor()
    cursor.execute("SELECT * FROM BOOKSELF")
    result=cursor.fetchall()
    return render_template("viewall.html",books=result)

@app.route("/delete",methods =['GET','POST'])
def delete():
    if request.method == "POST":
        getname = request.form['bookname']
        print(getname)
        try:
            con.execute("DELETE FROM BOOKSELF WHERE bookname='" + getname + "'")
            print("SUCCESSFULLY DELETED!")
            con.commit()
            return redirect("/viewall")
        except Exception as e:
            print(e)
    return flask.render_template("delete.html")



@app.route("/update",methods =['GET','POST'])
def update():
    if request.method == "POST":
        getname = request.form["bookname"]
        print(getname)
        try:
            query = "SELECT * FROM BOOKSELF WHERE bookname='" + getname + "'"
            cursor.execute(query)
            print("SUCCESSFULLY SELECTED!")
            result = cursor.fetchall()
            print(result)
            if len(result) == 0:
                print("Invalid Book Name")
            else:
                return redirect("/Viewupdate")

        except Exception as e:
            print(e)


    return render_template("update.html")

@app.route("/Viewupdate")
def viewupdate():
    if request.method=='POST':
        getname = request.form['bookname']
        getauthor = request.form['author']
        getcategory = request.form['category']
        getprice = request.form['price']
        getpublisher = request.form['publisher']

    try:
        querry=("UPDATE BOOKSELF SET bookname= '" + getname + "',author='" + getauthor + "',category='" + getcategory + "',price='" + getprice + "',publisher='" + getpublisher + "'WHERE name='" + getname + "'")
        print(querry)
        con.commit()

        return redirect("/viewall")

    except Exception as e:
        print(e)

    return render_template("Viewupdate.html")

@app.route("/userviewall")
def userviewall():
    if not session.get("name"):
        return redirect("/userlogin")
    else:
        cursor = con.cursor()
        cursor.execute("SELECT * FROM BOOKSELF")
        result=cursor.fetchall()
        return render_template("userviewall.html",books=result)

@app.route("/userlogout",methods=["GET","POST"])
def userlogout():

    if not session.get("name"):
        return redirect("/userlogin")
    else:
        session["name"]=None
        return redirect("/")

@app.route("/adminlogout",methods=['GET','POST'])
def adminlogout():
    if not session.get("name"):
        return redirect("/")
    else:
        session["name"]=None
        return redirect("/adminlogin")

if (__name__) =="__main__":
    app.run(debug=True)