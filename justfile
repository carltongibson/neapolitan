
test +FLAGS='':
    django-admin test --settings=tests.settings --pythonpath=. {{FLAGS}}

coverage:
    coverage erase
    coverage run -m django test --settings=tests.settings --pythonpath=.
    coverage report
