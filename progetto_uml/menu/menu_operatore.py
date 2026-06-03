import time

def start_menu_operatore(auth, serra_service):

    # menu operatore
    while True:
        print("\n=== MENU OPERATORE ===")
        print("\n1 - Avvia ciclo automatico serra")
        print("2 - Stato serra")
        print("3 - Logout")

        scelta = input("> ")

        # opzione 1 (avvio ciclo automatico serra)
        if scelta == "1":
            print("Serra funzionante")
            serra_service.esegui_ciclo_automatico()

        # opzione 2 (lettura stato serra)
        elif scelta == "2":
            print("Stato serra:")
            codice_serra = input("Inserisci il codice della serra: ")
            stato = serra_service.leggi_stato_serra(codice_serra)

            if stato:
                print(f"Ventole: {stato.ventole}")
                print(f"Irrigazione: {stato.irrigazione}")
                print(f"Lampada UV: {stato.lampada_uv}")
                print(f"Coltura: {stato.coltura}")
            else:
                print("Serra non trovata")

        # logout
        elif scelta == "3":
            print("Uscendo dal sistema...")
            time.sleep(3)
            auth.logout()
            break

        else:
            print("Scelta non valida")
