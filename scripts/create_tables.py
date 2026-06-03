from infrastructure.db.database import Base, engine
from infrastructure.db.models.user_model import UserModel
from infrastructure.db.models.habit_model import HabitModel
from infrastructure.db.models.habit_checkin_model import HabitCheckinModel
from infrastructure.db.models.daily_habit_list_model import DailyHabitListModel

if __name__ == '__main__':
    print('Creating database tables...')
    Base.metadata.create_all(bind=engine)
    print('Done.')
