
test +FLAGS='':
    django-admin test --settings=tests.settings --pythonpath=. {{FLAGS}}
