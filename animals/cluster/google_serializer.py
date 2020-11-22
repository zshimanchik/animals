import os

from google.cloud import storage
import random

import engine.serializer as file_serializer

TEMP_FILENAME_PATTERN = 'tmp{}.wrld'


def save(world, path):
    """
    Saves world and upload to google bucket
    """
    temp_filename = TEMP_FILENAME_PATTERN.format(random.randint(0, 200))
    file_serializer.save(world, temp_filename)
    client = storage.Client()
    blob = storage.Blob.from_string(path, client=client)
    blob.upload_from_filename(temp_filename)
    os.remove(temp_filename)


def load(path):
    """
    Loads world from google bucket
    """
    temp_filename = TEMP_FILENAME_PATTERN.format(random.randint(0, 200))
    client = storage.Client()
    blob = storage.Blob.from_string(path, client=client)
    blob.download_to_filename(temp_filename)
    result = file_serializer.load(temp_filename)
    os.remove(temp_filename)
    return result
