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


class PnPAdmin(Resource):
    def get(self):
        from website.grocery.pnp.db_helper_pnp import PnPDbHelper

        starting_time = datetime.now()

        db_helper = PnPDbHelper()
        db_helper.pnp_retrieve_and_clean_data()

        finish_time = datetime.now()

        time = finish_time - starting_time

        return {
            "response": 200,
            "starting time": str(starting_time),
            "finishing time": str(finish_time),
            "time": str(time),
        }


class PnPClient(Resource):
    def get(self):
        # from website.pnp.db_helper_pnp import get_best_buys,get_worst_buys
        from website.grocery.pnp.pnp_models import PnPBestBuys, PnPWorstBuys
        from website.grocery.pnp.db_helper_pnp import PnPDbHelper

        starting_time = datetime.now()

        basedir = os.path.abspath(os.path.dirname(__file__))
        path = "sqlite:///" + os.path.join(basedir, "..", "..", "data.sqlite")

        cnx = create_engine(path, connect_args={"check_same_thread": False}).connect()

        num = 50

        df = pd.read_sql("pnp_clean_df", cnx)

        price_decrease = [
            ProductChangeValue(i.price_change, i.title) for i in PnPBestBuys.query.all()
        ]
        price_increase = [
            ProductChangeValue(i.price_change, i.title)
            for i in PnPWorstBuys.query.all()
        ]

        logging.debug(df.head())

        # for i in PnPBestBuys.query.all():
        #     price_decrease.append(ProductChangeValue(i.price_change,i.title))

        # for i in PnPWorstBuys.query.all():
        #     price_increase.append(ProductChangeValue(i.price_change,i.title))

        logging.debug("increase")
        logging.debug(len(price_increase))
        logging.debug("decrease")
        logging.debug(len(price_decrease))

        cheap = PnPDbHelper.get_best_buys(df, price_decrease, num)
        expensive = PnPDbHelper.get_worst_buys(df, price_increase, num)

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

        # expensive_products_to_db = get_best_buys(modified_df)

    # cheap_products_to_db = get_worst_buys(modified_df)


class PnPGetProductData(Resource):
    def get(self, title):
        title = title.replace("@forwardslash@", "/")

        print(title)
        basedir = os.path.abspath(os.path.dirname(__file__))
        path = "sqlite:///" + os.path.join(basedir, "..", "..", "data.sqlite")
        cnx = create_engine(path, connect_args={"check_same_thread": False}).connect()

        df = pd.read_sql("pnp_clean_df", cnx)
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
