from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask import Flask, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from dl_songs import download_mp3
import re
import os

app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
bootstrap = Bootstrap(app)


class NameForm(FlaskForm):
    name = StringField('Enter URL(s) here..',
                       validators=[DataRequired()])
    submit = SubmitField('Download')


@app.route('/', methods=['GET', 'POST'])
def index():
    regex = re.compile(r'https:\/\/www.youtube.com/watch\?v=[aA-zZ0-9_=\-&]+', re.IGNORECASE)
    form = NameForm()
    name = None
    if form.validate_on_submit():
        name = form.name.data
        url_list = name.split(',')
        if url_list and all([bool(regex.match(ur)) for ur in url_list]):
            download_mp3(url_list)
            flash('You have completed download successfully!')
        else:
            flash("You didn't enter a valid youtube url. Please try again!")
        return redirect(url_for('index'))
    return render_template('index_form.html', form=form, name=name)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 505

if __name__ == '__main__':
    app.run()
