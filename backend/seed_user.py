from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
from passlib.context import CryptContext

# Setup the same password hashing as your main.py
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def seed_admin():
    db = SessionLocal()
    try:
        email = "demo@meda.test"
        exists = db.query(models.User).filter(models.User.email == email).first()

        if not exists:
            hashed = pwd_context.hash("Password123")

            new_user = models.User(
                username="admin",        # Now this will work
                email=email,
                hashed_password=hashed,
                full_name="Mark Espedido",
                role="Admin"
            )

            db.add(new_user)
            db.commit()
            print(f"✅ Success! User {email} created.")
        else:
            print(f"ℹ️ User {email} already exists.")
    except Exception as e:
        print(f"❌ Error seeding user: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_admin()
