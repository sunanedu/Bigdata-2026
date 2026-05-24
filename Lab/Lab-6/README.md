# Lab 6 — Mini Project: Dashboard ข้อมูลด้วย HTML

อ้างอิง `หน่วยที่6_Mini_Project_Dashboard_HTML.md`

## โครงสร้าง

| โฟลเดอร์ | เนื้อหา |
|----------|---------|
| `Lab6-1_architecture/` | Wireframe, สถาปัตยกรรม 3 ชั้น |
| `Lab6-2_flask/` | Hello Flask, ทดสอบ API |
| `Lab6-mini_project/` | **โปรเจกต์หลัก** — app.py, Dashboard, Chart.js |
| `Lab6-5_presentation/` | แนวทางนำเสนอ + checklist |
| `output/` | `school_data.db` (ไม่ commit) |

## เริ่มต้น

```bash
cd Lab/Lab-6
python setup_lab.py
pip install flask
cd Lab6-mini_project
python app.py
```

เปิด http://127.0.0.1:5000

## สถาปัตยกรรม

```
school_data.db  →  app.py (Flask API)  →  index.html + Chart.js
```

## API หลัก

- `/api/summary` — KPI
- `/api/by-province`, `/api/monthly`, `/api/vehicle-type`, `/api/severity`
- `/api/recent`, `/api/search`, `/api/by-region`

## หมายเหตุ

- คอลัมน์จริงใน CSV: `ประเภทยานพาหนะหลัก`, `จำนวนผู้บาดเจ็บ` (API ใช้ alias ตามเอกสาร)
- ต้องมี `road_accidents.db` จาก Lab 1–2 หรือ CSV ใน `data/`
- `hello_flask.py` ใช้ port **5001** เพื่อไม่ชนกับ Dashboard (5000)

ดู `Howto.txt` สำหรับลำดับ workshop
