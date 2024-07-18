from flask import Flask,render_template,redirect,session,request,url_for
from flask.helpers import total_seconds
from flaskext.mysql import MySQL
from pymysql import NULL
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
coordinates = []


app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'dementia'

mysql=MySQL(app)
mysql.init_app(app)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register',methods=["GET","POST"])
def register():
    if request.method=='GET':
        return render_template("register.html")
    else:
        # fname=request.form['first_name']
        # lname=request.form['last_name']
        email=request.form['email']
        # password=request.form['password']
        gender=request.form['gender']
        dob=request.form['birthday']
        username=request.form['username']
        contact=request.form['phone']


        conn=mysql.connect()
        cur=conn.cursor()
        
        cur.execute("INSERT INTO patients VALUES (%s,%s,%s,%s,%s)",(email, username, gender, contact, dob))
        # cur.execute("INSERT INTO leaderboard(username) VALUES (%s)",(username))
    
        conn.commit()
        cur.close()
        # session['fname']=request.form['first_name']
        # session['email']=request.form['email']
        return redirect(url_for('login'))

@app.route('/caretakerlogin',methods=["GET","POST"])
def caretakerlogin():
    if request.method=='POST':
        email=request.form['email']
        password=request.form['password']

        if email == "caretaker@admin.com" and password=="password":
            session['caretaker']=1
            return redirect(url_for('caretakerportal'))
        else:
            return "Error in password or email mismatch"
    else:
        return render_template('caretakerlogin.html')

@app.route('/caretakerportal',methods=["GET","POST"])
def caretakerportal():
    # total_Q=numQues()
    pass

@app.route('/login',methods=["GET","POST"])
def login():
    if request.method=='POST':
        email=request.form['email']
        password=request.form['password']

        cur=mysql.connect().cursor()
        cur.execute("select * from patients where email='"+email+"' ")
        user=cur.fetchone()
        
        cur.close()
        # print("hey")
        #if user > 0:
        if password == user[3]:
            print("hello")
            session['name']=user[0]
            session['lname']=user[1]
            session['email']=user[2]
            session['username']=user[6]
            session['user_marks']=0
            session['i']=1

            return render_template("home.html")

        else:
            return "Please enter Correct password again"

        # else:
        #     return "error User not found"
    else:
        return render_template('login.html')

@app.route('/send_coordinates', methods=['POST'])
def send_coordinates():
    data= request.get_json()
    if 'latitude' in data and 'longitude' in data:
        coordinates.append({'latitude': data['latitude'],'longitude': data['longitude']})
        return jsonify({'message': 'Coordinates received', 'data':data}),200
    else :
        return jsonify({'error':'Invalid data'}), 400

@app.route('/get_coordinates', methods=['GET'])
def get_coordinates():
    return jsonify({'coordinates': coordinates}),200


if __name__ =="__main__":
    app.run(debug=True,port=8080,use_reloader=False)