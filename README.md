# ZERO PARADES: For Dead Spies - Italian translation / traduzione italiana

**[English](#english)** · **[Italiano](#italiano)**

Unofficial fan translation. Translation 1.0, installer 1.1 (11 November 2026).

---

## English

A complete fan-made Italian translation of the game's text: dialogue, journal, items, thoughts, menus and UI (72,470 strings).

It is **not official**. If an official Italian localisation is ever released, use that one.

The package **contains no game files**: only the Italian text and a small installer that writes it into your own copy. You need the original game installed.

### What changes in the game

The game cannot load additional languages, so Italian takes the place of **German**. English, Spanish, Russian and Chinese are untouched. Voice acting stays in English.

### Requirements

- ZERO PARADES: For Dead Spies installed (Steam or GOG), Windows build. On Linux and Steam Deck the same build running under Proton works.
- [Python 3](https://www.python.org/downloads/), version 3.9 or newer.
- The [UnityPy](https://github.com/K0lb3/UnityPy) Python library, used to read and rewrite the text file. You install it once with one command, shown below. The scripts in this package never connect to the internet and never download anything.
- About 30 MB free in the game folder for the backup.

### Installation

Close the game first.

#### Windows

1. Install Python from python.org. On the first screen of the setup tick **Add python.exe to PATH**.
2. Install UnityPy: open the Command Prompt (Windows key, type `cmd`, Enter) and type `py -m pip install UnityPy==1.25.4`. You only do this once.
3. Unzip this package anywhere.
4. Double-click **Installa.bat**.
5. If the script cannot find the game by itself it asks for the folder: the one that contains `ZeroParades.exe`. In Steam: right-click the game > Manage > Browse local files. You can paste the path or drag the folder into the window.

If the game is in `C:\Program Files` and you get a permission error, right-click Installa.bat > Run as administrator.

#### Linux and Steam Deck

In a terminal (on Steam Deck: Desktop mode > Konsole), inside the package folder. The first time, install UnityPy into a local `.venv` folder, without touching the rest of the system:

```bash
python3 -m venv .venv
```

```bash
.venv/bin/python -m pip install -r requisiti.txt
```

Then run the installer:

```bash
./installa.sh
```

To give the game folder by hand:

```bash
./installa.sh "/path/to/the/game/folder"
```

#### Switching to Italian

Start the game, open **Settings > Text Language** and choose **Deutsch**. From then on the text is in Italian and the menu entry is shown as **Italiano**.

### Uninstall

Double-click **Ripristina.bat** (Windows) or run `./ripristina.sh` (Linux). It puts the two original files back and deletes the backup.

The store's file check works too: in Steam, right-click the game > Properties > Installed Files > Verify integrity of game files.

### After a game update

An update restores the original files and the text goes back to German. Just run Installa.bat or `./installa.sh` again: the script notices and redoes backup and installation.

If the update adds new text, it stays in German until the translation is updated.

### What is in this package

Everything is plain text. There is no compiled code and nothing to build.

| File | What it is |
|---|---|
| `traduzione_it.json` | The translation: `"game string key": "Italian text"` under `testi`, plus a small `meta` block. |
| `installa.py` | The installer (Python, about 450 lines). |
| `Installa.bat`, `installa.sh` | Launchers for Windows and Linux/Steam Deck. They check that Python and UnityPy are present, then run `installa.py`. |
| `Ripristina.bat`, `ripristina.sh` | Launchers for `installa.py --ripristina` (uninstall). |
| `requisiti.txt` | The single dependency: `UnityPy==1.25.4`. |

### What the installer does, exactly

The game ships its localisation as Unity ScriptableObjects (one `LocalizationTable` per language) inside one Addressables bundle. `installa.py` changes exactly two files under `ZeroParades_Data/StreamingAssets/aa`:

1. `StandaloneWindows64/g5ibkj7vdwf2g67g_assets_all_*.bundle`: the values of the German table are replaced with the Italian strings that share the same key. Keys with no translation keep their current value. Every other object in the bundle is left byte-identical. After writing, the file is read back and compared before it replaces the original.
2. `catalog.bin`: Unity Addressables stores a CRC32 of each bundle's uncompressed data and refuses a bundle that does not match. The installer computes that CRC from your unmodified bundle, finds those 4 bytes next to the bundle name in the catalog and sets them to zero, which tells Unity to skip the check for that one bundle. This is a content checksum, not DRM or anti-piracy protection, and the game still requires a legitimate installed copy.

Before writing, both originals are copied to `Backup_Traduzione_IT` inside the game folder. Nothing else is touched: no executables, no saves, no registry, no files outside the game folder and this folder. The installer does not connect to the internet and does not need administrator rights if the game folder is writable.

Commands for those who prefer the terminal:

```bash
python installa.py --verifica
```

shows the state of the two files without changing anything.

```bash
python installa.py --ripristina
```

puts the original files back.

### Known limits

- About 1,200 entries of the table have no English source (development strings the game never shows) and stay in German.
- Song, album and cartoon titles are left in English.
- Most of the translation and most of the installer code were generated with AI under the author's direction, then reviewed: automatic checks on every string and sample reading against the English, not a full read-through. Some errors and unnatural sentences certainly remain.
- Tested with game build 1.1.40707. Installation was tested on Linux; the Windows launcher performs the same steps.

### The translation file

`traduzione_it.json` is an ordinary text file: under `testi` every line reads `"game key": "Italian text"`. To fix a sentence, edit it there and run the installer again. Placeholders `{0}`, tags `<...>`, square brackets, emphasis asterisks and `\n` line breaks must stay exactly as in the original.

### Use and sharing

You may use, copy and redistribute this package, modified or not, as long as it stays free of charge and is not presented as an official translation.

### Legal notes and credits

ZERO PARADES and all related names, characters and content belong to ZA/UM. This project is not affiliated with or endorsed by ZA/UM, and requires a purchased copy of the game.

The installer uses [UnityPy](https://github.com/K0lb3/UnityPy) to read and rewrite the bundle. The idea of replacing the German table comes from the [zeroparades-translator](https://github.com/odoucet/zeroparades-translator) project.

---

## Italiano

Traduzione italiana completa dei testi del gioco: dialoghi, diario, oggetti, pensieri, menu e interfaccia (72.470 testi).

È una traduzione **non ufficiale**, fatta da un appassionato. Se un giorno uscirà l'italiano ufficiale, usa quello.

Il pacchetto **non contiene file del gioco**: contiene solo i testi italiani e un programmino che li inserisce nella tua copia. Serve quindi il gioco originale installato.

### Cosa cambia nel gioco

Il gioco non permette di aggiungere una lingua nuova, quindi l'italiano prende il posto del **tedesco**. Inglese, spagnolo, russo e cinese restano come sono. Le voci parlate restano in inglese.

### Cosa serve

- ZERO PARADES: For Dead Spies installato (Steam o GOG), versione per Windows. Su Linux e Steam Deck va bene la stessa versione avviata con Proton.
- [Python 3](https://www.python.org/downloads/), versione 3.9 o successiva.
- La libreria Python [UnityPy](https://github.com/K0lb3/UnityPy), che serve a leggere e riscrivere il file dei testi. Si installa una volta sola con un comando, spiegato qui sotto. Gli script di questo pacchetto non si collegano a Internet e non scaricano nulla.
- Circa 30 MB liberi nella cartella del gioco per il backup.

### Installazione

Chiudi il gioco prima di cominciare.

#### Windows

1. Installa Python da python.org. Nella prima schermata dell'installazione spunta **Add python.exe to PATH**.
2. Installa UnityPy: apri il Prompt dei comandi (tasto Windows, scrivi `cmd`, Invio) e scrivi `py -m pip install UnityPy==1.25.4`. Va fatto una volta sola.
3. Scompatta questo pacchetto dove vuoi.
4. Fai doppio clic su **Installa.bat**.
5. Se lo script non trova il gioco da solo, ti chiede la cartella: è quella che contiene `ZeroParades.exe`. In Steam la apri con clic destro sul gioco > Gestisci > Sfoglia i file locali. Puoi incollare il percorso o trascinare la cartella nella finestra.

Se il gioco sta in `C:\Program Files` e compare un errore di permessi, fai clic destro su Installa.bat > Esegui come amministratore.

#### Linux e Steam Deck

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

#### Attivare l'italiano

Avvia il gioco, apri **Settings > Text Language** e scegli **Deutsch**. Da quel momento i testi sono in italiano e la voce del menu compare come **Italiano**.

### Disinstallazione

Doppio clic su **Ripristina.bat** (Windows) oppure `./ripristina.sh` (Linux). Rimette al loro posto i due file originali e cancella il backup.

In alternativa basta la verifica dei file del negozio: in Steam, clic destro sul gioco > Proprietà > File installati > Verifica integrità dei file di gioco.

### Dopo un aggiornamento del gioco

Un aggiornamento rimette i file originali e i testi tornano in tedesco. Basta rilanciare Installa.bat o `./installa.sh`: lo script se ne accorge e rifà backup e installazione.

Se l'aggiornamento aggiunge testi nuovi, quelli restano in tedesco finché la traduzione non viene aggiornata.

### Cosa c'è nel pacchetto

Sono tutti file di testo leggibili. Non c'è codice compilato e non c'è nulla da compilare.

| File | Cos'è |
|---|---|
| `traduzione_it.json` | La traduzione: `"chiave del gioco": "testo italiano"` sotto `testi`, più un piccolo blocco `meta`. |
| `installa.py` | L'installer (Python, circa 450 righe). |
| `Installa.bat`, `installa.sh` | Avvio per Windows e per Linux/Steam Deck. Controllano che ci siano Python e UnityPy, poi lanciano `installa.py`. |
| `Ripristina.bat`, `ripristina.sh` | Avvio di `installa.py --ripristina` (disinstallazione). |
| `requisiti.txt` | L'unica dipendenza: `UnityPy==1.25.4`. |

### Cosa fa esattamente l'installer

Tocca due soli file dentro `ZeroParades_Data/StreamingAssets/aa`:

- `StandaloneWindows64/g5ibkj7vdwf2g67g_assets_all_*.bundle`: sostituisce i testi della tabella tedesca con quelli italiani. Il resto del file non cambia.
- `catalog.bin`: azzera i 4 byte del codice di controllo (CRC) di quel bundle. Senza questo passaggio il gioco rifiuta il file modificato. È un controllo di integrità del contenuto, non una protezione anticopia.

Prima di scrivere copia entrambi gli originali in `Backup_Traduzione_IT`, nella cartella del gioco. Non modifica salvataggi, eseguibili né altri file, non si collega a Internet e non richiede diritti di amministratore se la cartella del gioco è scrivibile.

Comandi disponibili per chi preferisce il terminale:

```bash
python installa.py --verifica
```

```bash
python installa.py --ripristina
```

### Limiti noti

- Circa 1.200 voci della tabella non hanno un originale inglese (testi di sviluppo che il gioco non mostra) e restano in tedesco.
- Titoli di canzoni, album e cartoni animati sono lasciati in inglese, come nella versione ufficiale.
- La traduzione e l'installer sono stati generati in gran parte con un'intelligenza artificiale, sotto la guida dell'autore, e poi rivisti: controlli automatici su tutti i testi e rilettura a campione sull'inglese, non una rilettura integrale. Qualche errore o frase poco naturale è rimasta di sicuro.
- Provata sulla build 1.1.40707 del gioco. L'installazione è stata provata su Linux; lo script per Windows segue gli stessi passi.

### Scelte di traduzione

- La protagonista Hershel è una donna: la narrazione le dà del tu al femminile.
- Tra i personaggi si usa il tu, salvo dove russo e tedesco ufficiali segnalano un registro formale (per esempio con Bagman, il dottor Hugo, Haya, Reno).
- Nomi propri e criptonimi restano invariati (CASCADE, PSEUDOPOD, HOLOCENE, EMTERR...).
- Alcuni termini ricorrenti: Operant = Operativo/a, Crew = la Banda, Check = Prova, Thought = Pensiero, Pressure = Tensione, Luzian = luziano, Weeping Eye = Occhio Piangente, 'It' = il 'Quid'.
- La base è sempre il testo inglese; spagnolo, tedesco e russo ufficiali sono serviti solo a chiarire generi, registro e sfumature.

### Il file della traduzione

`traduzione_it.json` è un normale file di testo: sotto `testi` ogni riga ha la forma `"chiave del gioco": "testo italiano"`. Chi vuole correggere una frase può modificarla lì e rilanciare l'installer. Nei testi vanno lasciati identici all'originale i segnaposto `{0}`, i tag `<...>`, le parentesi quadre, gli asterischi dell'enfasi e gli a capo `\n`.

### Uso e condivisione

Puoi usare, copiare e ridistribuire liberamente questo pacchetto, anche modificato, purché gratuitamente e senza presentarlo come traduzione ufficiale.

### Note legali e ringraziamenti

ZERO PARADES e tutti i nomi, personaggi e contenuti collegati appartengono a ZA/UM. Questo progetto non è affiliato a ZA/UM né approvato da ZA/UM, e richiede una copia acquistata del gioco.

L'installer usa [UnityPy](https://github.com/K0lb3/UnityPy) per leggere e riscrivere il bundle. L'idea di sostituire la tabella tedesca viene dal progetto [zeroparades-translator](https://github.com/odoucet/zeroparades-translator).
