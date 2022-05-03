# Introduzione alla fisica dei sistemi complessi

Progetto di un automa cellulare in un problema di opinion dinamics

## Guida all'installazione

Qui di seguito sono riassunte le generalità riguardanti il codice python utilizzato per l’implementazione e la visualizzazione animata delle simulazioni, il codice C++ per le analisi mostrate nel dettaglio in Sezione 4 e il file batch di comandi
di sistema per generazioni multiple. Per l’esecuzione si rammenta di scaricare l’interpreter di python (v >= 3.10) compatibile con il proprio sistema operativo e di installare il framework ROOT seguedo le istruzioni al link https://root.cern/install/. Inoltre è necessario avere installato le librerie richieste di python, in caso contrario sono facilmente reperibili utilizzando dei package manager come ad esempio pip.

# Funzionamento del codice

Le simulazioni sono eseguite da un codice python strutturato su 3 files:
1. ”global variables.py”,
2. ”functions.py”,
3. ”main.py”.

## global_variables.py

Il primo file, come suggerisce il nome, introduce e inizializza le variabili globali che caratterizzeranno il sistema e la sua dinamica nell’arco della simulazione.
Queste sono classificate in 6 categorie a seconda del loro utilizzo. Seguendo fedelmente l’ordine all’interno del file, si trovano:
1. • l’istanza degli assi utilli alla visualizzazione finale;
1. • le impostazioni temporali dell’animazione;
1. • il dimensionamento dell’automa cellulare (implementato da ambient, lista di 2D arrays, che caratterizzano uno ad uno ciascun sito e che hanno come elementi: l’identificativo e l’opinione dell’individuo che eventualmente occupa il sito, o [-3,-3], se il sito in esame è vuoto);
1. • la variabile (setup) di scelta dello scenario (”Normale”, ”Flocking gravitazionale” o ”Visione parziale”);
1. • le variabili booleane di selezione delle analisi da eseguire, di cui si consigliano le seguenti configurazioni:
    1. – ”False-True-True-False-False” per analisi simultanea di magnetizzazione e distribuzione dei tempi di decisione;
    1. – ”False(True)-False-False-True-True” per analisi di probabilità di osservazione di stati stazionari in condizioni di inizializzazione randomica (ordinata), ricordandosi di porre nsteps > 10000 e di eseguire
main.py tramite lo script start.bat per effettuare un numero arbitrario di esecuzioni automaticamente;
1. • i parametri di controllo del sistema e della dinamica;
1. • i test di adeguatezza delle inizializzazioni compiute, con relativo messaggio
d’errore.

## functions.py

Nel secondo file, invece, sono raccolte le funzioni utilizzate per l’esecuzione delle simulazioni. Tra queste le più importanti permettono:
1. • l’evoluzione temporale (”evolve norm”, ”evolve grav” e ”evolve vis”, ciascuna delle quali permette lo spostamento e il cambiamento di opinione degli individui della popolazione da un generico istante iniziale a quello successivo nello scenario selezionato tramite setup);
1. • il calcolo dell’influenza (”influence norm” e ”influence vis”, che stimano l’opinione media percepita da un singolo individuo, rispettivamente negli scenari di evoluzione normale e flocking gravitazionale e in quello di visione parziale);
1. • l’implementazione dei campi gravitazionali (”local density”, che organizza in un array gli indici di posizione di tutti gli agenti dotati della stessa opinione di quello in esame; ”gravity”, che calcola modulo e verso delle forze attrattive agenti su ciascun individuo ed ”empty probs grav”, che stima il cambiamento nella distribuzione di probabilità di scelta della direzione
di spostamento in accordo con quanto asserito in Sezione 3.3 )
1. • la raccolta dati (”magnetization data storage” e ”decision time data storage”, che sovrascrivono sull’output file selezionato i dati relativi alla magnetizzazione o alla distribuzione dei tempi di decisione della simulazione appena svolta).

## main.py

L'ultimo file si occupa di utilizzare opportunamente e funzioni implementate. Il nucleo del programma è il for loop che permette di evolvere l'automa cellulare nel tempo. La generazione di numeri pseudo-casuali attraverso la libreria numpy permette di ottenere dei risultati diversi ad ogni esecuinoe del codice. La libreria matplotlib si occupa invece della animazione dell'automa cellulare (simulation.gif) e della visualizzazione provvisoria dei grafici per studiarne l'andamento qualitativo. 
