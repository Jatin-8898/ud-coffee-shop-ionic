# Coffee Shop Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in `./src/database/models.py`. We recommend skimming this code first so you know how to interface with the Drink model.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

## Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

Each time you open a new terminal session, run:

```bash
export FLASK_APP=api.py;
```

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## Tasks

### Setup Auth0

1. Create a new Auth0 Account
2. Select a unique tenant domain
3. Create a new, single page web application
4. Create a new API
    - in API Settings:
        - Enable RBAC
        - Enable Add Permissions in the Access Token
5. Create new API permissions:
    - `get:drinks-detail`
    - `post:drinks`
    - `patch:drinks`
    - `delete:drinks`
6. Create new roles for:
    - Barista
        - can `get:drinks-detail`
    - Manager
        - can perform all actions
7. Test your endpoints with [Postman](https://getpostman.com). 
    - Register 2 users - assign the Barista role to one and Manager role to the other.
    - Sign into each account and make note of the JWT.
    - Import the postman collection `./starter_code/backend/udacity-fsnd-udaspicelatte.postman_collection.json`
    - Right-clicking the collection folder for barista and manager, navigate to the authorization tab, and including the JWT in the token field (you should have noted these JWTs).
    - Run the collection and correct any errors.
    - Export the collection overwriting the one we've included so that we have your proper JWTs during review!

## JWTS

`https://fsndjv.auth0.com/authorize?audience=image&response_type=token&client_id=CxWSnhjkNfzCjeakgjTulDLHI5vX41Yd&redirect_uri=http://localhost:8100/tabs/user-page`


- MANAGER USER
`eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkU4OUJDUHNYSlRaM2xpLW1kS0taNiJ9.eyJpc3MiOiJodHRwczovL2ZzbmRqdi5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWViZmIwMTE1ODMwYTkwYzZmZTUxY2Q3IiwiYXVkIjoiaW1hZ2UiLCJpYXQiOjE1ODk4Mjk4MjIsImV4cCI6MTU4OTgzNzAyMiwiYXpwIjoiQ3hXU25oamtOZnpDamVha2dqVHVsRExISTV2WDQxWWQiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTpkcmlua3MiLCJnZXQ6ZHJpbmtzLWRldGFpbCIsInBhdGNoOmRyaW5rcyIsInBvc3Q6ZHJpbmtzIl19.pnb8Gb02O8rV2jHqUR7IJauxAhdOAVAmEZVhIubZNL9Otj96EuzN-UQQ_R5GK_V_OOWS1G3OlD-WFFgK2t2SnQdeOCAQfLwN9GbfqoB4rUDWb7_5UOTMpP6C2Ui_9vl6mgydQcaWHWtvf0HGZj20U5YmWRLkl9b6_yQCpJG7-50Mr2uI9iUMho1_T3I3Wm4C3UxpZcchMvKwQgeob4ZJog8t9NGcIkHJipWBBpOxH421plYrNNC8luRqVAAGx1qcaFBtKRhWykKrX5JjwdECVx-gbMJejAJV2b1DoMmlzxFv1NB-fon3IHKOoQPYfc916P5sRGmsUdmY9h9jqWtOdA`


- BARISTA USER
`eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkU4OUJDUHNYSlRaM2xpLW1kS0taNiJ9.eyJpc3MiOiJodHRwczovL2ZzbmRqdi5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWVjMmM5M2Y2YTMwNTQwY2Q5ODQ1YWY0IiwiYXVkIjoiaW1hZ2UiLCJpYXQiOjE1ODk4Mjc1ODcsImV4cCI6MTU4OTgzNDc4NywiYXpwIjoiQ3hXU25oamtOZnpDamVha2dqVHVsRExISTV2WDQxWWQiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDpkcmlua3MtZGV0YWlsIl19.Nwfg-Ix33d3hamwuGlBglMXBWKp1SIGh1nZUO8AXYYTVc0AE2vyFBaH6hDBzX4_1VRt7hVFV5CGvHCIJ5NOEACoWtFuM_k9hXrn_cLC82eHN_kUr-3Qmw-ZuyNz6DULYRq9WSb9FEBIss3Jv-TYSG4wtbU3cdRq9hvsLPC8PbecQSb-YQ20hUmkB54GXTB6cqGAluRI9SR4tVk1TPWAizQPDuRdUa-GhpdUQwbqDIp6GmujsjLjU37a03MeuTTuucExya_g7uweNZTFuaT7IXE9smNN-XU_S-zhCUqE86CynhbPHvalqYYQb_uWawRqYNhU3py9uxI1gqJr07dEzxw`

### Implement The Server

There are `@TODO` comments throughout the `./backend/src`. We recommend tackling the files in order and from top to bottom:

1. `./src/auth/auth.py`
2. `./src/api.py`
