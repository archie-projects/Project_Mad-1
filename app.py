from flask import Flask, request, render_template, redirect, url_for
from flask_login import login_user, logout_user, current_user
from database import *
from flask_login import LoginManager, UserMixin, login_required



app = Flask(__name__)
app.secret_key = 'EvilMateInOne'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
db.init_app(app)

with app.app_context():
    db.create_all()

# User login route
@app.route("/")
def login():
    return render_template("login.html")

# User registration route
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        phone_no = request.form.get("phone_no")
        address = request.form.get("address")
        pincode = request.form.get("pincode")
        vehicle_no = request.form.get("vehicle_no")
        password = request.form["password"]
        if not username or not password or not email:
            return "Username, password, and email are required", 400
        if User.query.filter_by(username=username).first():
            return "Username already exists", 400
        new_user = User(username=username, password=password, email=email,phone_no=phone_no,
                        address=address, pincode=pincode, vehicle_no=vehicle_no)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("register.html")

# User login validation
@app.route("/login", methods=["POST"])
def user_login():
    username = request.form["username"]
    password = request.form["password"]
    user = User.query.filter_by(username=username, password=password).first()
    if user:
        login_user(user)
        return redirect(url_for("dashboard"))
    return "Invalid username or password", 401

# User loading
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# User dashboard route
@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", user=current_user)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

# User profile updation route
@app.route("/update_profile", methods=["POST"])
@login_required
def profile():
    return render_template("profile.html", user=current_user)

# User Search for parking spots 
@app.route("/search", methods=["GET"])
@login_required
def search():
    return render_template("user_search_parking.html", user=current_user)


#
@app.route("/logout", methods=["GET"])
@login_required
def logout():
    return render_template("logout.html", user=current_user)

