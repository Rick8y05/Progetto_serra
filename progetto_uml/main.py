from menu.menu import Menu
from menu.menu_proprietario import start_menu_proprietario
from menu.menu_operatore import start_menu_operatore
import repository
from repository.lettore_dati import DatiRepository
from services.serra_services import SerraService
import time

def main():

    menu = Menu()

    serra_service = SerraService(
        path_serre="data/catalogo_serre.json",
        path_colture="data/colture.json",
        path_temperature="data/valori_temperature.json",
        path_umidita="data/valori_umidita.json",
    )

    while True:

        menu.mostra_menu()
        scelta = menu.scegli_opzione()

        if scelta == "1":

            utente = menu.accesso()

            if utente is None:
                continue

            ruolo = utente.ruolo.strip().lower()

            if ruolo == "proprietario":
                start_menu_proprietario(menu.auth, serra_service)

            elif ruolo == "operatore":
                start_menu_operatore(menu.auth, serra_service)

        elif scelta == "2":
            menu.registrazione()

        elif scelta == "3":
            print("Uscita...")
            time.sleep(3)
            break


if __name__ == "__main__":
    main()