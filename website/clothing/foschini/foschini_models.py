from website import db


class FoschiniBestBuys(db.Model):
    __tablename__ = "foschini_best_buys"
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


class FoschiniWorstBuys(db.Model):
    __tablename__ = "foschini_worst_buys"
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


class FoschiniCleanDf(db.Model):
    __tablename__ = "foschini_clean_df"

    title = db.Column(db.Text)
    # image_url = db.Column(db.Text)
    date = db.Column(db.Text, primary_key=True)
    price = db.Column(db.Float)

    # colors = db.Column(db.Text)
    # link = db.Column(db.Text)
    # brand = db.Column(db.Text)

    # "index", brand, colors, date, image_url, link, price, title)
    def __init__(
        self,
        #  brand, colors,
        date,
        #    image_url, link,
        price,
        title,
    ):
        self.title = title
        # self.image_url = image_url
        self.date = date
        self.price = price
        # self.colors = colors
        # self.link = link
        # self.brand = brand

    # def __repr__(self):
    #     return f"{self.title}, {self.image_url}, {self.date}, {self.price} \n"
