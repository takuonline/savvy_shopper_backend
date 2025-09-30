import numpy as np
import pandas as pd
from website.dummy_objects.product_change_value import ProductChangeValue
from website.dummy_objects.firebase_helper import FirebaseHelper
from website.dummy_objects.dynamo_db_helper import DynamodbHelper
import multiprocessing as mp
from threading import Thread

import json


class DbHelper:
    ###################################################
    # array_size = 30_000
    # cheap_products = mp.Array("f",array_size)
    # expensive_products =  mp.Array("f",array_size)
    # no_change =  mp.Array("f",array_size)
    # unknown =  mp.Array("f",array_size)
    ###################################################

    cheap_products = []
    expensive_products = []
    no_change = []
    unknown = []

    # data going to database
    price_decrease = []  # mp.Array("f",array_size)
    price_increase = []  # mp.Array("f",array_size)

    def retrieve_and_clean_data(
        self, keyname, db_url, table_name, BestBuys, WorstBuys, CleanDf
    ):
        from website import db
        import pandas as pd

        db.create_all()
        # df = FirebaseHelper.load_from_firebase_db(
        #     keyname,
        #     db_url,
        #     table_name,
        # )

        # df = pd.read_csv("pnp_data.csv").drop('Unnamed: 0',axis=1)

        if len(df):
            from datetime import datetime

            print(".......................starting.........\n" * 10)
            print("len of df:  ", len(df))

            start = datetime.now()
            print("start: ", start)

            self.clean_old_data(BestBuys, WorstBuys, CleanDf)
            print("after clean_old_data: ", datetime.now() - start)

            modified_df = self.clean_df(df)

            print("after clean_df: ", datetime.now() - start)

            df_list = [df[df["title"] == unique] for unique in df["title"].unique()[:]]

            print("after df list: ", datetime.now() - start)

            for product_df in df_list[:]:
                self.process_all_data(product_df, db, BestBuys, WorstBuys)
            print("after process_all_data loop : ", datetime.now() - start)

            end = datetime.now()
            print("start: ", start)
            print("duration: ", datetime.now() - start)

            # print("after prev step: ",t1-start)
            # print("after clean_old_data start: ",t1 - start)

            # print("after clean_df step: ",t2 - t1)
            # print("after clean_df from start: ",t2 - start)

            # self.process_data(modified_df)
            # self.further_processing(modified_df)
            # self.store_data(BestBuys, WorstBuys)

        ##############################################################################
        # import time

        # start = time.time()

        # self.clean_old_data(BestBuys, WorstBuys, CleanDf)

        # t1 = time.time()

        # modified_df = self.clean_df(df)

        # t2 = time.time()

        # self.process_data(modified_df)

        # t3 = time.time()

        # self.further_processing(modified_df)

        # t4 = time.time()

        # self.store_data(BestBuys, WorstBuys)

        # end = time.time()

        # print("start time: ",start)

        # print("after prev step: ",t1-start)
        # print("after clean_old_data start: ",t1 - start)

        # print("after clean_df step: ",t2 - t1)
        # print("after clean_df from start: ",t2 - start)

        # print("after process_data step: ",t3 - t2)
        # print("after process_data from start: ",t3 - start)

        # print("after further_processing step: ",t4 - t3)
        # print("after further_processing from start: ",t4 - start)

        # print("after store_data step: ",end - t4)
        # print("after store_data from start: ",end - start)
        ##############################################################################

        else:
            raise Exception("Unable to fetch data from firebase.")

    def process_all_data(self, df, _db, BestBuys, WorstBuys):
        # get product name
        item_name = df["title"].iloc[0]
        _product_prices = df.sort_values("date")["price"]

        if len(_product_prices):
            average_price = _product_prices.mean()
            last_price = _product_prices.iloc[-1]
            percentage_change = (last_price - average_price) * 100 / average_price

            #             current_price = _product_price.iloc[-1]
            if last_price < average_price:
                # cheap
                _db.session.add(BestBuys(item_name, percentage_change))
                _db.session.commit()

            elif last_price == average_price:
                pass
                # no change
            elif last_price > average_price:
                # expensive
                _db.session.add(WorstBuys(item_name, percentage_change))
                _db.session.commit()
            else:
                # unknown item
                pass
        else:
            pass

    #     def retrieve_and_clean_data(
    #         self, keyname, db_url, table_name, BestBuys, WorstBuys, CleanDf
    #     ):
    #         from website import db

    #         db.create_all()
    #         df = FirebaseHelper.load_from_firebase_db(
    #             keyname,
    #             db_url,
    #             table_name,
    #         )

    #         if len(df):
    #             self.clear_old_data(BestBuys, WorstBuys, CleanDf)
    # # =============================================================

    #             # print("Processing data...\n"*7)

    #             # cpu_count = mp.cpu_count()
    #             # df_list = np.array_split(df,cpu_count)
    #             # cleaning_pool = mp.Pool(cpu_count)
    #             # dfs = cleaning_pool.map(self.clean_df ,df_list)
    #             # # processes = [ mp.Process(target= self.clean_df,args=(df_,))   for df_ in df_list   ]
    #             # # dfs = [i.start() for i in processes]
    #             # # dfs = [i.join() for i in dfs]
    #             # modified_df = pd.concat(dfs)
    #             # print(len(dfs))
    #             # print(type(dfs))

    # # =============================================================

    #             modified_df = self.clean_df(df)

    #             self.store_df(modified_df)

    # ##################################################################################################################

    #             # processing_pool = mp.Pool(cpu_count)
    #             # processing_pool.starmap(self.process_data , [(df_,
    #             #                                                 self.cheap_products,
    #             #                                                 self.no_change,
    #             #                                                 self.expensive_products,
    #             #                                                 self.unknown) for df_ in dfs   ])

    #             # processes = [ mp.Process(target= self.process_data,args=(df_,
    #             #                                                     self.cheap_products,
    #             #                                                     self.no_change,
    #             #                                                     self.expensive_products,
    #             #                                                     self.unknown)
    #             #                                                     )   for df_ in dfs   ]
    #             # processes = [i.start() for i in processes]
    #             # _ = [i.join() for i in processes]

    #             self.process_data(modified_df)
    #             self.further_processing(modified_df)
    #             self.store_data(BestBuys, WorstBuys)

    #         else:
    #             raise Exception(
    #                 "Unable to fetch data from firebase. db is empty"
    #             )
    #         print(" Done Done Done"*25)

    #     def dynamodb_retrieve_and_clean_data(
    #         self, table_name, BestBuys, WorstBuys, CleanDf
    #     ):
    #         from website import db

    #         db.create_all()

    #         df = DynamodbHelper.load_from_dynamodb(
    #             table_name=table_name,
    #         )

    #         if len(df):

    #             self.clean_old_data(BestBuys, WorstBuys, CleanDf)

    #             # modified_df = self.clean_df(df)

    #             df_list = np.array_split(df,mp.cpu_count())
    #             cpu_count = mp.cpu_count()

    #             pool = mp.Pool(cpu_count)
    #             dfs = pool.map(self.clean_df ,df_list)
    #             modified_df = pd.concat(dfs)

    # ##################################################################################################################

    #             # processes = [ mp.Process(target= self.process_data,args=(df_,
    #             #                                                         self.cheap_products,
    #             #                                                         self.no_change,
    #             #                                                         self.expensive_products,
    #             #                                                         self.unknown)
    #             #                                                         ) for df_ in dfs   ]
    #             # processes = [i.start() for i in processes]
    #             # modified_df = [i.join() for i in processes]

    #             process_pool = mp.Pool(cpu_count)
    #             process_pool.starmap(self.process_data ,[(df_,
    #                                                 self.cheap_products,
    #                                                 self.no_change,
    #                                                 self.expensive_products,
    #                                                 self.unknown) for df_ in dfs   ])

    #             # self.process_data(modified_df)

    #             self.further_processing(modified_df)

    #             self.store_data(BestBuys, WorstBuys)
    #         else:
    #             raise Exception(
    #                 "Unable to fetch data from firebase. Please check DynamodbHelper file"
    #             )

    def process_data(self, df, cheap_products, no_change, expensive_products, unknown):
        for item_name in df["title"].unique():
            if len(df[df["title"] == item_name]["price"]) > 0:
                mean = df[df["title"] == item_name]["price"].mean()
                last_figure = df[df["title"] == item_name]["price"].iloc[-1]

                if last_figure < mean:
                    # cheap
                    for i, k in enumerate(cheap_products):
                        if k == None:
                            cheap_products[i] = item_name
                            break

                elif last_figure == mean:
                    # no change
                    for i, k in enumerate(no_change):
                        if k == None:
                            no_change[i] = item_name
                            break
                    # no_change.append(item_name)

                elif last_figure > mean:
                    # expensive
                    for i, k in enumerate(expensive_products):
                        if k == None:
                            expensive_products[i] = item_name
                            break

                    # expensive_products.append(item_name)

                else:
                    # unknown item
                    for i, k in enumerate(unknown):
                        if k == None:
                            unknown[i] = item_name
                            break
                    # unknown.append(item_name)
            else:
                # unknown item
                for i, k in enumerate(unknown):
                    if k == None:
                        unknown[i] = item_name
                        break
                # unknown.append(item_name)

    def further_processing(self, df):
        # computes the min , max , average price for each unique item
        # these values are used for the y coordinate for the bar graph

        for product_name in self.cheap_products:
            if len(df[df["title"] == product_name]["price"]) > 0:
                current_price = df[df["title"] == product_name]["price"].iloc[-1]

                average_price = df[df["title"] == product_name]["price"].mean()

                percentage_change = (
                    (current_price - average_price) * 100 / average_price
                )

                self.price_decrease.append(
                    ProductChangeValue(percentage_change, product_name)
                )

        for product_name in self.expensive_products:
            if len(df[df["title"] == product_name]["price"]) > 0:
                current_price = df[df["title"] == product_name]["price"].iloc[-1]

                average_price = df[df["title"] == product_name]["price"].mean()

                percentage_change = (
                    (current_price - average_price) * 100 / average_price
                )

                self.price_increase.append(
                    ProductChangeValue(percentage_change, product_name)
                )

    def clear_old_data(self, BestBuys, WorstBuys, CleanDf):
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
        x = json.loads(x.replace("'", '"'))
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
