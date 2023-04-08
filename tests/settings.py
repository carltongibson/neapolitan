DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    },
}
MIDDLEWARE = []
ROOT_URLCONF = "tests.tests"


INSTALLED_APPS = [
    "neapolitan",
    "tests",
]
