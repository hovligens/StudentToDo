

from flask import Flask, render_template, request, redirect, url_for
import services

app= Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method=="POST":
        tittel = request.form.get("tittel")
        frist = request.form.get("frist")
        if tittel and frist:
            services.legg_til_oppgaver(tittel, frist)
        return redirect(url_for("home"))
    
    oppgaver = services.les_oppgaver()
    oppgaver = services.sorter_oppgaver(oppgaver)

    for i, o in enumerate(oppgaver):
        o["__global_index"] = i

    f = request.args.get("filter", "alle")
    if f == "uferdig":
        filtrerte = [o for o in oppgaver if not o.get("ferdig", False)]
    elif f == "ferdig":
        filtrerte = [o for o in oppgaver if o.get("ferdig", False)]
    else:
        filtrerte = oppgaver


    varslinger= services.varslinger_fra_liste(oppgaver, dager=3)
    kalender = services.neste_7_dager_gruppe(filtrerte)
    
    return render_template("index.html", oppgaver=filtrerte, varslinger=varslinger,kalender=kalender,filter_val=f )

    

@app.route("/fjern/<int:index>")
def fjern(index):
    services.fjern(index)
    return redirect(url_for("home"))


@app.route("/status/<int:index>")
def status(index):
    services.status(index)
    return redirect(url_for("home"))


@app.route("/snooze/<int:index>")
def snooze(index):
    services.snooze(index, days=1)
    return redirect(url_for("home"))


if __name__== "__main__":
    app.run(debug=True)
