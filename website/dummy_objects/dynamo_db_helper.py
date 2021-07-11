import boto3
from boto3.dynamodb.conditions import Key
import pandas as pd
import datetime
import os

from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

ACCESS_ID = os.environ["ACCESS_ID"]
ACCESS_KEY = os.environ["ACCESS_KEY"]


class DynamodbHelper:

    @staticmethod
    def load_from_dynamodb(table_name, dynamodb=None):
        items = []

        #  get the start and end data and reformat to make the db UTC
        start_date = datetime.datetime.now() - pd.DateOffset(months=3) 
        start_date = start_date.strftime('%FT%T+13:00')
        end_date =  datetime.datetime.now().strftime('%FT%T+13:00')
        
 
        if not dynamodb:
            dynamodb = boto3.resource(
                "dynamodb",
                region_name="us-east-2",
                endpoint_url="https://dynamodb.us-east-2.amazonaws.com",
                aws_access_key_id=ACCESS_ID,
                aws_secret_access_key=ACCESS_KEY,
            )

        table = dynamodb.Table(table_name)

        scan_kwargs = { 
        "FilterExpression": Key('date').between(start_date,end_date)
        }

        done = False # flag to escape loop
        start_key = None #this is the last item in query from a single page
        while not done:
            print(start_key, scan_kwargs, sep="\n")

            if start_key:
                scan_kwargs["ExclusiveStartKey"] = start_key
            response = table.scan(**scan_kwargs)
            items.append(response.get("Items", []))
            start_key = response.get("LastEvaluatedKey", None)
            done = start_key is None

        flat_list = [item for sublist in items for item in sublist]
        return pd.DataFrame.from_dict(data=flat_list)

 