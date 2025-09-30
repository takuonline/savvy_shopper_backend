from website import db


class SuperbalistBestBuys(db.Model):
    __tablename__ = "superbalist_best_buys"
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


class SuperbalistWorstBuys(db.Model):
    __tablename__ = "superbalist_worst_buys"

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


class SuperbalistCleanDf(db.Model):
    __tablename__ = "superbalist_clean_df"

    title = db.Column(db.Text)
    # image_url = db.Column(db.Text)
    date = db.Column(db.Text, primary_key=True)
    price = db.Column(db.Float)

    # colors = db.Column(db.Text)
    # link = db.Column(db.Text)
    # designer_name = db.Column(db.Text)

    def __init__(
        self,
        date,
        #  image_url,
        # designer_name,
        price,
        title,
    ):
        self.title = title
        # self.image_url = image_url
        self.date = date
        self.price = price
        # self.designer_name = designer_name

    # def __repr__(self):
    #     return f"{self.title}, {self.date}, {self.price} \n"
