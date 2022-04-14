from expiring_food_reminder import line_bot_api, db, TODAY
from linebot.models import TextSendMessage, FlexSendMessage
from .model import Food
from datetime import datetime, timedelta
from .flex_food_list import FlexFoodList


class InputFormatError(Exception):
    pass


def handle_other(event):
    line_bot_api.reply_message(
        event.reply_token, TextSendMessage(text="無法處理這則訊息，也許你可以看看詳細說明"))


def handle_time_string(time_string, suffix):
    if '-' in time_string:
        return datetime.strptime(time_string, '%Y-%m-%d')
    if suffix == 'day':
        return TODAY + \
            timedelta(days=int(time_string))
    if suffix == 'month':
        return TODAY + \
            timedelta(days=int(time_string) * 30)
    if suffix == 'year':
        return TODAY + \
            timedelta(days=int(time_string) * 365)
    raise InputFormatError('格式錯誤')


def handle_add(event):
    if event.message.text.count(' ') + 1 == 3:
        _, food_name, time_string = event.message.text.split(' ')
        expiry_time = handle_time_string(time_string, None)
    else:
        _, food_name, time_string, suffix = event.message.text.split(' ')
        expiry_time = handle_time_string(time_string, suffix)

    food = Food(food_name=food_name, owner_id=event.source.user_id,
                expiry_time=expiry_time)
    db.session.add(food)
    db.session.commit()

    line_bot_api.reply_message(
        event.reply_token, TextSendMessage(text="加入成功"))


def handle_read(event):
    read_method = event.message.text.split(' ')[1]
    foods = Food.query.filter_by(owner_id=event.source.user_id)
    if read_method == 'count':
        line_bot_api.reply_message(event.reply_token, TextSendMessage(
            text=str(foods.count())))
        return

    if read_method == 'all':
        food_list = foods.all()
    elif read_method == 'expiring':
        food_list = foods.filter(
            Food.expiry_time == TODAY).all()
    elif read_method == 'expired':
        food_list = foods.filter(
            Food.expiry_time < TODAY).all()
    else:
        raise InputFormatError('格式錯誤')

    result = FlexFoodList('查詢結果')
    for food in food_list:
        result.append_food(food)
    line_bot_api.reply_message(
        event.reply_token, FlexSendMessage(alt_text='查詢結果...', contents=result.message))


def handle_edit(event):
    if event.message.text.count(' ') + 1 == 4:
        _, id, food_name, time_string = event.message.text.split(' ')
        expiry_time = handle_time_string(time_string, None)
    else:
        _, id, food_name, time_string, suffix = event.message.text.split(' ')
        expiry_time = handle_time_string(time_string, suffix)
    food = Food.query.filter_by(id=id).first()
    if not food or food.owner_id != event.source.user_id:
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text="修改失敗"))
        return
    food.food_name = food_name
    food.expiry_time = expiry_time
    db.session.add(food)
    db.session.commit()
    line_bot_api.reply_message(
        event.reply_token, TextSendMessage(text="修改成功"))


def handle_delete(event):
    delete_method = event.message.text.split(' ')[1]
    if delete_method.isdigit():
        id = int(delete_method)
        food = Food.query.filter_by(id=id).first()
        if not food or food.owner_id != event.source.user_id:
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text="刪除失敗"))
        else:
            db.session.delete(food)
            db.session.commit()
            line_bot_api.reply_message(
                event.reply_token, TextSendMessage(text="刪除成功"))
        return

    foods = Food.query.filter_by(owner_id=event.source.user_id)
    if delete_method == 'all':
        food_list = foods
    elif delete_method == 'expiring':
        food_list = foods.filter(
            Food.expiry_time == TODAY)
    elif delete_method == 'expired':
        food_list = foods.filter(
            Food.expiry_time < TODAY)
    else:
        raise InputFormatError('格式錯誤')
    food_list.delete()
    db.session.commit()
    line_bot_api.reply_message(
        event.reply_token, TextSendMessage(text="刪除成功"))
