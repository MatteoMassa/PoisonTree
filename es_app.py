from flask import Flask, request
import sqlite3

app = Flask(__name__)

def db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

# CREA DATABASE
@app.route("/init")
def init():
    con = db()
    cur = con.cursor()

    cur.executescript("""
    DROP TABLE IF EXISTS video;
    DROP TABLE IF EXISTS canali;

    CREATE TABLE canali (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        numero_iscritti INTEGER,
        categoria TEXT
    );

    CREATE TABLE video (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        canale_id INTEGER,
        titolo TEXT,
        durata INTEGER,
        immagine TEXT
    );

    INSERT INTO canali (nome, numero_iscritti, categoria)
    VALUES ('Tech Guru',1500,'Tecnologia'),
           ('Chef Stellato',85000,'Cucina'),
           ('Gaming Zone',1200,'Gaming');

    INSERT INTO video (canale_id,titolo,durata,immagine)
    VALUES (1,'Recensione iPhone',600,'iphone.jpg'),
           (2,'Carbonara perfetta',450,'carbonara.jpg'),
           (3,'Minecraft Gameplay',1800,'minecraft.jpg');
    """)
    con.commit()
    con.close()
    return "Database creato!"

# LISTA CANALI
@app.route("/canali")
def canali():
    con = db()
    canali = con.execute("SELECT * FROM canali").fetchall()
    con.close()

    html = "<h1>Canali</h1>"
    for c in canali:
        html += f"<p>{c['nome']} - {c['categoria']} \
        <a href='/video/{c['id']}'>Video</a></p>"
    return html

# VIDEO DI UN CANALE
@app.route("/video/<int:id>")
def video(id):
    con = db()
    video = con.execute("SELECT * FROM video WHERE canale_id=?", (id,)).fetchall()
    con.close()

    html = "<h1>Video</h1>"
    for v in video:
        html += f"<p>{v['titolo']} ({v['durata']} sec)</p>"
    return html

# AGGIUNGI CANALE
@app.route("/nuovo_canale")
def nuovo_canale():
    nome = request.args.get("nome")
    iscritti = request.args.get("iscritti")
    categoria = request.args.get("categoria")

    con = db()
    con.execute("INSERT INTO canali VALUES (NULL,?,?,?)",
                (nome,iscritti,categoria))
    con.commit()
    con.close()
    return "Canale inserito"

# AGGIUNGI VIDEO
@app.route("/nuovo_video")
def nuovo_video():
    canale = request.args.get("canale")
    titolo = request.args.get("titolo")
    durata = request.args.get("durata")

    con = db()
    con.execute("INSERT INTO video VALUES (NULL,?,?,?,NULL)",
                (canale,titolo,durata))
    con.commit()
    con.close()
    return "Video inserito"

app.run(debug=True)
