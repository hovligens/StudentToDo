

from flask import Flask, render_template, request, redirect, url_for
import json
import os
from datetime import datetime

app= Flask(__name__)
FILNAVN= "oppgaver.json"

#prioritet 1, legge til og fjerne

def les_oppgaver():
    if not os.path.exists(FILNAVN):
        return[]
    with open(FILNAVN,"r", encoding="utf-8") as f:
        return json.load(f)
    
def skriv_oppgaver(oppgaver):
    with open(FILNAVN,"w", encoding="utf-8") as f:
        json.dump(oppgaver, f,indent=4, ensure_ascii=False)

#prioritet 2, sortere liste etter frist

def finn_dato(datestr):
    return datetime.strptime(datestr,"%Y-%m-%d")

def sorter_oppgaver(oppgaver):
    return sorted(oppgaver, key=lambda o:finn_dato(o["frist"]))


@app.route("/", methods=["GET", "POST"])
def home():
    oppgaver = les_oppgaver()

    if request.method=="POST":
        tittel=request.form.get("tittel")
        frist=request.form.get("frist")

        if tittel and frist:
            oppgaver.append({"tittel":tittel,"frist":frist,"ferdig":False})
            skriv_oppgaver(oppgaver)
        return redirect(url_for("home"))
    
    oppgaver=sorter_oppgaver(oppgaver)
    
    return render_template("index.html", oppgaver=oppgaver)
    

@app.route("/fjern/<int:index>")
def fjern(index):
    oppgaver = les_oppgaver()
    if 0<= index< len(oppgaver):
        oppgaver.pop(index)
        skriv_oppgaver(oppgaver)
    return redirect(url_for("home"))

@app.route("/status/<int:index>")
def status(index):
    oppgaver=les_oppgaver()
    if 0<=index<len(oppgaver):
        oppgaver[index]["ferdig"]= not oppgaver[index]["ferdig"]
        skriv_oppgaver(oppgaver)
    return redirect(url_for("home"))

if __name__== "__main__":
    app.run(debug=True)
