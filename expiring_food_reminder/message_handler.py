from expiring_food_reminder import line_bot_api, handler, db
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
                expiry_time = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + \
                    timedelta(days=int(time_string))
            elif suffix == 'month':
                expiry_time = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + \
                    timedelta(days=int(time_string) * 30)
            elif suffix == 'year':
                expiry_time = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + \
                    timedelta(days=int(time_string) * 365)
            else:
                raise InputFormatError('The format of time is wrong!')
        except:
            raise InputFormatError('The format of time is wrong!')

    food = Food(food_name=food_name, owner_id=event.source.user_id,
                expiry_time=expiry_time)
    db.session.add(food)
    db.session.commit()


def handle_read(event):
    pass


def handle_edit(event):
    pass


def handle_delete(event):
    pass
