import os
import pandas as pd
import numpy as np
from website import db
from website.pc.takealot.takealot_models import (
    TakealotBestBuys,
    TakealotWorstBuys,
    TakealotCleanDf,
)
from sqlalchemy import create_engine
from website.dummy_objects.dummy_db_helper import DbHelper

import logging

logging.basicConfig(
    level=logging.DEBUG,
    filemode="w",
    format="%(asctime)s - %(levelname)s - %(message)s",
)


class TakealotDbHelper(DbHelper):
    def __init__(self):
        DbHelper.__init__(self)

    def takealot_retrieve_and_clean_data(self):
        self.retrieve_and_clean_data(
            keyname="pc-components.json",
            db_url="https://pc-components-77a24-default-rtdb.firebaseio.com/",
            table_name="takealot",
            BestBuys=TakealotBestBuys,
            WorstBuys=TakealotWorstBuys,
            CleanDf=TakealotCleanDf,
        )

    def clean_df(self, df):
        # cleaning the data

        df["date"] = pd.to_datetime(df["date"])
        df["price"] = df["price"].apply(lambda x: float(x[0]))

        df["date_only"] = df["date"].dt.date
        df = df.drop_duplicates(subset=["title", "date_only"], keep=False)

        df.drop(["savings", "date_only", "listing_price"], axis=1, inplace=True)

        df["image_url"] = df["image_url"].apply(lambda x: x.replace("{size}", "fb"))

        df["brand"].fillna("Other")

        basedir = os.path.abspath(os.path.dirname(__file__))
        path = "sqlite:///" + os.path.join(basedir, "..", "..", "data.sqlite")
        cnx = create_engine(path, connect_args={"check_same_thread": False}).connect()

        df.to_sql("takealot_clean_df", cnx, if_exists="replace")

        return df

    @staticmethod
    def get_best_buys(df, price_decrease, num):
        # sort price_decrease list according to the price changes
        newlist = sorted(price_decrease, key=lambda x: x.price, reverse=False)

        # get the top n product into dict format and put in list

        cheap_products_list = []
        for i in newlist[:num]:
            df_item = df[df["title"] == i.title]
            if len(df_item) != 0:
                product_dict = {
                    i.title: {
                        "brand": df_item["brand"].iloc[0]
                        if (len(df_item["brand"]) > 0)
                        else "Other",
                        "image_url": df_item["image_url"].sort_values().iloc[0],
                        "prices_list": list(df_item["price"]),
                        "dates": list(df_item["date"].astype(str)),
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
            df_item = df[df["title"] == i.title]

            if len(df_item) != 0:
                url = df_item["image_url"].sort_values().iloc[0]
                product_dict = {
                    i.title: {
                        "brand": df_item["brand"].iloc[0]
                        if len(df_item["brand"]) > 0
                        else "Other",
                        "image_url": url,
                        "prices_list": list(df_item["price"]),
                        "dates": list(df_item["date"].astype(str)),
                        "change": i.price,
                    }
                }
                expensive_products_list.append(product_dict)

        return expensive_products_list


# #process data into different classes

# cheap_products = []

# expensive_products = []

# no_change = []

# unknown = []


# ############################

#         # data going to database

# all_products = []
# price_decrease = []
# price_increase =  []
# #############################

# # cheap_products_to_db = []
# # expensive_products_to_db = []


# def takealot_retrieve_and_clean_data():

#     db.create_all()

#     clean_old_data()

#     df = load_from_db()

#     modified_df = clean_df(df)

#     # print(modified_df.head())

#     process_data(modified_df)

#     further_processing(modified_df)

#     store_data()


# def load_from_db():

#     if (not len(firebase_admin._apps)):
#         basedir = os.path.abspath(os.path.dirname(__file__))
#         # Fetch the service account key JSON file contents
#         path =  os.path.join(basedir,"..","..","..", "keys","pc-components.json")

#         cred = credentials.Certificate(path)

#         # Initialize the app with a service account, granting admin privileges
#         firebase_admin.initialize_app(cred, {
#             'databaseURL': 'https://pc-components-77a24-default-rtdb.firebaseio.com/'
#         })

#     ref = fdb.reference("takealot")

#     # As an admin, the app has access to read and write all data, regradless of Security Rules
#     response = ref.get()

#     return pd.DataFrame.from_dict(response,orient="index")


# def clean_df(df):
#     #cleaning the data

#     df["date"] = pd.to_datetime(df["date"])
#     df["price"] = df["price"].apply(lambda x: float(x[0]) )


#     df["date_only"] = df["date"].dt.date
#     df =  df.drop_duplicates(subset = ["title",'date_only'], keep = 'last')

#     df.drop(["savings","date_only","listing_price"],axis=1,inplace=True)

#     df["image_url"] = df["image_url"].apply(lambda x: x.replace("{size}","fb"))

#     df["brand"].fillna("Other")

#     basedir = os.path.abspath(os.path.dirname(__file__))
#     path = "sqlite:///" + os.path.join(basedir,"..","..","data.sqlite")
#     cnx = create_engine(path,connect_args={'check_same_thread': False}).connect()

#     df.to_sql("takealot_clean_df", cnx ,if_exists="replace")

#     return df


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

#     db.session.query(TakealotBestBuys).delete()
#     db.session.commit()

#     db.session.query(TakealotWorstBuys).delete()
#     db.session.commit()

#     db.session.query(TakealotCleanDf).delete()
#     db.session.commit()


# def store_data():

#     # 3 things are stored

#     # all products
#     db.session.add_all([ TakealotAllProductList(i) for i in all_products ])
#     db.session.commit()

#     # cheap

#     db.session.add_all([ TakealotBestBuys(i.title,i.price) for i in price_decrease ])
#     db.session.commit()

#     # expensive
#     db.session.add_all([ TakealotWorstBuys(i.title,i.price) for i in price_increase ])
#     db.session.commit()
