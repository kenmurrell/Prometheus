

class Entity(object):
    def __init__(self,name,rating,ts,product_id,scores):
        self.name = name
        self.rating = rating
        self.ts = ts
        self.product_id = product_id
        self.sp = scores["SP"]
        self.wp = scores["WP"]
        self.wn = scores["WN"]
        self.sn = scores["SN"]
