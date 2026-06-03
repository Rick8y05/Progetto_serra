from menu.menu import Menu
from menu.menu_proprietario import start_menu_proprietario
from menu.menu_operatore import start_menu_operatore
from services.serra_services import GestoreSerra

from repository.lettore_dati import DatiRepository
from services.gestore_colture import GestoreColture
import time


def main():

    menu = Menu()

    # path che definisce i file json utilizzati
    path_serre = "data/catalogo_serre.json"
    path_colture = "data/colture.json"
    path_temp = "data/valori_temperature.json"
    path_umidita = "data/valori_umidita.json"

    # repository per leggere i dati dei file json
    repo_serre = DatiRepository(path_serre)
    repo_colture = DatiRepository(path_colture)
    repo_temp = DatiRepository(path_temp)
    repo_umidita = DatiRepository(path_umidita)

    # gestore delle colture
    gestore_colture = GestoreColture(
        repo_colture.get_dati,
        repo_colture.get_dati
    )

    serra_service = GestoreSerra(
        repo_serre.get_dati,
        repo_temp.get_dati,
        repo_umidita.get_dati,
        gestore_colture
    )

    # logica menu
    def run():

        menu.mostra_menu()
        scelta = menu.scegli_opzione()

        gestisci_scelta(scelta, menu, serra_service, run)

    def gestisci_scelta(scelta, menu, serra_service, run):

        # opzione 1 (login utente)
        if scelta == "1":

            utente = menu.accesso()

            if utente is None:
                run()
                return

            ruolo = utente.ruolo.strip().lower()

            # apertura menu corrispondente al ruolo
            if ruolo == "proprietario":
                start_menu_proprietario(menu.auth, serra_service)
            elif ruolo == "operatore":
                start_menu_operatore(menu.auth, serra_service)

            run()
            return

        # opzione 2 (registrazione nuovo proprietario)
        elif scelta == "2":
            menu.registrazione()
            run()
            return

        # opzione 3 (logout)
        elif scelta == "3":
            print("Uscita...")
            return
        else:
            print("Scelta non valida")
            run()

    run()


if __name__ == "__main__":
    main()
