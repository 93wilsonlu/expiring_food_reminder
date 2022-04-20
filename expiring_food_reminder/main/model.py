from expiring_food_reminder import db


class Food(db.Model):
    __tablename__ = 'Food'
    id = db.Column(db.Integer, primary_key=True)
    food_name = db.Column(db.String(20), nullable=False)
    owner_id = db.Column(db.String(35), nullable=False)
    expiry_time = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return '<Food %s>' % self.food_name
