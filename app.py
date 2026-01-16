from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from pathlib import Path

app = Flask(__name__)
DB_PATH = "database.db"
SQL_PATH = "db.sql"

def db():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    return con

def init_db():
    if not Path(DB_PATH).exists():
        con = db()
        with open(SQL_PATH, "r", encoding="utf-8") as f:
            con.executescript(f.read())
        con.commit()
        con.close()

@app.route("/")
def home():
    return redirect(url_for("lista_canali"))

# 3) Lista canali
@app.route("/canali")
def lista_canali():
    con = db()
    canali = con.execute("SELECT * FROM canali ORDER BY id").fetchall()
    con.close()
    return render_template("canali.html", canali=canali)

# 1) Nuovo canale
@app.route("/canali/nuovo", methods=["GET", "POST"])
def nuovo_canale():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        iscritti = request.form.get("numero_iscritti", "0").strip()
        categoria = request.form.get("categoria", "").strip()

        if nome and categoria:
            con = db()
            con.execute(
                "INSERT INTO canali(nome, numero_iscritti, categoria) VALUES (?,?,?)",
                (nome, int(iscritti or 0), categoria)
            )
            con.commit()
            con.close()
            return redirect(url_for("lista_canali"))

    return render_template("nuovo_canale.html")

# 4) Lista video di un canale
@app.route("/canali/<int:canale_id>/video")
def video_canale(canale_id):
    con = db()
    canale = con.execute("SELECT * FROM canali WHERE id=?", (canale_id,)).fetchone()
    video = con.execute("SELECT * FROM video WHERE canale_id=? ORDER BY id", (canale_id,)).fetchall()
    con.close()
    return render_template("video_canale.html", canale=canale, video=video)

# 2) Nuovo video per un canale
@app.route("/canali/<int:canale_id>/video/nuovo", methods=["GET", "POST"])
def nuovo_video(canale_id):
    if request.method == "POST":
        titolo = request.form.get("titolo", "").strip()
        durata = request.form.get("durata", "").strip()
        immagine = request.form.get("immagine", "").strip()  # facoltativa

        if titolo and durata.isdigit():
            con = db()
            con.execute(
                "INSERT INTO video(canale_id, titolo, durata, immagine) VALUES (?,?,?,?)",
                (canale_id, titolo, int(durata), immagine if immagine else None)
            )
            con.commit()
            con.close()
            return redirect(url_for("video_canale", canale_id=canale_id))

    return render_template("nuovo_video.html", canale_id=canale_id)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
