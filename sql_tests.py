import upload.Uploader as Uploader
import data_package.SQL_Connection_Provider.SQLConnectionProvider as SQLConnectionProvider
import time
#Uploader.Uploader().initialUploadName_of_feature()
Uploader.Uploader().initialUploadName_of_feature_modified_sql_db()

dw
conn, cursor = SQLConnectionProvider.SQLConnectionProvider().create_connection()


cursor.execute("SELECT DISTINCT name_of_camera, name_of_feature, value_of_feature FROM product_database "
               "WHERE name_of_feature = 'Dimensions' ")
print("start")
data3 = cursor.fetchall()

i=0
for camera_name, feature_name, value in data3:
    print(camera_name, feature_name, value)
    i+=1
print(i)
print("ende")

# pause for 10minutes
time.sleep(600)

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
    print("Feature ", feature, " checked")
conn.commit()



#cursor.execute("SELECT name_of_camera, name_of_feature, value_of_feature FROM product_database "
#               "WHERE value_of_feature = 'None' OR value_of_feature = ''")
#data13 = cursor.fetchall()

# Die abgerufenen Einträge löschen
#for camera_name, feature_name, value in data13:
#    cursor.execute("""
#    DELETE FROM [AI:Lean].[dbo].[chris_test_product_database]
#    WHERE name_of_camera = %s AND name_of_feature = %s
#    """, (camera_name, feature_name))
conn.commit()
conn.close()
