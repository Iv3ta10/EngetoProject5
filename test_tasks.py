import mysql.connector
import pytest
from main import pridat_ukol_db, aktualizovat_ukol_db, odstranit_ukol_db

@pytest.fixture
def nastaveni_db():
    """Připojení k databázi""" 
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="password", # změň dle svého nastavení hesla
            database="testDB"
        )
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ukoly (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nazev VARCHAR(20) NOT NULL,
                popis VARCHAR(50) NOT NULL,
                stav VARCHAR(20)
            )
        ''')
        conn.commit()

    except mysql.connector.Error as err:
        raise RuntimeError(f"Chyba při připojování k DB: {err}")

    yield conn, cursor

    cursor.execute("DROP TABLE IF EXISTS ukoly")
    conn.commit()
    cursor.close()
    conn.close()

def test_pridat_ukol_pozitivni(nastaveni_db):
    conn, cursor = nastaveni_db

    nazev = "název"
    popis = "popis"

    res = pridat_ukol_db(conn, nazev, popis)
    assert res == True, "Výsledek měl být True, ale program vypsal False"

    cursor.execute("SELECT * FROM ukoly")
    vysledek = cursor.fetchone()
    assert vysledek['nazev'] == nazev, f"Výsledek měl být '{nazev}', ale program vypsal '{vysledek['nazev']}'"
    assert vysledek['popis'] == popis, f"Výsledek měl být '{popis}', ale program vypsal '{vysledek['popis']}'"
    assert vysledek['stav'] == "Nezahájeno", f"Výsledek měl být 'Nezahájeno', ale program vypsal '{vysledek['stav']}'"

def test_pridat_ukol_negativni(nastaveni_db):
    conn, cursor = nastaveni_db

    nazev = None
    popis = None

    with pytest.raises(mysql.connector.Error):
        pridat_ukol_db(conn, nazev, popis)
           
def test_aktualizovat_ukol_pozitivni(nastaveni_db):
    conn, cursor = nastaveni_db
    
    cursor.execute(
    "INSERT INTO ukoly (nazev, popis, stav) VALUES (%s, %s, %s)",
    ("Testovací úkol", "Popis testu", "Nezahájeno"))

    ak_ukol = 1
    ak_stav = "Probíhá"
    res = aktualizovat_ukol_db(conn, ak_ukol, ak_stav)
    assert res == True, "Výsledek měl být True, ale program vypsal False"
    
    cursor.execute("SELECT * FROM ukoly WHERE id = %s", (ak_ukol,))
    vysledek = cursor.fetchone()
    assert vysledek['stav'] == ak_stav, f"Výsledek měl být {ak_stav}, ale program vypsal {vysledek['stav']}"

def test_aktualizovat_ukol_negativni(nastaveni_db):
    conn, cursor = nastaveni_db

    neexistujici_ukol = -1
    novy_stav = "Probíhá"

    with pytest.raises(ValueError):
        aktualizovat_ukol_db(conn, neexistujici_ukol, novy_stav)

def test_odstranit_ukol_pozitivni(nastaveni_db):
    conn, cursor = nastaveni_db

    cursor.execute(
        "INSERT INTO ukoly (nazev, popis, stav) VALUES (%s, %s, %s)",
        ("Název", "Popis", "Nezahájeno")
    )
    conn.commit()

    odstraneny_ukol = 1
    res = odstranit_ukol_db(conn, odstraneny_ukol)
    assert res == True, "Výsledek měl být True, ale program vypsal False"
    
    cursor.execute("SELECT * FROM ukoly WHERE id=%s", (odstraneny_ukol,))
    vysledek = cursor.fetchone()
    assert vysledek is None, "Úkol nebyl odstraněn z databáze"

def test_odstranit_ukol_negativni(nastaveni_db):
    """ Negativní test: Mazání neexistujícího záznamu. """
    conn, cursor = nastaveni_db

    neexistujici_id = -1

    with pytest.raises(ValueError):
        odstranit_ukol_db(conn, neexistujici_id)
