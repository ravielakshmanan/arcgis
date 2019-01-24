import os
import sqlalchemy
import datetime
import logging
from collections import defaultdict

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = './mysql_credentials.json'
os.environ["CLOUD_SQL_CONNECTION_NAME"] ='***'
os.environ["DB_USER"] = '***'
os.environ["DB_PASS"] = '***'
os.environ["DB_NAME"] = '***'

logger = logging.getLogger()

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
	pool_size=5,
	max_overflow=2,
	pool_timeout=30,
	pool_recycle=1800
)

def get_processed_data(data):
  processed_data_dict = defaultdict(list)
  
  iri_data_list = []
  for lat, long, anomaly, date in data:
  	date = date.replace('\r', '')
  	coords = "(" + long + ", " + lat + ")"
  	anomaly = anomaly
  	date = date[8:]
  	data_tuple = (coords, anomaly, date)
  	iri_data_list.append(data_tuple)

  for coords, anomaly, date in iri_data_list:
  	if coords not in processed_data_dict:
  		temp_dict = {'dates': [date], 'data': [anomaly]}
  		processed_data_dict[coords] = temp_dict
  	else:
  		processed_data_dict[coords]['dates'].append(date)
  		processed_data_dict[coords]['data'].append(anomaly)

  return processed_data_dict

def get_iri_data_from_gcloud():
    with db.connect() as conn:
        anomaly_data = conn.execute(
            "SELECT * FROM precipitation LIMIT 5"
        ).fetchall()

        print("The size of data returned: " + str(len(anomaly_data)))

        processed_data_dict = get_processed_data(anomaly_data)

    return processed_data_dict

if __name__ == '__main__':
		
		data = get_iri_data_from_gcloud()
		print(data)