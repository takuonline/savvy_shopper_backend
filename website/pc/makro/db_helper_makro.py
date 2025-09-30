import os
import pandas as pd
from sqlalchemy import create_engine

from website.dummy_objects.dummy_db_helper import DbHelper
from website import db
from website.pc.makro.makro_models import MakroBestBuys, MakroWorstBuys, MakroCleanDf
import logging

from config.config import AccessoriesConfig

logging.basicConfig(
    level=logging.DEBUG,
    filemode="w",
    format="%(asctime)s - %(levelname)s - %(message)s",
)


class MakroDbHelper(DbHelper):
    def __init__(self):
        DbHelper.__init__(self)

    def makro_retrieve_and_clean_data(self):
        self.dynamodb_retrieve_and_clean_data(
            table_name="makro",
            BestBuys=MakroBestBuys,
            WorstBuys=MakroWorstBuys,
            CleanDf=MakroCleanDf,
        )

    def clean_df(self, df):
        # cleaning the data

        df["date"] = pd.to_datetime(df["date"])

        df["price"] = df["price"].apply(
            lambda x: float(x.replace("R", "").replace(",", "").strip())
        )

        df["image_url"] = df["image_url"].apply(
            lambda x: x.replace("https://www.game.co.za", "")
        )
        df["title"] = df["title"].apply(
            lambda x: x.replace("<span>", "").replace("</span>", "").strip().lower()
        )

        df["date_only"] = df["date"].dt.date
        df.drop_duplicates(subset=["title", "date_only"], keep=False, inplace=True)
        df.drop(["date_only"], axis=1, inplace=True)

        # basedir = os.path.abspath(os.path.dirname(__file__))
        # path = "sqlite:///" + os.path.join(basedir, "..", "..", "data.sqlite")
        cnx = create_engine(
            AccessoriesConfig.DB_URI, connect_args={"check_same_thread": False}
        ).connect()

        df.to_sql("makro_clean_df", cnx, if_exists="replace")

        return df
