
import sqlite3
from datetime import date, datetime, timedelta

DB_FIL= "oppgaver.db"

def get_connection():
    conn = sqlite3.connect(DB_FIL)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS oppgaver(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tittel TEXT NOT NULL,
            frist TEXT NOT NULL,
            ferdig INTEGER NOT NULL DEFAULT 0
            )
    """)
    conn.commit()
    conn.close()

init_db()



def les_oppgaver():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, tittel, frist, ferdig FROM oppgaver ORDER BY frist")
    rows = cur.fetchall()
    conn.close()

    return[
        {"tittel": r["tittel"], "frist": r["frist"],"ferdig": bool(r["ferdig"])}
    for r in rows
    ]
    


def legg_til_oppgaver(tittel, frist):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO oppgaver (tittel, frist, ferdig) VALUES (?, ?, 0)",
        (tittel, frist)
    )
    conn.commit()
    conn.close()

def fjern(index):
    oppgaver = les_oppgaver()
    if not (0 <= index < len (oppgaver)):
        return
    
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id FROM oppgaver ORDER BY frist ASC")
    ids = [r["id"] for r in cur.fetchall()]
    
    if 0 <= index < len(ids):
        cur.execute("DELETE FROM oppgaver WHERE id = ?", (ids[index],))
        conn.commit()
    conn.close()

def status(index):
    oppgaver = les_oppgaver()
    if not (0 <= index < len(oppgaver)):
        return
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, ferdig FROM oppgaver ORDER BY frist ASC")
    rows = cur.fetchall()

    row= rows[index]
    ny_status = 0 if row["ferdig"] else 1

    cur.execute("UPDATE oppgaver SET ferdig = ? WHERE id = ?", (ny_status, row["id"]))
    conn.commit()
    conn.close()



def finn_dato(datestr):
    return datetime.strptime(datestr,"%Y-%m-%d")

def sorter_oppgaver(oppgaver):
    try:
        return sorted(oppgaver, key=lambda o:finn_dato(o["frist"]))
    except Exception:
        return oppgaver

#andre runde, varsling
def varslinger(dager=3):
    narmest =[]
    idag = datetime.today().date()
    for oppgave in les_oppgaver():
        frist = datetime.strptime(oppgave["frist"], "%Y-%m-%d").date()
        if 0 <= (frist-idag ).days <= dager:
            narmest.append(oppgave)
    return narmest 
#tredje runde, ekstra 

def add_days(iso_date:str, days: int) ->str:
    d=datetime.strptime(iso_date,"%Y-%m-%d").date()
    return (d+timedelta(days=days)).isoformat()

def snooze(index: int, days: int = 1 ):
    oppgaver = les_oppgaver()
    if not (0 <= index < len(oppgaver)):
        return
    
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, frist FROM oppgaver ORDER BY frist ASC")
    rows = cur.fetchall()

    row = rows[index]
    ny_frist = add_days(row["frist"], days)

    cur.execute("UPDATE oppgaver SET frist = ? WHERE id = ?", (ny_frist,row["id"]))
    conn.commit()
    conn.close()


def varslinger_fra_liste(oppgaver, dager=3):
    idag=date.today()
    result = []
    for o in oppgaver:
        try:
            frist_d=datetime.strptime(o["frist"], "%Y-%m-%d").date()
        except Exception:
            continue
        days_left = (frist_d - idag).days
        if 0 <= days_left <=dager:
            kopiert=dict(o)
            kopiert["days_left"]= days_left
            result.append(kopiert)
    return result 






# kalender 

def neste_7_dager_gruppe(oppgaver):
    idag = date.today()
    dag_keys= { (idag + timedelta(days=i)).isoformat():[]for i in range(21) }
    grupper = {d: [] for d in dag_keys}

    for o in oppgaver:
        frist = o.get("frist")
        if not frist:
            continue
        try:
            frist_dato = datetime.strptime(frist, "%Y-%m-%d").date()
        except Exception:
            continue 
        
        iso =frist_dato.isoformat()
        if iso in grupper:
            grupper[iso].append(o)
    
    return [(d, grupper[d]) for d in dag_keys]
        





