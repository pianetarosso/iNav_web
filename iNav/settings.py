# Django settings for iNav project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('marco', 'licantropus83@gmail.com'),
)

MANAGERS = ADMINS
 #'ENGINE': 'django.contrib.gis.db.backends.postgis',

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'inav',#/home/marco/workspace/iNav_web/test.db',#'postgis.db',                      # Or path to database file if using sqlite3.
        'USER': 'django_inav',                      # Not used with sqlite3.
        'PASSWORD': 'y79ce1',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    },
   
}


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = '/home/marco/workspace/iNav_web/media'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = "/home/marco/workspace/iNav_web/static/"

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    "/home/marco/workspace/iNav_web/buildings/static/",
    "/usr/local/lib/python2.7/dist-packages/floppyforms/static/floppyforms/js/",

    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'u8s%@keakevsk34^rw2*y8q#^o8ma5cr_(#78mb5qpw17bz^3#'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'iNav.urls'

TEMPLATE_DIRS = ("/home/marco/workspace/iNav_web/templates"
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.formtools',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    # geoposizione per db
    'django.contrib.gis',
    'floppyforms',
    'buildings',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
#    'allauth.socialaccount.providers.facebook',
#    'allauth.socialaccount.providers.google',
#    'allauth.socialaccount.providers.github',
#    'allauth.socialaccount.providers.linkedin',
#    'allauth.socialaccount.providers.openid',
#    'allauth.socialaccount.providers.persona',
#    'allauth.socialaccount.providers.soundcloud',
#    'allauth.socialaccount.providers.twitter',
    'south',
    'PIL',
    'sorl.thumbnail'
    
)

AUTH_PROFILE_MODULE = 'users.UserProfile'

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.static',
    "django.core.context_processors.media",
    'django.contrib.auth.context_processors.auth',
    "django.core.context_processors.request",
    "allauth.account.context_processors.account",
    "allauth.socialaccount.context_processors.socialaccount",
    'buildings.context_processors.constants',
)

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of 'allauth'
    "django.contrib.auth.backends.ModelBackend",

    # 'allauth' specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
)

ACCOUNT_AUTHENTICATION_METHOD = ("email")
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = (3)
ACCOUNT_EMAIL_REQUIRED = (True)
ACCOUNT_EMAIL_VERIFICATION = ("mandatory")
#ACCOUNT_EMAIL_SUBJECT_PREFIX (="[Site] ")
#Subject-line prefix to use for email messages sent. By default, the name of the current Site #(django.contrib.sites) is used.
ACCOUNT_SIGNUP_PASSWORD_VERIFICATION = (True)
ACCOUNT_UNIQUE_EMAIL = (True)
ACCOUNT_USERNAME_MIN_LENGTH = (1)
ACCOUNT_USERNAME_REQUIRED = (False)
ACCOUNT_PASSWORD_MIN_LENGTH = (6)
SOCIALACCOUNT_QUERY_EMAIL = (ACCOUNT_EMAIL_REQUIRED)
SOCIALACCOUNT_AUTO_SIGNUP = (True)
SOCIALACCOUNT_AVATAR_SUPPORT = (True)


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'licantropus83@gmail.com'
EMAIL_HOST_PASSWORD = 'Sara+Giovanni=Valentino&Carlotta'
EMAIL_PORT = 587

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}



# COSTANTI INTERNE A BUILDING #############################################################################

# Area massima e minima della geometria (m^2)
MAX_GEOMETRY_AREA = 20000
MIN_GEOMETRY_AREA = 10
                
# Lunghezza massima e minima di un lato della geometria
MAX_GEOMETRY_LENGTH = 200
MIN_GEOMETRY_LENGTH = 2
                
# Dimensione massima delle immagini in input (Mb)
MAX_IMAGE_SIZE = 3 * 1024 * 1024

# Numero massimo di piani mappabili
MAX_FLOORS = 6

# Chiave GooGle Maps
G_MAPS = "AIzaSyA6Cod-waBAQwWkS-vEsAIST3x2HtgsaNg"

# NGDC magnetic declination calculator
MAGNETIC_URL = 'http://www.ngdc.noaa.gov/geomag-web/calculators/calculateDeclination'
           
                
