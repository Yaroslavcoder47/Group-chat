import time
from app.data.init import get_connection


def row_to_model(row: tuple):
    pass

def model_to_tuple():
    pass

#USERS
def get_all_users():
    with get_connection() as conn, conn.cursor() as curs:
        query = """SELECT * FROM Users"""
        curs.execute(query)
        return curs.fetchall()

def get_user(email: str):
    with get_connection() as conn, conn.cursor() as curs:
        query = """SELECT * FROM Users WHERE email = %s"""
        params = (email,)
        curs.execute(query, params)
        return curs.fetchone()

def create_user(email: str, username: str, created_at: str): # заменить на Pydantic модель
    with get_connection() as conn, conn.cursor() as curs:
        query = """INSERT INTO Users (email, username, created_at) VALUES (%s, %s, %s)"""
        params = (email, username, created_at)
        curs.execute(query, params)
    return get_user(email)

def modify_user(email: str, username: str):
    with get_connection() as conn, conn.cursor() as curs:
        query = """UPDATE Users SET username=%s WHERE email=%s"""
        params = (username, email)
        curs.execute(query, params)
    return get_user(email)

def delete_user(email: str):
    with get_connection() as conn, conn.cursor() as curs:
        query = """DELETE FROM Users WHERE email = %s"""
        params = (email,)
        res = curs.execute(query, params)
    return bool(res)

#EMAIL_CODES
def get_all_email_codes():
    with get_connection() as conn, conn.cursor() as curs:
        query = """SELECT * FROM Email_codes"""
        curs.execute(query)
        return curs.fetchall()

def get_email_code(email: str):
    with get_connection() as conn, conn.cursor() as curs:
        query = """SELECT * FROM Email_codes WHERE email = %s"""
        params = (email,)
        curs.execute(query, params)
        return curs.fetchone()
    
def create_email_code(email: str, hashed_code: str, verified: bool, created_at: str):
    with get_connection() as conn, conn.cursor() as curs:
        query = """INSERT INTO Email_codes (email, hashed_code, verified, created_at)
        VALUES (%s, %s, %s, %s)"""
        params = (email, hashed_code, verified, created_at)
        curs.execute(query, params)
    return get_email_code(email)

def modify_email_code(email: str, verified_res: bool):
    with get_connection() as conn, conn.cursor() as curs:
        query = """UPDATE Email_codes SET verified = %s WHERE email = %s"""
        params = (verified_res, email)
        curs.execute(query, params)
    return get_email_code(email)

def delete_email_code(email: str):
    with get_connection() as conn, conn.cursor() as curs:
        query = """DELETE FROM Email_codes WHERE email = %s"""
        params = (email,)
        res = curs.execute(query, params)
    return bool(res)


#REFRESH_TOKENS
def get_all_refresh_token():
    with get_connection() as conn, conn.cursor() as curs:
        query = """SELECT * FROM Refresh_token"""
        curs.execute(query)
        return curs.fetchall()

def get_refresh_token(email: str):
    with get_connection() as conn, conn.cursor() as curs:
        query = """SELECT Refresh_tokens.id, email, hashed_token, expires_at, Refresh_tokens.created_at, revoked
          FROM Refresh_tokens JOIN Users ON Refresh_tokens.user_id = Users.id WHERE email = %s"""
        params = (email,)
        curs.execute(query, params)
        return curs.fetchone()
    
def create_refresh_token(email: str, hashed_token: str, expires_at: str, created_at: str, revoked: bool):
    with get_connection() as conn, conn.cursor() as curs:
        user = get_user(email)
        query = """INSERT INTO Refresh_tokens (user_id, hashed_token, expires_at, created_at, revoked)
        VALUES (%s, %s, %s, %s, %s)"""
        params = (user[0], hashed_token, expires_at, created_at, revoked)
        curs.execute(query, params)
    return get_refresh_token(email)

def modify_refresh_token(email: str, revoked_res: bool):
    with get_connection() as conn, conn.cursor() as curs:
        user = get_user(email)
        query = """UPDATE Refresh_tokens SET revoked = %s WHERE user_id = %s"""
        params = (revoked_res, user[0])
        curs.execute(query, params)
    return get_refresh_token(email)

def delete_refresh_token(email: str):
    with get_connection() as conn, conn.cursor() as curs:
        user = get_user(email)
        query = """DELETE FROM Refresh_tokens WHERE user_id = %s"""
        params = (user[0],)
        res = curs.execute(query, params)
    return bool(res)
