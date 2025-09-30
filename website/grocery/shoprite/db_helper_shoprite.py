import os
import pandas as pd
import pymongo
from sqlalchemy import create_engine
from website.dummy_objects.dummy_db_helper import DbHelper
from datetime import datetime

from config.config import GroceryConfig


MONGO_DB_USERNAME = os.environ["MONGO_DB_USERNAME"]
MONGO_DB_PASSWORD = os.environ["MONGO_DB_PASSWORD"]


class ShopriteDbHelper(DbHelper):
    def __init__(self):
        DbHelper.__init__(self)

    def shoprite_retrieve_and_clean_data(self):
        from website import db
        from website.grocery.shoprite.shoprite_models import (
            ShopriteBestBuys,
            ShopriteWorstBuys,
            ShopriteCleanDf,
        )

        # create all the tables in sqlite db if not created
        db.create_all()

        # load data from database
        df = self.load_from_db()

        # remove all the old data from the sqlite database
        self.clean_old_data(ShopriteBestBuys, ShopriteWorstBuys, ShopriteCleanDf)

        # clean up dataframe and remove unwanted data and columns
        modified_df = self.clean_df(df)

        # calculate the store features from df
        # self.process_data(modified_df)

        # self.further_processing(modified_df)

        # store the processed data
        # self.store_data(ShopriteBestBuys, ShopriteWorstBuys)

    def load_from_db(self):
        client = pymongo.MongoClient(
            f"mongodb+srv://{MONGO_DB_USERNAME}:{MONGO_DB_PASSWORD}@cluster0.mcpct.mongodb.net/ecommerce?retryWrites=true&w=majority"
        )
        db_mongo = client["ecommerce"]
        collection = db_mongo.shoprite

        # fetch data from Mongodb database
        return pd.DataFrame(list(collection.find()))

    def clean_df(self, df):
        start_date = datetime.now() - pd.DateOffset(months=3)

        # format datetime data
        df["date"] = pd.to_datetime(df["date"])
        df = df[df["date"] >= start_date]

        # format price data
        df["price"] = df["price"].apply(
            lambda x: float((x.strip()).replace(",", "").replace("R", "").split()[-1])
        )

        # remove duplicates
        df["date_only"] = df["date"].dt.date
        df = df.drop_duplicates(subset=["title", "date_only"], keep=False)
        df.drop("date_only", axis=1, inplace=True)

        df["title"] = df["title"].apply(
            lambda x: x.strip().lower() if type(x) != float else x
        )

        # add df file to database
        # basedir = os.path.abspath(os.path.dirname(__file__))
        # path = "sqlite:///" + os.path.join(basedir, "..", "..", "data.sqlite")
        cnx = create_engine(
            GroceryConfig.DB_URI, connect_args={"check_same_thread": False}
        ).connect()

        df.drop(["_id", "image_url"], axis=1).to_sql(
            "shoprite_clean_df", cnx, if_exists="replace"
        )

        return df
