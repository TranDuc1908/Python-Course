from tutorial.modelCustom.aa_core.mysqlLib import dbbasic as mysqlLib

class Category(mysqlLib):
    def __init__(self):
        self.pkey   = "id"
        self.tbl    = "categories"
        mysqlLib.__init__(self, self.pkey, self.tbl)