from website import db


class MakroBestBuys(db.Model):

    __tablename__ = "makro_best_buys"
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


class MakroWorstBuys(db.Model):

    __tablename__ = "makro_worst_buys"
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


class MakroCleanDf(db.Model):

    __tablename__ = "makro_clean_df"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    image_url = db.Column(db.Text)
    date = db.Column(db.Text)
    price = db.Column(db.Float)
   
    def __init__(self,  date, price, image_url, title):

        self.title = title
        self.image_url = image_url
        self.date = date
        self.price = price
 

    def __repr__(self):
        return f"{self.title}, {self.image_url}, {self.date}, {self.price} \n"
