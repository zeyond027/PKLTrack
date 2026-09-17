import os, sqlite3
from datetime import date, datetime
from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from werkzeug.utils import secure_filename
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm

app = Flask(__name__)
app.secret_key = "pkltrack-secret-key"
app.config["UPLOAD_FOLDER"] = os.path.join("static", "uploads")
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

def db():
    conn = sqlite3.connect("pkltrack.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = db()
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS activities (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        activity_date TEXT NOT NULL,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'Selesai',
        photo TEXT,
        created_at TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS competencies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        progress INTEGER NOT NULL DEFAULT 0
    );
    """)
    if conn.execute("SELECT COUNT(*) FROM competencies").fetchone()[0] == 0:
        conn.executemany(
            "INSERT INTO competencies(name, description, progress) VALUES (?, ?, ?)",
            [
                ("Monitoring jaringan", "Memantau koneksi dan aplikasi jaringan", 80),
                ("Konfigurasi perangkat", "Mempelajari konfigurasi perangkat jaringan", 60),
                ("Troubleshooting", "Menganalisis dan menangani gangguan", 70),
                ("Dokumentasi teknis", "Membuat catatan dan laporan kegiatan", 90),
            ],
        )
    conn.commit()
    conn.close()

@app.route("/")
def dashboard():
    conn = db()
    total = conn.execute("SELECT COUNT(*) FROM activities").fetchone()[0]
    done = conn.execute("SELECT COUNT(*) FROM activities WHERE status='Selesai'").fetchone()[0]
    process = conn.execute("SELECT COUNT(*) FROM activities WHERE status='Diproses'").fetchone()[0]
    pending = conn.execute("SELECT COUNT(*) FROM activities WHERE status='Belum'").fetchone()[0]
    activities = conn.execute("SELECT * FROM activities ORDER BY activity_date DESC, id DESC LIMIT 5").fetchall()
    competencies = conn.execute("SELECT * FROM competencies ORDER BY id").fetchall()
    conn.close()
    completion = round(done / total * 100) if total else 0
    avg_comp = round(sum(c["progress"] for c in competencies) / len(competencies)) if competencies else 0
    return render_template("dashboard.html", total=total, done=done, process=process,
                           pending=pending, completion=completion, avg_comp=avg_comp,
                           activities=activities, competencies=competencies)

@app.route("/activities")
def activities():
    conn = db()
    rows = conn.execute("SELECT * FROM activities ORDER BY activity_date DESC, id DESC").fetchall()
    conn.close()
    return render_template("activities.html", activities=rows)

@app.route("/activities/add", methods=["GET", "POST"])
def add_activity():
    if request.method == "POST":
        activity_date = request.form["activity_date"]
        title = request.form["title"].strip()
        description = request.form["description"].strip()
        status = request.form["status"]
        photo = request.files.get("photo")
        filename = None
        if photo and photo.filename:
            ext = photo.filename.rsplit(".", 1)[-1].lower()
            if ext not in ALLOWED_EXTENSIONS:
                flash("Format foto harus PNG, JPG, JPEG, atau WEBP.", "danger")
                return redirect(url_for("add_activity"))
            filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{secure_filename(photo.filename)}"
            photo.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        conn = db()
        conn.execute("""INSERT INTO activities
            (activity_date, title, description, status, photo, created_at)
            VALUES (?, ?, ?, ?, ?, ?)""",
            (activity_date, title, description, status, filename, datetime.now().isoformat()))
        conn.commit()
        conn.close()
        flash("Kegiatan berhasil ditambahkan.", "success")
        return redirect(url_for("activities"))
    return render_template("activity_form.html", today=date.today().isoformat())

@app.route("/activities/delete/<int:id>", methods=["POST"])
def delete_activity(id):
    conn = db()
    row = conn.execute("SELECT photo FROM activities WHERE id=?", (id,)).fetchone()
    if row and row["photo"]:
        path = os.path.join(app.config["UPLOAD_FOLDER"], row["photo"])
        if os.path.exists(path):
            os.remove(path)
    conn.execute("DELETE FROM activities WHERE id=?", (id,))
    conn.commit()
    conn.close()
    flash("Kegiatan dihapus.", "success")
    return redirect(url_for("activities"))

@app.route("/competencies", methods=["GET", "POST"])
def competencies():
    conn = db()
    if request.method == "POST":
        name = request.form["name"].strip()
        description = request.form["description"].strip()
        progress = max(0, min(100, int(request.form["progress"])))
        conn.execute("INSERT INTO competencies(name, description, progress) VALUES (?, ?, ?)",
                     (name, description, progress))
        conn.commit()
        flash("Kompetensi ditambahkan.", "success")
    rows = conn.execute("SELECT * FROM competencies ORDER BY id").fetchall()
    conn.close()
    return render_template("competencies.html", competencies=rows)

@app.route("/competencies/update/<int:id>", methods=["POST"])
def update_competency(id):
    progress = max(0, min(100, int(request.form["progress"])))
    conn = db()
    conn.execute("UPDATE competencies SET progress=? WHERE id=?", (progress, id))
    conn.commit()
    conn.close()
    flash("Progres diperbarui.", "success")
    return redirect(url_for("competencies"))

@app.route("/report/pdf")
def report_pdf():
    conn = db()
    activities = conn.execute("SELECT * FROM activities ORDER BY activity_date DESC").fetchall()
    competencies = conn.execute("SELECT * FROM competencies ORDER BY id").fetchall()
    conn.close()

    path = os.path.join("static", "pkltrack_report.pdf")
    c = canvas.Canvas(path, pagesize=A4)
    width, height = A4
    y = height - 2 * cm

    c.setFont("Helvetica-Bold", 18)
    c.drawString(2 * cm, y, "PKLTrack - Laporan Dokumentasi PKL")
    y -= 0.8 * cm
    c.setFont("Helvetica", 10)
    c.drawString(2 * cm, y, f"Dibuat pada: {datetime.now().strftime('%d-%m-%Y %H:%M')}")
    y -= 1.2 * cm

    c.setFont("Helvetica-Bold", 13)
    c.drawString(2 * cm, y, "Daftar Kompetensi")
    y -= 0.6 * cm
    c.setFont("Helvetica", 10)
    for item in competencies:
        c.drawString(2.2 * cm, y, f"- {item['name']}: {item['progress']}%")
        y -= 0.45 * cm

    y -= 0.4 * cm
    c.setFont("Helvetica-Bold", 13)
    c.drawString(2 * cm, y, "Kegiatan PKL")
    y -= 0.6 * cm
    c.setFont("Helvetica", 9)

    for item in activities:
        if y < 3 * cm:
            c.showPage()
            y = height - 2 * cm
            c.setFont("Helvetica", 9)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(2.2 * cm, y, f"{item['activity_date']} | {item['title']} | {item['status']}")
        y -= 0.4 * cm
        c.setFont("Helvetica", 9)
        description = item["description"]
        for i in range(0, len(description), 95):
            c.drawString(2.5 * cm, y, description[i:i+95])
            y -= 0.35 * cm
        y -= 0.25 * cm

    c.save()
    return send_file(path, as_attachment=True, download_name="laporan_pkltrack.pdf")

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)
