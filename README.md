# py-backend-app
[FastAPI](https://fastapi.tiangolo.com)-based backend service which implements registration and login services with optional 2FA.

### Clone the Repository
First, clone the repository:
```bash
$ git clone https://github.com/000emanresu111/py-backend-app.git
```

### Run PostgreSQL docker image
```bash
$ docker compose up
```

### Launch server
```bash
$ uvicorn app.main:app --host localhost --port 8086 --reload
```

### API documentation

Go to http://localhost:8086/docs to see the API documentation and interact with it.

### Test

#### Run single test file

```bash
$ pytest test/test_file_to_run.py
```

Example:

```bash
$ pytest -s test/test_users.py -vv
```

### Code formatting

This project uses [black](https://github.com/psf/black) code formatter.

## Solution overview

- The backend service will provide three routes: one to register users, one to log them in, and a third one to handle the 2FA process if it's enabled. The communication protocol will be HTTP, and the session will be managed via stateless authentication with JWT.

- The service will operate inside a micro-services architecture and will be shipped inside a Docker image for deployment in the cloud. We will use PostgreSQL as the database for storing user information.

- We will use Pydantic for data validation and FastAPI for building the web service. We will also use pytest for automated testing.

- For the OTP email sending, we will use a fake implementation that logs the OTP on the console instead of sending the email for real. This simplifies the implementation and testing process.
