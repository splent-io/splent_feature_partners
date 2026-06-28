from flask_wtf import FlaskForm
from wtforms import SubmitField


class SplentFeaturePartnersForm(FlaskForm):
    submit = SubmitField("Save splent_feature_partners")
