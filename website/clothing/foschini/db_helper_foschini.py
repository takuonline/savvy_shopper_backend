import os
import pandas as pd

# import numpy as np
from website import db
from website.clothing.foschini.foschini_models import (
    FoschiniBestBuys,
    FoschiniWorstBuys,
    FoschiniCleanDf,
)
from sqlalchemy import create_engine

# import firebase_admin
# from firebase_admin import credentials
# from firebase_admin import db as fdb
from config.config import ClothingConfig

# from website.dummy_objects.product_change_value import ProductChangeValue
from website.dummy_objects.dummy_db_helper import DbHelper

# from website.dummy_objects.firebase_helper import FirebaseHelper
import logging

logging.basicConfig(
    level=logging.DEBUG,
    filemode="w",
    format="%(asctime)s - %(levelname)s - %(message)s",
)


class FoschiniDbHelper(DbHelper):
    def __init__(self):
        DbHelper.__init__(self)

    def foschini_retrieve_and_clean_data(self):
        self.dynamodb_retrieve_and_clean_data(
            table_name="foschini",
            BestBuys=FoschiniBestBuys,
            WorstBuys=FoschiniWorstBuys,
            CleanDf=FoschiniCleanDf,
        )

    def clean_df(self, df):
        # cleaning the data

        # clean price and date
        df["price"] = df["price"].apply(
            lambda x: float(x.replace("R", "").replace(",", "").strip().split()[-1])
        )
        df["date"] = pd.to_datetime(df["date"])
        # df["colors"] = df["colors"].apply(self.get_color)

        # remove duplicates
        df["date_only"] = df["date"].dt.date
        df = df.drop_duplicates(subset=["title", "date_only"], keep=False)

        df.drop(
            ["date_only", "second_image_url", "colors", "brand", "image_url", "link"],
            axis=1,
            inplace=True,
        )

        df["title"] = df["title"].apply(lambda title: title.strip().lower())

        # basedir = os.path.abspath(os.path.dirname(__file__))
        # path = "sqlite:///" + os.path.join(basedir, "..", "..", "data.sqlite")

        cnx = create_engine(
            ClothingConfig.DB_URI, connect_args={"check_same_thread": False}
        ).connect()

        df.to_sql("foschini_clean_df", cnx, if_exists="replace")
        return df
