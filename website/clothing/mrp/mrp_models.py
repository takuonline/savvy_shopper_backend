from website import db


class MrpBestBuys(db.Model):
    __tablename__ = "mrp_best_buys"
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


class MrpWorstBuys(db.Model):
    __tablename__ = "mrp_worst_buys"

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


class MrpCleanDf(db.Model):
    __tablename__ = "mrp_clean_df"

    title = db.Column(db.Text)
    # image_url = db.Column(db.Text)
    date = db.Column(db.Text, primary_key=True)
    price = db.Column(db.Float)
    # brand = db.Column(db.Text)

    def __init__(
        self,
        #  brand,
        date,
        price,
        title,
    ):
        self.title = title
        # self.image_url = image_url
        self.date = date
        self.price = price
        # self.brand = brand

    def __repr__(self):
        return f"{self.title},  {self.date}, {self.price} \n"
