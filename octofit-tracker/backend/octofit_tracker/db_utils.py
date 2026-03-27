from django.db import connection
from django.conf import settings
from pymongo import ASCENDING

def get_db():
    return connection.cursor().db_client[settings.DATABASES['default']['NAME']]
