from flask import Flask,url_for,render_template,request,session, redirect,flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, abort,reqparse,marshal_with,fields
from datetime import datetime
import hashlib




app = Flask(__name__)
app.config["SECRET_KEY"]="5=dcw!p+w*&!y#is_i!#*+2=t9*(^_7#g)2l-09rh=(v7#)c)d"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:@localhost/adminsitedb"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.permanent_session_lifetime= timedelta(minutes=7)

db = SQLAlchemy(app)

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(50))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))
    date_register = db.Column(db.DateTime, nullable = True)
    is_admin = db.Column(db.Integer, default = 0)

    def __init__(self, username, email, password,is_admin,date_register):
        self.username = username
        self.email = email
        self.password = password
        self.date_register = date_register
        self.is_admin = is_admin


@app.route("/")
def index():
    if "dangnhapthanhcong" in session:
        return redirect(url_for("mainpage", username = session['username']))
    else:
        return redirect(url_for('login', alert = " "))

@app.route("/admin/<username>/", methods=["GET","POST"])
def mainpage(username):
    session["tranghientai"] = "mainpage"
    if "dangnhapthanhcong" in session:
        return render_template("index.html", username_login = username)
    else:
        return redirect(url_for('login', alert = "session_expired"))


@app.route("/login/<alert>", methods=['GET','POST'])
def login(alert):
    if request.method == "POST":
        get_email = request.form['EmailInputField']
        get_password = request.form['PasswordInputField']
        if get_email and get_password:
            find_user = User.query.filter_by(email=get_email).first()
            if find_user:
                if hashlib.md5(get_password.encode()).hexdigest() == find_user.password:
                    if find_user.is_admin == 1:
                        session['dangnhapthanhcong'] = 'OK'
                        session['username'] = find_user.username
                        session['email'] = find_user.email
                        session['password'] = get_password
                        # return render_template('index.html', username_login = find_user.username)
                        return redirect(url_for("mainpage", username = session['username']))
                    else:
                        return render_template("signin.html", error = "user_is_not_admin")
                else:
                    return render_template("signin.html", error = "not_found_user")
            else:
                return render_template("signin.html", error = "not_found_user")
    return render_template("signin.html", show_alert = alert)

@app.route("/register/", methods=['GET', "POST"])
def register():
    if request.method == "POST":
        get_username_register = request.form["UsernameInputFieldRegister"]
        get_email_register = request.form["EmailInputFieldRegister"]
        get_password_register = request.form["PasswordInputFieldRegister"]
        get_confirm_password_register = request.form["ConfirmPasswordInputFieldRegister"]
        user_already_check = User.query.filter_by(email=get_email_register).first()
        if user_already_check:
            return render_template("signup.html", error = "email_already_used")
        else:
            if get_password_register != get_confirm_password_register:
                return render_template("signup.html", error = "password_wrong")
            else:
                new_user = User(get_username_register,get_email_register,hashlib.md5(get_password_register.encode()).hexdigest(),0,date_register=datetime.now())
                db.session.add(new_user)
                db.session.commit()
                return redirect(url_for("login", alert = "register_done"))
    return render_template("signup.html")

@app.route("/logout/", methods=["GET","POST"])
def logout():
    session.pop("dangnhapthanhcong", None)
    session.pop("username", None)
    return redirect(url_for('login', alert = " "))

