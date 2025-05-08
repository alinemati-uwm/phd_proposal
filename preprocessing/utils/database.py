import glob
import os
# import sys to get more detailed Python exception info
import sys
# import the connect library for psycopg2
import psycopg2
# import the error handling libraries for psycopg2
from psycopg2 import OperationalError, errorcodes, errors
import psycopg2.extras as extras
import pandas as pd


# Define a function that handles and parses psycopg2 exceptions
def show_psycopg2_exception(err):
    # get details about the exception
    err_type, err_obj, traceback = sys.exc_info()    
    # get the line number when exception occured
    line_n = traceback.tb_lineno    
    # print the connect() error
    print ("\npsycopg2 ERROR:", err, "on line number:", line_n)
    print ("psycopg2 traceback:", traceback, "-- type:", err_type) 
    # psycopg2 extensions.Diagnostics object attribute
    print ("\nextensions.Diagnostics:", err.diag)    
    # print the pgcode and pgerror exceptions
    print ("pgerror:", err.pgerror)
    print ("pgcode:", err.pgcode, "\n")
    
    
# Define a connect function for PostgreSQL database server
def connect(conn_params_dic):
    conn = None
    try:
        print('Connecting to the PostgreSQL...........')
        conn = psycopg2.connect(**conn_params_dic)
        print("Connection successfully..................")
        
    except OperationalError as err:
        # passing exception to function
        show_psycopg2_exception(err)        
        # set the connection to 'None' in case of error
        conn = None
    return conn


# Define function using copy_from_dataFile to insert the dataframe.
def copy_from_dataFile(conn, tmp_df, table):
    
    f = open(tmp_df, 'r')
    cursor = conn.cursor()
    try:
        cursor.copy_from(f, table, sep=",")
        conn.commit()
        print("Data inserted using copy_from_datafile() successfully....")
        cursor.close()
    except (Exception, psycopg2.DatabaseError) as err:
        os.remove(tmp_df)
        # pass exception to function
        show_psycopg2_exception(err)
        cursor.close()
    os.remove(tmp_df)
    

def create_table_from_csv(csvPath,conn):

    # Loop through each CSV
    for filename in glob.glob(csvPath+"*.csv"):
        # Create a table name
        tablename = filename.replace("./TestDataLGA\\", "").replace(".csv", "")
        print(tablename)
        # Open file
        fileInput = open(filename, "r")
        # Extract first line of file
        firstLine = fileInput.readline().strip()
        # Split columns into an array [...]
        columns = firstLine.split(",")
        # Build SQL code to drop table if exists and create table
        sqlQueryCreate = 'DROP TABLE IF EXISTS '+ tablename + ";\n"
        sqlQueryCreate += 'CREATE TABLE '+ tablename + "("

        #some loop or function according to your requiremennt
        # Define columns for table
        for column in columns:
            sqlQueryCreate += column + " VARCHAR(64),\n"

        sqlQueryCreate = sqlQueryCreate[:-2]
        sqlQueryCreate += ");"

        cur = conn.cursor()
        cur.execute(sqlQueryCreate)
        conn.commit()
        cur.close()