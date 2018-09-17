import os
from api import models
from google.cloud import storage

GCS_BUCKET = "bumblebee-audiofiles"
GCS_RAW_PATH = "raw"
GCS_SNIPPET_PATH = "snippets"
LOCAL_FILE_PATH = '/Users/connerchyung/Desktop/to-upload'


def upload_snippets():
    for file_name in os.listdir(LOCAL_FILE_PATH):

        if file_name is not '.DS_Store':
            split_file_name = file_name.split('_')
            word_string = split_file_name[0]
            audio_file = split_file_name[1]


            try:
                word = models.Word.objects.get(value=word_string)
            except models.Word.DoesNotExist:
                word = models.Word(value=word_string)
                word.save()

            try:
                audio = models.Audio.objects.get(name=audio_file)
            except models.Audio.DoesNotExist:
                audio = None

            if not audio:
                # make fake audio file
                audio = models.Audio(name=audio_file, url='localhost', description=audio_file)
                audio.save()

            # upload snippet
            snippet_file_name = "%s/%s_%s_%s_%s" % (GCS_SNIPPET_PATH, word_string, '0', '1', file_name)
            upload_blob(GCS_BUCKET, file_name, snippet_file_name)

            gcs_uri = 'gs://%s/%s' % (GCS_BUCKET, snippet_file_name)
            snippet = models.Snippet(word=word, audio=audio, start=0, end=1, url=gcs_uri)
            snippet.save()


def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(LOCAL_FILE_PATH + '/' + source_file_name)

    print('File {} uploaded to {}.'.format(
        source_file_name,
        destination_blob_name))