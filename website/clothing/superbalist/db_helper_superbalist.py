import os
import pandas as pd
import numpy as np
from website import db
from website.clothing.superbalist.superbalist_models import (
    SuperbalistBestBuys,
    SuperbalistWorstBuys,
    SuperbalistCleanDf,
)
from sqlalchemy import create_engine

from website.dummy_objects.dummy_db_helper import DbHelper

import logging

logging.basicConfig(
    level=logging.DEBUG,
    filemode="w",
    format="%(asctime)s - %(levelname)s - %(message)s",
)


class SuperbalistDbHelper(DbHelper):
    def __init__(self):
        DbHelper.__init__(self)

    def superbalist_retrieve_and_clean_data(self):
        # self.retrieve_and_clean_data(
        #     keyname="e-clothing.json",
        #     db_url="https://e-clothing-2fe94-default-rtdb.firebaseio.com/",
        #     table_name="superbalist",
        #     BestBuys=SuperbalistBestBuys,
        #     WorstBuys=SuperbalistWorstBuys,
        #     CleanDf=SuperbalistCleanDf,
        # )

        self.dynamodb_retrieve_and_clean_data(
            table_name="superbalist",
            BestBuys=SuperbalistBestBuys,
            WorstBuys=SuperbalistWorstBuys,
            CleanDf=SuperbalistCleanDf,
        )

    def clean_df(self, df):
        # cleaning the data

        df["price"] = df["max_price"].apply(lambda x: float(x))

        df["title"] = df["name"]

        df["date"] = pd.to_datetime(df["date"])
        df["date_only"] = df["date"].dt.date
        df = df.drop_duplicates(subset=["title", "date_only"], keep=False)

        df["image_url"] = df["image_url_2"].apply(
            lambda x: x.format(size="300x432/", quality="75", extension="jpg")
            if type(x) is type("s")
            else x
        )

        df.drop(
            [
                "date_only",
                "has_discount",
                "min_price",
                "name",
                "max_price",
                "discount",
                "image_url_2",
            ],
            axis=1,
            inplace=True,
        )

        basedir = os.path.abspath(os.path.dirname(__file__))
        path = "sqlite:///" + os.path.join(basedir, "..", "..", "data.sqlite")
        cnx = create_engine(path, connect_args={"check_same_thread": False}).connect()

        df.to_sql("superbalist_clean_df", cnx, if_exists="replace")

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
                        "image_url": df[df["title"] == i.title]["image_url"]
                        .sort_values()
                        .iloc[0],
                        "prices_list": list(df[df["title"] == i.title]["price"]),
                        "dates": list(df[df["title"] == i.title]["date"].astype(str)),
                        "designer_name": df[df["title"] == i.title]["designer_name"]
                        .sort_values()
                        .iloc[0],
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
                url = df[df["title"] == i.title]["image_url"].sort_values().iloc[0]
                product_dict = {
                    i.title: {
                        "image_url": url,
                        "prices_list": list(df[df["title"] == i.title]["price"]),
                        "dates": list((df[df["title"] == i.title]["date"].astype(str))),
                        "designer_name": df[df["title"] == i.title]["designer_name"]
                        .sort_values()
                        .iloc[0],
                        "change": i.price,
                    }
                }
                expensive_products_list.append(product_dict)

        return expensive_products_list
