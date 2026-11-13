import hashlib

from user_repository import user_repository

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"


def seed_admin():
    if user_repository.get_by_username(ADMIN_USERNAME) is not None:
        print(f"User '{ADMIN_USERNAME}' already exists, nothing to do")
        return

    hashed_password = hashlib.md5(ADMIN_PASSWORD.encode()).hexdigest()
    user_repository.create(ADMIN_USERNAME, hashed_password, role="admin")
    print(f"Admin user created -> username: {ADMIN_USERNAME}, password: {ADMIN_PASSWORD}")


if __name__ == "__main__":
    seed_admin()
