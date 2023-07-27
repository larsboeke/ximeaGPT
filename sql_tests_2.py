import data_package.SQL_Connection_Provider.SQLConnectionProvider as SQLConnectionProvider
import re
import upload.Uploader as Uploader

conn, cursor = SQLConnectionProvider.SQLConnectionProvider().create_connection()


print("---------------------------------------------------------------------------------------------------------------")
print("Deleting old table")

cursor.execute("DROP TABLE [AI:Lean].[dbo].[chris_test_product_database]")
conn.commit()

print("---------------------------------------------------------------------------------------------------------------")
print("Creating new table")

cursor.execute("SELECT * INTO [AI:Lean].[dbo].[chris_test_product_database] FROM [AI:Lean].[dbo].[product_database]")
conn.commit()

print("---------------------------------------------------------------------------------------------------------------")
print("Data 1")

# Daten aus der bestehenden Tabelle abrufen
cursor.execute("SELECT DISTINCT name_of_camera, name_of_feature, value_of_feature FROM [AI:Lean].[dbo].[product_database] WHERE value_of_feature "
               "LIKE '<min>%%</min><max>%%</max><def>%%</def>'")
data = cursor.fetchall()


# Neue Daten in die Tabelle einfügen
for camera_name, feature_name, value in data:
    numbers = re.findall(r'[-+]?\d*\.\d+|\d+', value)
    if len(numbers) == 3:
        min_val, max_val, def_val = numbers
        cursor.execute("""
        INSERT INTO [AI:Lean].[dbo].[chris_test_product_database] (name_of_camera, name_of_feature, value_of_feature)
        VALUES (%s, %s, %s)
        """, (camera_name, feature_name + "Min", min_val))
        cursor.execute("""
        INSERT INTO [AI:Lean].[dbo].[chris_test_product_database] (name_of_camera, name_of_feature, value_of_feature)
        VALUES (%s, %s, %s)
        """, (camera_name, feature_name + "Max", max_val))
        cursor.execute("""
        INSERT INTO [AI:Lean].[dbo].[chris_test_product_database] (name_of_camera, name_of_feature, value_of_feature)
        VALUES (%s, %s, %s)
        """, (camera_name, feature_name + "Default", def_val))
    else:
        print("Error: ", camera_name, feature_name, value)
conn.commit()

# Die abgerufenen Einträge löschen
for camera_name, feature_name, value in data:
    cursor.execute("""
    DELETE FROM [AI:Lean].[dbo].[chris_test_product_database]
    WHERE name_of_camera = %s AND name_of_feature = %s AND value_of_feature = %s
    """, (camera_name, feature_name, value))
conn.commit()

print("---------------------------------------------------------------------------------------------------------------")
print("Data 2")

# Daten aus der bestehenden Tabelle abrufen
cursor.execute("SELECT DISTINCT name_of_camera, name_of_feature, value_of_feature FROM [AI:Lean].[dbo].[product_database] WHERE value_of_feature "
               "LIKE '<min>%%</min><max>%%</max><def>%%</def><inc>%%</inc>'")
data2 = cursor.fetchall()

# Neue Daten in die Tabelle einfügen
for camera_name, feature_name, value in data2:
    numbers = re.findall(r'[-+]?\d*\.\d+|\d+', value)
    if len(numbers) == 4:
        min_val, max_val, def_val, inc_val = numbers
        cursor.execute("""
        INSERT INTO [AI:Lean].[dbo].[chris_test_product_database] (name_of_camera, name_of_feature, value_of_feature)
        VALUES (%s, %s, %s)
        """, (camera_name, feature_name + "Min", min_val))
        cursor.execute("""
        INSERT INTO [AI:Lean].[dbo].[chris_test_product_database] (name_of_camera, name_of_feature, value_of_feature)
        VALUES (%s, %s, %s)
        """, (camera_name, feature_name + "Max", max_val))
        cursor.execute("""
        INSERT INTO [AI:Lean].[dbo].[chris_test_product_database] (name_of_camera, name_of_feature, value_of_feature)
        VALUES (%s, %s, %s)
        """, (camera_name, feature_name + "Default", def_val))
        cursor.execute("""
        INSERT INTO [AI:Lean].[dbo].[chris_test_product_database] (name_of_camera, name_of_feature, value_of_feature)
        VALUES (%s, %s, %s)
        """, (camera_name, feature_name + "Inc", inc_val))
    else:
        print("Error: ", camera_name, feature_name, value)
