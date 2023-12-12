# Task Management Application


### Description
Base FastApi project for applying general RestAPI application cases to manage tasks
![openapi-docs](./doc/images/openapi-docs.png)

### Concept
1. minimal functionality
2. Easy to read
3. Convincing architecture


### Base models
1. user
2. task


### Integrated with
1. Python3.9+
2. Fastapi 0.99.1
3. Database PostgreSQL
4. JWT authentication


### Server
1. uvicorn app.main:app --reload
2. options
    1. host: `--host 0.0.0.0`
    2. port: `--port 8000`


### References
1. [FastAPI official docs](https://fastapi.tiangolo.com/)
2. [alembic official tutorial](https://alembic.sqlalchemy.org/en/latest/tutorial.html)