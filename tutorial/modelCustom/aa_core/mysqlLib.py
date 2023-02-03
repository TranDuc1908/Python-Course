import mysql.connector

from scrapy.utils.project import get_project_settings
settings=get_project_settings()

mydb = mysql.connector.connect(
  host      = settings.get("MYSQL_HOST"),
  port      = settings.get("MYSQL_PORT"),
  user      = settings.get("MYSQL_USER"),
  password  = settings.get("MYSQL_PASSWORD"),
  database  = settings.get("MYSQL_DB")
)
mycursor = mydb.cursor()

# mycursor.execute("CREATE DATABASE python_practice")

# mycursor.execute("SHOW DATABASES")
# for x in mycursor:
#   print(x)

# mycursor.execute("CREATE TABLE categories (title VARCHAR(255), url VARCHAR(255))")

# mycursor.execute("SHOW TABLES")
# for x in mycursor:
#   print(x)

# mycursor.execute("alter table categories add column created_at DATETIME, add column updated_at DATETIME, add column deleted_at DATETIME")
# mycursor.execute("alter table categories add column `parent_id` int(10) null default '0' after url")

class dbbasic(object):
    def __init__(self, pkey, tbl):
      self.pkey = pkey
      self.tbl = tbl
    def showInfo(self):
      print(self.pkey + "|" + self.tbl)
        