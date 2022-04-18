from expiring_food_reminder import db, line_bot_api
from .model import Food
from .form import FormAddFood
from .flex_food_list import FlexFoodList
from flask import current_app, flash, redirect, render_template, request, url_for
from datetime import datetime
from . import main
from linebot.models import FlexSendMessage


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/add', methods=['GET', 'POST'])
def add():
    form = FormAddFood()
    if form.validate_on_submit():
        food = Food(food_name=form.food_name.data, owner_id=form.user_id.data,
                    expiry_time=form.expiry_time.data)
        db.session.add(food)
        db.session.commit()
        flash('新增成功')
        redirect(url_for('main.add'))
    return render_template('add.html', form=form)


@main.route("/daily_work", methods=['POST'])
def daily_work():
    if request.values.get('password') != current_app.config.get('DAILY_WORK_PASSWORD'):
        return 'Failed!'

    TODAY = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    food_list = Food.query.filter_by(
        expiry_time=TODAY).order_by('owner_id').all()

    result = FlexFoodList('今天到期的食物')
    for i in range(len(food_list)):
        result.append_food(food_list[i])
        if i == len(food_list) - 1 or food_list[i].owner_id != food_list[i + 1].owner_id:
            line_bot_api.push_message(
                food_list[i].owner_id, FlexSendMessage(alt_text='今天到期的食物...', contents=result.message))
            result.reset()
    current_app.logger.info('Daily work finished!')
    return 'Success!'

