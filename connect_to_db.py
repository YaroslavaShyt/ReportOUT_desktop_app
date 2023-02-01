from sqlalchemy import create_engine
import pymysql
import pandas as pd
import pymysql.cursors
import json

sqlEngine = create_engine('mysql+pymysql://reportbd_usr:0v7uh3K5nK19I6ir@45.145.52.129/reportbd', pool_recycle=3600)
dbConnection = sqlEngine.connect()





def setup_connection(db_host, db_user, db, db_password):
    with open('settings/connection_settings.json', 'r') as f:
        data = json.load(f)
    connection = pymysql.connect(host=db_host,
                                 user=db_user,
                                 database=db,
                                 password=db_password,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.SSCursor)
    return connection
