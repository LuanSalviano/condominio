from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, current_user, login_required
from models import db, User, Residence, Pet
from forms import LoginForm, RegisterForm, PetForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/condominio'
app.config['SECRET_KEY'] = 'secretkey'

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Invalid credentials')
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    form.residence.choices = [(res.id, res.address) for res in Residence.query.all()]
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data,
                    full_name=form.full_name.data, cpf=form.cpf.data, residence_id=form.residence.data)
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.is_admin:
        users = User.query.all()
        return render_template('admin.html', users=users)
    return redirect(url_for('pets'))

@app.route('/residences')
@login_required
def residences():
    if not current_user.is_admin:
        return redirect(url_for('pets'))
    residences = Residence.query.all()
    return render_template('residences.html', residences=residences)

if __name__ == '__main__':
    app.run(debug=True)
