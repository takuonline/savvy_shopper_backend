import os
import pandas as pd
from website import db
from website.clothing.sportscene.sportscene_models import (
    SportsceneBestBuys,
    SportsceneWorstBuys,
    SportsceneCleanDf,
)
from sqlalchemy import create_engine
from website.dummy_objects.dummy_db_helper import DbHelper
import logging

logging.basicConfig(
    level=logging.DEBUG,
    filemode="w",
    format="%(asctime)s - %(levelname)s - %(message)s",
)


class SportsceneDbHelper(DbHelper):
    def __init__(self):
        DbHelper.__init__(self)

    def sportscene_retrieve_and_clean_data(self):
        # self.retrieve_and_clean_data(
        #     keyname="e-clothing.json",
        #     db_url="https://e-clothing-2fe94-default-rtdb.firebaseio.com/",
        #     table_name="sportscene",
        #     BestBuys=SportsceneBestBuys,
        #     WorstBuys=SportsceneWorstBuys,
        #     CleanDf=SportsceneCleanDf,
        # )
        self.dynamodb_retrieve_and_clean_data(
            table_name="sportscene",
            BestBuys=SportsceneBestBuys,
            WorstBuys=SportsceneWorstBuys,
            CleanDf=SportsceneCleanDf,
        )

    def clean_df(self, df):
        # cleaning the data

        # clean price and date
        df["price"] = df["price"].apply(
            lambda x: float(x.replace("R", "").replace(",", "").strip().split()[-1])
        )
        df["date"] = pd.to_datetime(df["date"])

        df["colors"] = df["colors"].apply(self.get_color)
        # remove duplicates
        df["date_only"] = df["date"].dt.date
        df = df.drop_duplicates(subset=["title", "date_only"], keep=False)

        df.drop(["date_only", "second_image_url"], axis=1, inplace=True)

        basedir = os.path.abspath(os.path.dirname(__file__))
        path = "sqlite:///" + os.path.join(basedir, "..", "..", "data.sqlite")
        cnx = create_engine(path, connect_args={"check_same_thread": False}).connect()

        df.to_sql("sportscene_clean_df", cnx, if_exists="replace")

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
                        "image_url": df[df["title"] == i.title]["image_url"]
                        .sort_values()
                        .iloc[0],
                        "prices_list": list(df[df["title"] == i.title]["price"]),
                        "dates": list(df[df["title"] == i.title]["date"].astype(str)),
                        "brand": df[df["title"] == i.title]["brand"]
                        .sort_values()
                        .iloc[0],
                        "colors": df[df["title"] == i.title]["colors"].iloc[0],
                        "link": df[df["title"] == i.title]["link"]
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
                        "brand": df[df["title"] == i.title]["brand"]
                        .sort_values()
                        .iloc[0],
                        "colors": df[df["title"] == i.title]["colors"].iloc[0],
                        "link": df[df["title"] == i.title]["link"]
                        .sort_values()
                        .iloc[0],
                        "change": i.price,
                    }
                }
                expensive_products_list.append(product_dict)

        return expensive_products_list
