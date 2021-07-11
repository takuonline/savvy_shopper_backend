import os
import pandas as pd
import numpy as np
from sqlalchemy import create_engine

from website.dummy_objects.product_change_value import ProductChangeValue
from website.dummy_objects.dummy_db_helper import DbHelper
from website.dummy_objects.firebase_helper import FirebaseHelper
from website import db
from website.pc.game.game_models import GameBestBuys, GameWorstBuys, GameCleanDf
import logging

from config.config import AccessoriesConfig

logging.basicConfig(
    level=logging.DEBUG,
    filemode="w",
    format="%(asctime)s - %(levelname)s - %(message)s",
)


class GameDbHelper(DbHelper):
    def __init__(self):
        DbHelper.__init__(self)

    def game_retrieve_and_clean_data(self):

        self.dynamodb_retrieve_and_clean_data(
            table_name="game",
            BestBuys=GameBestBuys,
            WorstBuys=GameWorstBuys,
            CleanDf=GameCleanDf,
        )

    def clean_df(self, df):
        # cleaning the data

        df["date"] = pd.to_datetime(df["date"])
        df["title"] = df["title"].apply(lambda x: x.strip().lower() if type(x) != float else x)
        df["brand"] = df["brand"].apply(lambda x: x.strip().lower())
        df["image_url"] = df["image_url"].apply(lambda x: "https://www.game.co.za" + x)
 

        df["date_only"] = df["date"].dt.date
        df.drop_duplicates(subset=["title", "date_only"],keep = False,inplace=True)
        df.drop(["date_only"], axis=1, inplace=True)

        df.dropna(subset=["price"], inplace=True)
        df["price"] = df["price"].apply(lambda x: float(x.replace("R","").replace(",","").split()[-1]))

        

        # basedir = os.path.abspath(os.path.dirname(__file__))
        # path = "sqlite:///" + os.path.join(basedir, "..", "..", "data.sqlite")
        cnx = create_engine(AccessoriesConfig.DB_URI, connect_args={"check_same_thread": False}).connect()

        df.to_sql("game_clean_df", cnx, if_exists="replace")

        return df

    # @staticmethod
    # def get_best_buys(df, price_decrease, num):
    #     # sort price_decrease list according to the price changes
    #     newlist = sorted(price_decrease, key=lambda x: x.price, reverse=False)

    #     # get the top n product into dict format and put in list
    #     cheap_products_list = []
    #     for i in newlist[:num]:
    #         if len(df[df["title"] == i.title]) != 0:
    #             try:
    #                 img_url = (
    #                     df[df["title"] == i.title]["image_url"].sort_values().iloc[0]
    #                 )
    #             except KeyError:
    #                 img_url = None

    #             product_dict = {
    #                 i.title: {
    #                     "image_url": img_url,
    #                     "prices_list": list(df[df["title"] == i.title]["price"]),
    #                     "dates": list(df[df["title"] == i.title]["date"].astype(str)),
    #                     "brand": df[df["title"] == i.title]["brand"]
    #                     .sort_values()
    #                     .iloc[0],
    #                     "change": i.price,
    #                 }
    #             }

    #             cheap_products_list.append(product_dict)

    #     return cheap_products_list

    # @staticmethod
    # def get_worst_buys(df, price_increase_list, num):

    #     # sort price_decrease list according to the price changes
    #     newlist = sorted(price_increase_list, key=lambda x: x.price, reverse=True)

    #     # get into dict format and put in list
    #     expensive_products_list = []
    #     for i in newlist[:num]:

    #         if len(df[df["title"] == i.title]) != 0:
    #             try:
    #                 img_url = (
    #                     df[df["title"] == i.title]["image_url"].sort_values().iloc[0]
    #                 )
    #             except KeyError:
    #                 img_url = None

    #             product_dict = {
    #                 i.title: {
    #                     "image_url": img_url,
    #                     "prices_list": list(df[df["title"] == i.title]["price"]),
    #                     "dates": list((df[df["title"] == i.title]["date"].astype(str))),
    #                     "brand": df[df["title"] == i.title]["brand"]
    #                     .sort_values()
    #                     .iloc[0],
    #                     "change": i.price,
    #                 }
    #             }
    #             expensive_products_list.append(product_dict)

    #     return expensive_products_list
