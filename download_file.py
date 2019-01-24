from google.cloud import storage

file_name = 'credentials.txt'

client = storage.Client()

bucket = client.get_bucket('noah-water.appspot.com')

blob = bucket.blob(file_name)
# blob = bucket.get_blob('transposed.csv')

# downloaded_blob = blob.download_as_string()
blob.download_to_filename(file_name)

print('Blob {} downloaded to {}.'.format(file_name, file_name))