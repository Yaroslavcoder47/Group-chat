from sqlalchemy import Column, Text, Integer, String, DateTime, Boolean, ForeignKey, create_engine
from app.config import settings
from sqlalchemy.orm import DeclarativeBase, Session, relationship
from contextlib import contextmanager


class DatabaseORM:
    def __init__(self):
        self.engine = create_engine(settings.conn_str)

    class Base(DeclarativeBase):
        pass

    @contextmanager
    def get_db(self):
        db = Session(bind=self.engine)
        try:
            yield db
        finally:
            db.close()

    class User(Base):
        __tablename__ = "users"
        id = Column(Integer, primary_key=True)
        email = Column(String)
        username = Column(String)
        created_at = Column(DateTime)

        tokens = relationship("Refresh_token", back_populates='user', cascade="all, delete-orphan")

        def __repr__(self):
            return f"User(id={self.id}, email='{self.email}', username='{self.username}', created_at='{self.created_at}')"

    class Email_code(Base):
        __tablename__ = "email_codes"
        id = Column(Integer, primary_key=True)
        email = Column(String)
        hashed_code = Column(Text)
        verified = Column(Boolean)
        created_at = Column(DateTime)

        def __repr__(self):
            return f"EmailCode(id={self.id}, email='{self.email}', verified={self.verified})"

    class Refresh_token(Base):
        __tablename__ = "refresh_tokens"
        id = Column(Integer, primary_key=True)
        user_id = Column(Integer, ForeignKey("users.id"))
        hashed_token = Column(Text)
        expires_at = Column(DateTime)
        created_at = Column(DateTime)
        revoked = Column(Boolean)

        user = relationship('User', back_populates='tokens')

        def __repr__(self):
            return f"Refresh_token(id={self.id}, user_id={self.user_id}, revoked={self.revoked})"

    #USERS
    def get_user(self, email: str):
        with self.get_db() as db:
            req = db.query(self.User).filter(self.User.email == email).first()
            return req
        
    def create_user(self, email: str, username: str, created_at: str):
        with self.get_db() as db:
            new_user = self.User(email=email, username=username, created_at=created_at)
            db.add(new_user)
            db.commit()
        return self.get_user(email)
    
    def modify_user(self, email: str, username: str):
        with self.get_db() as db:
            req = db.query(self.User).filter(self.User.email == email).first()
            req.username = username
            db.commit()
        return self.get_user(email)
    
    def delete_user(self, email: str):
        with self.get_db() as db:
            del_user = db.query(self.User).filter(self.User.email == email).first()
            db.delete(del_user)
            db.commit()
        return bool(self.get_user(email))
    
    #EMAIL_CODES
    def get_email_code(self, email: str):
        with self.get_db() as db:
            req = db.query(self.Email_code).filter(self.Email_code.email == email).first()
            return req
        
    def create_email_code(self, email: str, hashed_code: str, verified: bool, created_at: str):
        with self.get_db() as db:
            new_code = self.Email_code(email=email, hashed_code=hashed_code, verified=verified, created_at=created_at)
            db.add(new_code)
            db.commit()
        return self.get_email_code(email)


    def modify_email_code(self, email: str, verified_res: bool):
        with self.get_db() as db:
            code = db.query(self.Email_code).filter(self.Email_code.email == email).first()
            code.verified = verified_res
            db.commit()
        return self.get_email_code(email)

    def delete_email_code(self, email: str):
        with self.get_db() as db:
            del_code = db.query(self.Email_code).filter(self.Email_code.email == email).first()
            db.delete(del_code)
            db.commit()
        return bool(self.get_email_code(email)) 
    

    #REFRESH_TOKEN
    def get_refresh_token(self, email: str):
        with self.get_db() as db:
            req = db.query(self.Refresh_token).join(self.User).filter(self.User.email == email).first()
            return req
        
    def create_refresh_token(self, email: str, hashed_token: str, expires_at: str, created_at: str, revoked: bool):
        with self.get_db() as db:
            user = self.get_user(email)
            new_token = self.Refresh_token(user_id=user.id, hashed_token=hashed_token, expires_at=expires_at, created_at=created_at, revoked=revoked)
            db.add(new_token)
            db.commit()
        return self.get_refresh_token(email)

    def modify_refresh_token(self, email: str, revoked_res: bool):
        with self.get_db() as db:
            token = db.query(self.Refresh_token).join(self.User).filter(self.User.email == email).first()
            token.revoked = revoked_res
            db.commit()
        return self.get_refresh_token(email)

    def delete_refresh_token(self, email: str):
        with self.get_db() as db:
            del_token = db.query(self.Refresh_token).join(self.User).filter(self.User.email == email).first()
            db.delete(del_token)
            db.commit()
        return bool(self.get_refresh_token(email))
