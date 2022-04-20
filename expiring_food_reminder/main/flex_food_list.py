class FlexFoodList:
    def __init__(self, title):
        self.title = title
        self.reset()

    def reset(self):
        self.message = {
            "type": "bubble",
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": self.title,
                        "weight": "bold",
                        "size": "xl"
                    }
                ]
            }
        }

    def append_food(self, food):
        new_item = {
            "type": "box",
            "layout": "horizontal",
            "spacing": "sm",
            "contents": [
                {
                    "type": "text",
                    "text": str(food.id) + '. ' + food.food_name
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "text",
                            "text": food.expiry_time.strftime('%Y-%m-%d'),
                            "size": "xs",
                            "gravity": "center"
                        },
                        {
                            "type": "text",
                            "text": "delete",
                            "action": {
                                "type": "message",
                                "label": "action",
                                "text": "delete " + str(food.id)
                            },
                            "color": "#ff0000",
                            "flex": 0
                        }
                    ]
                }
            ],
            "margin": "lg",
            "flex": 2
        }
        self.message['body']['contents'].append(new_item)
