import secrets
# MYSQL Configuration
MYSQL_DATABASE_USERNAME = 'root'
MYSQL_DATABASE_PASSWORD = 'snowflake6365stark'
MYSQL_DATABASE_DB = 'dp_sp'
MYSQL_DATABASE_HOST = 'mysql-development'
MYSQL_DATABASE_PORT = 3306
MYSQL_AUTH_PLUGIN = 'mysql_native_password'

# API/Flask Keys
ZOMATO_API_KEY = "eeb2c8d6b993c20bfd856f1b092ea075"
GOOGLE_MAPS_API_KEY = "AIzaSyBTIYFA8avWuLBtGteyCUXhFdDFrqlS648"
SECRET_KEY = secrets.token_urlsafe(16)
SECURITY_PASSWORD_SALT = "rowan"

#Email Config
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USERNAME = 'decidedine@gmail.com'
MAIL_PASSWORD = 'DineDecide'
MAIL_USE_TLS = False
MAIL_USE_SSL = True