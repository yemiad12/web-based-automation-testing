from datetime import datetime, date
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.choices import SelectField
from wtforms.fields.datetime import DateField
from wtforms.validators import DataRequired, url
from flask import Flask, abort, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap5
# from dotenv import load_dotenv  # Install: pip install python-dotenv
import os
from flask import Flask, render_template, request
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
# from sqlalchemy import Integer, String, Boolean, DateTime, func

from test_script import *

# load_dotenv()  # Load the .env file

SECRET_KEY = os.environ.get("SECRET_KEY")

API_KEY = os.environ.get("API_KEY")

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
Bootstrap5(app)

#
# # CREATE DB
# class Base(DeclarativeBase):
#     pass
#
# database_url = os.environ.get("DATABASE_URL")
#
# # Connect to Database
# app.config['SQLALCHEMY_DATABASE_URI'] =f"{database_url}"
# db = SQLAlchemy(model_class=Base)
# db.init_app(app)
#
# class Todo(db.Model):
#     # __tablename__ = "todos"
#     id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     task: Mapped[str] = mapped_column(String(250),  nullable=False)
#     created_date: Mapped[datetime] = mapped_column(
#         DateTime(timezone=True), server_default=func.now()
#     )
#     status: Mapped[str] = mapped_column(String(10), nullable=False)


test_options = [('seller creates p2p', 'seller creates p2p'),('buyer creates p2p', 'buyer creates p2p'),('end to end', 'end to end')]
class TestForm(FlaskForm):
    scope = SelectField('Test Scope', validators=[DataRequired()], choices=test_options)
    submit = SubmitField('Submit')


# with app.app_context():
#     db.create_all()


class FlaskForm:
    pass

selected_scope=""

@app.route("/")
def home():
    return render_template("index.html")


@app.route('/scope', methods=['GET', 'POST'])
def scope():
    global selected_scope
    form = TestForm(formdata=request.form)
    if form.validate_on_submit():
        print("True")
        print(form.errors)
        selected_scope = form.scope.data

        return redirect('/test')

    return render_template('select_scope.html', form=form)



@app.route('/test')
def test():
    global selected_scope
    test_script(selected_scope)
    print(selected_scope)


    return render_template('success.html', todos=f'You have successfully tested "{selected_scope}"')


if __name__ == '__main__':
    app.run(debug=False)
