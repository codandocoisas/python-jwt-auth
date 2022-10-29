## JWT FASTAPI PYTHON BOILER PLATE

### steps to run the project
- create a postgres container using docker
```
docker run --name some-postgres -p 5432:5432 -e POSTGRES_PASSWORD=mysecretpassword -e POSTGRES_USER=postgres -e POSTGRES_DB=mydatabasename -d postgres:latest
```
- create a `.env` file in the folder with the following environment variables:

```
SECRET_KEY={A 32 HEX AND UNGUESSABLE STRING}
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
DATABASE_URL=postgresql+psycopg2://{username}:{password}@localhost:5432/{db_name}
```
- run `alembic upgrade head` to run migrations
- if you want to run this project in https you will need to generate ssl keys in the root folder
 ```
openssl req -newkey rsa:2048 -new -nodes -x509 -days 3650 -keyout key.pem -out cert.pem
```
- run `main.py` to start the project
- once project is running go to [title](https://localhost:8000/docs) and you'll be able to access swagger and check routes
- the project has ***only the necessary*** to start an API with JWT authentication using *FASTAPI* and ASGI server 