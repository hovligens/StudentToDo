#test for assignment 4. 

import services
from datetime import date
 

def test_sqlite_basic (tmp_path):
    db_fil = tmp_path / "test_basic.db"
    services.DB_FIL = str(db_fil)

    services.init_db()

    i_dag = date.today().isoformat()
    services.legg_til_oppgaver("Testoppgave", i_dag)

    oppgaver = services.les_oppgaver()

    assert len(oppgaver) == 1
    assert oppgaver[0]["tittel"]== "Testoppgave"
