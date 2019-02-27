from google.cloud import storage
import os
import sqlalchemy

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = './noah_credentials.json'
os.environ["CLOUD_SQL_CONNECTION_NAME"] ='noah-water:us-east4:precipitation'
os.environ["DB_USER"] = 'root'
os.environ["DB_PASS"] = 'y3hsG5O7cDCPv00B'
os.environ["DB_NAME"] = 'prec_anomaly'

# Manage SQL connection pool
db = sqlalchemy.create_engine(
    sqlalchemy.engine.url.URL(
        drivername='mysql+pymysql',
        username=os.environ["DB_USER"],
        password=os.environ["DB_PASS"],
        database=os.environ["DB_NAME"],
        query={
            'unix_socket': '/cloudsql/{}'.format(os.environ["CLOUD_SQL_CONNECTION_NAME"])
        }
    ),
    pool_size=10,
    max_overflow=2,
    pool_timeout=30,
    pool_recycle=1800
)

client = storage.Client()

bucket = client.get_bucket('noah-water.appspot.com')

blobs = bucket.list_blobs(prefix='trend_data')

with db.connect() as conn:
	for blob in blobs:
		print(blob)
		downloaded_blob = blob.download_as_string().decode('utf-8') 
		blob_list = downloaded_blob.split('\n')
		for row in blob_list:
			row_data = row.split(',')
			if row_data[0] != 'placeholder' and row_data[0] != 'Time':
				print(row_data)
				row_data[3] = '0' if not row_data[3] else row_data[3]
				row_data[4] = '0' if not row_data[4] else row_data[4]
				row_data[5] = '0' if not row_data[5] else row_data[5]
				query = """INSERT INTO precipitation_trend values (%s, %s, %s, %s, %s, %s)"""
				conn.execute(query, (row_data[0], row_data[1], row_data[2], float(row_data[3]), float(row_data[4]), float(row_data[5])))