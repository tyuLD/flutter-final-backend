import os
import sys

# Ensure project root is on sys.path so imports work when running script directly
ROOT = os.path.dirname(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from infrastructure.db.database import Base, engine, SessionLocal
from infrastructure.db.models.user_model import UserModel
from infrastructure.db.models.habit_model import HabitModel
from core.security import hash_password


def main():
    print('Ensuring tables exist...')
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        username = "test_user"
        password = "TestPass123!"
        user = db.query(UserModel).filter(UserModel.username == username).first()
        if user:
            print('Test user already exists:', user.username, 'id=', user.id)
            user_id = user.id
        else:
            hashed = hash_password(password)
            user = UserModel(username=username, email=f"{username}@example.com", hashed_password=hashed, is_active=True)
            db.add(user)
            db.commit()
            db.refresh(user)
            user_id = user.id
            print('Created user:', username)

        existing = db.query(HabitModel).filter(HabitModel.user_id == user_id).all()
        if existing:
            print('Habits already exist for user', user_id)
        else:
            samples = [
                {
                    "name": "跑步",
                    "description": "每天早上跑步30分鐘",
                    "frequency_type": "daily",
                    "reminder_time": "06:00",
                    "minimum_action": "跑步3公里",
                    "identity_label": "跑者",
                    "is_active": True,
                },
                {
                    "name": "閱讀",
                    "description": "每天閱讀一章節",
                    "frequency_type": "daily",
                    "reminder_time": "21:00",
                    "minimum_action": "閱讀1章",
                    "identity_label": "讀者",
                    "is_active": True,
                },
                {
                    "name": "冥想",
                    "description": "每週三次冥想",
                    "frequency_type": "weekly",
                    "reminder_time": "07:00",
                    "minimum_action": "10分鐘",
                    "identity_label": "冥想者",
                    "is_active": True,
                },
            ]
            for s in samples:
                habit = HabitModel(user_id=user_id, **s)
                db.add(habit)
            db.commit()
            print('Inserted sample habits for user', user_id)

        print('\nCREDENTIALS')
        print('username:', username)
        print('password:', password)
        print('user_id:', user_id)
    finally:
        db.close()


if __name__ == '__main__':
    main()
