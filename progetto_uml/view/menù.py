# Menù
import time
from models.Utente import Utente

def mostra_menu():
    print("\n\n°°°°°° BENVENUTO NEL MENU' PRINCIPALE °°°°°°")
    print("Scegli un'opzione:")
    print("1 - Accedi")
    print("2 - Registrati")
    print("3 - Esci")

# selezione opzione
def scegli_opzione():
    scelta = input("\n> ")
    return scelta

# accesso
def accesso():
    while True:
        print("\n=== ACCESSO ===")
        email = input("Email: ")
        password = input("Password: ")
        utente = Utente(email, password)
        if utente.login():
            print("\nAccesso effettuato con successo!")
            return(False)
        else:
            print("\nCredenziali non valide. Riprova.")

# registrazione
def registrazione():
    print("\n=== REGISTRAZIONE ===")
    email = input("Email: ")
    utente = Utente(email, "")

    while email in Utente.utenti_registrati:
        print("\nQuesta email è già registrata.")
        email = input("Email: ")
        utente.email = email

    password = input("Password (minimo 6 caratteri): ")
    while len(password) < 6:
        print("La password deve contenere almeno 6 caratteri.")
        password = input("Password: ")

    utente_nuovo = Utente(email, password)
    if utente_nuovo.registra():
        print("\nUtente registrato correttamente!")
    else:
        print("\nErrore nella registrazione. Riprovare più tardi.")

    print("\n=== ACCESSO ===")
    email = input("Email: ")
    password = input("Password: ")
    utente = Utente(email, password)
    if utente.login():
        print("\nAccesso effettuato con successo!")
        return(False)
    else:
        print("\nCredenziali non valide. Riprova.")

# uscita dal sistema
def esci():
    print("\nUscendo dal sistema... Arrivederci!")
    time.sleep(3)

def main():
    while True:
        mostra_menu()
        scelta = scegli_opzione()
        
        if scelta == "1":
            accesso()
            return(False)
        elif scelta == "2":
            registrazione()
            return(False)
        elif scelta == "3":
            esci()
            break
        else:
            print("\nScelta non valida. Seleziona 1, 2 o 3.")

if __name__ == "__main__":
    main()