from upload.UpdateUploader import UpdateUploader
from data_package.PDB_Handler.PDBSetup import PDBSetup
import data_package.SQL_Connection_Provider.SQLConnectionProvider as SQLConnectionProvider

sql_connection = SQLConnectionProvider.SQLConnectionProvider().create_connection()

UpdateUploader().fetchingStagingPDB()
PDBSetup(sql_connection).settingUpPDB()
PDBSetup(sql_connection).pushingNewFeaturesToPinecone()
