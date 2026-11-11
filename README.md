# ZERO PARADES: For Dead Spies - traduzione italiana amatoriale

Traduzione italiana completa dei testi del gioco: dialoghi, diario, oggetti, pensieri, menu e interfaccia (72.470 testi). Traduzione 1.0, installer 1.1 (11 novembre 2026).

È una traduzione **non ufficiale**, fatta da un appassionato. Se un giorno uscirà l'italiano ufficiale, usa quello.

Il pacchetto **non contiene file del gioco**: contiene solo i testi italiani e un programmino che li inserisce nella tua copia. Serve quindi il gioco originale installato.

## Cosa cambia nel gioco

Il gioco non permette di aggiungere una lingua nuova, quindi l'italiano prende il posto del **tedesco**. Inglese, spagnolo, russo e cinese restano come sono. Le voci parlate restano in inglese.

## Cosa serve

- ZERO PARADES: For Dead Spies installato (Steam o GOG), versione per Windows. Su Linux e Steam Deck va bene la stessa versione avviata con Proton.
- [Python 3](https://www.python.org/downloads/), versione 3.9 o successiva.
- La libreria Python [UnityPy](https://github.com/K0lb3/UnityPy), che serve a leggere e riscrivere il file dei testi. Si installa una volta sola con un comando, spiegato qui sotto. Gli script di questo pacchetto non si collegano a Internet e non scaricano nulla.
- Circa 30 MB liberi nella cartella del gioco per il backup.

## Installazione

Chiudi il gioco prima di cominciare.

### Windows

1. Installa Python da python.org. Nella prima schermata dell'installazione spunta **Add python.exe to PATH**.
2. Installa UnityPy: apri il Prompt dei comandi (tasto Windows, scrivi `cmd`, Invio) e scrivi `py -m pip install UnityPy==1.25.4`. Va fatto una volta sola.
3. Scompatta questo pacchetto dove vuoi.
4. Fai doppio clic su **Installa.bat**.
5. Se lo script non trova il gioco da solo, ti chiede la cartella: è quella che contiene `ZeroParades.exe`. In Steam la apri con clic destro sul gioco > Gestisci > Sfoglia i file locali. Puoi incollare il percorso o trascinare la cartella nella finestra.

Se il gioco sta in `C:\Program Files` e compare un errore di permessi, fai clic destro su Installa.bat > Esegui come amministratore.

### Linux e Steam Deck

Da terminale (sullo Steam Deck: modalità Desktop > Konsole), dentro la cartella del pacchetto. La prima volta installa UnityPy in una cartella `.venv` locale, senza toccare il resto del sistema:

```bash
python3 -m venv .venv
```

```bash
.venv/bin/python -m pip install -r requisiti.txt
```

Poi avvia l'installer:

```bash
./installa.sh
```

Per indicare la cartella del gioco a mano:

```bash
./installa.sh "/percorso/della/cartella/del/gioco"
```

### Attivare l'italiano

Avvia il gioco, apri **Settings > Text Language** e scegli **Deutsch**. Da quel momento i testi sono in italiano e la voce del menu compare come **Italiano**.

## Disinstallazione

Doppio clic su **Ripristina.bat** (Windows) oppure `./ripristina.sh` (Linux). Rimette al loro posto i due file originali e cancella il backup.

In alternativa basta la verifica dei file del negozio: in Steam, clic destro sul gioco > Proprietà > File installati > Verifica integrità dei file di gioco.

## Dopo un aggiornamento del gioco

Un aggiornamento rimette i file originali e i testi tornano in tedesco. Basta rilanciare Installa.bat o `./installa.sh`: lo script se ne accorge e rifà backup e installazione.

Se l'aggiornamento aggiunge testi nuovi, quelli restano in tedesco finché la traduzione non viene aggiornata.

## Cosa fa esattamente l'installer

Tocca due soli file dentro `ZeroParades_Data/StreamingAssets/aa`:

- `StandaloneWindows64/g5ibkj7vdwf2g67g_assets_all_*.bundle`: sostituisce i testi della tabella tedesca con quelli italiani. Il resto del file non cambia.
- `catalog.bin`: azzera i 4 byte del codice di controllo (CRC) di quel bundle. Senza questo passaggio il gioco rifiuta il file modificato.

Prima di scrivere copia entrambi gli originali in `Backup_Traduzione_IT`, nella cartella del gioco. Non modifica salvataggi, eseguibili né altri file, non si collega a Internet e non richiede diritti di amministratore se la cartella del gioco è scrivibile.

Comandi disponibili per chi preferisce il terminale:

```bash
python installa.py --verifica
```

```bash
python installa.py --ripristina
```

## Limiti noti

- Circa 1.200 voci della tabella non hanno un originale inglese (testi di sviluppo che il gioco non mostra) e restano in tedesco.
- Titoli di canzoni, album e cartoni animati sono lasciati in inglese, come nella versione ufficiale.
- La traduzione e l'installer sono stati generati in gran parte con un'intelligenza artificiale, sotto la guida dell'autore, e poi rivisti: controlli automatici su tutti i testi e rilettura a campione sull'inglese, non una rilettura integrale. Qualche errore o frase poco naturale è rimasta di sicuro.
- Provata sulla build 1.1.40707 del gioco. L'installazione è stata provata su Linux; lo script per Windows segue gli stessi passi.

## Scelte di traduzione

- La protagonista Hershel è una donna: la narrazione le dà del tu al femminile.
- Tra i personaggi si usa il tu, salvo dove russo e tedesco ufficiali segnalano un registro formale (per esempio con Bagman, il dottor Hugo, Haya, Reno).
- Nomi propri e criptonimi restano invariati (CASCADE, PSEUDOPOD, HOLOCENE, EMTERR...).
- Alcuni termini ricorrenti: Operant = Operativo/a, Crew = la Banda, Check = Prova, Thought = Pensiero, Pressure = Tensione, Luzian = luziano, Weeping Eye = Occhio Piangente, 'It' = il 'Quid'.
- La base è sempre il testo inglese; spagnolo, tedesco e russo ufficiali sono serviti solo a chiarire generi, registro e sfumature.

## Il file della traduzione

`traduzione_it.json` è un normale file di testo: sotto `testi` ogni riga ha la forma `"chiave del gioco": "testo italiano"`. Chi vuole correggere una frase può modificarla lì e rilanciare l'installer. Nei testi vanno lasciati identici all'originale i segnaposto `{0}`, i tag `<...>`, le parentesi quadre, gli asterischi dell'enfasi e gli a capo `\n`.

## Uso e condivisione

Puoi usare, copiare e ridistribuire liberamente questo pacchetto, anche modificato, purché gratuitamente e senza presentarlo come traduzione ufficiale.

## Note legali e ringraziamenti

ZERO PARADES e tutti i nomi, personaggi e contenuti collegati appartengono a ZA/UM. Questo progetto non è affiliato a ZA/UM né approvato da ZA/UM, e richiede una copia acquistata del gioco.

Il codice sorgente è tutto in questo pacchetto: sono file di testo leggibili, senza programmi compilati.

L'installer usa [UnityPy](https://github.com/K0lb3/UnityPy) per leggere e riscrivere il bundle. L'idea di sostituire la tabella tedesca viene dal progetto [zeroparades-translator](https://github.com/odoucet/zeroparades-translator).
