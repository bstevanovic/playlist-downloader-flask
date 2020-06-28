from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from dl_songs import download_mp3
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
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


if __name__ == '__main__':
    app.run()
