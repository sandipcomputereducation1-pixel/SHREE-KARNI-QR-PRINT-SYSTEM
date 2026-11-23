# Shree Karni QR Print System v2

## शामिल सुविधाएँ
- Customer photo/PDF upload और order ID
- Browser photo preview, rotate और zoom
- 4×6 inch sheet पर 8 passport-size (25×35 mm) फोटो
- PDF preview, page range, rotation और crop margin
- Admin login, orders, print status और payment status
- QR code: `/qr.png`

## Local run
```bash
pip install -r requirements.txt
python app.py
```
फिर `http://127.0.0.1:5000` खोलें।

## Render Environment Variables
- `ADMIN_USER`
- `ADMIN_PASSWORD` (मजबूत नया पासवर्ड)
- `SECRET_KEY` (लंबी random secret string)
- `UPI_ID` (वैकल्पिक)
- `DATA_DIR` (Persistent Disk mount path, जैसे `/var/data`)

## महत्वपूर्ण Storage नोट
Render Free Web Service का local filesystem persistent storage नहीं है। Orders और uploaded files को deploy/restart के बाद सुरक्षित रखने के लिए Persistent Disk या external database/object storage जोड़ें। `DATA_DIR=/var/data` तभी रखें जब Render में उस path पर Persistent Disk attach हो; अन्यथा इसे हटाएँ और समझें कि data ephemeral होगा।

## Editor सीमाएँ
Photo editor में rotate/zoom और 8-photo sheet उपलब्ध हैं। PDF में browser preview, page range, rotation और percentage crop उपलब्ध हैं। यह अभी professional freehand crop editor, payment gateway verification या direct printer driver integration नहीं है। Admin downloaded file को दुकान के Windows PC से print कर सकता है।
