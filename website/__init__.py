from flask import Flask
from flask_restful import Api

from website.grocery.shoprite.shoprite_api import (
    ShopriteAdmin,
    ShopriteClient,
    ShopriteGetProductData,
)
from website.grocery.pnp.pnp_api import (
    PnPClient, 
    PnPGetProductData, 
    PnPAdmin
)
from website.grocery.woolies.woolies_api import (
    WooliesClient,
    WooliesGetProductData,
    WooliesAdmin,
)

from website.pc.computermania.computermania_api import (
    ComputermaniaClient,
    ComputermaniaGetProductData,
    ComputermaniaAdmin,
)
from website.pc.hifi.hifi_api import HifiClient, HifiGetProductData, HifiAdmin
from website.pc.takealot.takealot_api import (
    TakealotClient,
    TakealotGetProductData,
    TakealotAdmin,
)
from website.pc.game.game_api import GameClient, GameGetProductData, GameAdmin

from website.pc.makro.makro_api import MakroClient, MakroGetProductData, MakroAdmin

from website.clothing.foschini.foschini_api import (
    FoschiniClient,
    FoschiniGetProductData,
    FoschiniAdmin,
)
from website.clothing.markham.markham_api import (
    MarkhamClient,
    MarkhamGetProductData,
    MarkhamAdmin,
)
from website.clothing.sportscene.sportscene_api import (
    SportsceneClient,
    SportsceneGetProductData,
    SportsceneAdmin,
)
from website.clothing.woolworths_clothing.woolworths_clothing_api import (
    WoolworthsClothingClient,
    WoolworthsClothingGetProductData,
    WoolworthsClothingAdmin,
)
from website.clothing.superbalist.superbalist_api import (
    SuperbalistClient,
    SuperbalistGetProductData,
    SuperbalistAdmin,
)
from website.clothing.mrp.mrp_api import MrpClient, MrpGetProductData, MrpAdmin


from flask_sqlalchemy import SQLAlchemy
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "<h1 style={font-size:3.5rem; margin-top: 7rem; text-align: center; }>Nothing to see here😎</h1>"


basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    basedir, "data.sqlite"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

api = Api(app)


#####################
# Groceries
#####################
api.add_resource(ShopriteAdmin, "/admin")
api.add_resource(ShopriteClient, "/client")


api.add_resource(PnPAdmin, "/pnp-admin")
api.add_resource(PnPClient, "/pnp-client")


api.add_resource(WooliesAdmin, "/woolies-admin")
api.add_resource(WooliesClient, "/woolies-client")

##########################
# pc components
##########################

api.add_resource(ComputermaniaAdmin, "/computermania-admin")
api.add_resource(ComputermaniaClient, "/computermania-client")


api.add_resource(HifiAdmin, "/hifi-admin")
api.add_resource(HifiClient, "/hifi-client")


api.add_resource(TakealotAdmin, "/takealot-admin")
api.add_resource(TakealotClient, "/takealot-client")

api.add_resource(GameAdmin, "/game-admin")
api.add_resource(GameClient, "/game-client")

api.add_resource(MakroAdmin, "/makro-admin")
api.add_resource(MakroClient, "/makro-client")

##########################
# clothing
##########################

api.add_resource(FoschiniAdmin, "/foschini-admin")
api.add_resource(FoschiniClient, "/foschini-client")


api.add_resource(MarkhamAdmin, "/markham-admin")
api.add_resource(MarkhamClient, "/markham-client")


api.add_resource(SportsceneAdmin, "/sportscene-admin")
api.add_resource(SportsceneClient, "/sportscene-client")


api.add_resource(WoolworthsClothingAdmin, "/woolworths-clothing-admin")
api.add_resource(WoolworthsClothingClient, "/woolworths-clothing-client")


api.add_resource(SuperbalistAdmin, "/superbalist-admin")
api.add_resource(SuperbalistClient, "/superbalist-client")


api.add_resource(MrpAdmin, "/mrp-admin")
api.add_resource(MrpClient, "/mrp-client")


##########################
# get data
##########################

api.add_resource(ShopriteGetProductData, "/get-product-data/<string:title>")
api.add_resource(PnPGetProductData, "/pnp-get-product-data/<string:title>")
api.add_resource(WooliesGetProductData, "/woolies-get-product-data/<string:title>")

api.add_resource(ComputermaniaGetProductData, "/computermania-get-product-data/<string:title>")
api.add_resource(HifiGetProductData, "/hifi-get-product-data/<string:title>")
api.add_resource(TakealotGetProductData, "/takealot-get-product-data/<string:title>")
api.add_resource(GameGetProductData, "/game-get-product-data/<string:title>")
api.add_resource(MakroGetProductData, "/makro-get-product-data/<string:title>")

api.add_resource(FoschiniGetProductData, "/foschini-get-product-data/<string:title>")
api.add_resource(MarkhamGetProductData, "/markham-get-product-data/<string:title>")
api.add_resource(SportsceneGetProductData, "/sportscene-get-product-data/<string:title>")
api.add_resource(WoolworthsClothingGetProductData,"/woolworths-clothing-get-product-data/<string:title>",)
api.add_resource(SuperbalistGetProductData, "/superbalist-get-product-data/<string:title>")
api.add_resource(MrpGetProductData, "/mrp-get-product-data/<string:title>")
