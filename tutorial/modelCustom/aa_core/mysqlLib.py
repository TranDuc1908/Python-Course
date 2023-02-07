import mysql.connector
import datetime

from scrapy.utils.project import get_project_settings
settings=get_project_settings()

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

class dbBasic(object):
    def __init__(self, pkey, tbl):
      self.pkey = pkey
      self.tbl = tbl
      self.conn = mysql.connector.connect(
        host      = settings.get("MYSQL_HOST"),
        port      = settings.get("MYSQL_PORT"),
        user      = settings.get("MYSQL_USER"),
        password  = settings.get("MYSQL_PASSWORD"),
        database  = settings.get("MYSQL_DB")
      )
      self.cur = self.conn.cursor(dictionary=True)
      
    def showInfo(self):
      print(self.pkey + "|" + self.tbl)

    
      
    def insertOne(self, tup):
      feilds = ""
      sqlValues = ""
      values = []
      if tup is not None:
        for dict in tup:
          for key in dict:
            feilds += "`"+key+"`,"
            sqlValues += "%s," 
            values.append(str(dict[key]))
            # values.append(u''.join((dict[key])).encode('utf-8').strip())
      feilds += "created_at"
      sqlValues += "%s"
      values.append(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
      values = tuple(values)

      sqlStr = "INSERT INTO `"+self.tbl+"`("+feilds+") VALUES ("+sqlValues+")"
      try:
        self.cur.execute(sqlStr, values)
        self.conn.commit()
        return True
      except:
        self.conn.rollback()
        return False
    
    # get all columns 
    def getAll(self, string):
      compare = str(string).strip()
      compare = compare[:5]
      if compare == "order" or compare == "limit":
        self.cur.execute("SELECT * FROM "+self.tbl+" WHERE is_trash = 0 "+string)
      else:
        self.cur.execute("SELECT * FROM "+self.tbl+" WHERE is_trash = 0 and "+string)
      res = self.cur.fetchall()
      self.cur.close()
      self.conn.close()
      return res
    
    # get id columns
    def getListId(self, string):
      self.cur.execute("SELECT "+self.pkey+" FROM "+self.tbl+" WHERE is_trash = 0 and "+string)
      res = self.cur.fetchall()
      self.cur.close()
      self.conn.close()
      return res
        
    # get a row
    def getOne(self, id):
      self.cur.execute("SELECT * FROM "+self.tbl+" WHERE is_trash = 0 and "+self.pkey+" = "+str(id))
      res = self.cur.fetchall()
      self.cur.close()
      self.conn.close()
      if res[0] is not None:
        return res[0]
      else:
        return False
      
    # update a record
    def updateOne(self, id, dict):
      sqlStr = "UPDATE "+self.tbl+" SET "
      for key in dict:
        val = dict[key]
        sqlStr += key + " = '"+str(val)+"', "
      sqlStr += "updated_at = '"+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+"' WHERE "+self.pkey+" = "+str(id)
      try:
        self.cur.execute(sqlStr)
        self.conn.commit()
        self.cur.close()
        self.conn.close()
        return True
      except:
        self.conn.rollback()
        self.cur.close()
        self.conn.close()
        return False

    # soft delete a record
    def softDelete(self, id):
      sqlStr = "UPDATE "+self.tbl+" SET `is_trash` = 1, `deleted_at` = "+datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+" WHERE id = "+str(id)
      try:
        self.cur.execute(sqlStr)
        self.conn.commit()
        self.cur.close()
        self.conn.close()
        return True
      except:
        self.conn.rollback()
        self.cur.close()
        self.conn.close()
        return False

      