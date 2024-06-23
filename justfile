
test +FLAGS='':
    python tests/manage.py test tests/ {{FLAGS}}

coverage:
    coverage erase
    coverage run -m tests/manage.py test tests/
    coverage report
