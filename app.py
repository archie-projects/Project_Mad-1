from flask import Flask, request, render_template, redirect, url_for, session
from flask_login import login_user, logout_user, current_user
from database import *
from flask_login import LoginManager,login_required


app = Flask(__name__)
app.secret_key = 'EvilMateInOne'


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
db.init_app(app)

with app.app_context():
    db.create_all()

# Helper function to check if current user is admin
def is_admin():
    return session.get('user_type') == 'admin'



# User login route
@app.route("/",methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            login_user(user)
            session['user_type'] = 'user'  # Set user type in session
            return redirect(url_for("dashboard"))
        else:
            return "Invalid username or password", 401
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
            return f'''
              Username "{username}" already exists.<br>
              Please <a href="{url_for('login')}">sign in</a> if this is your account, 
              or <a href="{url_for('register')}">pick another username</a>.
          ''', 400

        new_user = User(username=username, password=password, email=email,phone_no=phone_no,
                        address=address, pincode=pincode, vehicle_no=vehicle_no)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("user_registration.html")


# User loading
@login_manager.user_loader
def load_user(user_id):
    # First try to load as User
    user = User.query.get(int(user_id))
    if user:
        return user
    # If not found, try to load as Admin
    admin = Admin.query.get(int(user_id))
    return admin


# User dashboard route
@app.route("/dashboard",methods=["GET", "POST"])
@login_required
def dashboard():
    # Redirect admin to admin dashboard if they access user dashboard
    if is_admin():
        return redirect(url_for("admin_dashboard"))
    return render_template("user_dashboard.html", user=current_user)



# User profile updation route
@app.route("/update_profile", methods=["POST", "GET"])
@login_required
def profile():
    if is_admin():
        return redirect(url_for("admin_dashboard"))
    return render_template("user_edit_profile.html", user=current_user)

# User Search for parking spots 
@app.route("/search", methods=["GET", "POST"])
@login_required
def search_parking():
    if is_admin():
        return redirect(url_for("admin_dashboard"))
    return render_template("user_search_parking.html", user=current_user)

@app.route("/summary", methods=["GET", "POST"])
@login_required
def summary():
    if is_admin():
        return redirect(url_for("admin_dashboard"))
    return render_template("user_summary.html", user=current_user)


@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    if request.method == "POST":
        logout_user()
        session.pop('user_type', None)  # Clear user type from session
        return redirect(url_for("login"))
    return render_template("user_logout.html", user=current_user)

@app.route("/auth/google")
def auth_google():
    # Placeholder for Google authentication logic
    return "Google authentication not implemented yet", 501

@app.route("/forgotPassword")
def forgot_password():
    # Placeholder for forgot password logic
    return "Forgot password functionality not implemented yet", 501


@app.route("/auth/github")
def auth_github():
    # Placeholder for GitHub authentication logic
    return "GitHub authentication not implemented yet", 501



@app.route("/admin",methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        admin = Admin.query.filter_by(username=username, password=password).first()
        if admin:
            login_user(admin)
            session['user_type'] = 'admin'  # Set user type as admin in session
            return redirect(url_for("admin_dashboard"))
        else:
            return "Invalid admin credentials", 401
    return render_template("admin_login.html")

@app.route("/admin/dashboard", methods=["GET", "POST"])
@login_required
def admin_dashboard():
    return render_template("admin_dashboard.html", user=current_user)

@app.route("/admin/logout", methods=["GET", "POST"])
@login_required
def admin_logout():
    if request.method == "POST":
        logout_user()
        session.pop('user_type', None)  # Clear user type from session
        return redirect(url_for("admin_login"))  # Redirect to admin login, not admin
    return render_template("admin_logout.html", user=current_user)

@app.route("/admin/add_parking_lot", methods=["GET", "POST"])
@login_required
def admin_add_lot():
    return render_template("admin_add_lot.html", user=current_user)


@app.route("/admin/users")
@login_required
def admin_users():
    users = User.query.all()
    return render_template("admin_users.html", users=users, user=current_user)

@app.route("/admin/search")
@login_required
def admin_search():
    return render_template("admin_search.html", user=current_user)

@app.route("/admin/summary")
@login_required
def admin_summary():
    return render_template("admin_summary.html", user=current_user)

@app.route("/admin/add_lot")
@login_required
def add_lot():
    return render_template("admin_add_parking_lot.html", user=current_user)



if __name__ == "__main__":
    app.run(debug=True)
# This is the main entry point for the Flask application.
