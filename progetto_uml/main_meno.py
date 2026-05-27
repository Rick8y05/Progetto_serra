from repository.lettore_dati import DatiRepository
from service.gestore_colture import GestoreColture
from service.gestore_serra import GestoreSerra
from view.interfacci_di_test import Interfaccia

#from service.gestore_serra import GestoreSerra
path_cat_serre="data/catalogo_serre.json"
path_colture="data/colture.json"
path_dati_colt_utente="data/dati_colture_utente.json"
path_val_temperatura="data/valori_temperature.json"
path_val_umidita="data/valori_umidita.json"
#repository
repository_serre = DatiRepository(path_cat_serre)
repository_colture = DatiRepository(path_colture)
repository_dati_colt_utente = DatiRepository(path_dati_colt_utente)
repository_val_temperatura = DatiRepository(path_val_temperatura)
repository_val_umidita = DatiRepository(path_val_umidita)
#repository
#inizializzazione_gestori

gestore_colture = GestoreColture(repository_colture.get_dati,repository_dati_colt_utente.get_dati)
gestore_serra = GestoreSerra(repository_serre.get_dati,repository_val_temperatura.get_dati,repository_val_umidita.get_dati, gestore_colture)
view1 = Interfaccia(gestore_serra, gestore_colture)
view1.menu_selezione_proprietario_operatore()
repository_serre.salvatggio_dati(gestore_serra.dati_salvataggio)
repository_dati_colt_utente.salvatggio_dati(gestore_colture.dati_colture_utente)