conn.commit()

# Die abgerufenen Einträge löschen
for camera_name, feature_name, value in data2:
    cursor.execute("""
    DELETE FROM [AI:Lean].[dbo].[chris_test_product_database]
    WHERE name_of_camera = %s AND name_of_feature = %s AND value_of_feature = %s
    """, (camera_name, feature_name, value))
conn.commit()

print("---------------------------------------------------------------------------------------------------------------")
print("Data 3")

cursor.execute("SELECT DISTINCT name_of_camera, name_of_feature, value_of_feature FROM [AI:Lean].[dbo].[product_database] WHERE value_of_feature "
               "LIKE '<wid>%%</wid>%<hei>%%</hei>%<dep>%%</dep>%<mas>%%</mas>'")
data3 = cursor.fetchall()

for camera_name, feature_name, value in data3:
    #numbers = re.findall(r'[-+]?\d*\.\d+|\d+', value)
    wid_val = re.search(r'<wid>(.*?)</wid>', value)
    hei_val = re.search(r'<hei>(.*?)</hei>', value)
    dep_val = re.search(r'<dep>(.*?)</dep>', value)
    mas_val = re.search(r'<mas>(.*?)</mas>', value)
    if len(numbers) == 4:
        wid_val, hei_val, dep_val, mas_val = numbers
        cursor.execute("""
        INSERT INTO [AI:Lean].[dbo].[chris_test_product_database] (name_of_camera, name_of_feature, value_of_feature)
        VALUES (%s, %s, %s)
        """, (camera_name, feature_name + "Width", wid_val))
        cursor.execute("""
        INSERT INTO [AI:Lean].[dbo].[chris_test_product_database] (name_of_camera, name_of_feature, value_of_feature)
        VALUES (%s, %s, %s)
        """, (camera_name, feature_name + "Height", hei_val))
        cursor.execute("""
        INSERT INTO [AI:Lean].[dbo].[chris_test_product_database] (name_of_camera, name_of_feature, value_of_feature)
        VALUES (%s, %s, %s)
        """, (camera_name, feature_name + "Depth", dep_val))
        cursor.execute("""
        INSERT INTO [AI:Lean].[dbo].[chris_test_product_database] (name_of_camera, name_of_feature, value_of_feature)
        VALUES (%s, %s, %s)
        """, (camera_name, feature_name + "Mass", mas_val))
    else:
        print("Error: ", camera_name, feature_name, value)
conn.commit()

# Die abgerufenen Einträge löschen
for camera_name, feature_name, value in data3:
    cursor.execute("""
    DELETE FROM [AI:Lean].[dbo].[chris_test_product_database]
    WHERE name_of_camera = %s AND name_of_feature = %s AND value_of_feature = %s
    """, (camera_name, feature_name, value))
conn.commit()

print("---------------------------------------------------------------------------------------------------------------")
print("Data 4")

cursor.execute("SELECT DISTINCT name_of_camera, name_of_feature, value_of_feature FROM [AI:Lean].[dbo].[product_database] WHERE value_of_feature "
               "LIKE '<wid>%%</wid><hei>%%</hei><dep>%%</dep>'")
data4 = cursor.fetchall()

for camera_name, feature_name, value in data4:
    numbers = re.findall(r'[-+]?\d*\.\d+|\d+', value)
    if len(numbers) == 3:
        wid_val, hei_val, dep_val = numbers
        cursor.execute("""
        INSERT INTO [AI:Lean].[dbo].[chris_test_product_database] (name_of_camera, name_of_feature, value_of_feature)
        VALUES (%s, %s, %s)
        """, (camera_name, feature_name + "Width", wid_val))
        cursor.execute("""
        INSERT INTO [AI:Lean].[dbo].[chris_test_product_database] (name_of_camera, name_of_feature, value_of_feature)
        VALUES (%s, %s, %s)
        """, (camera_name, feature_name + "Height", hei_val))
        cursor.execute("""
        INSERT INTO [AI:Lean].[dbo].[chris_test_product_database] (name_of_camera, name_of_feature, value_of_feature)
        VALUES (%s, %s, %s)
        """, (camera_name, feature_name + "Depth", dep_val))
    else:
        print("Error: ", camera_name, feature_name, value)
