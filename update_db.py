from website.clothing.markham.markham_api import MarkhamAdmin
from website.clothing.foschini.foschini_api import FoschiniAdmin
from website.clothing.mrp.mrp_api import MrpAdmin
from website.clothing.sportscene.sportscene_api import SportsceneAdmin
from website.clothing.superbalist.superbalist_api import  SuperbalistAdmin
from website.clothing.woolworths_clothing.woolworths_clothing_api import WoolworthsClothingAdmin

from website.grocery.pnp.pnp_api import PnPAdmin
from website.grocery.shoprite.shoprite_api import ShopriteAdmin
from website.grocery.woolies.woolies_api import WooliesAdmin

from website.pc.computermania.computermania_api import ComputermaniaAdmin
from website.pc.game.game_api import GameAdmin
from website.pc.hifi.hifi_api import HifiAdmin
from website.pc.makro.makro_api import MakroAdmin
from website.pc.takealot.takealot_api import TakealotAdmin

import traceback
from datetime import datetime
import logging



# # error logger
# error_logger = logging.getLogger("update_db.error_messages")
# logger.setLevel(logging.WARNING)

# formatter = logging.Formatter("%(asctime)s:    %(levelname)s -  %(funcName)s - %(message)s")

# fh = logging.FileHandler(r"update_logs/errors.log")
# fh.setLevel(logging.DEBUG)
# fh.setFormatter(formatter)

# sh = logging.StreamHandler()  # for cmd logging
# # add streamheandler to root logger
# logging.getLogger('').addHandler(sh)
# error_logger.addHandler(fh)
# error_logger.addHandler(sh)


# # response logger
# fh_response = logging.FileHandler(r"update_logs/response.log")
# fh_response.setLevel(logging.DEBUG)
# fh_response.setFormatter(formatter)

# response_logger = logging.getLogger("update_db.response_logger")
# response_logger.addHandler(fh_response)
# response_logger.addHandler(sh)



# # success logger
# fh_succesful = logging.FileHandler(r"update_logs/succesful.log")
# fh_succesful.setLevel(logging.DEBUG)
# fh_succesful.setFormatter(formatter)

# succesful_logger = logging.getLogger("update_db.succesful_logger")
# succesful_logger.addHandler(fh_succesful)
# succesful_logger.addHandler(sh)
    


# # general logger
# fh_general = logging.FileHandler(r"update_logs/general_db_update.log")
# fh_general.setLevel(logging.DEBUG)
# fh_general.setFormatter(formatter)

# general_logger = logging.getLogger("update_db.general_logger")
# general_logger.addHandler(fh_general)
# general_logger.addHandler(sh)
    
 

stores = [

# PnPAdmin,
# ShopriteAdmin,
# WooliesAdmin,

# ComputermaniaAdmin,
# GameAdmin,
HifiAdmin,
# MakroAdmin,
# TakealotAdmin,

# MarkhamAdmin,
# MrpAdmin,
# SportsceneAdmin,
# WoolworthsClothingAdmin,
# FoschiniAdmin,
# SuperbalistAdmin,

]

failed = []
successful = []

def get_data(store):
    for i in range(1,4):
        starting_time = datetime.now()
        try:
            # general_logger.info("\n",store.__name__,f" attempt number {i}\n")
            print("\n",store.__name__,f" attempt number {i}\n")
            admin = store()
            response = admin.get()

            successful.append(store.__name__)
            
            return {
            "response":response,
            "message": f"{store.__name__} has successfully been updated",
            "store": store.__name__,
            }
        except Exception as e:
            error_message = f"Received Error for {store.__name__}: " + str(type(e).__name__) + "\n"
                   
            tb = traceback.format_exc()
           # error_logger.warning(str(tb) + str(error_message) + str(store.__name__) +" "+ f"attempt number {i}\n" )

            print(tb)
            print(error_message)
            finish_time = datetime.now()
            time = finish_time - starting_time

            with open("updates_logs/errors.txt","a") as f:
                f.write(str(tb) + str(error_message) + str(store.__name__) \
                    +" "+ f"attempt number {i} \n" + f"time: {time}\n" \
                    +f"finishing time: {finish_time}\n" +
                    f"starting time time: {starting_time}"  + "\n\n\n" )
            continue
    
    finish_time = datetime.now()
    time = finish_time - starting_time
    print(f"{store.__name__} has failed to update")
    failed.append(store.__name__)

    return {"message" : f"store {store.__name__} has failed",
            "store": store.__name__,
            "response":None,
            "starting time": str(starting_time),
            "finishing time": str(finish_time),
            "time": str(time),
             }



if __name__ == '__main__':
    for store in stores:
        response = get_data(store)
        # print(failed,"\n")

        with open("updates_logs/response_to_update.txt","a") as f:
            f.write(response.get("message","") +"    "+ response.get("store","") +"   " + str(response.get("response",""))  + "\n")

   
        with open("updates_logs/successful.txt","w") as f:
            for i in successful:
                f.write(str(datetime.now())+" " + str(i) + "\n")

        with open("updates_logs/failed_to_update.txt","w") as f:
            for i in failed:
                f.write(str(i) + "\n")

 
