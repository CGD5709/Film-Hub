from flask_wtf import FlaskForm
from wtforms import SubmitField


class FilmdatasetForm(FlaskForm):
    submit = SubmitField('Save filmdataset')
