import os
import pandas as pd
import numpy as np
from sqlalchemy import create_engine

from website.clothing.mrp.mrp_models import MrpBestBuys, MrpWorstBuys, MrpCleanDf
from website.dummy_objects.dummy_db_helper import DbHelper

import logging
from config.config import ClothingConfig

logging.basicConfig(
    level=logging.DEBUG,
    filemode="w",
    format="%(asctime)s - %(levelname)s - %(message)s",
)


class MrpDbHelper(DbHelper):
    def __init__(self):
        DbHelper.__init__(self)

    def mrp_retrieve_and_clean_data(self):
        self.dynamodb_retrieve_and_clean_data(
            table_name="mrprice",
            BestBuys=MrpBestBuys,
            WorstBuys=MrpWorstBuys,
            CleanDf=MrpCleanDf,
        )

    def clean_df(self, df):
        # cleaning the data

        # clean price and date
        df["date"] = pd.to_datetime(df["date"])

        df["price"] = df["price"].apply(
            lambda x: float(x.replace("R", "").replace(",", "").strip().split()[-1])
        )

        # df["image_url"] = df["image_url"].apply(lambda x: x.replace("https://www.game.co.za",""))

        df["title"] = df["title"].apply(
            lambda x: x.replace("<span>", "").replace("</span>", "").strip().lower()
        )
        df.drop(["brand"], axis=1, inplace=True)

        # basedir = os.path.abspath(os.path.dirname(__file__))
        # path = "sqlite:///" + os.path.join(basedir, "..", "..", "data.sqlite")
        cnx = create_engine(
            ClothingConfig.DB_URI, connect_args={"check_same_thread": False}
        ).connect()

        df.to_sql("mrp_clean_df", cnx, if_exists="replace")

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
                        # brand, colors, date, image_url, link, price, title)
                        # "image_url":df[df["title"] == i.title]["image_url"].sort_values().iloc[0],
                        "prices_list": list(df[df["title"] == i.title]["price"]),
                        "dates": list(df[df["title"] == i.title]["date"].astype(str)),
                        "brand": df[df["title"] == i.title]["brand"]
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
                # url = df[df["title"] == i.title]["image_url"].sort_values().iloc[0]
                product_dict = {
                    i.title: {
                        # "image_url": url ,
                        "prices_list": list(df[df["title"] == i.title]["price"]),
                        "dates": list((df[df["title"] == i.title]["date"].astype(str))),
                        "brand": df[df["title"] == i.title]["brand"]
                        .sort_values()
                        .iloc[0],
                        "change": i.price,
                    }
                }
                expensive_products_list.append(product_dict)

        return expensive_products_list
