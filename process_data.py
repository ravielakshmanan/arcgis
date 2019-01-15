import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = './noah_credentials.json'

collection_name = "precipitation_test"

def process_data(doc_ref):
    docs = doc_ref.get()
    json_data = []
    for doc in docs:
        json_data.append(doc.to_dict())
    return json_data


def get_iri_data_from_store(store):
    doc_ref = store.collection(collection_name).limit(5)
    json_data = process_data(doc_ref)
    return json_data


# Use a service account
cred = credentials.Certificate(os.environ["GOOGLE_APPLICATION_CREDENTIALS"])
firebase_admin.initialize_app(cred)

db = firestore.client()

json_data = get_iri_data_from_store(db)

data_dict = {}
for row in json_data:
	coords = "(" + row['long'] + ", " + row['lat'] + ")"
	anomaly = row['anomaly']
	date = row['date'][8:]
	if coords not in data_dict:
		data_dict[coords] = {"dates":[date], "data":[anomaly]}
	else:
		value = data_dict[coords]
		dates_list = value["dates"].append(date)
		data_list = value["data"].append(anomaly)
		data_dict[coords] = {"dates":dates_list, "data":data_list}

print(data_dict)