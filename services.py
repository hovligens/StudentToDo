import json
import os
from datetime import datetime
from datetime import date, datetime, timedelta 
from collections import defaultdict



FILNAVN= "oppgaver.json"

def les_oppgaver():
    if not os.path.exists(FILNAVN):
        return[]
    with open(FILNAVN,"r", encoding="utf-8") as f:
        return json.load(f)
    
def skriv_oppgaver(oppgaver):
    with open(FILNAVN,"w", encoding="utf-8") as f:
        json.dump(oppgaver, f,indent=4, ensure_ascii=False)

def legg_til_oppgaver(tittel, frist):
    oppgaver=les_oppgaver()
    oppgaver.append({"tittel": tittel,"frist":frist, "ferdig": False})
    skriv_oppgaver(oppgaver)

def fjern(index):
    oppgaver = les_oppgaver()
    if 0<= index< len(oppgaver):
        oppgaver.pop(index)
        skriv_oppgaver(oppgaver)

def status(index):
    oppgaver=les_oppgaver()
    if 0<=index<len(oppgaver):
        oppgaver[index]["ferdig"]= not oppgaver[index]["ferdig"]
        skriv_oppgaver(oppgaver)

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
    if 0 <= index < len(oppgaver):
        frist = oppgaver[index].get("frist")
        if frist:
            oppgaver[index]["frist"]= add_days(frist, days)
            skriv_oppgaver(oppgaver)


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
    dag_keys= { (idag + timedelta(days=i)).isoformat():[]for i in range(7) }
    grupper = {d: [] for d in dag_keys}
    fremtidige = []

    for o in oppgaver:
        frist = o.get("frist")
        if not frist:
            continue
        try:
            frist_dato = datetime.strptime(frist, "%Y-%m-%d").date()
        except Exception:
            continue 
        if frist_dato<= idag + timedelta(days=6):
            if frist in grupper:
                grupper[frist].append(o)
        else:
            fremtidige.append(o)
        
    liste = [(d, grupper[d]) for d in dag_keys]
    if fremtidige:
        liste.append(("Senere", fremtidige))
    return liste
    




