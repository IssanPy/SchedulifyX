import os
from datetime import datetime
from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY','dev-secret')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR,'booking.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(140))

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    email = db.Column(db.String(120))
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'))
    scheduled_for = db.Column(db.DateTime)
    status = db.Column(db.String(40), default='pending')

class BookingForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    service = SelectField('Service', coerce=int)
    scheduled_for = StringField('DateTime (YYYY-MM-DD HH:MM)', validators=[DataRequired()])
    notes = TextAreaField('Notes')
    submit = SubmitField('Book')

@app.route('/')
def index():
    services = Service.query.all()
    return render_template('index.html', services=services)

@app.route('/book/<int:service_id>', methods=['GET','POST'])
def book(service_id):
    s = Service.query.get_or_404(service_id)
    form = BookingForm()
    form.service.choices = [(s.id, s.title)]
    if form.validate_on_submit():
        try:
            dt = datetime.strptime(form.scheduled_for.data.strip(), '%Y-%m-%d %H:%M')
        except Exception:
            flash('Invalid datetime format', 'danger')
            return render_template('book.html', form=form, service=s)
        appt = Appointment(name=form.name.data, email=form.email.data, service_id=s.id, scheduled_for=dt)
        db.session.add(appt)
        db.session.commit()
        flash('Booked — awaiting confirmation', 'success')
        return redirect(url_for('index'))
    return render_template('book.html', form=form, service=s)

@app.cli.command('seed')
def seed():
    if Service.query.count() == 0:
        db.session.add_all([Service(title='Consultation'), Service(title='1-on-1 Session')])
        db.session.commit()
        print('seeded')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
