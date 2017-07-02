import sqlite3 as lite
import sys

# ~ Logging KungFoo
import logging

__author__ = "Jan Harrie"
__version__ = "0.1"
__maintainer__ = "Jan Harrie"
__email__ = "harrymcfly@protonmail.com"
__status__ = "Prodction"


class IdMaintainer:
    __log__ = logging.getLogger()

    def __init__(self, db_name):
        self.CON = None
        try:
            self.CON = lite.connect(db_name)
            cur = self.CON.cursor()
            cur.execute('CREATE TABLE IF NOT EXISTS processed (ID INTEGER)')

        except lite.Error as e:
            self.__log__.error("Error %s:" % e.args[0])
            sys.exit(1)

    def add(self, expose_id):
        self.__log__.debug('add(' + str(expose_id) + ')')
        cur = self.CON.cursor()
        cur.execute('INSERT INTO processed VALUES(' + str(expose_id) + ')')
        self.CON.commit()

    def get(self):
        res = []
        cur = self.CON.cursor()
        cur.execute("SELECT * FROM processed ORDER BY 1")
        while True:
            row = cur.fetchone()
            if row == None:
                break
            res.append(row[0])

        self.__log__.info('already processed: ' + str(len(res)))
        self.__log__.debug(str(res))
        return res

    def foo(self):
        return 'foo'
