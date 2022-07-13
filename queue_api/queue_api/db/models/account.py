import sqlalchemy as db


class Account(db.Model):
    __bind_key__ = 'atlas_game_server'

    name = db.Column(db.String, primary_key=True)
    password = db.Column(db.String, nullable=False)
    privlevel = db.Column(db.INTEGER, nullable=False)
    discordid = db.Column(db.TEXT, nullable=True)
    lastlogin = db.Column(db.DATETIME, nullable=True)
    # lastdisconnected = db.Column(db.DATETIME, nullable=True)