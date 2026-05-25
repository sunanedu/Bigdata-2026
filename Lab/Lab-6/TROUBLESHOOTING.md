# Lab 6 — ปัญหาที่พบจากการทดลองจริง

## พอร์ต 5000 ใช้ไม่ได้ (Windows)

**อาการ:** `An attempt was made to access a socket in a way forbidden...` หรือ Flask ไม่ขึ้น

**สาเหตุ:** บริการ `iphlpsvc` (IP Helper) มักจอง `127.0.0.1:5000`

**วิธีแก้ (แนะนำ):** ใช้พอร์ตที่ `app.py` แจ้งอัตโนมัติ (มักเป็น **5050**)

```powershell
cd Lab\Lab-6\Lab6-mini_project
python app.py
# เปิด URL ที่ Terminal แสดง เช่น http://127.0.0.1:5050
```

บังคับพอร์ต:

```powershell
$env:PORT=5050
python app.py
```

ถ้าต้องการ 5000 จริงๆ: เปิด PowerShell **แบบ Administrator** → `Stop-Service iphlpsvc` (อาจกระทบบริการอื่น)

---

## ชื่อคอลัมน์ SQL ผิด

| ผิด (เอกสารเก่า) | ถูก (ใน DB จริง) |
|-----------------|------------------|
| `ยานพาหนะหลัก` | `ประเภทยานพาหนะหลัก` |
| `จำนวนผู้บาดเจ็บรวม` | `จำนวนผู้บาดเจ็บ` |

ตรวจด้วย DB Browser: `PRAGMA table_info(road_accidents);`

---

## setup_lab.py ขึ้น UnicodeEncodeError

**สาเหตุ:** Terminal Windows ใช้ encoding cp1252

```powershell
$env:PYTHONIOENCODING='utf-8'
python setup_lab.py
```

---

## กราฟสูงเต็มหน้า

ใช้ layout ใน Lab แล้ว: `charts-row` คู่ Doughnut + Line และ `.chart-canvas-wrap` สูง ~280px

---

## กราฟไม่ขึ้น

1. มี `Lab6-mini_project/static/chart.min.js` (รัน `setup_lab.py` ต้องมีเน็ตครั้งแรก)
2. กด F12 → Console ดู error
3. รีเฟรช `Ctrl+F5`

---

## PowerShell

ใช้ `;` แทน `&&`:

```powershell
cd Lab\Lab-6; python setup_lab.py; pip install flask
```
