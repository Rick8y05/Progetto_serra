import time
import json

def start_menu_proprietario(auth, serra_service):

    # menu proprietario
    while True:
        print("\n=== MENU PROPRIETARIO ===")
        print("1 - Visualizza utenti")
        print("2 - Modalità funzionamento")
        print("3 - Aziona dispositivi")
        print("4 - Configura coltura")
        print("5 - Dati plancia")
        print("6 - Logout")

        scelta = input("> ").strip()

        # opzione 1 (visualizzazione utenti registrati)
        if scelta == "1":
            utenti = auth.get_utenti()

            for email, dati in utenti.items():
                print(f"{email} ({dati['ruolo']})")

        # opzione 2 (selezione modalità automatica o manuale)
        elif scelta == "2":
            print("\n1 - Automatica")
            print("2 - Manuale")

            scelta_mod = input("Modalità: ").strip()

            modalita = "automatica" if scelta_mod == "1" else "manuale"

            serra_service.set_modalita(modalita)

            print(f"Modalità impostata: {modalita}")

        # opzione 3 (attivazione/disattivazione ventole, irrigazione e lampade UV)
        elif scelta == "3":
            print("\n--- CONTROLLO MANUALE ---")
            print("1 - Ventole")
            print("2 - Irrigazione")
            print("3 - Lampada UV")

            codice = input("Codice serra: ").strip().lower()

            dispositivo = input("Dispositivo (1/2/3): ").strip()
            stato = input("ON/OFF: ").strip().lower()

            if stato == "on":
                print(f"Accensione dispositivo {dispositivo} in corso...")
            elif stato == "off":
                print(f"Spegnimento dispositivo {dispositivo} in corso...")
            else:
                print("Stato non valido (usa ON/OFF)")
                continue

            serra_service.azione_manuale(codice, dispositivo, stato)

        # opzione 4 (configurazione colture)
        elif scelta == "4":
            coltura = input("Nome coltura: ").strip().lower()

            try:
                with open("data/colture.json", "r") as f:
                    colture = json.load(f)
            except:
                print("Errore lettura file colture")
                continue

            if coltura not in colture:
                print("Coltura non trovata")
                continue

            codice = input("Codice serra: ").strip().lower()
            serra_service.configura_coltura(codice, coltura)
            print("Coltura configurata!")

        # opzione 5 (dati plancia)
        elif scelta == "5":
            print("\n--- PLANCIA ---")

            dati = serra_service.get_dati_plancia()

            if not dati:
                print("Nessuna serra disponibile")
                continue

            for codice, info in dati.items():
                print(f"\nSERRA {codice}")
                print(f"Temperatura: {info.get('temperatura')}")
                print(f"Umidità: {info.get('umidita')}")
                print(f"Modalità: {info.get('modalita')}")

        # opzione 6 (logout)
        elif scelta == "6":
            print("Logout...")
            time.sleep(1)
            auth.logout()
            break

        else:
            print("Scelta non valida")