conn.commit()

# Die abgerufenen Einträge löschen
for camera_name, feature_name, value in data4:
    cursor.execute("""
    DELETE FROM [AI:Lean].[dbo].[chris_test_product_database]
    WHERE name_of_camera = %s AND name_of_feature = %s AND value_of_feature = %s
    """, (camera_name, feature_name, value))
conn.commit()

print("---------------------------------------------------------------------------------------------------------------")
print("Data 5")

cursor.execute("SELECT DISTINCT name_of_camera, name_of_feature, value_of_feature FROM [AI:Lean].[dbo].[product_database] WHERE value_of_feature "
               "LIKE '<db>%%</db>'")
data5 = cursor.fetchall()

# Neue Daten in die Tabelle einfügen
for camera_name, feature_name, value in data5:
    #numbers = re.findall(r'\d+\.\d+', value)  # Updated to handle decimal numbers
    numbers = re.findall(r'[-+]?\d*\.\d+|\d+', value)
    if len(numbers) == 1:
        db_val = numbers[0]
        cursor.execute("""
        INSERT INTO [AI:Lean].[dbo].[chris_test_product_database] (name_of_camera, name_of_feature, value_of_feature)
        VALUES (%s, %s, %s)
        """, (camera_name, feature_name, db_val))
    else:
        print("Error: ", camera_name, feature_name, value)
conn.commit()

# Die abgerufenen Einträge löschen
for camera_name, feature_name, value in data5:
    cursor.execute("""
    DELETE FROM [AI:Lean].[dbo].[chris_test_product_database]
    WHERE name_of_camera = %s AND name_of_feature = %s AND value_of_feature = %s
    """, (camera_name, feature_name, value))
conn.commit()

print("---------------------------------------------------------------------------------------------------------------")
print("Data 6")

cursor.execute("SELECT DISTINCT name_of_camera, name_of_feature, value_of_feature FROM [AI:Lean].[dbo].[product_database] WHERE value_of_feature "
               "LIKE '<global>%%</global>'")
data6 = cursor.fetchall()

# Neue Daten in die Tabelle einfügen
for camera_name, feature_name, value in data6:
    numbers = re.findall(r'[-+]?\d*\.\d+|\d+', value)
    if len(numbers) == 1:
        db_val = numbers[0]
        cursor.execute("""
        INSERT INTO [AI:Lean].[dbo].[chris_test_product_database] (name_of_camera, name_of_feature, value_of_feature)
        VALUES (%s, %s, %s)
        """, (camera_name, feature_name, db_val))
    else:
        print("Error: ", camera_name, feature_name, value)
conn.commit()

# Die abgerufenen Einträge löschen
for camera_name, feature_name, value in data6:
    cursor.execute("""
    DELETE FROM [AI:Lean].[dbo].[chris_test_product_database]
    WHERE name_of_camera = %s AND name_of_feature = %s AND value_of_feature = %s
    """, (camera_name, feature_name, value))
conn.commit()

print("---------------------------------------------------------------------------------------------------------------")
print("Data 7")

cursor.execute("SELECT DISTINCT name_of_camera, name_of_feature, value_of_feature FROM [AI:Lean].[dbo].[product_database] WHERE value_of_feature "
               "LIKE '<pub>%%</pub>'")
data7 = cursor.fetchall()

# Neue Daten in die Tabelle einfügen
for camera_name, feature_name, value in data7:
    numbers = re.findall(r'[-+]?\d*\.\d+|\d+', value)
    if len(numbers) == 1:
        db_val = numbers[0]
        cursor.execute("""
        INSERT INTO [AI:Lean].[dbo].[chris_test_product_database] (name_of_camera, name_of_feature, value_of_feature)
        VALUES (%s, %s, %s)
        """, (camera_name, feature_name, db_val))
    else:
        print("Error: ", camera_name, feature_name, value)
conn.commit()

# Die abgerufenen Einträge löschen
for camera_name, feature_name, value in data7:
    cursor.execute("""
    DELETE FROM [AI:Lean].[dbo].[chris_test_product_database]
    WHERE name_of_camera = %s AND name_of_feature = %s AND value_of_feature = %s
    """, (camera_name, feature_name, value))
