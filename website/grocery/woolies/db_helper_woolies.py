import os
import pandas as pd
from website import db
from website.grocery.woolies.woolies_models import (
    WooliesBestBuys,
    WooliesWorstBuys,
    WooliesCleanDf,
)
from sqlalchemy import create_engine
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db as fdb


from config.config import GroceryConfig


from website.dummy_objects.product_change_value import ProductChangeValue
from website.dummy_objects.dummy_db_helper import DbHelper
import logging

logging.basicConfig(
    level=logging.DEBUG,
    filemode="w",
    format="%(asctime)s - %(levelname)s - %(message)s",
)

class WooliesDbHelper(DbHelper):
    def __init__(self):
        DbHelper.__init__(self)

    def woolies_retrieve_and_clean_data(self):

        self.retrieve_and_clean_data(
            keyname="e-grocery.json",
            db_url="https://e-grocery-20812-default-rtdb.firebaseio.com/",
            table_name="woolworths",
            BestBuys=WooliesBestBuys,
            WorstBuys=WooliesWorstBuys,
            CleanDf=WooliesCleanDf,
        )

    def clean_df(self, df):
        # cleaning the data

        df["price"] = df["price_not_on_discount"].fillna(df["price_discounted"])

        df["price"] = df["price"].apply(lambda x: float(x))

        df["price_not_on_discount"] = df["price_not_on_discount"].apply(
            lambda x: float(x)
        )

        df["price_discounted"] = df["price_discounted"].apply(self.to_float)

        df["date"] = pd.to_datetime(df["date"])

        df.drop(
            ["price_crossed_out", "price_discounted", "price_not_on_discount"],
            axis=1,
            inplace=True,
        )

        df["title"] = df["title"].apply(lambda x: x.strip().lower() if type(x) != float else x)

        df["date_only"] = pd.to_datetime(df["date"].dt.date)

        clean_df = df.drop_duplicates(subset=["title", "date_only"], keep=False)

        clean_df.drop(["date_only"], axis=1, inplace=True)

        clean_df.dropna(inplace=True)

        # df["date"] = pd.to_datetime(df["date"])

        # df["price"] = df["price"].apply(lambda x:  x if (type(x)==float) else float(x.strip().replace("R","").replace(",","")) )

        # basedir = os.path.abspath(os.path.dirname(__file__))
        # path = "sqlite:///" + os.path.join(basedir, "..","..", "data.sqlite")

        cnx = create_engine(GroceryConfig.DB_URI).connect()
        clean_df.to_sql("woolies_clean_df", cnx, if_exists="replace")
        return clean_df

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
                        # "image_url":df[df["title"] == i.title]["image_url"].sort_values().iloc[0],
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

                # url = df[df["title"] == i.title]["image_url"].sort_values().iloc[0]
                product_dict = {
                    i.title: {
                        # "image_url": url ,
                        "prices_list": list(df[df["title"] == i.title]["price"]),
                        "dates": list((df[df["title"] == i.title]["date"].astype(str))),
                        "change": i.price,
                    }
                }
                expensive_products_list.append(product_dict)

        return expensive_products_list

