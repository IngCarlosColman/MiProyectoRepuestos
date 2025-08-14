import os
from pathlib import Path
import sys

# =================================================================
# Configuración de librerías geoespaciales para Django en Windows
# =================================================================
# Esta sección establece las variables de entorno para que GeoDjango
# pueda encontrar las librerías GDAL y PROJ en un entorno de Conda.
# Esto ayuda a evitar problemas de codificación y de rutas.

if "win32" in sys.platform and 'CONDA_PREFIX' in os.environ:
    # La ruta base de las librerías suele ser 'Library' dentro del entorno Conda.
    conda_lib_path = Path(os.environ['CONDA_PREFIX']) / 'Library'

    # Establecemos las rutas de datos para PROJ y GDAL, que son necesarias
    # y pueden ser el origen del error de codificación.
    os.environ['PROJ_DATA'] = str(conda_lib_path / 'share' / 'proj')
    os.environ['GDAL_DATA'] = str(conda_lib_path / 'share' / 'gdal')

    # Ahora buscamos los archivos DLL en la carpeta 'bin'
    conda_bin_path = conda_lib_path / 'bin'

    # Buscamos el archivo GDAL DLL. El nombre del archivo puede variar.
    gdal_dll = next(
        (str(path) for path in conda_bin_path.glob('gdal*.dll')),
        None
    )
    # Buscamos el archivo GEOS DLL.
    geos_dll = next(
        (str(path) for path in conda_bin_path.glob('geos_c*.dll')),
        None
    )

    # Si se encuentran los archivos, configuramos las variables de entorno de Django.
    if gdal_dll:
        os.environ['GDAL_LIBRARY_PATH'] = gdal_dll
    else:
        print("Advertencia: No se pudo encontrar un archivo gdal.dll en el entorno de Conda.")
    
    if geos_dll:
        os.environ['GEOS_LIBRARY_PATH'] = geos_dll
    else:
        print("Advertencia: No se pudo encontrar un archivo geos_c.dll en el entorno de Conda.")

    # Aseguramos que la ruta de las librerías esté en el PATH del sistema
    # para que otros programas la encuentren si es necesario.
    if str(conda_bin_path) not in os.environ.get('PATH', ''):
        os.environ['PATH'] += os.pathsep + str(conda_bin_path)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-@1r+2j5c5$wz2!n%m#f@r3!$c_i8j_c*2*v&i6$u^k8+w-q-m!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',   # Requerido para usar PostGIS
    'django_filters',
    'corsheaders',          # Para permitir peticiones desde el frontend de React
    'rest_framework',       # Para la API
    'buscador',             # Tu aplicación
]

# Configuración de Django REST Framework para usar el filtro
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
    ]
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',    # Middleware de CORS
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Ahora Django buscará el index.html directamente en la carpeta 'build'
        'DIRS': [os.path.join(BASE_DIR, 'build')], 
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'sisrep_db', # Revisa que el nombre sea correcto
        'USER': 'postgres',
        'PASSWORD': 'root',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'es-es'

TIME_ZONE = 'America/Asuncion'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field
#STATICFILES_DIRS = [
#    os.path.join(BASE_DIR, 'build'),
#]
#STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CORS
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000", # Permite a React acceder a la API
]
