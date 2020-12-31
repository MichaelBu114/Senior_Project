import secrets
# MYSQL Configuration
MYSQL_DATABASE_USER = 'root'
MYSQL_DATABASE_PASSWORD = 
MYSQL_DATABASE_DB = 'dp_sp'
MYSQL_DATABASE_HOST = 'mysql-development'
MYSQL_DATABASE_PORT = 3306
MYSQL_AUTH_PLUGIN = 'mysql_native_password'

# API/Flask Keys
ZOMATO_API_KEY = 
GOOGLE_MAPS_API_KEY = 
MAPAPIKEY = 
SECRET_KEY = secrets.token_urlsafe(16)
SECURITY_PASSWORD_SALT = 

#Email Config
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465
MAIL_USERNAME = 
MAIL_PASSWORD =
MAIL_USE_TLS = False
MAIL_USE_SSL = True
