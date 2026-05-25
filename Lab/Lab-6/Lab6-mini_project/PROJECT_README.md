# Mini Project — Dashboard อุบัติเหตุทางถนน ปี 2568

## รัน

```powershell
pip install flask
python app.py
```

เปิด **URL ที่ Terminal แสดง** (ค่าเริ่มต้นพยายามพอร์ต 5000 — ถ้า Windows จองไว้จะใช้ **5050**)

```powershell
# บังคับพอร์ต
$env:PORT=5050
python app.py
```

## ชื่อคอลัมน์ใน SQL

| ในฐานข้อมูล | ใน JSON (alias) |
|-------------|-----------------|
| `ประเภทยานพาหนะหลัก` | `ยานพาหนะ` / `ยานพาหนะหลัก` |
| `จำนวนผู้บาดเจ็บ` | `จำนวนผู้บาดเจ็บรวม` (ในตารางหน้าเว็บ) |

## UI (Modern Dashboard)

- Sidebar + Topbar สไตล์ [Modernize](https://modernize-react-main.netlify.app/dashboards/modern)
- ตัวกรอง 7 มิติ + ค้นหา + pagination (25–500 แถว)
- กราฟ 7 ชุด: จังหวัด, ภูมิภาค, รายเดือน, ความรุนแรง, ยานพาหนะ, ประเภทถนน, ช่วงเวลา
- KPI 6 ตัว รวมอัตราเสียชีวิตและจำนวนจังหวัด

## ปัญหา

ดู `../TROUBLESHOOTING.md`
