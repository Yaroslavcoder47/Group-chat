from sqlalchemy import MetaData, Table, Column, Text, Integer, String, DateTime, Boolean, ForeignKey, create_engine, select, desc
from app.config import settings
from app.schemas.models import User, Email_code, Refresh_token

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
    
    def model_to_row_user(self, user: User) -> tuple:
        return user.tuple()
    
    def row_to_model_user(self, row: tuple) -> User:
        id, email, username, created_at = row
        return User(id=id, email=email, username=username, created_at=created_at)
    
    def model_to_row_emailcode(self, email_code: Email_code) -> tuple:
        return email_code.tuple()
    
    def row_to_model_emailcode(self, row: tuple) -> Email_code:
        id, email, hashed_code, verified, created_at = row
        return Email_code(email=email, hashed_code=hashed_code, verified=verified, created_at=created_at)
    
    def model_to_row_refreshtoken(self, refresh_token: Refresh_token) -> tuple:
        return refresh_token.tuple()
    
    def row_to_model_refreshtoken(self, row: tuple) -> Refresh_token:
        id, email, hashed_token, expires_at, created_at, revoked = row
        return Refresh_token(email=email, hashed_token=hashed_token, expires_at=expires_at, created_at=created_at, revoked=revoked)

    #USERS
    def get_all_users(self):
        with self.get_connection() as conn:
            req = self.users.select()
            result = conn.execute(req)
            rows = list(result.fetchall())
            return [self.row_to_model_user(i) for i in rows] 

    def get_user(self, email: str):
        with self.get_connection() as conn:
            req = self.users.select().where(self.users.c.email == email)
            result = conn.execute(req)
            return self.row_to_model_user(result.fetchone()) 

    def create_user(self, user: User):
        email, username, created_at = self.model_to_row_user(user)
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
            res = conn.execute(req)
            conn.commit()
            return bool(res) 

    #EMAIL_CODES
    def get_all_email_code(self):
        with self.get_connection() as conn:
            req = self.email_codes.select()
            result = conn.execute(req)
            rows = result.fetchall()
            return [self.row_to_model_emailcode(i) for i in rows]

    def get_email_code(self, email: str):
        with self.get_connection() as conn:
            req = self.email_codes.select().where(self.email_codes.c.email == email).order_by(desc(self.email_codes.c.id))
            result = conn.execute(req)
            return self.row_to_model_emailcode(result.fetchone())
        
    def create_email_code(self, code: Email_code):
        email, hashed_code, verified, created_at = self.model_to_row_emailcode(code)
        with self.get_connection() as conn:
            req = self.email_codes.insert().values(email = email, hashed_code = hashed_code, verified = verified, created_at = created_at)
            conn.execute(req)
            conn.commit()
        return self.get_email_code(email)


    def modify_email_code(self, email: str, code_hash : str, verified_res: bool):
        with self.get_connection() as conn:
            req = self.email_codes.update().where(self.email_codes.c.email == email, self.email_codes.c.hashed_code == code_hash).values(verified = verified_res)
            conn.execute(req)
            conn.commit()
        return self.get_email_code(email)

    def delete_email_code(self, email: str):
        with self.get_connection() as conn:
            req = self.email_codes.delete().where(self.email_codes.c.email == email)
            res = conn.execute(req)
            conn.commit()
            return bool(res) 

    #REFRESH_TOKENS
    def get_all_refresh_token(self, email : str):
        with self.get_connection() as conn:
            req = select(
                self.refresh_tokens.c.id,
                self.users.c.email,
                self.refresh_tokens.c.hashed_token,
                self.refresh_tokens.c.expires_at,
                self.refresh_tokens.c.created_at,
                self.refresh_tokens.c.revoked
            ).select_from(
                self.refresh_tokens.join(self.users, self.refresh_tokens.c.user_id == self.users.c.id)
            ).where(self.users.c.email == email)
            
            result = conn.execute(req)
            rows = result.fetchall()
            return [self.row_to_model_refreshtoken(i) for i in rows]

    def get_refresh_token(self, email: str):
        with self.get_connection() as conn:
            user_subquery = select(self.users.c.id).where(self.users.c.email == email).scalar_subquery()
            
            req = select(
                self.refresh_tokens.c.id,
                self.users.c.email,
                self.refresh_tokens.c.hashed_token,
                self.refresh_tokens.c.expires_at,
                self.refresh_tokens.c.created_at,
                self.refresh_tokens.c.revoked
            ).select_from(
                self.refresh_tokens.join(self.users, self.refresh_tokens.c.user_id == self.users.c.id)
            ).where(self.refresh_tokens.c.user_id == user_subquery)
            
            result = conn.execute(req)
            row = result.fetchone()
            return self.row_to_model_refreshtoken(row)
            
        
    def create_refresh_token(self, token: Refresh_token):
        email, hashed_token, expires_at, created_at, revoked = self.model_to_row_refreshtoken(token)
        with self.get_connection() as conn:
            user_select = select(self.users.c.id).where(self.users.c.email == email)
            req = self.refresh_tokens.insert().values(user_id = user_select.scalar_subquery(), hashed_token = hashed_token, expires_at = expires_at, created_at = created_at, revoked = revoked)
            conn.execute(req)
            conn.commit()
        return self.get_refresh_token(email)

    def modify_refresh_token(self, email: str, revoked_res: bool):
        with self.get_connection() as conn:
            user_select = select(self.users.c.id).where(self.users.c.email == email)
            req = self.refresh_tokens.update().where(self.refresh_tokens.c.user_id == user_select.scalar_subquery()).values(revoked = revoked_res)
            conn.execute(req)
            conn.commit()
        return self.get_refresh_token(email)

    def delete_refresh_token(self, email: str):
        with self.get_connection() as conn:
            user_select = select(self.users.c.id).where(self.users.c.email == email)
            req = self.refresh_tokens.delete().where(self.refresh_tokens.c.user_id == user_select.scalar_subquery())
            res = conn.execute(req)
            conn.commit()
            return bool(res)
