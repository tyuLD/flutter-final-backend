from sqlalchemy import inspect, text
from sqlalchemy.exc import SQLAlchemyError

from infrastructure.db.database import engine

TABLE_NAME = "daily_task_records"
COLUMN_NAME = "user_id"
FK_NAME = "fk_daily_task_records_user"
UNIQUE_NAME = "uq_user_day_record"
INDEX_NAME = "ix_daily_task_records_user_id"
USERS_TABLE = "users"
DEFAULT_USER_ID = 1


def column_exists(inspector, table_name: str, column_name: str) -> bool:
    return any(col["name"] == column_name for col in inspector.get_columns(table_name))


def fk_exists(inspector, table_name: str, fk_name: str) -> bool:
    return any(fk.get("name") == fk_name for fk in inspector.get_foreign_keys(table_name))


def unique_exists(inspector, table_name: str, unique_name: str) -> bool:
    return any(uq.get("name") == unique_name for uq in inspector.get_unique_constraints(table_name))


def index_exists(inspector, table_name: str, index_name: str) -> bool:
    return any(idx.get("name") == index_name for idx in inspector.get_indexes(table_name))


def main():
    inspector = inspect(engine)
    tables = inspector.get_table_names()

    if TABLE_NAME not in tables:
        print(f"[ERROR] 找不到資料表: {TABLE_NAME}")
        return

    if USERS_TABLE not in tables:
        print(f"[ERROR] 找不到使用者資料表: {USERS_TABLE}")
        return

    with engine.begin() as conn:
        inspector = inspect(conn)

        if not column_exists(inspector, TABLE_NAME, COLUMN_NAME):
            print(f"[INFO] 新增欄位 {COLUMN_NAME} 到 {TABLE_NAME}...")
            conn.execute(text(
                f"ALTER TABLE {TABLE_NAME} ADD COLUMN {COLUMN_NAME} INTEGER"
            ))
        else:
            print(f"[INFO] 欄位 {COLUMN_NAME} 已存在，略過新增。")

        print(f"[INFO] 將既有資料的 {COLUMN_NAME} 設為 {DEFAULT_USER_ID}...")
        conn.execute(text(
            f"UPDATE {TABLE_NAME} SET {COLUMN_NAME} = :default_user_id WHERE {COLUMN_NAME} IS NULL"
        ), {"default_user_id": DEFAULT_USER_ID})

        print(f"[INFO] 將 {COLUMN_NAME} 設為 NOT NULL...")
        conn.execute(text(
            f"ALTER TABLE {TABLE_NAME} ALTER COLUMN {COLUMN_NAME} SET NOT NULL"
        ))

        inspector = inspect(conn)
        if not fk_exists(inspector, TABLE_NAME, FK_NAME):
            print(f"[INFO] 新增 foreign key {FK_NAME}...")
            conn.execute(text(
                f"ALTER TABLE {TABLE_NAME} "
                f"ADD CONSTRAINT {FK_NAME} FOREIGN KEY ({COLUMN_NAME}) REFERENCES {USERS_TABLE}(id)"
            ))
        else:
            print(f"[INFO] foreign key {FK_NAME} 已存在，略過新增。")

        inspector = inspect(conn)
        if not unique_exists(inspector, TABLE_NAME, UNIQUE_NAME):
            print(f"[INFO] 新增 unique constraint {UNIQUE_NAME} on (user_id, day)...")
            conn.execute(text(
                f"ALTER TABLE {TABLE_NAME} "
                f"ADD CONSTRAINT {UNIQUE_NAME} UNIQUE ({COLUMN_NAME}, day)"
            ))
        else:
            print(f"[INFO] unique constraint {UNIQUE_NAME} 已存在，略過新增。")

        inspector = inspect(conn)
        if not index_exists(inspector, TABLE_NAME, INDEX_NAME):
            print(f"[INFO] 新增 index {INDEX_NAME}...")
            conn.execute(text(
                f"CREATE INDEX {INDEX_NAME} ON {TABLE_NAME} ({COLUMN_NAME})"
            ))
        else:
            print(f"[INFO] index {INDEX_NAME} 已存在，略過新增。")

    print("[DONE] migration 完成。")


if __name__ == "__main__":
    try:
        main()
    except SQLAlchemyError as e:
        print(f"[ERROR] migration 失敗: {e}")
        raise