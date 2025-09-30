from flask_restx import Resource
import os
import pandas as pd
from sqlalchemy import create_engine
import json
from datetime import datetime

from website.dummy_objects.product_change_value import ProductChangeValue
import logging
import traceback

logging.basicConfig(
    level=logging.DEBUG,
    filemode="w",
    format="%(asctime)s - %(levelname)s - %(message)s",
)


class FoschiniAdmin(Resource):
    def get(self):
        from website.clothing.foschini.db_helper_foschini import FoschiniDbHelper

        starting_time = datetime.now()
        # try:

        FoschiniDbHelper().foschini_retrieve_and_clean_data()
        # except Exception as e:
        #     finish_time = datetime.now()

        #     time = finish_time - starting_time

        #     return {
        #         "response": "error",
        #         "starting time": str(starting_time),
        #         "finishing time": str(finish_time),
        #         "time":time,
        #         "tb":traceback.format_exc(),
        #         "description": "Something went wrong fetching data from firebase. Please check the db connection",
        #     }
        finish_time = datetime.now()

        time = finish_time - starting_time

        return {
            "response": 200,
            "starting time": str(starting_time),
            "finishing time": str(finish_time),
            "time": str(time),
        }


class FoschiniClient(Resource):
    def get(self):
        from website.clothing.foschini.db_helper_foschini import FoschiniDbHelper
        from website.clothing.foschini.foschini_models import (
            FoschiniBestBuys,
            FoschiniWorstBuys,
        )

        starting_time = datetime.now()

        basedir = os.path.abspath(os.path.dirname(__file__))
        path = "sqlite:///" + os.path.join(basedir, "..", "..", "data.sqlite")

        cnx = create_engine(path, connect_args={"check_same_thread": False}).connect()

        num = 50

        df = pd.read_sql("foschini_clean_df", cnx)

        price_decrease = [
            ProductChangeValue(i.price_change, i.title)
            for i in FoschiniBestBuys.query.all()
        ]
        price_increase = [
            ProductChangeValue(i.price_change, i.title)
            for i in FoschiniWorstBuys.query.all()
        ]

        cheap = FoschiniDbHelper.get_best_buys(df, price_decrease, num)
        expensive = FoschiniDbHelper.get_worst_buys(df, price_increase, num)

        finish_time = datetime.now()

        time = finish_time - starting_time

        return {
            "cheap": json.dumps(cheap),
            "expensive": json.dumps(expensive),
            "all_products": json.dumps(list(df["title"].unique())),
            "starting time": str(starting_time),
            "finishing time": str(finish_time),
            "time": str(time),
        }


class FoschiniGetProductData(Resource):
    def get(self, title):
        title = title.replace("@forwardslash@", "/")
        logging.debug(title)

        basedir = os.path.abspath(os.path.dirname(__file__))
        path = "sqlite:///" + os.path.join(basedir, "..", "..", "data.sqlite")
        cnx = create_engine(path, connect_args={"check_same_thread": False}).connect()

        df = pd.read_sql("foschini_clean_df", cnx)

        if len(df[df["title"] == title]) != 0:
            current_price = df[df["title"] == title]["price"].iloc[-1]

            # average_price
            average_price = df[df["title"] == title]["price"].mean()

            percentage_change = (current_price - average_price) * 100 / average_price
            item_response = {
                title: {
                    "image_url": df[df["title"] == title]["image_url"].iloc[0],
                    "prices_list": list(df[df["title"] == title]["price"]),
                    "dates": list(df[df["title"] == title]["date"].astype(str)),
                    "brand": df[df["title"] == title]["brand"].sort_values().iloc[0],
                    "colors": df[df["title"] == title]["colors"].iloc[0],
                    "link": df[df["title"] == title]["link"].sort_values().iloc[0],
                    "change": percentage_change,
                }
            }
            return json.dumps(item_response)

        else:
            return {"response": "product not found", "product-title": json.dumps(title)}
