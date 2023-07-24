import mysql.connector
config = {
  'host':'ximeapdbdev.mysql.database.azure.com',
  'user':'ai_lean_dev',
  'password':'8CXhkZqU5FxyKT',
  'database':'products',
  'client_flags': [mysql.connector.ClientFlag.SSL],
  'ssl_ca': 'DigiCertGlobalRootG2.crt.pem'}
destination_host = '127.0.0.1'
destination_database = 'prototype'
destination_username = 'root'
destination_password = '859760Si.'


try:
    source_connection = mysql.connector.connect(**config
    )
    source_cursor = source_connection.cursor()
    destination_connection = mysql.connector.connect(
        host=destination_host,
        database=destination_database,
        user=destination_username,
        password=destination_password,
    )
    destination_cursor = destination_connection.cursor()
except:
    print("doesn't work")
# Source SQL Server connection details

create_table_sql = """
CREATE TABLE IF NOT EXISTS product_database (
    name_of_feature varchar(45) DEFAULT NULL,
    name_of_product varchar(145) DEFAULT NULL,
    value_of_feature text,
    unit varchar(45) DEFAULT NULL,
    description varchar(245) DEFAULT NULL
);"""


# SQL command to retrieve data from the source server
source_sql_command = """
SELECT p.id, f.id, f.name, p.name, pfr.value_txt, f.gentl_unit, f.gentl_description
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
    source_cursor.execute(source_sql_command)
    data_to_insert = source_cursor.fetchall()

    # Insert the data into the newly created table in the destination server
    insert_query = "INSERT INTO product_database (id_product, id_feature, name_of_feature, name_of_product, value_of_feature, unit, description) VALUES (%s, %s,%s,%s,%s,%s,%s)"
    destination_cursor.executemany(insert_query, data_to_insert)
    destination_connection.commit()

except Exception as e:
    print("Error occurred:", e)

finally:
    # Close the connections
    source_cursor.close()
    source_connection.close()
    destination_cursor.close()
    destination_connection.close()
