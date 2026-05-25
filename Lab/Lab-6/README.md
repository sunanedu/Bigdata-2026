# Lab 6 — Mini Project: Dashboard ข้อมูลด้วย HTML

อ้างอิง `หน่วยที่6_Mini_Project_Dashboard_HTML.md` (อัปเดตตาม Lab ล่าสุด — Modern Dashboard)

## เริ่มต้น (Windows PowerShell)

```powershell
cd Lab\Lab-6
$env:PYTHONIOENCODING='utf-8'
python setup_lab.py
pip install -r requirements.txt
cd Lab6-mini_project
python app.py
```

เปิด **URL ที่ Terminal แสดง** — บน Windows มักเป็น `http://127.0.0.1:5050` (พอร์ต 5000 ถูกระบบจอง)

## โครงสร้าง

| โฟลเดอร์ | เนื้อหา |
|----------|---------|
| `Lab6-1_architecture/` | Wireframe, สถาปัตยกรรม 3 ชั้น |
| `Lab6-2_flask/` | Hello Flask (port 5001), ทดสอบ API |
| `Lab6-mini_project/` | **โปรเจกต์หลัก** — Flask + Chart.js |
| `Lab6-5_presentation/` | นำเสนอ + checklist |
| `TROUBLESHOOTING.md` | แก้ปัญหาจากการทดลองจริง |

## สิ่งที่แก้จากการทดสอบจริง

| ปัญหา | การแก้ใน Lab |
|--------|----------------|
| พอร์ต 5000 ใช้ไม่ได้ (Windows `iphlpsvc`) | `app.py` ตรวจพอร์ต → fallback **5050** |
| ชื่อคอลัมน์ SQL ผิด | ใช้ `ประเภทยานพาหนะหลัก`, `จำนวนผู้บาดเจ็บ` + alias |
| กราฟ Doughnut/Line สูงเต็มหน้า | จัดคู่ใน `charts-row` + `.chart-canvas-wrap` |
| `setup_lab.py` encoding error | `PYTHONIOENCODING=utf-8` / reconfigure stdout |

## API

- `/api/summary`, `/api/by-province`, `/api/monthly`
- `/api/vehicle-type`, `/api/severity`, `/api/recent`
- `/api/search`, `/api/by-region`

## ฐานข้อมูล

`school_data.db`: `road_accidents` (20,000 แถว) + `students` / `subjects` / `enrollments`

ดู `Howto.txt` และ `TROUBLESHOOTING.md`
