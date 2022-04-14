from flask import Flask, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, FlexSendMessage
from .config import config_dict
import os
from datetime import datetime
from sqlalchemy import func
from .flex_food_list import FlexFoodList

line_bot_api = LineBotApi(os.environ.get('CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.environ.get('CHANNEL_SECRET'))

db = SQLAlchemy()
migrate = Migrate(compare_type=True)
TODAY = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)


def create_app(config='develop'):
    app = Flask(__name__)
    app.config.from_object(config_dict[config])
    db.init_app(app)
    migrate.init_app(app, db)

    @app.route("/callback", methods=['POST'])
    def callback():
        signature = request.headers['X-Line-Signature']

        body = request.get_data(as_text=True)
        app.logger.info("Request body: " + body)

        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            abort(400)

        return 'OK'

    from expiring_food_reminder.model import Food

    @app.route("/daily_work", methods=['POST'])
    def daily_work():
        if request.values.get('password') != app.config.get('DAILY_WORK_PASSWORD'):
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
        app.logger.info('Daily work finished!')
        return 'Success!'

    from .commands import init_cli
    init_cli(app)

    from .message_handler import handle_add, handle_read, handle_edit, handle_delete, display_help, handle_other

    @handler.add(MessageEvent, message=TextMessage)
    def main_handler(event):
        try:
            action_type = event.message.text.split(' ')[0]
            if action_type == 'add':
                handle_add(event)
            elif action_type == 'read':
                handle_read(event)
            elif action_type == 'edit':
                handle_edit(event)
            elif action_type == 'delete':
                handle_delete(event)
            elif action_type == 'help':
                display_help(event)
            else:
                handle_other(event)
        except:
            handle_other(event)

    return app