conn.commit()

print("---------------------------------------------------------------------------------------------------------------")
print("Data 8")
cursor.execute("SELECT DISTINCT name_of_camera, name_of_feature, value_of_feature FROM [AI:Lean].[dbo].[product_database] WHERE value_of_feature "
               "LIKE '<max>%%</max><def>%%</def>'")
data8 = cursor.fetchall()

# Neue Daten in die Tabelle einfügen
for camera_name, feature_name, value in data8:
    numbers = re.findall(r'[-+]?\d*\.\d+|\d+', value)
    if len(numbers) == 2:
        max_val, def_val = numbers
        cursor.execute("""
        INSERT INTO [AI:Lean].[dbo].[chris_test_product_database] (name_of_camera, name_of_feature, value_of_feature)
        VALUES (%s, %s, %s)
        """, (camera_name, feature_name + "Max", max_val))
        cursor.execute("""
        INSERT INTO [AI:Lean].[dbo].[chris_test_product_database] (name_of_camera, name_of_feature, value_of_feature)
        VALUES (%s, %s, %s)
        """, (camera_name, feature_name + "Def", def_val))
    else:
        print("Error: ", camera_name, feature_name, value)
conn.commit()

# Die abgerufenen Einträge löschen
for camera_name, feature_name, value in data8:
    cursor.execute("""
    DELETE FROM [AI:Lean].[dbo].[chris_test_product_database]
    WHERE name_of_camera = %s AND name_of_feature = %s AND value_of_feature = %s
    """, (camera_name, feature_name, value))
conn.commit()

print("---------------------------------------------------------------------------------------------------------------")
print("Data 9")
cursor.execute("SELECT DISTINCT name_of_camera, name_of_feature, value_of_feature FROM [AI:Lean].[dbo].[product_database] WHERE value_of_feature "
               "LIKE '<min>%%</min><max>%%</max><bands>%%</bands>'")
data9 = cursor.fetchall()

# Neue Daten in die Tabelle einfügen
for camera_name, feature_name, value in data9:
    numbers = re.findall(r'[-+]?\d*\.\d+|\d+', value)
    if len(numbers) == 3:
        min_val, max_val, bands_val = numbers
        cursor.execute("""
        INSERT INTO [AI:Lean].[dbo].[chris_test_product_database] (name_of_camera, name_of_feature, value_of_feature)
        VALUES (%s, %s, %s)
        """, (camera_name, feature_name + "Min", min_val))
        cursor.execute("""
        INSERT INTO [AI:Lean].[dbo].[chris_test_product_database] (name_of_camera, name_of_feature, value_of_feature)
        VALUES (%s, %s, %s)
        """, (camera_name, feature_name + "Max", max_val))
        cursor.execute("""
        INSERT INTO [AI:Lean].[dbo].[chris_test_product_database] (name_of_camera, name_of_feature, value_of_feature)
        VALUES (%s, %s, %s)
        """, (camera_name, feature_name + "Bands", bands_val))
    else:
        print("Error: ", camera_name, feature_name, value)
conn.commit()

# Die abgerufenen Einträge löschen
for camera_name, feature_name, value in data9:
    cursor.execute("""
    DELETE FROM [AI:Lean].[dbo].[chris_test_product_database]
    WHERE name_of_camera = %s AND name_of_feature = %s AND value_of_feature = %s
    """, (camera_name, feature_name, value))
conn.commit()

print("---------------------------------------------------------------------------------------------------------------")
print("Data 10")

cursor.execute("SELECT DISTINCT name_of_camera, name_of_feature, value_of_feature FROM [AI:Lean].[dbo].[product_database] WHERE value_of_feature "
               "LIKE '<min>%%</min><max>%%</max>'")
data10 = cursor.fetchall()

# Neue Daten in die Tabelle einfügen
for camera_name, feature_name, value in data10:
    numbers = re.findall(r'[-+]?\d*\.\d+|\d+', value)
    if len(numbers) == 2:
        min_val, max_val = numbers
        cursor.execute("""
        INSERT INTO [AI:Lean].[dbo].[chris_test_product_database] (name_of_camera, name_of_feature, value_of_feature)
        VALUES (%s, %s, %s)
        """, (camera_name, feature_name + "Min", min_val))
        cursor.execute("""
        INSERT INTO [AI:Lean].[dbo].[chris_test_product_database] (name_of_camera, name_of_feature, value_of_feature)
        VALUES (%s, %s, %s)
        """, (camera_name, feature_name + "Max", max_val))
    else:
        print("Error: ", camera_name, feature_name, value)
