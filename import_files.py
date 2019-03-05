from google.cloud import storage
import os

client = storage.Client()

bucket = client.get_bucket('noah-water.appspot.com')

blobs = bucket.list_blobs(prefix='trends3/Part6')

os.system("gsutil acl ch -u qqbi676scrf4nlgyg6e3hqrm6e@speckle-umbrella-16.iam.gserviceaccount.com:W gs://noah-water.appspot.com")

for blob in blobs:
	print(blob.name)
	file_read_perm = "gsutil acl ch -u qqbi676scrf4nlgyg6e3hqrm6e@speckle-umbrella-16.iam.gserviceaccount.com:R gs://noah-water.appspot.com/" + blob.name
	os.system(file_read_perm)
	# print(file_read_perm)
	file_import = "gcloud sql import csv precipitation gs://noah-water.appspot.com/" + blob.name + " --database=prec_anomaly --table=precipitation_trend -q"
	os.system(file_import)
	# print(file_import)