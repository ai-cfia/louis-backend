# pgvector==0.1.8
# psycopg2==2.9.6
import os
import dotenv
dotenv.load_dotenv()

import numpy as np
import psycopg
from pgvector.psycopg import register_vector
from psycopg.rows import dict_row

LOUIS_DSN = os.environ.get("LOUIS_DSN")
print(LOUIS_DSN)
connection = psycopg.connect(
    conninfo=LOUIS_DSN,
    row_factory=dict_row,
    autocommit=True)
register_vector(connection)
cursor = connection.cursor()
# 15 passes, 16 failsp about 4 characters per unit so
# 4*32=128
data = {'params': np.array([1 for i in range(1536)])}
# cursor.callproc('example_function', data)
cursor.execute("SELECT * FROM example_function(%(params)s::vector)", data)
results = cursor.fetchall()
print(results)