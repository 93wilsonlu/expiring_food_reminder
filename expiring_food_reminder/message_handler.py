from expiring_food_reminder import line_bot_api, handler, db
from linebot.models import TextSendMessage


class InputFormatError(Exception):
    pass


def handle_other(event):
    line_bot_api.reply_message(
        event.reply_token, TextSendMessage(text="無法處理這則訊息，也許你可以看看詳細說明"))


def handle_add(event):
    pass

def handle_read(event):
    pass


def handle_edit(event):
    pass


def handle_delete(event):
    pass
