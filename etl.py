import mysql.connector
from data_package.SQL_Connection_Provider.SQLConnectionProvider import SQLConnectionProvider
config = {
  'host':'ximeapdbdev.mysql.database.azure.com',
  'user':'ai_lean_dev',
  'password':'8CXhkZqU5FxyKT',
  'database':'products',
  'client_flags': [mysql.connector.ClientFlag.SSL],
  'ssl_ca': 'DigiCertGlobalRootG2.crt.pem'}
# destination_host = '127.0.0.1'
# destination_database = 'prototype'
# destination_username = 'root'
# destination_password = '859760Si.'


try:
    source_connection = mysql.connector.connect(**config
    )
    source_cursor = source_connection.cursor()
    # destination_connection = mysql.connector.connect(
    #     host=destination_host,
    #     database=destination_database,
    #     user=destination_username,
    #     password=destination_password,
    # )
    # destination_cursor = destination_connection.cursor()
    destination_connection, destination_cursor = SQLConnectionProvider().create_connection()
except:
    print("doesn't work")
# Source SQL Server connection details

create_table_sql = """
CREATE TABLE [AI:Lean].[dbo].[product_database] (
    name_of_camera VARCHAR(145) NULL,
    name_of_feature VARCHAR(45) NULL,
    value_of_feature VARCHAR(MAX),
    unit VARCHAR(45) NULL,
    description_of_feature VARCHAR(245) NULL
);"""


# # SQL command to retrieve data from the source server
source_sql_command = """
SELECT p.name, f.name, pfr.value_txt, f.gentl_unit, f.gentl_description
FROM feat f
INNER JOIN prodfeat pfr
ON f.id = pfr.id_feat
INNER JOIN prod p
ON pfr.id_product = p.id;
;"""


try:
    # Connect to the source SQL Server
    # Execute the SQL command to create the new table in the destination server
    destination_cursor.execute(create_table_sql)
    print('hi')
    source_cursor.execute(source_sql_command)
    data_to_insert = source_cursor.fetchall()

    # Insert the data into the newly created table in the destination server
    insert_query = "INSERT INTO [AI:Lean].[dbo].[product_database] (name_of_camera, name_of_feature, value_of_feature, unit, description_of_feature) VALUES (%s, %s,%s,%s,%s)"
    print('2')
    destination_cursor.executemany(insert_query, data_to_insert)
    print('3')
    destination_connection.commit()
    print("4")
    destination_cursor.execute("""UPDATE [AI:Lean].[dbo].[product_database]
SET value_of_feature = 'None'
WHERE CAST(value_of_feature AS varchar(max)) = 'used';""")
    destination_cursor.commit()

except Exception as e:
    print("Error occurred:", e)

finally:
    # Close the connections
    source_cursor.close()
    source_connection.close()
    
