# ทดสอบ API ในเบราว์เซอร์

รัน `cd Lab6-mini_project && python app.py` แล้วเปิด:

| URL | ผลที่ได้ |
|-----|---------|
| http://127.0.0.1:5000/ | หน้า Dashboard |
| http://127.0.0.1:5000/api/summary | KPI JSON |
| http://127.0.0.1:5000/api/by-province | Top 10 จังหวัด |
| http://127.0.0.1:5000/api/monthly | รายเดือน |
| http://127.0.0.1:5000/api/vehicle-type | ยานพาหนะ |
| http://127.0.0.1:5000/api/severity | ความรุนแรง |
| http://127.0.0.1:5000/api/recent | 20 รายการล่าสุด |
| http://127.0.0.1:5000/api/search?province=เชียงใหม่ | ค้นหา |

หรือรัน: `python Lab6-2_flask/test_api.py`
