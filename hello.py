from flask import Flask, render_template, session, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, PasswordField
from wtforms.validators import DataRequired
from datetime import datetime
from flask_moment import Moment
import sys

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

bootstrap = Bootstrap(app)
moment = Moment(app)


class NameForm(FlaskForm):
    name = StringField('Informe o seu nome', validators=[DataRequired()])
    surname = StringField('Informe o seu sobrenome:', validators=[DataRequired()])
    institution = StringField('Informe a sua Insituição de ensino:', validators=[DataRequired()])
    discipline = SelectField(u'Informe a sua disciplina:', choices=[('dswa5', 'DSWA5'), ('dwba4', 'DWBA4'), ('GPSA5', 'Gestão de projetos')])
    submit = SubmitField('Submit')

class LoginForm(FlaskForm):
    username = StringField('Informe o seu usuário', validators=[DataRequired()])
    password = PasswordField('Informe a sua senha:', validators=[DataRequired()])
    submit = SubmitField('Enviar')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Você alterou o seu nome!')
        session['name'] = form.name.data
        session['surname'] = form.surname.data
        session['institution'] = form.institution.data
        session['discipline'] = form.discipline.data
        session['remote_addr'] = request.remote_addr;
        session['host'] = request.host;
        return redirect(url_for('index'))
    
    return render_template('index.html', 
                           form=form, 
                           name=session.get('name'), 
                           surname=session.get('surname'),
                           institution=session.get('institution'),
                           discipline=session.get('discipline'),
                           choices=dict(form.discipline.choices),
                           remote_addr=session.get('remote_addr'),
                           remote_host=session.get('host'),
                           current_time=datetime.utcnow())

@app.route('/loginResponse', methods=['GET'])
def loginResponse():
    return render_template('loginResponse.html', 
                           username=session.get('username'), 
                           password=session.get('password'),
                           remote_addr=session.get('remote_addr'),
                           remote_host=session.get('host'),
                           current_time=datetime.utcnow())

@app.route('/login', methods=['GET', 'POST'])
def login():
    formLogin = LoginForm()    
    if formLogin.validate_on_submit():
        print('Hello world I!', file=sys.stderr);
        session['username'] = formLogin.username.data
        session['password'] = formLogin.password.data
        session['remote_addr'] = request.remote_addr;
        session['host'] = request.host;
        return redirect(url_for('loginResponse'))  
    
    return render_template('login.html', 
                           form=formLogin,                            
                           remote_addr=request.remote_addr,
                           remote_host=request.remote_addr,
                           current_time=datetime.utcnow())

