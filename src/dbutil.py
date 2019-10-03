import sqlite3
from sqlite3 import Error
import os
import logging

logging.basicConfig(
        datefmt = '%Y-%m-%d %H:%M:%S ',
        format = '%(asctime)s %(message)s',
        level=logging.INFO)

class dbutil:
    

    def create_connection(self, db_file):
        """ create a database connection to the SQLite database
            specified by the db_file
        """
        conn = None
        try:
            conn = sqlite3.connect(db_file)
            conn.row_factory = self.dict_factory
        except Error as e:
            # print(e)
            logging.error("-----------------")
            logging.error(str(e))
    
        return conn
    
    def dict_factory(self, cursor, row):
        """ convert the recordset into a dict object
        """
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d
    
    def select_all_tasks(self, conn, cmd):
        """
        Query all rows in the tasks table
        """
        cur = conn.cursor()
        # logging.info(cmd)

        cur.execute(cmd)
        # cur.execute("PRAGMA table_info(deploys)")
        rows = cur.fetchall()
        
        return rows
    
 
 
    def exec(self, conn, cmd):
    
        # create a database connection
        with conn:
            return self.select_all_tasks(conn, cmd)