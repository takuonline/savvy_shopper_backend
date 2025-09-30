from flask_restx import Resource
import os
import pandas as pd
from sqlalchemy import create_engine
import json
from datetime import datetime

from website.grocery.shoprite.db_helper_shoprite import ShopriteDbHelper
from website.dummy_objects.product_change_value import ProductChangeValue

import json
import logging

logging.basicConfig(
    filename="api_logs.txt",
    level=logging.DEBUG,
    filemode="w",
    format="%(asctime)s - %(levelname)s - %(message)s",
)


class ShopriteAdmin(Resource):
    def get(self):
        starting_time = datetime.now()

        db_helper = ShopriteDbHelper()

        db_helper.shoprite_retrieve_and_clean_data()

        finish_time = datetime.now()

        time = finish_time - starting_time

        return {
            "response": 200,
            "starting time": str(starting_time),
            "finishing time": str(finish_time),
            "time": str(time),
        }


class ShopriteClient(Resource):
    def get(self):
        from website.grocery.shoprite.shoprite_models import (
            ShopriteBestBuys,
            ShopriteWorstBuys,
        )

        starting_time = datetime.now()

        basedir = os.path.abspath(os.path.dirname(__file__))
        path = "sqlite:///" + os.path.join(basedir, "..", "..", "data.sqlite")
        # remove warning that says the sqlalchemy must run on the main thread
        cnx = create_engine(path, connect_args={"check_same_thread": False}).connect()

        num = 50

        logging.debug(num)

        df = pd.read_sql("shoprite_clean_df", cnx)
        logging.debug(df.head())

        price_decrease = []
        price_increase = []

        for i in ShopriteBestBuys.query.all():
            price_decrease.append(ProductChangeValue(i.price_change, i.title))

        for i in ShopriteWorstBuys.query.all():
            price_increase.append(ProductChangeValue(i.price_change, i.title))

        logging.debug("price_decrease")
        logging.debug(len(price_decrease))

        logging.debug("price_increase")
        logging.debug(len(price_increase))

        cheap = ShopriteDbHelper.get_best_buys(df, price_decrease, num)
        expensive = ShopriteDbHelper.get_worst_buys(df, price_increase, num)

        logging.debug("cheap")
        logging.debug(len(cheap))

        logging.debug("expensive")
        logging.debug(len(expensive))

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


class ShopriteGetProductData(Resource):
    def get(self, title):
        title = title.replace("@forwardslash@", "/")

        basedir = os.path.abspath(os.path.dirname(__file__))
        path = "sqlite:///" + os.path.join(basedir, "..", "..", "data.sqlite")
        cnx = create_engine(path, connect_args={"check_same_thread": False}).connect()

        df = pd.read_sql("shoprite_clean_df", cnx)

        logging.debug("df")
        logging.debug(df.head())

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
                    "change": percentage_change,
                }
            }
            return json.dumps(item_response)

        else:
            return {"response": "product not found", "product-title": json.dumps(title)}
