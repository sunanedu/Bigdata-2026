# Lab 5 — ข้อมูลไม่มีโครงสร้างและ NoSQL

อ้างอิง `หน่วยที่5_ข้อมูลไม่มีโครงสร้างและ_NoSQL.md`

## โครงสร้าง

| โฟลเดอร์ | เนื้อหา |
|----------|---------|
| `Lab5-1_data_types_worksheet.md` | ประเภทข้อมูล Structured / Semi / Unstructured |
| `Lab5-2_json/` | JSON → Pandas → SQLite `accidents_api` |
| `Lab5-3_mongodb/` | CRUD products, นำเข้า accidents (MongoDB หรือออฟไลน์) |
| `Lab5-4_pipeline/` | CSV → Pandas → `dashboard_data.json` |
| `data/` | `sample_api_data.json`, `sample_nested_accidents.json` |
| `output/` | DB, JSON ผลลัพธ์ (ไม่ commit) |

## เริ่มต้น

```bash
cd Lab/Lab-5
python setup_lab.py
pip install pandas pymongo
```

ดู `Howto.txt` สำหรับลำดับ workshop

## หมายเหตุ

- **MongoDB**: ถ้าไม่ติดตั้ง สคริปต์ใช้ `output/mongo_collections/*.json` แทน
- ข้อมูล API 50 รายการสร้างจาก `data/thailand_road_accidents_2568_fix.csv`
- Pipeline 5.4 ใช้ CSV จริง ~20,000 แถว
