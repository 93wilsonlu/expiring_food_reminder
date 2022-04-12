from expiring_food_reminder import line_bot_api, db, TODAY
from linebot.models import TextSendMessage
from .model import Food
from datetime import datetime, timedelta


class InputFormatError(Exception):
    pass


def handle_other(event):
    line_bot_api.reply_message(
        event.reply_token, TextSendMessage(text="無法處理這則訊息，也許你可以看看詳細說明"))


def handle_add(event):
    food_name = event.message.text.split(' ')[1]
    time_string = event.message.text.split(' ')[2]
    if '-' in time_string:
        expiry_time = datetime.strptime(time_string, '%Y-%m-%d')
    else:
        try:
            suffix = event.message.text.split(' ')[3]
            if suffix == 'day':
                expiry_time = TODAY + \
                    timedelta(days=int(time_string))
            elif suffix == 'month':
                expiry_time = TODAY + \
                    timedelta(days=int(time_string) * 30)
            elif suffix == 'year':
                expiry_time = TODAY + \
                    timedelta(days=int(time_string) * 365)
            else:
                raise InputFormatError('格式錯誤')
        except:
            raise InputFormatError('格式錯誤')

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

    result = '以下是查詢結果:'
    for food in food_list:
        result += f"\n{food.id} {food.food_name} {food.expiry_time.strftime('%Y-%m-%d')}"
    line_bot_api.reply_message(
        event.reply_token, TextSendMessage(text=result))


def handle_edit(event):
    pass


def handle_delete(event):
    pass
