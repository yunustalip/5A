from faker import Faker
import psycopg2
from time import time

class MyFaker:
    def Creator(num):
        f = Faker()
        eandp = []
        for i in range(0,num):
            eandp.append((f.email(), f.password()))
        return eandp
class conn():
    def __init__(self):
        self.db = psycopg2.connect(user = "postgres", password = "864327", host = "localhost", port = "5432",
                                   database = "postgres")
        self.imlec = self.db.cursor()
    def tablecreater(self):
        if (self.selector("""select exists(SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'public'
                          AND TABLE_NAME = 'login')""")[0][0]==False):
        
            komut_CREATE = """ CREATE TABLE login(
                            email TEXT NOT NULL,
                            password TEXT NOT NULL
                            );
                            """
            self.imlec.execute(komut_CREATE)
            self.db.commit()
        if (self.selector("""select exists(SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'public'
                          AND TABLE_NAME = 'finding')""")[0][0]==False):
            komut_CREATE = """ CREATE TABLE finding(
                            email TEXT NOT NULL,
                            password TEXT NOT NULL
                            );
                            """
            self.imlec.execute(komut_CREATE)
            self.db.commit()
    def Inserter(self,users,tablename):
        code = ""
        for i,val in enumerate(users):
            code = code + str(val)
            if (i != len(users)-1):
                code = code + ","
                
        komut_INSERT = "INSERT INTO "+tablename+" (email,password) VALUES " + code
    
        self.imlec.execute(komut_INSERT)
        self.db.commit()
        
    def selector(self,sql):
        self.imlec.execute(sql)
        if((self.imlec.statusmessage!="CREATE TABLE") and (self.imlec.statusmessage!="DROP TABLE")):
            return self.imlec.fetchall()
    

insert = conn()
insert.selector("Drop table login")
insert.selector("Drop table finding")
insert.tablecreater()

# 1. adım
userandpass = MyFaker.Creator(10000)
# 2.adım

insert.Inserter(userandpass,"login")

# 3. adım
newmaillist = insert.selector("SELECT email,password FROM login ORDER BY RANDOM() LIMIT 1000")
newmaillist.extend(MyFaker.Creator(9000))

# 4.adım
starttime = time()
insert.selector("CREATE TEMPORARY TABLE gecicitablo(email text,password text)")
insert.Inserter(newmaillist,"gecicitablo")
gecicitabloverileri = insert.selector("SELECT l.email,l.password FROM login as l inner join gecicitablo g ON l.email=g.email and l.password=g.password")
insert.Inserter(gecicitabloverileri,"finding")
insert.selector("Drop table gecicitablo")
finishtime = time()

print(finishtime-starttime)  
























