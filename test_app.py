
#test for assignment 2 
from app import app

def test_homepage_loads():
    client=app.test_client()
    response=client.get("/")
    assert response.status_code ==200


#test for assignmest 3 

import services
import json
from datetime import date, timedelta
import os 

def test_snooze_function(tmp_path):
    test_fil=tmp_path/ "test_oppgaver.json"
    services.FILNAVN = str(test_fil)

    idag=date.today().isoformat()
    oppgave = {"tittel": "Test", "frist": idag, "ferdig" :False}
    with open (test_fil,"w", encoding="utf-8") as f:
        json.dump([oppgave], f, indent=4)

    services.snooze(0, days=1)

    with open(test_fil, "r", encoding="utf-8") as f: 
        oppgaver=json.load(f)
    
    ny_frist= oppgaver[0]["frist"]
    forventet_dato= (date.today()+ timedelta(days=1)).isoformat()

    assert ny_frist == forventet_dato