from app.database import SessionLocal
from app.auth.hashing import hash_password
from app.enums.roles import UserRole
from app.models.user import User

db = SessionLocal()

try:
    # Check if an admin already exists
    existing_admin = (
        db.query(User)
        .filter(
            User.role == UserRole.ADMIN,
            User.is_deleted == False,
        )
        .first()
    )

    if existing_admin:
        print("=" * 50)
        print("Admin already exists.")
        print(f"Email : {existing_admin.email}")
        print("=" * 50)
        exit()

    admin = User(
        name="Admin",
        email="admin@annasetu.com",
        phone="9999999999",
        password_hash=hash_password("Admin@123"),
        role=UserRole.ADMIN,
        is_active=True,
        is_deleted=False,
    )

    db.add(admin)
    db.commit()
    db.refresh(admin)

    print("=" * 50)
    print("Admin created successfully!")
    print(f"ID       : {admin.id}")
    print(f"Email    : {admin.email}")
    print("Password : Admin@123")
    print("=" * 50)

except Exception:
    db.rollback()
    raise

finally:
    db.close()