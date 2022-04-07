# Import the required modules
import mysql.connector
import base64
from PIL import Image
import io

# Create a connection
mydb = mysql.connector.connect(user='root',password='123456', host='127.0.0.1', database='makeup')

# Create a cursor object
cursor = mydb.cursor()

# Open a file in binary mode
file = open('./imgs/no_makeup/3.png','rb').read()

# We must encode the file to get base64 string
file = base64.b64encode(file)

# Sample data to be inserted
args = ('3', file)

# Prepare a query
query = 'INSERT INTO pictures VALUES(%s, %s)'

# Execute the query and commit the database.
cursor.execute(query,args)
mydb.commit()

