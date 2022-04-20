from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, DateField, HiddenField, SubmitField, validators, ValidationError
from .model import Food

class FormAddFood(FlaskForm):
    food_name = StringField('食物名', validators=[
        validators.DataRequired(),
        validators.Length(1, 20)
    ])
    expiry_time = DateField('到期日')
    user_id = HiddenField('使用者 ID')

    submit = SubmitField('完成')


class FormEditFood(FlaskForm):
    id = IntegerField('id')
    food_name = StringField('食物名', validators=[
        validators.DataRequired(),
        validators.Length(1, 20)
    ])
    expiry_time = DateField('到期日')
    user_id = HiddenField('使用者 ID')

    submit = SubmitField('完成')
