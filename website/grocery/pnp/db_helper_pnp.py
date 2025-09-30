import os
import pandas as pd
from website.grocery.pnp.pnp_models import PnPBestBuys, PnPWorstBuys, PnPCleanDf
from sqlalchemy import create_engine

from website.dummy_objects.dummy_db_helper import DbHelper
import logging

logging.basicConfig(
    level=logging.DEBUG,
    filemode="w",
    format="%(asctime)s - %(levelname)s - %(message)s",
)


class PnPDbHelper(DbHelper):
    def __init__(self):
        DbHelper.__init__(self)

    def pnp_retrieve_and_clean_data(self):
        self.retrieve_and_clean_data(
            keyname="e-grocery.json",
            db_url="https://e-grocery-20812-default-rtdb.firebaseio.com/",
            table_name="pnp",
            BestBuys=PnPBestBuys,
            WorstBuys=PnPWorstBuys,
            CleanDf=PnPCleanDf,
        )

    def clean_df(self, df):
        # cleaning the data
        df.dropna(subset=["price"], inplace=True)

        df["date"] = pd.to_datetime(df["date"])

        df["price"] = df["price"].apply(
            lambda x: x
            if (type(x) == float)
            else float(x.strip().replace("R", "").replace(",", ""))
        )

        df["date_only"] = df["date"].dt.date
        df = df.drop_duplicates(subset=["title", "date_only"], keep=False)

        df.drop("date_only", axis=1, inplace=True)

        # not able to multiprocess this
        basedir = os.path.abspath(os.path.dirname(__file__))
        path = "sqlite:///" + os.path.join(basedir, "..", "..", "data.sqlite")
        cnx = create_engine(path).connect()

        df.to_sql("pnp_clean_df", cnx, if_exists="replace")

        return df

    def store_df(self, df):
        basedir = os.path.abspath(os.path.dirname(__file__))
        path = "sqlite:///" + os.path.join(basedir, "..", "..", "data.sqlite")
        cnx = create_engine(path).connect()

        df.to_sql("pnp_clean_df", cnx, if_exists="replace")

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
                        "change": i.price,
                    }
                }
                expensive_products_list.append(product_dict)

        return expensive_products_list
