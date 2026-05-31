# API 範例與回傳格式

此檔列出目前後端實作的 Habit 與 Check-in 相關路由與範例請求/回傳。可作為前端介面對接參考。

## Endpoints

- GET /habits
- POST /habits
- GET /habits/{habit_id}
- PATCH /habits/{habit_id}
- DELETE /habits/{habit_id}
- POST /habits/{habit_id}/checkins
- GET /habits/{habit_id}/checkins
- GET /calendar/overview?month=YYYY-MM
- GET /stats/overview
- GET /profile/me

---

## Habit 建立（POST /habits）
Request:

```json
{
  "name": "跑步",
  "description": "每天早上跑步30分鐘",
  "frequency_type": "daily",
  "reminder_time": "06:00",
  "minimum_action": "跑步3公里",
  "identity_label": "跑者"
}
```

Response (示例):

```json
{
  "id": 1,
  "name": "跑步",
  "description": "每天早上跑步30分鐘",
  "frequency_type": "daily",
  "reminder_time": "06:00",
  "minimum_action": "跑步3公里",
  "identity_label": "跑者",
  "is_checked_in": false,
  "is_active": true,
  "created_at": "2026-05-27T08:00:00Z",
  "updated_at": "2026-05-27T08:00:00Z"
}
```

---

## 新增打卡（POST /habits/{habit_id}/checkins）
Request:

```json
{
  "date": "2026-05-27",
  "status": "completed",
  "note": "今天完成得很好"
}
```

Response (示例):

```json
{
  "id": 1,
  "habit_id": 1,
  "date": "2026-05-27",
  "status": "completed",
  "note": "今天完成得很好",
  "created_at": "2026-05-27T06:30:00Z"
}
```

---

## 日常頁回傳（GET /habits，可在前端計算或後端提供附加欄位）
建議回傳每個 habit 加入計算欄位：`today_status`, `current_streak`, `best_streak`, `is_synced`。

示例 item:

```json
{
  "id": 1,
  "name": "跑步",
  "description": "每天早上跑步30分鐘",
  "frequency_type": "daily",
  "reminder_time": "06:00",
  "minimum_action": "跑步3公里",
  "identity_label": "跑者",
  "is_checked_in": true,
  "today_status": "completed",
  "current_streak": 15,
  "best_streak": 21,
  "is_synced": true
}
```

---

## 月曆頁（GET /calendar/overview?month=YYYY-MM）
Response (示例):

```json
{
  "month": "2026-05",
  "summary": {
    "completed_days": 18,
    "total_days": 31,
    "completion_rate": 0.58
  },
  "days": [
    {"date": "2026-05-01", "completion_count": 2, "intensity": 2},
    {"date": "2026-05-02", "completion_count": 4, "intensity": 4}
  ]
}
```

---

## 統計頁（GET /stats/overview）
Response (示例):

```json
{
  "completion_rate": 0.67,
  "today_completed": 4,
  "today_total": 6,
  "average_streak": 8.4,
  "max_streak": 15,
  "trend_7_days": [
    { "date": "2026-05-21", "count": 3 },
    { "date": "2026-05-22", "count": 2 }
  ],
  "streak_distribution": { "long_term": 2, "building": 3, "new": 1 },
  "top_habits": [ { "habit_id": 1, "name": "跑步", "current_streak": 15 } ]
}
```

---

## 個人資料（GET /profile/me）
Response (示例):

```json
{
  "user": {
    "id": "user_001",
    "display_name": "習慣實踐者",
    "email": "habit.user@example.com",
    "avatar_url": null
  },
  "summary": {
    "completion_rate": 0.67,
    "total_streak": 31,
    "best_habit": { "habit_id": 1, "name": "跑步", "current_streak": 15 }
  },
  "settings": {
    "notifications_enabled": true,
    "theme": "dark",
    "timezone": "Asia/Taipei"
  }
}
```

---

> 註: 目前後端已完成資料模型、repository 與基本 service/路由綁定（CRUD 與 checkin）。月曆、統計與個人檔案的聚合仍為未實作（service stub）。可依此文件與前端進一步協調需要哪些聚合在後端計算。
