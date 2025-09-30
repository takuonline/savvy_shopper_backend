import os
import pandas as pd
from website import db
from website.clothing.woolworths_clothing.woolworths_clothing_models import (
    WoolworthsClothingBestBuys,
    WoolworthsClothingWorstBuys,
    WoolworthsClothingCleanDf,
)
from sqlalchemy import create_engine
from config.config import ClothingConfig
from website.dummy_objects.dummy_db_helper import DbHelper
import logging

logging.basicConfig(
    level=logging.DEBUG,
    filemode="w",
    format="%(asctime)s - %(levelname)s - %(message)s",
)


class WoolworthsClothingDbHelper(DbHelper):
    def __init__(self):
        DbHelper.__init__(self)

    def woolworths_clothing_retrieve_and_clean_data(self):
        self.dynamodb_retrieve_and_clean_data(
            table_name="woolworths_clothing",
            BestBuys=WoolworthsClothingBestBuys,
            WorstBuys=WoolworthsClothingWorstBuys,
            CleanDf=WoolworthsClothingCleanDf,
        )

    def clean_df(self, df):
        # fills all missing prices with prices discounted
        df["price"] = df["price_not_on_discount"].fillna(df["price_discounted"])

        # change price to float
        df["price"] = df["price"].apply(lambda x: float(x))

        # change date from string to datatime
        df["date"] = pd.to_datetime(df["date"])

        # get the date only from a datetime column
        df["date_only"] = df["date"].dt.date

        # drop products with a duplicate date and title (products with the same name)
        df = df.drop_duplicates(subset=["title", "date_only"], keep=False)

        df["title"] = df["title"].apply(lambda title: title.strip().lower())

        # drop columns which are not needed in the final product
        df.drop(
            [
                "date_only",
                "price_crossed_out",
                "price_discounted",
                "price_not_on_discount",
            ],
            axis=1,
            inplace=True,
        )

        # get the path to the data
        # basedir = os.path.abspath(os.path.dirname(__file__))
        # path = "sqlite:///" + os.path.join(basedir, "..", "..", "data.sqlite")
        cnx = create_engine(
            ClothingConfig.DB_URI, connect_args={"check_same_thread": False}
        ).connect()

        df.to_sql("woolworths_clothing_clean_df", cnx, if_exists="replace")

        return df
