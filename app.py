import os, uuid, sqlite3, qrcode
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory, flash, jsonify
from werkzeug.utils import secure_filename

BASE = os.path.abspath(os.path.dirname(__file__))
DB = os.path.join(BASE, "orders.db")
UPLOAD_DIR = os.path.join(BASE, "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "change-this-secret-before-production")
app.config["MAX_CONTENT_LENGTH"] = 25 * 1024 * 1024
ADMIN_USER = os.environ.get("ADMIN_USER", "admin")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "ChangeMe123!")
UPI_ID = os.environ.get("UPI_ID", "7891411425@ptyes")
SHOP_NAME = "Shree Karni Computer Dalot"

ALLOWED = {".jpg", ".jpeg", ".png", ".webp", ".pdf"}

def db():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    return con

def init_db():
    with db() as con:
        con.execute("""CREATE TABLE IF NOT EXISTS orders (
            id TEXT PRIMARY KEY, customer_name TEXT, mobile TEXT, print_size TEXT,
            copies INTEGER, payment_mode TEXT, amount REAL, status TEXT,
            filename TEXT, original_name TEXT, created_at TEXT
        )""")
init_db()

def allowed_file(name):
    return os.path.splitext(name.lower())[1] in ALLOWED

@app.route("/")
def home():
    return redirect(url_for("upload_page"))

@app.route("/upload", methods=["GET", "POST"])
def upload_page():
    if request.method == "POST":
        f = request.files.get("file")
        if not f or not f.filename:
            flash("कृपया फोटो या PDF चुनें।")
            return redirect(url_for("upload_page"))
        if not allowed_file(f.filename):
            flash("केवल JPG, PNG, WEBP और PDF फाइल स्वीकार हैं।")
            return redirect(url_for("upload_page"))
        order_id = "SK" + datetime.now().strftime("%y%m%d") + uuid.uuid4().hex[:5].upper()
        original = secure_filename(f.filename)
        ext = os.path.splitext(original)[1].lower()
        stored = order_id + ext
        f.save(os.path.join(UPLOAD_DIR, stored))
        name = request.form.get("customer_name", "").strip()
        mobile = request.form.get("mobile", "").strip()
        size = request.form.get("print_size", "A4")
        copies = max(1, min(100, int(request.form.get("copies", 1) or 1)))
        payment = request.form.get("payment_mode", "Cash")
        amount = max(0, float(request.form.get("amount", 0) or 0))
        with db() as con:
            con.execute("""INSERT INTO orders VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
                (order_id, name, mobile, size, copies, payment, amount, "Pending", stored, original,
                 datetime.now().strftime("%d-%m-%Y %I:%M %p")))
        return redirect(url_for("order_page", order_id=order_id))
    return render_template("upload.html", upi_id=UPI_ID, shop_name=SHOP_NAME)

@app.route("/order/<order_id>")
def order_page(order_id):
    with db() as con:
        order = con.execute("SELECT * FROM orders WHERE id=?", (order_id,)).fetchone()
    if not order:
        return "Order not found", 404
    return render_template("order.html", order=order, upi_id=UPI_ID)

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        if request.form.get("username") == ADMIN_USER and request.form.get("password") == ADMIN_PASSWORD:
            session["admin"] = True
            return redirect(url_for("admin"))
        flash("गलत यूज़रनेम या पासवर्ड")
    return render_template("login.html")

@app.route("/admin/logout")
def admin_logout():
    session.clear()
    return redirect(url_for("admin_login"))

@app.route("/admin")
def admin():
    if not session.get("admin"):
        return redirect(url_for("admin_login"))
    with db() as con:
        orders = con.execute("SELECT * FROM orders ORDER BY rowid DESC").fetchall()
    return render_template("admin.html", orders=orders)

@app.route("/admin/status/<order_id>", methods=["POST"])
def update_status(order_id):
    if not session.get("admin"):
        return jsonify(ok=False), 401
    status = request.form.get("status")
    if status not in {"Pending", "Printing", "Completed"}:
        return jsonify(ok=False, error="Invalid status"), 400
    with db() as con:
        con.execute("UPDATE orders SET status=? WHERE id=?", (status, order_id))
    return redirect(url_for("admin"))

@app.route("/file/<filename>")
def get_file(filename):
    # Files are intentionally served only to the admin session.
    if not session.get("admin"):
        return "Unauthorized", 401
    return send_from_directory(UPLOAD_DIR, filename, as_attachment=False)

@app.route("/qr.png")
def qr_code():
    # QR points to the public upload page.
    base = request.url_root.rstrip("/")
    img = qrcode.make(base + url_for("upload_page"))
    from io import BytesIO
    from flask import send_file
    buf = BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return send_file(buf, mimetype="image/png")

@app.route("/health")
def health():
    return {"ok": True, "app": "Shree Karni QR Print System"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)
