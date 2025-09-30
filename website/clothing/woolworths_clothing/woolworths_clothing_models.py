from website import db


class WoolworthsClothingBestBuys(db.Model):
    __tablename__ = "woolworths_clothing_best_buys"
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


class WoolworthsClothingWorstBuys(db.Model):
    __tablename__ = "woolworths_clothing_worst_buys"

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


class WoolworthsClothingCleanDf(db.Model):
    __tablename__ = "woolworths_clothing_clean_df"

    title = db.Column(db.Text)
    image_url = db.Column(db.Text)
    date = db.Column(db.Text, primary_key=True)
    price = db.Column(db.Float)

    def __init__(self, date, price, title):
        self.title = title
        self.date = date
        self.price = price

    def __repr__(self):
        return f"{self.title}, {self.date}, {self.price} \n"
