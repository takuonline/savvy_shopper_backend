import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db as fdb
import pandas as pd
import logging
from datetime import datetime
from requests.exceptions import SSLError
import traceback


class FirebaseHelper:
    @staticmethod
    def load_from_firebase_db(keyname, db_url, table_name):
        start_date = str(datetime.now() - pd.DateOffset(months=2))
        end_date = str(datetime.now())

        for i in range(7):
            try:
                basedir = os.path.abspath(os.path.dirname(__file__))
                path = os.path.join(basedir, "..", "..", "keys", keyname)

                # Fetch the service account key JSON file contents
                if not len(firebase_admin._apps):
                    cred = credentials.Certificate(path)
                    # Initialize the app with a service account, granting admin privileges
                    firebase_admin.initialize_app(cred, {"databaseURL": db_url})

                ref = fdb.reference(table_name)

                response = (
                    ref.order_by_child("date")
                    .start_at(start_date)
                    .end_at(end_date)
                    .get()
                )

                return pd.DataFrame.from_dict(response, orient="index")

            except SSLError:
                logging.debug(f"Network error -----{table_name}-------->{i}")
                print(f"Network error -----{table_name}-------->{i}")
                continue

            except Exception as e:
                tb = traceback.format_exc()
                error_message = (
                    f"Non network error -----{table_name}-----{type(e).__name__}--->{i}"
                )
                logging.debug(error_message + tb)
                print(error_message + tb)
                continue

        logging.debug(f"was unable to get any of the data from --->{table_name}")

        return pd.DataFrame([])
