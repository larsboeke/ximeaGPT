import data_package.SQL_Connection_Provider.SQLConnectionProvider as SQLConnectionProvider
import re
import upload.Uploader as Uploader

class PDBSetup:

    def __init__(self, sql_connection):
        self.conn, self.cursor = sql_connection
    def settingUpPDB(self):
        """
        This function is used to set up the product database which mean separating different feature versions into
        unique features, like Framerate in FramerateMin, FramerateMax, FramerateDefault
        """

        print("Deleting outdated table")

        self.cursor.execute("DROP TABLE [AI:Lean].[dbo].[product_database]")
        self.conn.commit()


        print("Creating PDB table")

        self.cursor.execute("SELECT * INTO [AI:Lean].[dbo].[product_database] "
                            "FROM [AI:Lean].[dbo].[product_database_staging]")
        self.conn.commit()


        print("Adjusting Data 1")

        self.cursor.execute("SELECT DISTINCT name_of_camera, name_of_feature, value_of_feature "
                            "FROM [AI:Lean].[dbo].[product_database_staging] WHERE value_of_feature "
                            "LIKE '<min>%%</min><max>%%</max><def>%%</def>'")
        data1 = self.cursor.fetchall()


        for camera_name, feature_name, value in data1:
            numbers = re.findall(r'[-+]?\d*\.\d+|\d+', value)
            if len(numbers) == 3:
                min_val, max_val, def_val = numbers
                self.cursor.execute("""
                INSERT INTO [AI:Lean].[dbo].[product_database] (name_of_camera, name_of_feature, value_of_feature)
                VALUES (%s, %s, %s)
                """, (camera_name, feature_name + "Min", min_val))
                self.cursor.execute("""
                INSERT INTO [AI:Lean].[dbo].[product_database] (name_of_camera, name_of_feature, value_of_feature)
                VALUES (%s, %s, %s)
                """, (camera_name, feature_name + "Max", max_val))
                self.cursor.execute("""
                INSERT INTO [AI:Lean].[dbo].[product_database] (name_of_camera, name_of_feature, value_of_feature)
                VALUES (%s, %s, %s)
                """, (camera_name, feature_name + "Default", def_val))
            else:
                print("Error: ", camera_name, feature_name, value)
        self.conn.commit()

        for camera_name, feature_name, value in data1:
            self.cursor.execute("""
            DELETE FROM [AI:Lean].[dbo].[product_database]
            WHERE name_of_camera = %s AND name_of_feature = %s AND value_of_feature = %s
            """, (camera_name, feature_name, value))
        self.conn.commit()

        print("Adjusting 1 buggy entry MQ022MG-CM-SR2 Gain <min>0-1.5</min><max>6</max><def>0</def>")
        self.cursor.execute("""
        INSERT INTO [AI:Lean].[dbo].[product_database] (name_of_camera, name_of_feature, value_of_feature)
        VALUES (%s, %s, %s)
        """, ("MQ022MG-CM-SR2", "GainMin", "1.5"))
        self.cursor.execute("""
            INSERT INTO [AI:Lean].[dbo].[product_database] (name_of_camera, name_of_feature, value_of_feature)
            VALUES (%s, %s, %s)
            """, ("MQ022MG-CM-SR2", "GainMax", "6"))
        self.cursor.execute("""
            INSERT INTO [AI:Lean].[dbo].[product_database] (name_of_camera, name_of_feature, value_of_feature)
            VALUES (%s, %s, %s)
            """, ("MQ022MG-CM-SR2", "GainDefault", "0"))
        self.conn.commit()
        self.cursor.execute("""
        DELETE FROM [AI:Lean].[dbo].[product_database]
        WHERE name_of_camera = %s AND name_of_feature = %s AND value_of_feature = %s
        """, ("MQ022MG-CM-SR2", "Gain", "<min>0-1.5</min><max>6</max><def>0</def>"))
        self.conn.commit()


        print("Adjusting Data 2")

        self.cursor.execute("SELECT DISTINCT name_of_camera, name_of_feature, value_of_feature "
                            "FROM [AI:Lean].[dbo].[product_database_staging] WHERE value_of_feature "
                            "LIKE '<min>%%</min><max>%%</max><def>%%</def><inc>%%</inc>'")
        data2 = self.cursor.fetchall()

        for camera_name, feature_name, value in data2:
            numbers = re.findall(r'[-+]?\d*\.\d+|\d+', value)
            if len(numbers) == 4:
                min_val, max_val, def_val, inc_val = numbers
                self.cursor.execute("""
                INSERT INTO [AI:Lean].[dbo].[product_database] (name_of_camera, name_of_feature, value_of_feature)
                VALUES (%s, %s, %s)
                """, (camera_name, feature_name + "Min", min_val))
                self.cursor.execute("""
                INSERT INTO [AI:Lean].[dbo].[product_database] (name_of_camera, name_of_feature, value_of_feature)
                VALUES (%s, %s, %s)
                """, (camera_name, feature_name + "Max", max_val))
                self.cursor.execute("""
                INSERT INTO [AI:Lean].[dbo].[product_database] (name_of_camera, name_of_feature, value_of_feature)
                VALUES (%s, %s, %s)
                """, (camera_name, feature_name + "Default", def_val))
                self.cursor.execute("""
                INSERT INTO [AI:Lean].[dbo].[product_database] (name_of_camera, name_of_feature, value_of_feature)
                VALUES (%s, %s, %s)
                """, (camera_name, feature_name + "Inc", inc_val))
            else:
                print("Error: ", camera_name, feature_name, value)
        self.conn.commit()

        for camera_name, feature_name, value in data2:
            self.cursor.execute("""
            DELETE FROM [AI:Lean].[dbo].[product_database]
            WHERE name_of_camera = %s AND name_of_feature = %s AND value_of_feature = %s
            """, (camera_name, feature_name, value))
        self.conn.commit()


        print("Adjusting Data 3")

        self.cursor.execute("SELECT DISTINCT name_of_camera, name_of_feature, value_of_feature "
                            "FROM [AI:Lean].[dbo].[product_database_staging] WHERE value_of_feature "
                            "LIKE '<wid>%%</wid>%<hei>%%</hei>%<dep>%%</dep>%<mas>%%</mas>'")
        data3 = self.cursor.fetchall()

        for camera_name, feature_name, value in data3:
            wid_val = re.search(r'<wid>(.*?)</wid>', value).group(1)
            hei_val = re.search(r'<hei>(.*?)</hei>', value).group(1)
            dep_val = re.search(r'<dep>(.*?)</dep>', value).group(1)
            mas_val = re.search(r'<mas>(.*?)</mas>', value).group(1)
            if len(numbers) == 4:
                self.cursor.execute("""
                INSERT INTO [AI:Lean].[dbo].[product_database] (name_of_camera, name_of_feature, value_of_feature)
                VALUES (%s, %s, %s)
                """, (camera_name, feature_name + "Width", wid_val))
                self.cursor.execute("""
                INSERT INTO [AI:Lean].[dbo].[product_database] (name_of_camera, name_of_feature, value_of_feature)
                VALUES (%s, %s, %s)
                """, (camera_name, feature_name + "Height", hei_val))
                self.cursor.execute("""
                INSERT INTO [AI:Lean].[dbo].[product_database] (name_of_camera, name_of_feature, value_of_feature)
                VALUES (%s, %s, %s)
                """, (camera_name, feature_name + "Depth", dep_val))
                self.cursor.execute("""
                INSERT INTO [AI:Lean].[dbo].[product_database] (name_of_camera, name_of_feature, value_of_feature)
                VALUES (%s, %s, %s)
                """, (camera_name, feature_name + "Mass", mas_val))
            else:
                print("Error: ", camera_name, feature_name, value)
        self.conn.commit()

        for camera_name, feature_name, value in data3:
            self.cursor.execute("""
            DELETE FROM [AI:Lean].[dbo].[product_database]
            WHERE name_of_camera = %s AND name_of_feature = %s AND value_of_feature = %s
            """, (camera_name, feature_name, value))
        self.conn.commit()


        print("Adjusting Data 4")

        self.cursor.execute("SELECT DISTINCT name_of_camera, name_of_feature, value_of_feature "
                            "FROM [AI:Lean].[dbo].[product_database_staging] WHERE value_of_feature "
                            "LIKE '<wid>%%</wid><hei>%%</hei><dep>%%</dep>'")
        data4 = self.cursor.fetchall()

        for camera_name, feature_name, value in data4:
            numbers = re.findall(r'[-+]?\d*\.\d+|\d+', value)
            if len(numbers) == 3:
                wid_val, hei_val, dep_val = numbers
                self.cursor.execute("""
                INSERT INTO [AI:Lean].[dbo].[product_database] (name_of_camera, name_of_feature, value_of_feature)
                VALUES (%s, %s, %s)
                """, (camera_name, feature_name + "Width", wid_val))
                self.cursor.execute("""
                INSERT INTO [AI:Lean].[dbo].[product_database] (name_of_camera, name_of_feature, value_of_feature)
                VALUES (%s, %s, %s)
                """, (camera_name, feature_name + "Height", hei_val))
                self.cursor.execute("""
                INSERT INTO [AI:Lean].[dbo].[product_database] (name_of_camera, name_of_feature, value_of_feature)
                VALUES (%s, %s, %s)
                """, (camera_name, feature_name + "Depth", dep_val))
            else:
                print("Error: ", camera_name, feature_name, value)
        self.conn.commit()

        for camera_name, feature_name, value in data4:
            self.cursor.execute("""
            DELETE FROM [AI:Lean].[dbo].[product_database]
            WHERE name_of_camera = %s AND name_of_feature = %s AND value_of_feature = %s
            """, (camera_name, feature_name, value))
        self.conn.commit()


        print("Adjusting Data 5")

        self.cursor.execute("SELECT DISTINCT name_of_camera, name_of_feature, value_of_feature "
                            "FROM [AI:Lean].[dbo].[product_database_staging] WHERE value_of_feature "
                            "LIKE '<db>%%</db>'")
        data5 = self.cursor.fetchall()

        for camera_name, feature_name, value in data5:
            numbers = re.findall(r'[-+]?\d*\.\d+|\d+', value)
            if len(numbers) == 1:
                db_val = numbers[0]
                self.cursor.execute("""
                INSERT INTO [AI:Lean].[dbo].[product_database] (name_of_camera, name_of_feature, value_of_feature)
                VALUES (%s, %s, %s)
                """, (camera_name, feature_name, db_val))
            else:
                print("Error: ", camera_name, feature_name, value)
        self.conn.commit()

        for camera_name, feature_name, value in data5:
            self.cursor.execute("""
            DELETE FROM [AI:Lean].[dbo].[product_database]
            WHERE name_of_camera = %s AND name_of_feature = %s AND value_of_feature = %s
            """, (camera_name, feature_name, value))
        self.conn.commit()


        print("Adjusting Data 6")

        self.cursor.execute("SELECT DISTINCT name_of_camera, name_of_feature, value_of_feature "
                            "FROM [AI:Lean].[dbo].[product_database_staging] WHERE value_of_feature "
                            "LIKE '<global>%%</global>'")
        data6 = self.cursor.fetchall()

        for camera_name, feature_name, value in data6:
            numbers = re.findall(r'[-+]?\d*\.\d+|\d+', value)
            if len(numbers) == 1:
                db_val = numbers[0]
                self.cursor.execute("""
                INSERT INTO [AI:Lean].[dbo].[product_database] (name_of_camera, name_of_feature, value_of_feature)
                VALUES (%s, %s, %s)
                """, (camera_name, feature_name, db_val))
            else:
                print("Error: ", camera_name, feature_name, value)
        self.conn.commit()

        for camera_name, feature_name, value in data6:
            self.cursor.execute("""
            DELETE FROM [AI:Lean].[dbo].[product_database]
            WHERE name_of_camera = %s AND name_of_feature = %s AND value_of_feature = %s
            """, (camera_name, feature_name, value))
        self.conn.commit()


        print("Adjusting Data 7")

        self.cursor.execute("SELECT DISTINCT name_of_camera, name_of_feature, value_of_feature "
                            "FROM [AI:Lean].[dbo].[product_database_staging] WHERE value_of_feature "
                            "LIKE '<pub>%%</pub>'")
        data7 = self.cursor.fetchall()

        for camera_name, feature_name, value in data7:
            numbers = re.findall(r'[-+]?\d*\.\d+|\d+', value)
            if len(numbers) == 1:
                db_val = numbers[0]
                self.cursor.execute("""
                INSERT INTO [AI:Lean].[dbo].[product_database] (name_of_camera, name_of_feature, value_of_feature)
                VALUES (%s, %s, %s)
                """, (camera_name, feature_name, db_val))
            else:
                print("Error: ", camera_name, feature_name, value)
        self.conn.commit()

        for camera_name, feature_name, value in data7:
            self.cursor.execute("""
            DELETE FROM [AI:Lean].[dbo].[product_database]
            WHERE name_of_camera = %s AND name_of_feature = %s AND value_of_feature = %s
            """, (camera_name, feature_name, value))
        self.conn.commit()


        print("Adjusting Data 8")

        self.cursor.execute("SELECT DISTINCT name_of_camera, name_of_feature, value_of_feature "
                            "FROM [AI:Lean].[dbo].[product_database_staging] WHERE value_of_feature "
                            "LIKE '<max>%%</max><def>%%</def>'")
        data8 = self.cursor.fetchall()

        for camera_name, feature_name, value in data8:
            numbers = re.findall(r'[-+]?\d*\.\d+|\d+', value)
            if len(numbers) == 2:
                max_val, def_val = numbers
                self.cursor.execute("""
                INSERT INTO [AI:Lean].[dbo].[product_database] (name_of_camera, name_of_feature, value_of_feature)
                VALUES (%s, %s, %s)
                """, (camera_name, feature_name + "Max", max_val))
                self.cursor.execute("""
                INSERT INTO [AI:Lean].[dbo].[product_database] (name_of_camera, name_of_feature, value_of_feature)
                VALUES (%s, %s, %s)
                """, (camera_name, feature_name + "Default", def_val))
            else:
                print("Error: ", camera_name, feature_name, value)
        self.conn.commit()

        for camera_name, feature_name, value in data8:
            self.cursor.execute("""
            DELETE FROM [AI:Lean].[dbo].[product_database]
            WHERE name_of_camera = %s AND name_of_feature = %s AND value_of_feature = %s
            """, (camera_name, feature_name, value))
        self.conn.commit()


        print("Adjusting Data 9")

        self.cursor.execute("SELECT DISTINCT name_of_camera, name_of_feature, value_of_feature "
                            "FROM [AI:Lean].[dbo].[product_database_staging] WHERE value_of_feature "
                            "LIKE '<min>%%</min><max>%%</max><bands>%%</bands>'")
        data9 = self.cursor.fetchall()

        for camera_name, feature_name, value in data9:
            numbers = re.findall(r'[-+]?\d*\.\d+|\d+', value)
            if len(numbers) == 3:
                min_val, max_val, bands_val = numbers
                self.cursor.execute("""
                INSERT INTO [AI:Lean].[dbo].[product_database] (name_of_camera, name_of_feature, value_of_feature)
                VALUES (%s, %s, %s)
                """, (camera_name, feature_name + "Min", min_val))
                self.cursor.execute("""
                INSERT INTO [AI:Lean].[dbo].[product_database] (name_of_camera, name_of_feature, value_of_feature)
                VALUES (%s, %s, %s)
                """, (camera_name, feature_name + "Max", max_val))
                self.cursor.execute("""
                INSERT INTO [AI:Lean].[dbo].[product_database] (name_of_camera, name_of_feature, value_of_feature)
                VALUES (%s, %s, %s)
                """, (camera_name, feature_name + "Bands", bands_val))
            else:
                print("Error: ", camera_name, feature_name, value)
        self.conn.commit()

        for camera_name, feature_name, value in data9:
            self.cursor.execute("""
            DELETE FROM [AI:Lean].[dbo].[product_database]
            WHERE name_of_camera = %s AND name_of_feature = %s AND value_of_feature = %s
            """, (camera_name, feature_name, value))
        self.conn.commit()


        print("Adjusting Data 10")

        self.cursor.execute("SELECT DISTINCT name_of_camera, name_of_feature, value_of_feature "
                            "FROM [AI:Lean].[dbo].[product_database_staging] WHERE value_of_feature "
                            "LIKE '<min>%%</min><max>%%</max>'")
        data10 = self.cursor.fetchall()

        for camera_name, feature_name, value in data10:
            numbers = re.findall(r'[-+]?\d*\.\d+|\d+', value)
            if len(numbers) == 2:
                min_val, max_val = numbers
                self.cursor.execute("""
                INSERT INTO [AI:Lean].[dbo].[product_database] (name_of_camera, name_of_feature, value_of_feature)
                VALUES (%s, %s, %s)
                """, (camera_name, feature_name + "Min", min_val))
                self.cursor.execute("""
                INSERT INTO [AI:Lean].[dbo].[product_database] (name_of_camera, name_of_feature, value_of_feature)
                VALUES (%s, %s, %s)
                """, (camera_name, feature_name + "Max", max_val))
            else:
                print("Error: ", camera_name, feature_name, value)
        self.conn.commit()

        for camera_name, feature_name, value in data10:
            self.cursor.execute("""
            DELETE FROM [AI:Lean].[dbo].[product_database]
            WHERE name_of_camera = %s AND name_of_feature = %s AND value_of_feature = %s
            """, (camera_name, feature_name, value))
        self.conn.commit()


        print("Adjusting Data 11")

        self.cursor.execute("SELECT DISTINCT name_of_camera, name_of_feature, value_of_feature "
                            "FROM [AI:Lean].[dbo].[product_database_staging] WHERE value_of_feature "
                            "LIKE '<min>%%</min><max>%%</max><def>%%</def>used'")
        data11 = self.cursor.fetchall()

        for camera_name, feature_name, value in data11:
            numbers = re.findall(r'[-+]?\d*\.\d+|\d+', value)
            if len(numbers) == 3:
                min_val, max_val, def_val = numbers
                self.cursor.execute("""
                INSERT INTO [AI:Lean].[dbo].[product_database] (name_of_camera, name_of_feature, value_of_feature)
                VALUES (%s, %s, %s)
                """, (camera_name, feature_name + "Min", min_val))
                self.cursor.execute("""
                INSERT INTO [AI:Lean].[dbo].[product_database] (name_of_camera, name_of_feature, value_of_feature)
                VALUES (%s, %s, %s)
                """, (camera_name, feature_name + "Max", max_val))
                self.cursor.execute("""
                INSERT INTO [AI:Lean].[dbo].[product_database] (name_of_camera, name_of_feature, value_of_feature)
                VALUES (%s, %s, %s)
                """, (camera_name, feature_name + "Default", def_val))
                self.cursor.execute("""
                INSERT INTO [AI:Lean].[dbo].[product_database] (name_of_camera, name_of_feature, value_of_feature)
                VALUES (%s, %s, 'used')
                """, (camera_name, feature_name + "Used"))
            else:
                print("Error: ", camera_name, feature_name, value)
        self.conn.commit()

        for camera_name, feature_name, value in data11:
            self.cursor.execute("""
            DELETE FROM [AI:Lean].[dbo].[product_database]
            WHERE name_of_camera = %s AND name_of_feature = %s AND value_of_feature = %s
            """, (camera_name, feature_name, value))
        self.conn.commit()


        print("Clearing unfilled data")

        self.cursor.execute("SELECT DISTINCT name_of_feature FROM product_database")
        features = self.cursor.fetchall()

        for feature in features:
            self.cursor.execute("""
            SELECT 1 FROM product_database
            WHERE name_of_feature = %s AND value_of_feature <> 'None' AND value_of_feature <> ''
            """, (feature,))
            if self.cursor.fetchone() is None:
                self.cursor.execute("""
                DELETE FROM product_database
                WHERE name_of_feature = %s
                """, (feature,))
                print("Feature ", feature, " deleted")
            else:
                print("Feature ", feature, " checked")
        self.conn.commit()


        print("Clearing empty data")

        self.cursor.execute("SELECT DISTINCT name_of_camera, name_of_feature, value_of_feature "
                    "FROM product_database "
                    "WHERE value_of_feature = 'None'")
        empty_data = self.cursor.fetchall()

        for camera_name, feature_name, value in empty_data:
            self.cursor.execute("""
            DELETE FROM [AI:Lean].[dbo].[product_database]
            WHERE name_of_camera = %s AND name_of_feature = %s AND value_of_feature = %s
            """, (camera_name, feature_name, value))
        self.conn.commit()

        self.cursor.execute("SELECT DISTINCT name_of_camera, name_of_feature, value_of_feature "
                            "FROM product_database "
                            "WHERE value_of_feature is NULL")
        empty_data = self.cursor.fetchall()

        for camera_name, feature_name, value in empty_data:
            self.cursor.execute("""
                    DELETE FROM [AI:Lean].[dbo].[product_database]
                    WHERE name_of_camera = %s AND name_of_feature = %s AND value_of_feature is NULL
                    """, (camera_name, feature_name))
        self.conn.commit()




        self.conn.close()

    def pushingNewFeaturesToPinecone(self):
        """
        This function is used to push the new features to Pinecone
        :return:
        """
        print("Uploading new features to Pinecone")
        Uploader.Uploader().initialUploadName_of_feature_modified_sql_db()