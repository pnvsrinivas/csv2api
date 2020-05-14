import os
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv(os.path.join(BASE_DIR, '.env'))

from .common import *

if os.environ.get('CSV2API_SETTINGS') == 'production':
   from .production import *
else:
   from .development import *