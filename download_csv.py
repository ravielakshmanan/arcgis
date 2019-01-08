from google.cloud import storage
client = storage.Client()
bucket = client.get_bucket('magicgrant.appspot.com')
blob = bucket.blob('transposed.csv')
# blob = bucket.get_blob('transposed.csv')
# downloaded_blob = blob.download_as_string()
blob.download_to_filename('iri_data.csv')
print('Blob {} downloaded to {}.'.format('transposed.csv','iri_data.csv'))