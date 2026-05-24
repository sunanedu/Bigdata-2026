# Mini Project — Dashboard อุบัติเหตุทางถนน ปี 2568

## โครงสร้าง

```
Lab6-mini_project/
├── app.py              ← Flask Backend
├── school_data.db      ← SQLite (สร้างจาก setup_lab.py)
├── static/
│   ├── style.css
│   └── chart.min.js
└── templates/
    └── index.html
```

## รัน

```bash
pip install flask
python app.py
```

เปิด http://127.0.0.1:5000

## API

| URL | คำอธิบาย |
|-----|----------|
| `/api/summary` | KPI รวม |
| `/api/by-province` | Top 10 จังหวัด |
| `/api/monthly` | รายเดือน |
| `/api/vehicle-type` | สัดส่วนยานพาหนะ |
| `/api/severity` | สัดส่วนความรุนแรง (Doughnut) |
| `/api/recent` | รายการล่าสุด 20 |
| `/api/search?province=...` | ค้นหาจังหวัด |
| `/api/by-region?region=...` | กรองภูมิภาค |

## ความปลอดภัย

- ทุก query ใช้ `?` (Parameterized)
- ไม่แสดงข้อมูลระบุตัวบุคคล (อายุ, เพศ, พิกัด) ในตาราง Dashboard
