import mysql.connector

def pripojeni_db():
    """Připojení k databázi""" 
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="password", # změň dle svého nastavení hesla
            database="sys"
        )
        print("Připojení k databázi bylo úspěšné.")
    except mysql.connector.Error as err:
        print(f"Chyba při připojování: {err}")
    
    return conn

def odpojeni_db(conn):
    conn.close()
    print("Připojení k databázi bylo uzavřeno.")

def pridat_ukol_db(conn, uziv_nazev, uziv_popis):
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO ukoly (nazev, popis, stav) VALUES (%s, %s, %s)", (uziv_nazev, uziv_popis, "Nezahájeno"))
        conn.commit()
        print("Záznam byl vložen.")
        cursor.close()
        return True
    except mysql.connector.Error as err:
        print(f"Chyba při vkládání dat: {err}")
        raise

def pridat_ukol(conn):
    while True:
        uziv_nazev = input("Zadejte název úkolu: ")
        uziv_popis = input("Zadejte popis úkolu: ")
        if uziv_nazev == "" or uziv_popis == "":
            print("Zadal jste prázdný vstup.")
            continue
        
        pridat_ukol_db(conn, uziv_nazev, uziv_popis)
        break

def zobrazit_ukoly(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, nazev, popis, stav FROM ukoly WHERE stav IN (%s, %s)", ("Nezahájeno", "Probíhá"))
        ukoly = cursor.fetchall()
        cursor.close()
        if not ukoly:
            print("Seznam úkolů je prázdný.")
        else:
            print("Seznam úkolů:")
            for ukol in ukoly:
                print(f"{ukol[0]} - {ukol[1]} - {ukol[2]} - {ukol[3]}")
    except mysql.connector.Error as err:
        print(f"Chyba při načítání dat: {err}")

def aktualizovat_ukol_db(conn, aktualizovany_ukol, aktualizovany_stav):
    cursor = conn.cursor()
    cursor.execute("UPDATE ukoly SET stav = %s WHERE ID = %s", (aktualizovany_stav, aktualizovany_ukol))
    conn.commit()

    if cursor.rowcount == 0:
        cursor.close()
        raise ValueError(f"Úkol s ID={aktualizovany_ukol} neexistuje.")
    
    cursor.close()
    print("Záznam byl aktualizován.")
    return True

def aktualizovat_ukol(conn):
    while True:
        zobrazit_ukoly(conn)
        try:
            aktualizovany_ukol = int(input("Vyber ID úkolu k aktualizaci: "))
        except ValueError:
            print("Chyba: zadejte platné číslo.")
            continue
        
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM ukoly WHERE id = %s AND stav != 'Hotovo'", (aktualizovany_ukol,))
        if cursor.fetchone()[0] == 0:
            print(f"Úkol s ID {aktualizovany_ukol} neexistuje. Zkuste to znovu.")
            continue
        
        while True:
            aktualizovany_stav = input("Vyber stav úkolu: Probíhá (p) / Hotovo (h)")
            if aktualizovany_stav.lower() == "p":
                aktualizovany_stav = "Probíhá"
                break
            elif aktualizovany_stav.lower() == "h":
                aktualizovany_stav = "Hotovo"
                break
            else:
                print("Neplatná volba. Zkuste to znovu.")
    
        aktualizovat_ukol_db(conn, aktualizovany_ukol, aktualizovany_stav)
        break

def odstranit_ukol_db(conn, odstraneny_ukol):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM ukoly WHERE ID = %s", (odstraneny_ukol,))
    conn.commit()
    
    if cursor.rowcount == 0:
        cursor.close()
        raise ValueError(f"Úkol s ID={odstraneny_ukol} neexistuje.")
    
    cursor.close()
    print("Záznam byl smazán.")
    return True

def odstranit_ukol(conn):
    while True:
        zobrazit_ukoly(conn)
        try:
            odstraneny_ukol = int(input("Zadejte ID úkolu, který chcete odstranit: "))
        except ValueError:
            print("Chyba: zadejte platné číslo.")
            continue

        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM ukoly WHERE id = %s", (odstraneny_ukol,))
        if cursor.fetchone()[0] == 0:
            print(f"Úkol s ID {odstraneny_ukol} neexistuje. Zkuste to znovu.")
            continue

        odstranit_ukol_db(conn, odstraneny_ukol)
        break
       
def hlavni_menu():
    while True:
        print(
"""
1. Přidat nový úkol
2. Zobrazit úkoly
3. Aktualizovat úkol
4. Odstranit úkol
5. Konec programu
""")
        uziv_vstup = input("Vyberte možnost(1-5): ")
        if uziv_vstup == "1":
            pridat_ukol(conn)
        elif uziv_vstup == "2":
            zobrazit_ukoly(conn)
        elif uziv_vstup == "3":
            aktualizovat_ukol(conn)
        elif uziv_vstup == "4":
            odstranit_ukol(conn)
        elif uziv_vstup == "5":
            print("Konec programu.")
            break
        else: 
            print("Neplatná volba.")

def vytvoreni_tabulky(conn):
    try:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ukoly (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nazev VARCHAR(20),
                popis VARCHAR(50),
                stav VARCHAR(20)
            )
        ''')
        cursor.close()
        print("Tabulka 'ukoly' byla vytvořena.")
    except mysql.connector.Error as err:
        print(f"Chyba při vytváření tabulky: {err}")

if __name__ == "__main__":
    conn = pripojeni_db()
    hlavni_menu()
    odpojeni_db(conn)
