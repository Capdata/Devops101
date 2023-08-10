import MySQLdb
from lxml import etree
import os.path

class alldbmyconnection:

    cstr = {}

    def __init__(self, cstrfile):
        host = ""
        port = ""
        user = ""
        passwd = ""
        db = ""

        if os.path.isfile(cstrfile):
            tree = etree.parse(cstrfile)
            host = tree.xpath("/connectionstring/host")
            port = tree.xpath("/connectionstring/port")
            user = tree.xpath("/connectionstring/user")
            passwd = tree.xpath("/connectionstring/passwd")
            db = tree.xpath("/connectionstring/database")

            ''' --------------------------------------------------------
            Ref : http://mysql-python.sourceforge.net/MySQLdb-1.2.2/
            - host      : string, host to connect
            - user      : string, user to connect as
            - passwd    : string, password to use
            - db        : string, database to use
            - port      : integer, TCP/IP port to connect to
            ---------------------------------------------------------'''
            self.cstr = {
                'host': host[0].text,
                'port': int(port[0].text),
                'user': user[0].text,
                'passwd': passwd[0].text,
                'db': db[0].text
            }

    def runquery(self, sql):
        try:
            conn = MySQLdb.connect(**self.cstr)
            cur = conn.cursor(MySQLdb.cursors.DictCursor)
            cur.execute(sql)
            conn.commit()
            rows = cur.fetchall()
            cur.close()
            conn.close()
            return rows

        except MySQLdb.Error as err:
            print (self.cstr)
            print (err)
