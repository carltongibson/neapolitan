
test +FLAGS='':
    python tests/manage.py test tests/ {{FLAGS}}

coverage:
    coverage erase
    coverage run tests/manage.py test tests/
    coverage report
