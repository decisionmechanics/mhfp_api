from datetime import datetime, timedelta
from fastapi import FastAPI, HTTPException, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from jose import jwt
from pydantic import BaseModel

VERSION = "0.1.2"
ALGORITHM = "HS256"
# This should be an environment variable in a production app
SECRET_KEY = "58295488f4cf41bd37e8a4848569638bca84493107df4d28aa3d3405f9a8186b"
COOKIE_EXPIRATION_PERIOD_SECONDS = 3600


class Account(BaseModel):
    email: str
    password: str

    class Config:
        schema_extra = {
            "example": {"email": "rmckinnon@avenirhealth.org", "password": "pw"}
        }


class User(BaseModel):
    email: str

    class Config:
        schema_extra = {"example": {"email": "rmckinnon@avenirhealth.org"}}


def create_authentication_token(email: str) -> str:
    """Create a JWT authentication token for the given email address."""

    expiration_time = datetime.utcnow() + timedelta(
        seconds=COOKIE_EXPIRATION_PERIOD_SECONDS
    )

    return jwt.encode(
        {"email": email, "exp": expiration_time}, SECRET_KEY, algorithm=ALGORITHM
    )


def decode_authentication_token(token: str) -> str:
    """Decode the JWT authentication token and return the email address."""

    data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    return data["email"]


def verify_authentication_token(token: str) -> bool:
    """Verify the authentication token and return True if valid."""

    # Missing tokens are invalid
    if not token:
        return False

    # Invalid tokens throw an exception when decoded
    try:
        decode_authentication_token(token)
    except jwt.JWTError:
        return False

    return True


def set_authentication_cookie(response: Response, authentication_token: str) -> None:
    """Set the authentication cookie in the response."""

    response.set_cookie(
        key="authentication_token",
        value=authentication_token,
        httponly=True,
        samesite="none",
        secure=True,
    )


# Create the API app
app = FastAPI(
    title="Auth Skeleton",
    description="Skeleton demonstration of using JWT and HTTP-only cookies to authenticate users.",
    version=VERSION,
    # Hide schemas
    swagger_ui_parameters={"defaultModelsExpandDepth": -1},
)

# Enable CORS for all requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def validate_request(request: Request, call_next):
    """FastAPI middleware to validate the request."""

    # Allow unauthenticated requests to the OpenAPI documentation or the session endpoint
    if not request.url.path.startswith("/api") or request.url.path == "/api/session":
        return await call_next(request)

    authentication_token = request.cookies.get("authentication_token")

    # Reject requests with invalid authentication tokens
    if verify_authentication_token(authentication_token):
        # Complete the processing of the request
        response = await call_next(request)

        email = decode_authentication_token(authentication_token)

        # Refresh the authentication token so that it doesn't expire during the session
        updated_authentication_token = create_authentication_token(email)
        set_authentication_cookie(response, updated_authentication_token)

        return response
    else:
        return JSONResponse("Unauthorized", status_code=status.HTTP_401_UNAUTHORIZED)


@app.post(
    "/api/session",
    tags=["session"],
    response_model=User,
    status_code=status.HTTP_201_CREATED,
)
async def sign_in(response: Response, account: Account) -> User:
    """Sign in to the application."""

    # User credentials should be validated here
    if account.password != "pw":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    authentication_token = create_authentication_token(account.email)
    set_authentication_cookie(response, authentication_token)

    return User(email=account.email)


@app.delete("/api/session", tags=["session"], status_code=status.HTTP_204_NO_CONTENT)
async def sign_out(response: Response) -> None:
    """Sign out of the application."""

    # Expire the authentication token
    response.delete_cookie(
        key="authentication_token", httponly=True, samesite="none", secure=True
    )


@app.get("/api/user", tags=["user"], response_model=User)
async def get_user(request: Request) -> User:
    """Get the signed in user's details."""

    authentication_token = request.cookies.get("authentication_token")

    # Decode the authentication token to get the email address
    email = decode_authentication_token(authentication_token)

    return User(email=email)
