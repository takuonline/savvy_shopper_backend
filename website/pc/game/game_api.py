from flask_restx import Resource
import os
import pandas as pd
from sqlalchemy import create_engine
import json
from datetime import datetime

from website.dummy_objects.product_change_value import ProductChangeValue
import logging

logging.basicConfig(
    level=logging.DEBUG,
    filemode="w",
    format="%(asctime)s - %(levelname)s - %(message)s",
)


class GameAdmin(Resource):
    def get(self):
        from website.pc.game.db_helper_game import GameDbHelper

        starting_time = datetime.now()

        GameDbHelper().game_retrieve_and_clean_data()

        finish_time = datetime.now()

        time = finish_time - starting_time

        return {
            "response": 200,
            "starting time": str(starting_time),
            "finishing time": str(finish_time),
            "time": str(time),
        }


class GameClient(Resource):
    def get(self):
        from website.pc.game.game_models import GameBestBuys, GameWorstBuys
        from website.pc.game.db_helper_game import GameDbHelper

        starting_time = datetime.now()

        num = 50

        basedir = os.path.abspath(os.path.dirname(__file__))
        path = "sqlite:///" + os.path.join(basedir, "..", "..", "data.sqlite")

        cnx = create_engine(path, connect_args={"check_same_thread": False}).connect()

        df = pd.read_sql("game_clean_df", cnx)

        print(df.head())

        price_decrease = []
        price_increase = []

        for i in GameBestBuys.query.all():
            price_decrease.append(ProductChangeValue(i.price_change, i.title))

        for i in GameWorstBuys.query.all():
            price_increase.append(ProductChangeValue(i.price_change, i.title))

        len(price_decrease)

        cheap = GameDbHelper.get_best_buys(df, price_decrease, num)
        expensive = GameDbHelper.get_worst_buys(df, price_increase, num)

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


class GameGetProductData(Resource):
    def get(self, title):
        title = title.replace("@forwardslash@", "/")
        print(title)
        basedir = os.path.abspath(os.path.dirname(__file__))
        path = "sqlite:///" + os.path.join(basedir, "..", "..", "data.sqlite")
        cnx = create_engine(path, connect_args={"check_same_thread": False}).connect()

        df = pd.read_sql("game_clean_df", cnx)

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
                    "change": percentage_change,
                }
            }
            return json.dumps(item_response)

        else:
            return {"response": "product not found", "product-title": json.dumps(title)}
