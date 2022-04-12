from flask import Flask, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from .config import config_dict
import os

line_bot_api = LineBotApi(os.environ.get('CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.environ.get('CHANNEL_SECRET'))

db = SQLAlchemy()
migrate = Migrate(compare_type=True)


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
    
    from .commands import init_cli
    init_cli(app)

    from .message_handler import handle_add, handle_read, handle_edit, handle_delete, handle_other

    @handler.add(MessageEvent, message=TextMessage)
    def main_handler(event):
        action_type = event.message.text.split(' ')[0]
        if action_type == 'add':
            handle_add(event)
        elif action_type == 'read':
            handle_read(event)
        elif action_type == 'edit':
            handle_edit(event)
        elif action_type == 'delete':
            handle_delete(event)
        else:
            handle_other(event)

    return app
