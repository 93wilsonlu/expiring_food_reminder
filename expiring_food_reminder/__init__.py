from flask import Flask, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage
from .config import config_dict
import os
from datetime import datetime
from flask_bootstrap import Bootstrap5

line_bot_api = LineBotApi(os.environ.get('CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.environ.get('CHANNEL_SECRET'))

db = SQLAlchemy()
migrate = Migrate(compare_type=True)
bootstrap = Bootstrap5()
TODAY = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)


def create_app(config='develop'):
    app = Flask(__name__)
    app.config.from_object(config_dict[config])
    db.init_app(app)
    migrate.init_app(app, db)
    bootstrap.init_app(app)

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

    @app.context_processor
    def inject_variable():
        return dict(liff_id=app.config.get('LIFF_ID'))

    @app.shell_context_processor
    def make_shell_context():
        return dict(app=app, db=db)

    from .commands import init_cli
    init_cli(app)

    from .main import main
    app.register_blueprint(main)

    from .main.message_handler import handle_read, handle_delete, display_help, handle_other

    @handler.add(MessageEvent, message=TextMessage)
    def main_handler(event):
        try:
            action_type = event.message.text.split(' ')[0]
            if action_type == 'read':
                handle_read(event)
            elif action_type == 'delete':
                handle_delete(event)
            elif action_type == 'help':
                display_help(event)
            else:
                handle_other(event)
        except:
            handle_other(event)

    return app
