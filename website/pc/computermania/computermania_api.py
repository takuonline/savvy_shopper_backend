from flask_restful import Resource
import os
import pandas as pd
from sqlalchemy import create_engine
import json
from datetime import datetime
import logging
from website.dummy_objects.product_change_value import ProductChangeValue


class ComputermaniaAdmin(Resource):
    def get(self):
        from website.pc.computermania.db_helper_computermania import (
            ComputermaniaDbHelper,
        )

        starting_time = datetime.now()

        ComputermaniaDbHelper().computermania_retrieve_and_clean_data()

        finish_time = datetime.now()

        time = finish_time - starting_time

        return {
            "response": 200,
            "starting time": str(starting_time),
            "finishing time": str(finish_time),
            "time": str(time),
        }


class ComputermaniaClient(Resource):
    def get(self):

        from website.pc.computermania.computermania_models import (
            ComputermaniaBestBuys,
            ComputermaniaWorstBuys,
        )
        from website.pc.computermania.db_helper_computermania import (
            ComputermaniaDbHelper,
        )

        starting_time = datetime.now()

        basedir = os.path.abspath(os.path.dirname(__file__))
        path = "sqlite:///" + os.path.join(basedir, "..", "..", "data.sqlite")
        cnx = create_engine(path, connect_args={"check_same_thread": False}).connect()

        logging.debug(path)

        num = 30

        df = pd.read_sql("computermania_clean_df", cnx)
        logging.debug(df.head())

        price_decrease = []
        price_increase = []

        logging.debug(price_decrease)
        logging.debug(price_increase)

        for i in ComputermaniaBestBuys.query.all():
            price_decrease.append(ProductChangeValue(i.price_change, i.title))

        for i in ComputermaniaWorstBuys.query.all():
            price_increase.append(ProductChangeValue(i.price_change, i.title))

        logging.debug(len(price_decrease))

        cheap = ComputermaniaDbHelper.get_best_buys(df, price_decrease, num)
        expensive = ComputermaniaDbHelper.get_worst_buys(df, price_increase, num)

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


class ComputermaniaGetProductData(Resource):
    def get(self, title):
        title = title.replace("@forwardslash@", "/")
        print(title)
        basedir = os.path.abspath(os.path.dirname(__file__))

        path = "sqlite:///" + os.path.join(basedir, "..", "..", "data.sqlite")
        cnx = create_engine(path, connect_args={"check_same_thread": False}).connect()

        df = pd.read_sql("computermania_clean_df", cnx)

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
