import os
import pandas as pd
from website import db
from website.clothing.woolworths_clothing.woolworths_clothing_models import (
    WoolworthsClothingBestBuys,
    WoolworthsClothingWorstBuys,
    WoolworthsClothingCleanDf,
)
from sqlalchemy import create_engine

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
        # self.retrieve_and_clean_data(
        #     keyname="e-clothing.json",
        #     db_url="https://e-clothing-2fe94-default-rtdb.firebaseio.com/",
        #     table_name="woolworths_clothing",
        #     BestBuys=WoolworthsClothingBestBuys,
        #     WorstBuys=WoolworthsClothingWorstBuys,
        #     CleanDf=WoolworthsClothingCleanDf,
        # )

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
        basedir = os.path.abspath(os.path.dirname(__file__))
        path = "sqlite:///" + os.path.join(basedir, "..", "..", "data.sqlite")
        cnx = create_engine(path, connect_args={"check_same_thread": False}).connect()

        df.to_sql("woolworths_clothing_clean_df", cnx, if_exists="replace")

        return df

    @staticmethod
    def get_best_buys(df, price_decrease, num):
        # sort price_decrease list according to the price changes
        newlist = sorted(price_decrease, key=lambda x: x.price, reverse=False)

        # get the top n product into dict format and put in list
        cheap_products_list = []
        for i in newlist[:num]:
            if len(df[df["title"] == i.title]) != 0:
                product_dict = {
                    i.title: {
                        "prices_list": list(df[df["title"] == i.title]["price"]),
                        "dates": list(df[df["title"] == i.title]["date"].astype(str)),
                        "change": i.price,
                    }
                }

                cheap_products_list.append(product_dict)

        return cheap_products_list

    @staticmethod
    def get_worst_buys(df, price_increase_list, num):
        # sort price_decrease list according to the price changes
        newlist = sorted(price_increase_list, key=lambda x: x.price, reverse=True)

        # get into dict format and put in list
        expensive_products_list = []
        for i in newlist[:num]:
            if len(df[df["title"] == i.title]) != 0:
                product_dict = {
                    i.title: {
                        "prices_list": list(df[df["title"] == i.title]["price"]),
                        "dates": list((df[df["title"] == i.title]["date"].astype(str))),
                        "change": i.price,
                    }
                }
                expensive_products_list.append(product_dict)

        return expensive_products_list
