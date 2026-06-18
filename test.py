from sqlalchemy import create_engine, text
import os

DATABASE_URL = 'postgresql://atomicflow_db_user:FnuurgtrswAmz3H9NQ5MhcLG89gmXZJk@dpg-d8d8587avr4c73ff1pb0-a.oregon-postgres.render.com/atomicflow_db'

def main():
    engine = create_engine(DATABASE_URL)

    with engine.begin() as conn:
        print("開始檢查 daily_task_records 的 constraint / index...")

        constraints = conn.execute(text("""
            SELECT conname, pg_get_constraintdef(c.oid) AS definition
            FROM pg_constraint c
            JOIN pg_class t ON c.conrelid = t.oid
            JOIN pg_namespace n ON n.oid = t.relnamespace
            WHERE t.relname = 'daily_task_records'
              AND c.contype = 'u';
        """)).fetchall()

        indexes = conn.execute(text("""
            SELECT indexname, indexdef
            FROM pg_indexes
            WHERE tablename = 'daily_task_records';
        """)).fetchall()

        print("\\n目前 unique constraints:")
        for row in constraints:
            print(f"- {row.conname}: {row.definition}")

        print("\\n目前 indexes:")
        for row in indexes:
            print(f"- {row.indexname}: {row.indexdef}")

        for row in constraints:
            name = row.conname
            definition = row.definition.lower()
            if "unique (day)" in definition:
                print(f"\\n刪除單欄位 day unique constraint: {name}")
                conn.execute(text(f'ALTER TABLE daily_task_records DROP CONSTRAINT "{name}"'))

        for row in indexes:
            name = row.indexname
            definition = row.indexdef.lower()
            if "unique index" in definition and "(day)" in definition and "user_id" not in definition:
                print(f"\\n刪除單欄位 day unique index: {name}")
                conn.execute(text(f'DROP INDEX IF EXISTS "{name}"'))

        exists = conn.execute(text("""
            SELECT 1
            FROM pg_constraint c
            JOIN pg_class t ON c.conrelid = t.oid
            WHERE t.relname = 'daily_task_records'
              AND c.conname = 'uq_user_day_record';
        """)).fetchone()

        if not exists:
            print("\\n建立複合唯一鍵 uq_user_day_record (user_id, day)")
            conn.execute(text("""
                ALTER TABLE daily_task_records
                ADD CONSTRAINT uq_user_day_record UNIQUE (user_id, day);
            """))
        else:
            print("\\nuq_user_day_record 已存在，略過建立")

        print("\\n更新完成。")

if __name__ == "__main__":
    main()