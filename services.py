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

# kalender 

def neste_7_dager_gruppe(oppgaver):
    idag = date.today()
    grupper = { (idag + timedelta(days=i)).isoformat():[]for i in range(7) }
    for o in oppgaver:
        frist = o.get("frist")
        if frist in grupper:
            grupper[frist].append(o)
    return [(d, grupper[d]) for d in sorted(grupper.keys())]
    




