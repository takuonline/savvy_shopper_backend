import numpy as np
from website.dummy_objects.product_change_value import ProductChangeValue
from website.dummy_objects.firebase_helper import FirebaseHelper
from website.dummy_objects.dynamo_db_helper import DynamodbHelper
import json

class DbHelper:
    cheap_products = []
    expensive_products = []
    no_change = []
    unknown = []

    # data going to database
    price_decrease = []
    price_increase = []

 
    def retrieve_and_clean_data(
        self, keyname, db_url, table_name, BestBuys, WorstBuys, CleanDf
    ):
        from website import db

        db.create_all()
        df = FirebaseHelper.load_from_firebase_db(
            keyname,
            db_url,
            table_name,
        )

        if len(df):
            self.clean_old_data(BestBuys, WorstBuys, CleanDf)
            modified_df = self.clean_df(df)

            # self.process_data(modified_df)
            # self.further_processing(modified_df)
            # self.store_data(BestBuys, WorstBuys)
            
        else:
            raise Exception(
                "Unable to fetch data from firebase."
            )

    def dynamodb_retrieve_and_clean_data(
        self, table_name, BestBuys, WorstBuys, CleanDf
    ):
        from website import db

        db.create_all()

        df = DynamodbHelper.load_from_dynamodb(
            table_name=table_name,
        )

        if len(df):

            self.clean_old_data(BestBuys, WorstBuys, CleanDf)

            modified_df = self.clean_df(df)

            # self.process_data(modified_df)

            # self.further_processing(modified_df)

            # self.store_data(BestBuys, WorstBuys)
        else:
            raise Exception(
                "Unable to fetch data from Dynamodb. Dataframe returned is empty: {}".format(len(df))
            )

    # def process_data(self, df):

    #     for item_name in df["title"].unique():

    #         if len(df[df["title"] == item_name]["price"]) > 0:

    #             mean = df[df["title"] == item_name]["price"].mean()
    #             last_figure = df[df["title"] == item_name]["price"].iloc[-1]

    #             if last_figure < mean:
    #                 # cheap
    #                 self.cheap_products.append(item_name)

    #             elif last_figure == mean:
    #                 # no change
    #                 self.no_change.append(item_name)

    #             elif last_figure > mean:
    #                 # expensive
    #                 self.expensive_products.append(item_name)

    #             else:
    #                 # unknown item
    #                 self.unknown.append(item_name)
    #         else:
                # self.unknown.append(item_name)

    # def further_processing(self, df):
    #     # computes the min , max , average price for each unique item
    #     # these values are used for the y coordinate for the bar graph

    #     for product_name in self.cheap_products:
    #         if len(df[df["title"] == product_name]["price"]) > 0:

    #             current_price = df[df["title"] == product_name]["price"].iloc[-1]

    #             average_price = df[df["title"] == product_name]["price"].mean()

    #             percentage_change = (
    #                 (current_price - average_price) * 100 / average_price
    #             )

    #             self.price_decrease.append(
    #                 ProductChangeValue(percentage_change, product_name)
    #             )

    #     for product_name in self.expensive_products:
    #         if len(df[df["title"] == product_name]["price"]) > 0:
    #             current_price = df[df["title"] == product_name]["price"].iloc[-1]

    #             average_price = df[df["title"] == product_name]["price"].mean()

    #             percentage_change = (
    #                 (current_price - average_price) * 100 / average_price
    #             )

    #             self.price_increase.append(
    #                 ProductChangeValue(percentage_change, product_name)
    #             )

    def clean_old_data(self, BestBuys, WorstBuys, CleanDf):
        from website import db

        db.session.query(BestBuys).delete()
        db.session.commit()

        db.session.query(WorstBuys).delete()
        db.session.commit()

        db.session.query(CleanDf).delete()
        db.session.commit()

    def store_data(self, BestBuys, WorstBuys):
        from website import db

        # cheap
        db.session.add_all([BestBuys(i.title, i.price) for i in self.price_decrease])
        db.session.commit()

        # expensive
        db.session.add_all([WorstBuys(i.title, i.price) for i in self.price_increase])
        db.session.commit()

    def to_float(self, x):
        try:
            return float(x.replace("R", "").replace(" ", ""))
        except:
            return x

    def to_float_if_has_special_price(self, x):

        if x != "Special Price":
            try:

                return float(x.replace("R", "").replace(",", ""))
            except AttributeError:
                return x
        else:
            np.nan

    def get_color(self, x):
        x = json.loads(x.replace("'",'"'))
        my_dict = {}

        if type(x) != float: 

            for i in x:
                my_dict[i.get("name")] = i.get("path")

            return str(my_dict)
        else:
            return np.nan

    @staticmethod
    def get_best_buys(df, price_decrease, num):

        # sort price_decrease list according to the price changes
        newlist = sorted(price_decrease, key=lambda x: x.price, reverse=False)

        # get the top n product into dict format and put in list

        cheap_products_list = []
        for i in newlist[:num]:
            product_dict = {
                i.title: {
                    "image_url": df[df["title"] == i.title]["image_url"].iloc[0],
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
            product_dict = {
                i.title: {
                    "image_url": df[df["title"] == i.title]["image_url"].iloc[0],
                    "prices_list": list(df[df["title"] == i.title]["price"]),
                    "dates": list((df[df["title"] == i.title]["date"].astype(str))),
                    "change": i.price,
                }
            }
            expensive_products_list.append(product_dict)

        # print(expensive_products_list)

        return expensive_products_list
