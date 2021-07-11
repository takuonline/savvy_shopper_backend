
				List of all the spiders

e_scrapy  ---- shoprite, hifi, computermania, takealot , mrp, makro, game

e_grocery ---- woolworths, pnp 

e_clothing  ---- foschini, sportscene, markham, speedtrainer, woolworths_clothing, superbalist

===============================================================================
      				List of Database structure
		mongodb

- shoprite

		firebase realtime db
pc components
-hifi
-takealot
-computermania
-markham
-speedtrainer

e-clothing ---full
-foschini*
-woolies-clothing*
-sportscene*
-superbalist*

e-grocery
- woolworths
- pnp

		dynamodb
-makro
-mrp
-game

-foschini
-woolies-clothing
-sportscene
-superbalist

* is full
================================================================================
--- clothing

curl https://e-clothing-sa.herokuapp.com/schedule.json -d project=default -d spider=foschini

curl https://e-clothing-sa.herokuapp.com/schedule.json -d project=default -d spider=markham

curl https://e-clothing-sa.herokuapp.com/schedule.json -d project=default -d spider=sportscene

curl https://e-clothing-sa.herokuapp.com/schedule.json -d project=default -d spider=speedtrainer

curl https://e-clothing-sa.herokuapp.com/schedule.json -d project=default -d spider=woolworths_clothing

--- grocery

curl https://e-grocery-sa.herokuapp.com/schedule.json -d project=default -d spider=pnp

curl https://e-grocery-sa.herokuapp.com/schedule.json -d project=default -d spider=woolworths


--- e-scrapy

curl https://e-scrapy.herokuapp.com/schedule.json -d project=default -d spider=takealot

curl https://e-scrapy.herokuapp.com/schedule.json -d project=default -d spider=hifi

curl https://e-scrapy.herokuapp.com/schedule.json -d project=default -d spider=computermania

curl https://e-scrapy.herokuapp.com/schedule.json -d project=default -d spider=e-commerce

====================================================================================
************************************************************************************
       

====================================================================================
************************************************************************************
