import os

from google.cloud import storage

import engine.serializer as file_serializer

TEMP_FILENAME = 'tmp.wrld'


def save(world, path):
    """
    Saves world and upload to google bucket
    """
    file_serializer.save(world, TEMP_FILENAME)
    client = storage.Client()
    blob = storage.Blob.from_string(path, client=client)
    blob.upload_from_filename(TEMP_FILENAME)
    os.remove(TEMP_FILENAME)


def load(path):
    """
    Loads world from google bucket
    """
    client = storage.Client()
    blob = storage.Blob.from_string(path, client=client)
    blob.download_to_filename(TEMP_FILENAME)
    result = file_serializer.load(TEMP_FILENAME)
    os.remove(TEMP_FILENAME)
    return result
