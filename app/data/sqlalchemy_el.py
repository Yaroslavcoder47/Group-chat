from sqlalchemy import MetaData, Table, Column, Text, Integer, String, DateTime, Boolean, ForeignKey, create_engine
from app.config import settings

class Database:
    def __init__(self):
        self.engine = create_engine(settings.conn_str)
        self.meta = MetaData()
        self._init_tables()

    def _init_tables(self):
        self.users = Table(
            'users', self.meta,
            Column('id', Integer, primary_key = True),
            Column('email', String),
            Column('username', String),
            Column('created_at', DateTime)
        )

        self.email_codes = Table(
            'email_codes', self.meta,
            Column('id', Integer, primary_key = True),
            Column('email', String),
            Column('hashed_code', Text),
            Column('verified', Boolean),
            Column('created_at', DateTime)
        )

        self.refresh_tokens = Table(
            'refresh_tokens', self.meta,
            Column('id', Integer, primary_key = True),
            Column('user_id', Integer, ForeignKey('users.id')),
            Column('hashed_token', Text),
            Column('expires_at', DateTime),
            Column('created_at', DateTime),
            Column('revoked', Boolean)
        )

        self.meta.create_all(self.engine)

    def get_connection(self):
        return self.engine.connect()

    #USERS
    def get_all_users(self):
        with self.get_connection() as conn:
            req = self.users.select()
            result = conn.execute(req)
            return result.fetchall()

    def get_user(self, email: str):
        with self.get_connection() as conn:
            req = self.users.select().where(self.users.c.email == email)
            result = conn.execute(req)
            return result.fetchone()

    def create_user(self, email: str, username: str, created_at: str): # заменить на Pydantic модель
        with self.get_connection() as conn:
            req = self.users.insert().values(email = email, username = username, created_at = created_at)
            conn.execute(req)
            conn.commit()
        return self.get_user(email)

    def modify_user(self, email: str, username: str):
        with self.get_connection() as conn:
            req = self.users.update().where(self.users.c.email == email).values(username = username)
            conn.execute(req)
            conn.commit()
        return self.get_user(email)

    def delete_user(self, email: str):
        with self.get_connection() as conn:
            req = self.users.delete().where(self.users.c.email == email)
            conn.execute(req)
            conn.commit()
        return bool(self.get_user(email)) 

    #EMAIL_CODES
    def get_all_email_code(self):
        with self.get_connection() as conn:
            req = self.email_codes.select()
            result = conn.execute(req)
            return result.fetchall()

    def get_email_code(self, email: str):
        with self.get_connection() as conn:
            req = self.email_codes.select().where(self.email_codes.c.email == email)
            result = conn.execute(req)
            return result.fetchone()
        
    def create_email_code(self, email: str, hashed_code: str, verified: bool, created_at: str):
        with self.get_connection() as conn:
            req = self.email_codes.insert().values(email = email, hashed_code = hashed_code, verified = verified, created_at = created_at)
            conn.execute(req)
            conn.commit()
        return self.get_email_code(email)


    def modify_email_code(self, email: str, verified_res: bool):
        with self.get_connection() as conn:
            req = self.email_codes.update().where(self.email_codes.c.email == email).values(verified = verified_res)
            conn.execute(req)
            conn.commit()
        return self.get_email_code(email)

    def delete_email_code(self, email: str):
        with self.get_connection() as conn:
            req = self.email_codes.delete().where(self.email_codes.c.email == email)
            conn.execute(req)
            conn.commit()
        return bool(self.get_email_code(email)) 

    #REFRESH_TOKENS
    def get_all_refresh_token(self):
        with self.get_connection() as conn:
            req = self.refresh_tokens.select()
            result = conn.execute(req)
            return result.fetchall()

    def get_refresh_token(self, email: str):
        with self.get_connection() as conn:
            user = self.get_user(email)
            req = self.refresh_tokens.select().where(self.refresh_tokens.c.user_id == user[0])
            result = conn.execute(req)
            return result.fetchone()
        
    def create_refresh_token(self, email: str, hashed_token: str, expires_at: str, created_at: str, revoked: bool):
        with self.get_connection() as conn:
            user = self.get_user(email)
            req = self.refresh_tokens.insert().values(user_id = user[0], hashed_token = hashed_token, expires_at = expires_at, created_at = created_at, revoked = revoked)
            conn.execute(req)
            conn.commit()
        return self.get_refresh_token(email)

    def modify_refresh_token(self, email: str, revoked_res: bool):
        with self.get_connection() as conn:
            user = self.get_user(email)
            req = self.refresh_tokens.update().where(self.refresh_tokens.c.user_id == user[0]).values(revoked = revoked_res)
            conn.execute(req)
            conn.commit()
        return self.get_refresh_token(email)

    def delete_refresh_token(self, email: str):
        with self.get_connection() as conn:
            user = self.get_user(email)
            req = self.refresh_tokens.delete().where(self.refresh_tokens.c.user_id == user[0])
            conn.execute(req)
            conn.commit()
        return bool(self.get_refresh_token(email))
