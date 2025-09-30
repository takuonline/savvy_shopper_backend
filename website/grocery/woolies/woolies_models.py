from website import db


class WooliesBestBuys(db.Model):
    __tablename__ = "woolies_best_buys"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    price_change = db.Column(db.Float)

    def __init__(
        self,
        title,
        price_change,
    ):
        self.title = title
        self.price_change = price_change

    def __repr__(self):
        return f"{self.title} {self.price_change}"


class WooliesWorstBuys(db.Model):
    __tablename__ = "woolies_worst_buys"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    price_change = db.Column(db.Float)

    def __init__(
        self,
        title,
        price_change,
    ):
        self.title = title
        self.price_change = price_change

    def __repr__(self):
        pass


class WooliesCleanDf(db.Model):
    __tablename__ = "woolies_clean_df"

    title = db.Column(db.Text)
    # image_url = db.Column(db.Text)
    date = db.Column(db.Text, primary_key=True)
    price = db.Column(db.Float)

    def __init__(self, title, price, date):
        self.title = title
        # self.image_url = image_url
        self.date = date
        self.price = price

    def __repr__(self):
        return f"{self.title}, {self.date}, {self.price} \n"
