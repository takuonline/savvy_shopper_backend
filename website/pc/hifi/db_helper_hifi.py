import os

import pandas as pd
import numpy as np
from website import db
from website.pc.hifi.hifi_models import HifiBestBuys, HifiWorstBuys, HifiCleanDf
from sqlalchemy import create_engine

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db as fdb

from config.config import AccessoriesConfig

from website.dummy_objects.product_change_value import ProductChangeValue
from website.dummy_objects.dummy_db_helper import DbHelper
from website.dummy_objects.firebase_helper import FirebaseHelper
import logging

logging.basicConfig(
    level=logging.DEBUG,
    filemode="w",
    format="%(asctime)s - %(levelname)s - %(message)s",
)


class HifiDbHelper(DbHelper):
    def __init__(self):
        DbHelper.__init__(self)

    def hifi_retrieve_and_clean_data(self):
        self.retrieve_and_clean_data(
            keyname="pc-components.json",
            db_url="https://pc-components-77a24-default-rtdb.firebaseio.com/",
            table_name="hifi",
            BestBuys=HifiBestBuys,
            WorstBuys=HifiWorstBuys,
            CleanDf=HifiCleanDf,
        )

    def clean_df(self, df):
        # cleaning the data

        df.dropna(subset=["price"], inplace=True)

        df["date"] = pd.to_datetime(df["date"])

        df["price"] = df["price"].apply(self.to_float_if_has_special_price)

        df["title"] = df["title"].apply(lambda x: x.replace("\n", ""))

        df["title"] = df["title"].apply(
            lambda x: x.strip().lower() if type(x) != float else x
        )

        df["date_only"] = df["date"].dt.date
        df.drop_duplicates(subset=["title", "date_only"], keep=False, inplace=True)

        df.drop(["date_only"], axis=1, inplace=True)

        # basedir = os.path.abspath(os.path.dirname(__file__))
        # path = "sqlite:///" + os.path.join(basedir, "..", "..", "data.sqlite")

        cnx = create_engine(
            AccessoriesConfig.DB_URI, connect_args={"check_same_thread": False}
        ).connect()

        df.to_sql("hifi_clean_df", cnx, if_exists="replace")

        return df

    @staticmethod
    def get_best_buys(df, price_decrease, num):
        # sort price_decrease list according to the price changes
        newlist = sorted(price_decrease, key=lambda x: x.price, reverse=False)

        # get the top n product into dict format and put in list
        cheap_products_list = []
        for i in newlist[:num]:
            if len(df[df["title"] == i.title]) != 0:
                try:
                    img_url = (
                        df[df["title"] == i.title]["image_url"].sort_values().iloc[0]
                    )
                except KeyError:
                    img_url = None

                product_dict = {
                    i.title: {
                        "image_url": img_url,
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
                try:
                    img_url = (
                        df[df["title"] == i.title]["image_url"].sort_values().iloc[0]
                    )
                except KeyError:
                    img_url = None

                product_dict = {
                    i.title: {
                        "image_url": img_url,
                        "prices_list": list(df[df["title"] == i.title]["price"]),
                        "dates": list((df[df["title"] == i.title]["date"].astype(str))),
                        "change": i.price,
                    }
                }
                expensive_products_list.append(product_dict)

        return expensive_products_list


# def hifi_retrieve_and_clean_data():

#     db.create_all()

#     clean_old_data()

#     df = load_from_db()

#     modified_df = clean_df(df)

#     # print(modified_df.head())

#     process_data(modified_df)

#     further_processing(modified_df)

#     store_data()

# def to_float(x):

#     if(x != "Special Price"):
#         try:

#             return float(x.replace("R","").replace(",",""))
#         except AttributeError:
#             return x
#     else:
#         np.nan


# def load_from_db():

#     if (not len(firebase_admin._apps)):
#         basedir = os.path.abspath(os.path.dirname(__file__))
#         # Fetch the service account key JSON file contents
#         path =  os.path.join(basedir,"..", "..","..", "keys","pc-components.json")

#         cred = credentials.Certificate(path)

#         # Initialize the app with a service account, granting admin privileges
#         firebase_admin.initialize_app(cred, {
#             'databaseURL': 'https://pc-components-77a24-default-rtdb.firebaseio.com/'
#         })

#     ref = fdb.reference("hifi")

#     # As an admin, the app has access to read and write all data, regradless of Security Rules
#     response = ref.get()

#     return pd.DataFrame.from_dict(response,orient="index")


# def process_data(df):
#     #classify data into cheap, expensive , non food items and the no change classes
#     for item_name in df["title"].unique():
#         # count = df[df["title"] == item_name]["price"].count()
#         mean = df[df["title"] == item_name]["price"].mean()


#         last_figure = df[df["title"] == item_name]["price"].iloc[-1]

#         if (last_figure < mean):
#             # cheap
#             cheap_products.append(item_name)

#         elif (last_figure == mean):
#             #no change
#             no_change.append(item_name)

#         elif (last_figure > mean):
#             #expensive
#             expensive_products.append(item_name)

#         else:
#             #unknow item
#             unknown.append(item_name)


# # send list


# def further_processing(df):
#     # computes the min , max , average price for each unique item
#     # these values are used for the y coordinate for the bar graph


#     for product_name in cheap_products:

#         current_price =  df[df["title"]==product_name]["price"].iloc[-1]

#         average_price = df[df["title"]==product_name]["price"].mean()

#         percentage_change = (current_price-average_price)*100/average_price

#         price_decrease.append(ProductChangeValue(percentage_change,product_name))


#     for product_name in expensive_products:

#         current_price =  df[df["title"]==product_name]["price"].iloc[-1]

#         average_price = df[df["title"]==product_name]["price"].mean()

#         percentage_change = (current_price-average_price)*100/average_price

#         price_increase.append(ProductChangeValue(percentage_change,product_name))


# def clean_old_data():

#     db.session.query(HifiBestBuys).delete()
#     db.session.commit()

#     db.session.query(HifiWorstBuys).delete()
#     db.session.commit()


#     db.session.query(HifiCleanDf).delete()
#     db.session.commit()


# def store_data():

#     # 3 things are stored


#     # all products
#     db.session.add_all([ HifiAllProductList(i) for i in all_products ])
#     db.session.commit()

#     # cheap

#     db.session.add_all([ HifiBestBuys(i.title,i.price) for i in price_decrease ])
#     db.session.commit()

#     # expensive
#     db.session.add_all([ HifiWorstBuys(i.title,i.price) for i in price_increase ])
#     db.session.commit()
