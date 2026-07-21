# Progetto ECOSHELTER


Sistema di gestione di serre automatizzate dedicate all’agricoltura.
Il sistema consente il monitoraggio delle condizioni ambientali interne alla serra e il controllo automatico o manuale degli attuatori per garantire condizioni ottimali di crescita delle colture.
La gestione può essere effettuata localmente dal proprietario tramite una plancia di controllo oppure da remoto dagli operatori dell’azienda per l’aggiornamento delle impostazioni delle colture. 
(per maggiori informazioni consultare documento Word relativo)


# Funzionalità principali
GESTIONE AUTENTICAZIONE

-Registrazione iniziale del proprietario con verifica
 sulle credenziali usate e sul rispetto dei criteri di sicurezza
 
-Login obbligatorio ad ogni nuova sessione.

GESTIONE DELLA SERRA

-Monitoraggio di temperatura e di umidità ambientali.

-Visualizzazione dello stato generale della serra.

-Selezione della modalità che può essere automatica o manuale.


CONTROLLO AUTOMATICO

Il sistema gestisce automaticamente irrigazione, ventole di aerazione, lampada UV.

Le decisioni vengono prese in base ai:

-valori rilevati dai sensori;

-parametri della coltura selezionata.


GESTIONE COLTURE

-Consultazione del catalogo delle colture.

-Selezione della coltura installata nella serra.

-Caricamento automatico dei parametri ottimali.

RACCOLTA DATI CRESCITA

Il proprietario può inserire:

-altezza della pianta;

-dimensione del busto della pianta.

Deve specificare se ha usato impostazioni per la coltivazione diverse da quelle di fabbrica, cioè se ha usato
la modalità automatica oppure manuale per le sua coltivazione.

# Requisiti Software
-Python 3.11 o superiore

-Libreria PyQt6 versione 6.11.0 presente nel file requirements.txt

# Installazione
-Scaricare i file da Github ed entrare nella cartella:

cd progetto_uml

-Avviare l'ambiente virtuale

-Installare le dipendenze:

pip install -r requirements.txt

# Avvio del progetto
Per avviare il software:

python main_GUI.py

All’avvio verrà mostrata la schermata di autenticazione.

# Autori
Riccardo Tiberi

Giovanni Bertozzi

Alessio Menotti

# Implementazione
Implementato in Python 3, rispettando il pattern ECB(Entity-Control-Boundary).

Progetto sviluppato per il corso di ingegneria del software e programmazione.