@app.route("/admin/profile/", methods=["GET","POST"])
def profile():
    session["tranghientai"] = "profile"
    if "dangnhapthanhcong" in session:
        email = session['email'] 
        password = session['password'] 
        username = session["username"]
        context = [email,password]
        if request.method == "POST":
            get_username_modify = request.form["UsernameModify"]
            get_email_modify = request.form['EmailModify']
            get_password_modify = request.form["PasswordModify"]
            get_confirm_password_modify = request.form["ConfirmPasswordModify"]
            # Check email
            if get_email_modify != email:
                user_already_check = User.query.filter_by(email=get_email_modify).first()
                # check xem đã tồn tại user có email bằng email_modify hay chưa?
                if user_already_check:
                    return render_template("profile.html", context = context, alert = "email da ton tai", username_login = session['username'])
                else:
                    user_modify = User.query.filter_by(email=email).first()
                    user_modify.email = get_email_modify
                    user_modify.username = get_username_modify
                    if password != get_password_modify:
                        if get_password_modify == get_confirm_password_modify:
                            user_modify.password = hashlib.md5(get_password_modify.encode()).hexdigest()
                        else:
                            return render_template("profile.html", context = context, alert = "matkhau va xacnhanmatkhau khong chinh xac", username_login = session['username'])
                    session["username"] = get_username_modify
                    session["email"] = get_email_modify
                    session['password'] = get_password_modify
                    db.session.commit()
                    return redirect(url_for("profile"))
            # Check username
            if get_username_modify != username:
                user_modify = User.query.filter_by(username=username, email = email).first()
                if get_password_modify == get_confirm_password_modify:
                    user_modify.password = hashlib.md5(get_password_modify.encode()).hexdigest()
                    session['password'] = get_password_modify
                else:
                    return render_template("profile.html", context = context, alert = "matkhau va xacnhanmatkhau khong chinh xac", username_login = session['username'])
                user_modify.username = get_username_modify
                session["username"] = get_username_modify
                db.session.commit()
                return redirect(url_for("profile"))
            if password != get_password_modify:
                user_modify = User.query.filter_by(email=email).first()
                if get_password_modify == get_confirm_password_modify:
                    user_modify.password = hashlib.md5(get_password_modify.encode()).hexdigest()
                    session['password'] = get_password_modify
                    db.session.commit()
                    return redirect(url_for("profile"))
                else:
                    return render_template("profile.html", context = context, alert = "matkhau va xacnhanmatkhau khong chinh xac", username_login = session['username'])
        return render_template("profile.html", context = context, username_login = session["username"] )
    else:
        return redirect(url_for('login', alert = "session_expired"))


@app.route("/admin/createAcc/", methods=["GET", "POST"])
def createAcc():
    session["tranghientai"] = "createAcc"
    if "dangnhapthanhcong" in session:
        if request.method == "POST":
            createUsernameInput = request.form['CreateUsernameInput']
            createEmailInput = request.form['CreateEmailInput']
            createPasswordInput1 = request.form['CreatePasswordInput1']
            createPasswordInput2 = request.form['CreatePasswordInput2']
            createSwitchAdmin = request.form.get('SwitchAdmin')
            user_check_exist = User.query.filter_by(email = createEmailInput).first()
            if createUsernameInput and createEmailInput and createPasswordInput1 and createPasswordInput2:
                if user_check_exist:
                    return render_template("createAcc.html", alert = "Email đã tồn tại",username_login = session["username"])
                else:
                    if createPasswordInput1 == createPasswordInput2:
                        if createSwitchAdmin == "checked":
                            new_user = User(createUsernameInput,createEmailInput,hashlib.md5(createPasswordInput1.encode()).hexdigest(),1,date_register=datetime.now())
                            db.session.add(new_user)
                            db.session.commit()
                        else:
                            new_user = User(createUsernameInput,createEmailInput,hashlib.md5(createPasswordInput1.encode()).hexdigest(),0,date_register=datetime.now())
                            db.session.add(new_user)
                            db.session.commit()
                        return render_template("createAcc.html", alert = "Tạo tài khoản thành công",username_login = session["username"])
                    else:
                        return render_template("createAcc.html", alert = "Mật khẩu và xác nhận mật khẩu không chính xác",username_login = session["username"])
            else:
                return render_template("createAcc.html", alert = "Thông tin chưa nhập đủ",username_login = session["username"])
        return render_template("createAcc.html",username_login = session["username"])
    else:
        return redirect(url_for('login', alert = "session_expired"))

@app.route("/admin/showAcc/", methods=["GET","POST"])
def showAcc():
    session["tranghientai"] = "showAcc"
    if "dangnhapthanhcong" in session:
        return render_template("showAcc.html", username_login = session["username"])
    else:
        return redirect(url_for("login", alert = "session_expired"))
# API 
api = Api(app=app)

resourse_fields = {
    "user_id": fields.Integer,
    "username": fields.String,
    "email": fields.String,
    "is_admin": fields.Integer,
}

class GetAllUser(Resource):
    @marshal_with(resourse_fields)
    def get(self):
        users = User.query.all()         
        return users, 200


api.add_resource(GetAllUser, "/api/getallusers")


if __name__ == "__main__":
    app.run(debug=True, host='localhost', port=8000)