from flask_restx import Resource
import os
import pandas as pd
from sqlalchemy import create_engine
import json
from datetime import datetime

import logging
from website.dummy_objects.product_change_value import ProductChangeValue


class SportsceneAdmin(Resource):
    def get(self):
        from website.clothing.sportscene.db_helper_sportscene import SportsceneDbHelper

        starting_time = datetime.now()

        SportsceneDbHelper().sportscene_retrieve_and_clean_data()

        finish_time = datetime.now()

        time = finish_time - starting_time

        return {
            "response": 200,
            "starting time": str(starting_time),
            "finishing time": str(finish_time),
            "time": str(time),
        }


class SportsceneClient(Resource):
    def get(self):
        from website.clothing.sportscene.sportscene_models import (
            SportsceneBestBuys,
            SportsceneWorstBuys,
        )
        from website.clothing.sportscene.db_helper_sportscene import SportsceneDbHelper

        starting_time = datetime.now()

        basedir = os.path.abspath(os.path.dirname(__file__))
        path = "sqlite:///" + os.path.join(basedir, "..", "..", "data.sqlite")

        cnx = create_engine(path, connect_args={"check_same_thread": False}).connect()

        num = 50

        df = pd.read_sql("sportscene_clean_df", cnx)

        price_decrease = [
            ProductChangeValue(i.price_change, i.title)
            for i in SportsceneBestBuys.query.all()
        ]
        price_increase = [
            ProductChangeValue(i.price_change, i.title)
            for i in SportsceneWorstBuys.query.all()
        ]

        print(len(price_decrease))
        print(len(price_increase))

        cheap = SportsceneDbHelper.get_best_buys(df, price_decrease, num)
        expensive = SportsceneDbHelper.get_worst_buys(df, price_increase, num)

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


class SportsceneGetProductData(Resource):
    def get(self, title):
        title = title.replace("@forwardslash@", "/")
        print(title)
        basedir = os.path.abspath(os.path.dirname(__file__))
        path = "sqlite:///" + os.path.join(basedir, "..", "..", "data.sqlite")
        cnx = create_engine(path, connect_args={"check_same_thread": False}).connect()

        df = pd.read_sql("sportscene_clean_df", cnx)

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
