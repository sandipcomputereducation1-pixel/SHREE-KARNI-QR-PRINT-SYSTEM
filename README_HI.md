# Shree Karni QR Print System – Starter Version

## इस पैकेज में
- Customer Upload: JPG, PNG, WEBP और PDF
- फोटो का बेसिक Preview
- Print Size: A4, 4×6 Inch, ID Card, PVC 98×54 mm
- Order ID और Order Status
- Admin Login और Orders Dashboard
- Pending / Printing / Completed
- QR Code `/qr.png`
- UPI ID display (manual verification; automatic payment gateway नहीं)

## जरूरी बातें
यह पहला working foundation है। इसमें अभी advanced Photo Editor (crop/resize/rotate/background removal), PDF page editor (page select/rotate/crop), payment gateway verification और Windows Print Agent शामिल नहीं हैं। उन्हें अगले चरण में जोड़ना है। Printing फिलहाल Admin के browser से file खोलकर Windows/Canon printer में manual Print के लिए है।

## Local Windows 11 पर चलाएँ
1. Python 3.11 install करें।
2. इस folder में Command Prompt खोलें।
3. चलाएँ:
   `py -m venv venv`
   `venv\\Scripts\\activate`
   `pip install -r requirements.txt`
   `set ADMIN_PASSWORD=अपना-मजबूत-पासवर्ड`
   `python app.py`
4. Browser में `http://127.0.0.1:5000/upload` खोलें।
5. Admin: `http://127.0.0.1:5000/admin`

Default local login username `admin` है। Production में `ADMIN_PASSWORD` और `SECRET_KEY` Render Environment में जरूर सेट करें।

## Render Deploy
- Runtime: Python
- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn app:app`
- Environment Variables:
  - `ADMIN_USER` = admin
  - `ADMIN_PASSWORD` = मजबूत नया पासवर्ड
  - `SECRET_KEY` = लंबी random secret
  - `UPI_ID` = 7891411425@ptyes

**महत्वपूर्ण:** Render Free instance की local disk स्थायी नहीं होती। इस starter में SQLite और uploads local disk पर हैं; production customer orders/files सुरक्षित रखने के लिए Persistent Disk या managed PostgreSQL + object storage जोड़ना जरूरी है। सार्वजनिक उपयोग से पहले यह काम करें।
