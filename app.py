from flask import Flask, render_template, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, func
from flask_login import UserMixin, login_user, LoginManager, logout_user, current_user, login_required
from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, StringField
from wtforms.validators import InputRequired, Length, ValidationError, EqualTo
from flask_bcrypt import Bcrypt
from user_update import get_user, update_user

app = Flask(__name__)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
app.config["SECRET_KEY"] = "thisisasecretkey"
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///database.db"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view="login"

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

class Users(db.Model, UserMixin):
    userID = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False)
    password = Column(String(80), nullable=False)
    balance = Column(Integer)

    def get_id(self):
        return self.userID

class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired()], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired()], render_kw={"placeholder": "Password"})
    submit = SubmitField("Login")

class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired()], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=8)], render_kw={"placeholder": "Password"})
    confirm_password = PasswordField(validators=[InputRequired(), EqualTo('password')], render_kw={"placeholder": "Confirm Password"})
    submit = SubmitField("Register")

    def validate_username(self, username):
        existing_username = Users.query.filter_by(username=username.data).first()

        if existing_username:
            flash("An account with this username already exists.", category='error')
            raise ValidationError("An account with this username already exists.")

class WithdrawButtons(FlaskForm):
    withdraw_1 = SubmitField("Withdraw £1")
    withdraw_2 = SubmitField("Withdraw £2")
    deposit_1 = SubmitField("Deposit £1")
    deposit_2 = SubmitField("Deposit £2")

@app.route('/', methods=['POST', 'GET'])
def home():
    print('yo')
    form = LoginForm()

    empty = False
    if db.session.query(func.count(Users.userID)).scalar() == 0:
        empty = True

    money = db.session.query(func.sum(Users.balance)).scalar()

    if form.validate_on_submit():
        print('valid')
        user = Users.query.filter_by(username=form.username.data).first()
        print(f'{user}')

        if user:

            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                update_user(user.username)
                print("user logged in")
                return redirect(url_for('account', action='welcome'))
            
            else:
                flash("Incorrect Password.", category='error')
            
        else:

            flash("Invalid Username.", category='error')
    print('ho')
    return render_template('home.html', form=form, money=money, empty=empty)

@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = Users(username=form.username.data, password=hashed_password, balance=0)
        db.session.add(new_user)
        db.session.commit()
        flash("Account created successfully.", category="success")
        return redirect(url_for('home'))
    
    if form.confirm_password.data != form.password.data:
        flash("Passwords must match.", category='error')

    return render_template('register.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash("Logged out successfully!", category="success")
    return redirect(url_for('home'))

@app.route('/account/<action>', methods=['POST', 'GET'])
@login_required
def account(action):
    buttons = WithdrawButtons()
    user = Users.query.filter_by(username=current_user.username).first()

    if action == 'w1':
        # code to withdraw 1 from user account
        if user.balance >= 1:
            user.balance -= 1
            db.session.commit()
            # code telling arduino to release 1 pound coin

        else:
            flash("You don't have enough.", category='error')

    elif action == 'w2':
        # code to withdraw 2 from user account
        if user.balance >= 2:
            user.balance -= 2
            db.session.commit()
            # code telling arduino to release 2 pound coin

        else:
            flash("You don't have enough.", category='error')

    # replace with arduino detecting 1 pound coin inserted
    elif action == 'd1':
        # code to deposit 1 to user account
        user.balance += 1
        db.session.commit()

    # replace with arduino detecting 2 pound coin inserted
    elif action == 'd2':
        # code to deposit 2 to user account
        user.balance += 2
        db.session.commit()

    return render_template('account.html', buttons=buttons)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)