conn.commit()

# Die abgerufenen Einträge löschen
for camera_name, feature_name, value in data10:
    cursor.execute("""
    DELETE FROM [AI:Lean].[dbo].[chris_test_product_database]
    WHERE name_of_camera = %s AND name_of_feature = %s AND value_of_feature = %s
    """, (camera_name, feature_name, value))
conn.commit()

print("---------------------------------------------------------------------------------------------------------------")
print("Data 12")

cursor.execute("SELECT DISTINCT name_of_camera, name_of_feature, value_of_feature FROM [AI:Lean].[dbo].[product_database] WHERE value_of_feature "
               "LIKE '<min>%%</min><max>%%</max><def>%%</def>used'")
data12 = cursor.fetchall()

# Neue Daten in die Tabelle einfügen
for camera_name, feature_name, value in data12:
    numbers = re.findall(r'[-+]?\d*\.\d+|\d+', value)
    if len(numbers) == 3:
        min_val, max_val, def_val = numbers
        cursor.execute("""
        INSERT INTO [AI:Lean].[dbo].[chris_test_product_database] (name_of_camera, name_of_feature, value_of_feature)
        VALUES (%s, %s, %s)
        """, (camera_name, feature_name + "Min", min_val))
        cursor.execute("""
        INSERT INTO [AI:Lean].[dbo].[chris_test_product_database] (name_of_camera, name_of_feature, value_of_feature)
        VALUES (%s, %s, %s)
        """, (camera_name, feature_name + "Max", max_val))
        cursor.execute("""
        INSERT INTO [AI:Lean].[dbo].[chris_test_product_database] (name_of_camera, name_of_feature, value_of_feature)
        VALUES (%s, %s, %s)
        """, (camera_name, feature_name + "Def", def_val))
        cursor.execute("""
        INSERT INTO [AI:Lean].[dbo].[chris_test_product_database] (name_of_camera, name_of_feature, value_of_feature)
        VALUES (%s, %s, 'used')
        """, (camera_name, feature_name + "Used"))  # Für "Used" wird kein Wert eingefügt, da "used" keinem numerischen Wert zugeordnet ist
    else:
        print("Error: ", camera_name, feature_name, value)
conn.commit()

# Die abgerufenen Einträge löschen
for camera_name, feature_name, value in data12:
    cursor.execute("""
    DELETE FROM [AI:Lean].[dbo].[chris_test_product_database]
    WHERE name_of_camera = %s AND name_of_feature = %s AND value_of_feature = %s
    """, (camera_name, feature_name, value))
conn.commit()

print("---------------------------------------------------------------------------------------------------------------")
print("Clearing unfilled data")

cursor.execute("SELECT DISTINCT name_of_feature FROM chris_test_product_database")
features = cursor.fetchall()

for feature in features:
    # Prüfen, ob das Feature irgendwo einen nicht-leeren, nicht-None-Wert hat
    cursor.execute("""
    SELECT 1 FROM chris_test_product_database
    WHERE name_of_feature = %s AND value_of_feature <> 'None' AND value_of_feature <> ''
    """, (feature,))
    if cursor.fetchone() is None:  # Wenn es keinen solchen Eintrag gibt, löschen Sie das Feature
        cursor.execute("""
        DELETE FROM chris_test_product_database
        WHERE name_of_feature = %s
        """, (feature,))
        print("Feature ", feature, " deleted")
    else:
        print("Feature ", feature, " checked")
conn.commit()




# Verbindung schließen
conn.close()

from data_package.Pinecone_Connection_Provider.PineconeConnectionProvider import PineconeConnectionProvider
print("---------------------------------------------------------------------------------------------------------------")
print("Uploading new features to Pinecone")
ghh
#Uploader.Uploader().initialUploadName_of_feature_modified_sql_db()
#pinecone_connection = PineconeConnectionProvider().initPinecone()
#pinecone_connection.delete(delete_all = True, namespace = "name_of_sql_features_modified_sql_db")