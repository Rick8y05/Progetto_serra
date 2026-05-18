import os
import time
from models.serra import Serra
from models.sensore import Sensori

# Calcoliamo i percorsi assoluti per evitare l'errore "File non trovato"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Modifica questi nomi/cartelle in base a dove si trovano i tuoi file JSON reali
PATH_COLTURA =  "data/colture.json"
PATH_TEMP = "data/valori_temperature.json"
PATH_UMIDITA = "data/valori_umidita.json"


def stampa_separatore(titolo):
    print("\n" + "=" * 60)
    print(f"{titolo.center(60)}")
    print("=" * 60)


def main():
    stampa_separatore("AVVIO COLLAUDO COMPLETO SISTEMA SERRA")

    # 1. ISTANZIAMO LA SERRA
    # Passiamo Alessio come proprietario e il basilico come coltura iniziale
    try:
        mia_serra = Serra(
            proprietario="Alessio",
            path_dati_coltura=PATH_COLTURA,
            modalita="manuale",
            path_temperature=PATH_TEMP,
            path_umidita=PATH_UMIDITA
        )
        print("[OK] Istanza della Serra creata correttamente.")
        print(f"Proprietario: {mia_serra.proprietario}")
    except Exception as e:
        print(f"❌ Errore durante la creazione della serra: {e}")
        return

    # -------------------------------------------------------------------------
    # TEST 1: CAMBIO COLTURA (E TEST ANTI-IMBECILLE)
    # -------------------------------------------------------------------------
    stampa_separatore("TEST 1: Gestione e Cambio Coltura")

    print("\n--> Provo a impostare 'ROSMARINO' (con le maiuscole):")
    mia_serra.set_coltura("ROSMARINO")

    print("\n--> Provo a inserire una pianta inesistente per testare il KeyError:")
    mia_serra.set_coltura("Ananas")

    print("\n--> Ripristino 'basilico' per i successivi test automatici:")
    mia_serra.set_coltura("basilico")

    # -------------------------------------------------------------------------
    # TEST 2: MODALITÀ MANUALE (Controllo diretto attuatori)
    # -------------------------------------------------------------------------
    stampa_separatore("TEST 2: Controllo Manuale Attuatori")

    print("[MANUALE] Attivazione forzata di tutti i sistemi...")
    mia_serra.mod_manuale_ventole(True)
    mia_serra.mod_manuale_lampada_UV(True)
    mia_serra.mod_manuale_sistema_irrigazione(True)

    print("\n[MANUALE] Disattivazione forzata di tutti i sistemi...")
    mia_serra.mod_manuale_ventole(False)
    mia_serra.mod_manuale_lampada_UV(False)
    mia_serra.mod_manuale_sistema_irrigazione(False)

    # -------------------------------------------------------------------------
    # TEST 3: MODALITÀ AUTOMATICA (Simulazione Cicli)
    # -------------------------------------------------------------------------
    stampa_separatore("TEST 3: Simulazione Modalità Automatica")
    print(
        "Il sistema leggerà i file dei sensori ed eseguirà la logica sugli if."
    )
    print("Vengono eseguiti 3 cicli di controllo distanziati nel tempo.\n")

    mia_serra.modalita = "automatico"

    for ciclo in range(1, 4):
        print(f"\n--- [CICLO AUTOMATICO #{ciclo}] ---")

        # Eseguiamo la logica di controllo che hai scritto in serra.py
        mia_serra.mod_automatica()

        # Stampiamo lo stato attuale per vedere cosa ha deciso di fare la serra
        print(f"Temperatura rilevata: {mia_serra.get_temperatura_serra}°C")
        print(f"Umidità rilevata: {mia_serra.get_umidita_serra}%")
        print(
            f"Target impostati per la pianta: Temp {mia_serra.pianta_selezioanta['temperatura']}°C | Umidità {mia_serra.pianta_selezioanta['umidita']}%"
        )

        # Pausa di 2 secondi tra un ciclo e l'altro per simulare il tempo reale
        time.sleep(2)

    stampa_separatore("FINE TEST - TUTTI I SISTEMI VERIFICATI")


if __name__ == "__main__":
    main()