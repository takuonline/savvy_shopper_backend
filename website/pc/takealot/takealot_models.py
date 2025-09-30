from website import db


class TakealotBestBuys(db.Model):
    __tablename__ = "takealot_best_buys"
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


class TakealotWorstBuys(db.Model):
    __tablename__ = "takealot_worst_buys"
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
        return f"{self.title}"


class TakealotCleanDf(db.Model):
    __tablename__ = "takealot_clean_df"

    title = db.Column(db.Text)
    # image_url = db.Column(db.Text)
    date = db.Column(db.Text, primary_key=True)
    # brand = db.Column(db.Text)
    price = db.Column(db.Float)

    def __init__(
        self,
        title,
        price,
        # image_url, brand,
        date,
    ):
        self.title = title
        # self.image_url = image_url
        self.date = date
        self.price = price
        # self.brand = brand

    def __repr__(self):
        return f"{self.title}, {self.image_url}, {self.date}, {self.price} , {self.brand} \n"
