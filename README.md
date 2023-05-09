# py-backend-app

[FastAPI](https://fastapi.tiangolo.com)-based backend service which implements registration and login services with
optional 2FA.

#### 1) Clone the Repository
```bash
$ git clone https://github.com/000emanresu111/py-backend-app.git
```
#### 2) Install deps with Poetry

Ensure you have [Poetry](https://python-poetry.org) installed.

```bash
$ poetry install # or "make install"
```

#### 3) Run docker compose

```bash
$ docker compose up
```
#### 4) Populate db

```bash
$ python playground.py
```
#### 5) API documentation

Go to http://localhost:8086/docs to see the API documentation and interact with it.

#### Launch server manually (if needed)

```bash
$ uvicorn main:app --host 0.0.0.0 --port 8086 --reload
```

### Test

#### Run tests
```bash
$ pytest -vv
```

### Code formatting

This project uses [black](https://github.com/psf/black) code formatter.

### Project description

- The backend service will provide three routes: one to register users, one to log them in, and a third one to handle
  the 2FA process if it's enabled. The communication protocol will be HTTP, and the session will be managed via
  stateless authentication with JWT.

- The service will operate inside a micro-services architecture and will be shipped inside a Docker image for deployment
  in the cloud. We will use PostgreSQL as the database for storing user information.

- We will use Pydantic for data validation and FastAPI for building the web service. We will also use pytest for
  automated testing.

- For the OTP email sending, we will use a fake implementation that logs the OTP on the console instead of sending the
  email for real. This simplifies the implementation and testing process.

### Example

You can register a user, then log in and verify the 2FA (OTP) code.

#### 1) Signup

Request
```bash
POST /users
{
  "email": "test01@example.com",
  "password": "test",
  "username": "test01",
  "is_2fa_enabled": true
}
```

Response body
```bash
{
  "email": "test01@example.com",
  "password": "$2b$12$Gp2bpwLXo.D8nGaRin9/VO4JfTqAPpmH1fUSSRi.8.5s389QJ.8py",
  "username": "test01",
  "is_2fa_enabled": true
}
```

#### 2) Login

Request
```bash
curl -X 'POST' \
  'http://localhost:8086/login' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'username=test01&password=test&send_otp=true'
```

Response body
```bash
{
  "detail": "Please provide the following OTP: 602580"
}
```
#### 3) Verify 2FA

Request
```bash
curl -X 'POST' \
  'http://localhost:8086/verify-2fa' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'username=test01&otp_code=602580'
```

Response body
```bash
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0MDEiLCJleHAiOjE2ODM1NjgzMjR9.XOx1ZW8usgKG2_nDdccvvMcNSSPBn88ZdTRC9ObzKxM",
  "token_type": "bearer"
}
```
