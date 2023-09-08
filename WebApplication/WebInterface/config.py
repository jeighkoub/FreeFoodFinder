"""Development configuration."""
import pathlib
# Root of this application, useful if it doesn't occupy an entire domain
APPLICATION_ROOT = '/'
# Secret key for encrypting cookies
SECRET_KEY = b'\xf73\x11\xf3\xb8W\xba\xe1]\xddE=S\\\x14;9-R#\xe1\xc3\xb9\xf2'
#SESSION_COOKIE_NAME = 'login'
# File Upload to var/uploads/
WEBINT_ROOT = pathlib.Path(__file__).resolve().parent.parent
UPLOAD_FOLDER = WEBINT_ROOT / 'var' / 'uploads'
#ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
MAX_CONTENT_LENGTH = 16 * 1024 * 1024
# Database file is var/insta485.sqlite3
DATABASE_FILENAME = WEBINT_ROOT / 'var' / 'WebInterface.sqlite3'