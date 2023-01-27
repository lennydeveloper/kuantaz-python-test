# kuantaz-python-test
The main objective of this test is to develop a REST API with Python + Flask managing the data through a PostgreSQL database for three entities that are Institutions, Projects and Users.

### Documentation

The API documentation can be found at the following link: `https://documenter.getpostman.com/view/16939864/2s8ZDeSyYL`

### How to create a virtual environment

```bash
python -m venv name_of_virtual_env
source name_of_virtual_env/Scripts/activate
```

### Requirements

- Python 3.x

### How to install dependency libraries
```bash
cd kuantaz-python-test
pip install -r requirements.txt
```

### Run the flask project

```python
flask run
```

In Flask default port is 5000: `http://localhost:5000/<endpoint>`

### How to test database from console

```python
flask shell
from app import db
from models import Institucion, Proyecto, Usuario
e.g. Institucion.query.all()
```

### How to run unit test cases

```python
pytest test.py
```

![test_cases](https://user-images.githubusercontent.com/90154644/214923836-b9b04f8e-b292-4070-9f09-87c870ac8251.png)

### References

- [SQLAlchemy](https://docs.sqlalchemy.org/en/14/intro.html)
- [pytest](https://docs.pytest.org/en/7.2.x/)
- [Flask](https://flask.palletsprojects.com/en/2.2.x/)