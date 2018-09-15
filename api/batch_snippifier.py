import io
import os

from pydub import AudioSegment
from pydub.utils import mediainfo
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

from google.cloud import storage

from create_snippet import create_snippet

GCS_BUCKET = "bumblebee-audiofiles"
GCS_RAW_PATH = "raw"
GCS_SNIPPET_PATH = "snippets"
LOCAL_RAW_PATH = GCS_RAW_PATH
LOCAL_SNIPPET_PATH = GCS_SNIPPET_PATH


def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print('File {} uploaded to {}.'.format(
        source_file_name,
        destination_blob_name))

def download_blob(bucket_name, source_blob_name, destination_file_name):
    """Downloads a blob from the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(source_blob_name)

    blob.download_to_filename(destination_file_name)

    print('Blob {} downloaded to {}.'.format(
        source_blob_name,
        destination_file_name))

def convert_to_wav(file_name):
    wav_name = file_name.replace(".mp3", ".wav")
    AudioSegment.from_mp3(file_name).set_channels(1).export(wav_name, format="wav")
    upload_blob(GCS_BUCKET, wav_name, wav_name)
    return wav_name


def get_word_infos(file_name):
    gcs_uri = 'gs://%s/%s' % (GCS_BUCKET, file_name)

    speech_client = speech.SpeechClient()

    audio = types.RecognitionAudio(uri=gcs_uri)
    config = types.RecognitionConfig(
        language_code='en-US',
        enable_word_time_offsets=True
    )

    operation = speech_client.long_running_recognize(config, audio)

    print('Waiting for operation to complete...')
    response = operation.result(timeout=900)

    word_infos = []
    for result in response.results:
        for alternative in result.alternatives:
            for word_info in alternative.words:
                word_infos.append({
                    "word": word_info.word,
                    "start": word_info.start_time.seconds + word_info.start_time.nanos / 1000000000.0,
                    "end": word_info.end_time.seconds + word_info.end_time.nanos / 1000000000.0
                })
    return word_infos

def generate_snippet(file_name, word_info):
    source = AudioSegment.from_wav(file_name)
    snippet = source[word_info["start"]*1000.0:word_info["end"]*1000.0]
    snippet_file_name = "%s/%s_%s_%s_%s" % (GCS_SNIPPET_PATH ,word_info["word"], str(word_info["start"]), str(word_info["end"]), file_name.split("/")[1])
    snippet.export(snippet_file_name, format="wav")
    return snippet_file_name


 '''
 1. ) Convert an audio file to single channel wav
 2. ) Submit each file to Google Speech API
 3. ) Use start and end values to trim audio files into one word snippets
 4. ) Upload snippets to GCS
 5. ) Call Drew's function to add snippet info to DB
 '''
def process_file(file_name):
    raw_file_name = file_name
    file_name = convert_to_wav(file_name)
    word_infos = get_word_infos(file_name)
    for word_info in word_infos:
        snippet_file_name = generate_snippet(file_name, word_info)
        upload_blob(GCS_BUCKET, snippet_file_name, snippet_file_name)

        raw_url = "gs://%s/%s" % (GCS_BUCKET, raw_file_name)
        snippet_url = "gs://%s/%s" % (GCS_BUCKET, snippet_file_name)

        create_snippet(word_info["word"], raw_url, snippet_url, int(word_info["start"]), int(word_info["end"]))
