# ทดสอบ API

รัน Dashboard ก่อน:

```powershell
cd Lab\Lab-6\Lab6-mini_project
python app.py
```

ดูพอร์ตใน Terminal (มัก **5050** บน Windows) แล้วเปิด:

| URL | ผลที่ได้ |
|-----|---------|
| http://127.0.0.1:5050/ | หน้า Dashboard |
| http://127.0.0.1:5050/api/summary | KPI JSON |
| http://127.0.0.1:5050/api/by-province | Top 10 จังหวัด |
| http://127.0.0.1:5050/api/monthly | รายเดือน |
| http://127.0.0.1:5050/api/vehicle-type | ยานพาหนะ |
| http://127.0.0.1:5050/api/severity | ความรุนแรง |
| http://127.0.0.1:5050/api/recent | 20 รายการล่าสุด |
| http://127.0.0.1:5050/api/search?province=เชียงใหม่ | ค้นหา |

หรือ: `python Lab6-2_flask\test_api.py` (ใช้ Flask test client — ไม่ต้องเปิดเบราว์เซอร์)
