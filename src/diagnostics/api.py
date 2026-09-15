import os
import sqlite3
from datetime import datetime, timedelta, timezone

import bcrypt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from pydantic import BaseModel, Field

DATABASE = "api.db"

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "rabtech-demo-secret-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI(
    title="RabTech Secure Inventory API",
    description="FastAPI microservice with JWT authentication and secure CRUD operations.",
    version="1.0.0",
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# ---------------- DATABASE ----------------

def get_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            quantity INTEGER NOT NULL CHECK(quantity >= 0)
        )
    """)

    connection.commit()
    connection.close()


init_db()


# ---------------- SCHEMAS ----------------

class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=6, max_length=100)


class Token(BaseModel):
    access_token: str
    token_type: str


class ProductCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    quantity: int = Field(ge=0)


class ProductUpdate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    quantity: int = Field(ge=0)


class ProductOut(BaseModel):
    id: int
    name: str
    quantity: int


# ---------------- PASSWORD HASHING ----------------

def hash_password(password: str) -> str:
    password_bytes = password.encode("utf-8")
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed.decode("utf-8")


def verify_password(password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(
        password.encode("utf-8"),
        password_hash.encode("utf-8"),
    )


# ---------------- JWT ----------------

def create_access_token(username: str):
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": username,
        "exp": expire,
    }

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired authentication token",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )

        username = payload.get("sub")

        if not username:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    connection = get_connection()
    user = connection.execute(
        "SELECT * FROM users WHERE username = ?",
        (username,),
    ).fetchone()
    connection.close()

    if user is None:
        raise credentials_exception

    return dict(user)


# ---------------- REGISTER ----------------

@app.post("/register", status_code=201)
def register(user: UserCreate):
    connection = get_connection()

    existing_user = connection.execute(
        "SELECT id FROM users WHERE username = ?",
        (user.username,),
    ).fetchone()

    if existing_user:
        connection.close()
        raise HTTPException(
            status_code=400,
            detail="Username already exists",
        )

    password_hash = hash_password(user.password)

    connection.execute(
        "INSERT INTO users (username, password_hash) VALUES (?, ?)",
        (user.username, password_hash),
    )

    connection.commit()
    connection.close()

    return {
        "message": "User registered successfully",
        "username": user.username,
    }


# ---------------- LOGIN ----------------

@app.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    connection = get_connection()

    user = connection.execute(
        "SELECT * FROM users WHERE username = ?",
        (form_data.username,),
    ).fetchone()

    connection.close()

    if user is None or not verify_password(
        form_data.password,
        user["password_hash"],
    ):
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(user["username"])

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


# ---------------- CURRENT USER ----------------

@app.get("/users/me")
def read_current_user(current_user=Depends(get_current_user)):
    return {
        "id": current_user["id"],
        "username": current_user["username"],
    }


# ---------------- CREATE PRODUCT ----------------

@app.post("/products", response_model=ProductOut, status_code=201)
def create_product(
    product: ProductCreate,
    current_user=Depends(get_current_user),
):
    connection = get_connection()

    cursor = connection.execute(
        "INSERT INTO products (name, quantity) VALUES (?, ?)",
        (product.name, product.quantity),
    )

    product_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return {
        "id": product_id,
        "name": product.name,
        "quantity": product.quantity,
    }


# ---------------- READ PRODUCTS ----------------

@app.get("/products", response_model=list[ProductOut])
def get_products(current_user=Depends(get_current_user)):
    connection = get_connection()

    products = connection.execute(
        "SELECT id, name, quantity FROM products"
    ).fetchall()

    connection.close()

    return [dict(product) for product in products]


# ---------------- READ ONE PRODUCT ----------------

@app.get("/products/{product_id}", response_model=ProductOut)
def get_product(
    product_id: int,
    current_user=Depends(get_current_user),
):
    connection = get_connection()

    product = connection.execute(
        "SELECT id, name, quantity FROM products WHERE id = ?",
        (product_id,),
    ).fetchone()

    connection.close()

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )

    return dict(product)


# ---------------- UPDATE PRODUCT ----------------

@app.put("/products/{product_id}", response_model=ProductOut)
def update_product(
    product_id: int,
    product: ProductUpdate,
    current_user=Depends(get_current_user),
):
    connection = get_connection()

    existing = connection.execute(
        "SELECT id FROM products WHERE id = ?",
        (product_id,),
    ).fetchone()

    if existing is None:
        connection.close()
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )

    connection.execute(
        """
        UPDATE products
        SET name = ?, quantity = ?
        WHERE id = ?
        """,
        (product.name, product.quantity, product_id),
    )

    connection.commit()

    updated = connection.execute(
        "SELECT id, name, quantity FROM products WHERE id = ?",
        (product_id,),
    ).fetchone()

    connection.close()

    return dict(updated)


# ---------------- DELETE PRODUCT ----------------

@app.delete("/products/{product_id}")
def delete_product(
    product_id: int,
    current_user=Depends(get_current_user),
):
    connection = get_connection()

    existing = connection.execute(
        "SELECT id FROM products WHERE id = ?",
        (product_id,),
    ).fetchone()

    if existing is None:
        connection.close()
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )

    connection.execute(
        "DELETE FROM products WHERE id = ?",
        (product_id,),
    )

    connection.commit()
    connection.close()

    return {
        "message": "Product deleted successfully",
        "product_id": product_id,
    }