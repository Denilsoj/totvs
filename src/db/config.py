import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv

load_dotenv()

con = psycopg2.connect(
    dbname = os.getenv('NAME_DB'), 
    user = os.getenv('USER_DB'), 
    password = os.getenv('PASSWORD_DB'),
    host = os.getenv('HOST_DB'),
    port = os.getenv('PORT_DB')
    
    )


