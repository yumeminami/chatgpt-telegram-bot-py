# black all python files in the project but exclude the __init__.py files and redis/ directory
black --exclude=__init__.py --exclude=redis/  --exclude=tests/  --exclude=env/  --line-length=79 . 
# black .
# autoflake8 --in-place --remove-unused-variables --recursive  --exclude=__init__.py .