#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Traduzione italiana amatoriale di ZERO PARADES: For Dead Spies - installer.

Uso:
    python installa.py                     installa (cerca il gioco da solo o lo chiede)
    python installa.py "C:\\percorso\\gioco"  installa nella cartella indicata
    python installa.py --ripristina        rimette i file originali dal backup
    python installa.py --verifica          dice solo in che stato sono i file

Non si collega a Internet e non scarica nulla.
Cosa fa: scrive i testi italiani nella tabella della lingua tedesca dentro
g5ibkj7vdwf2g67g_assets_all_*.bundle e azzera il CRC di quel bundle in catalog.bin,
altrimenti il gioco rifiuta il file modificato. Prima salva gli originali in
Backup_Traduzione_IT dentro la cartella del gioco. Non contiene file del gioco.
"""
import argparse
import base64
import io
import json
import os
import re
import shutil
import struct
import sys
import time
import zlib
from pathlib import Path

VERSIONE = "1.1"
QUI = Path(__file__).resolve().parent
FILE_TRADUZIONE = QUI / "traduzione_it.json"
DATI = "ZeroParades_Data"
AA = Path(DATI) / "StreamingAssets" / "aa"
BUNDLE_GLOB = "g5ibkj7vdwf2g67g_assets_all_*.bundle"
TABELLA = "Assets/FELDRuntime/Scriptables/Main/Localization/de/deLocalizationTable.asset"
BACKUP = "Backup_Traduzione_IT"
STATO = "stato.json"


class Errore(Exception):
    pass


def chiedi_invio():
    """Tiene aperta la finestra quando lo script e' stato avviato con doppio clic."""
    if os.environ.get("ZP_IT_NO_PAUSA") or not sys.stdin or not sys.stdin.isatty():
        return
    try:
        input("\nPremi Invio per chiudere...")
    except EOFError:
        pass


# --------------------------------------------------------------- ricerca del gioco
def e_cartella_gioco(p):
    return p is not None and (Path(p) / AA).is_dir()


def librerie_steam():
    casa = Path.home()
    radici = [
        Path(os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)")) / "Steam",
        Path(os.environ.get("ProgramFiles", r"C:\Program Files")) / "Steam",
        casa / ".steam" / "steam",
        casa / ".steam" / "root",
        casa / ".local" / "share" / "Steam",
        casa / ".var" / "app" / "com.valvesoftware.Steam" / ".local" / "share" / "Steam",
        casa / "Library" / "Application Support" / "Steam",
    ]
    viste = []
    for r in radici:
        vdf = r / "steamapps" / "libraryfolders.vdf"
        trovate = [r]
        try:
            testo = vdf.read_text(encoding="utf-8", errors="replace")
            trovate += [Path(m.replace("\\\\", "\\")) for m in re.findall(r'"path"\s+"([^"]+)"', testo)]
        except OSError:
            pass
        for t in trovate:
            if t not in viste:
                viste.append(t)
    return viste


def cerca_gioco(indicata):
    if indicata:
        p = Path(indicata.strip().strip('"').strip("'")).expanduser()
        # accetta anche un percorso dentro la cartella del gioco (es. ZeroParades_Data)
        for c in [p] + list(p.parents)[:4]:
            if e_cartella_gioco(c):
                return c
        raise Errore(f"In '{p}' non trovo la cartella {AA}. Indica la cartella che contiene ZeroParades.exe.")
    for base in (QUI, Path.cwd()):
        for c in [base] + list(base.parents)[:3]:
            if e_cartella_gioco(c):
                return c
    candidati = []
    for lib in librerie_steam():
        comuni = lib / "steamapps" / "common"
        try:
            candidati += [d for d in comuni.iterdir() if e_cartella_gioco(d)]
        except OSError:
            pass
    for radice in (Path(r"C:\GOG Games"), Path(r"C:\Program Files (x86)\GOG Galaxy\Games"), Path.home() / "GOG Games", Path.home() / "Games"):
        try:
            candidati += [d for d in radice.iterdir() if e_cartella_gioco(d)]
        except OSError:
            pass
    if len(candidati) == 1:
        return candidati[0]
    if len(candidati) > 1:
        print("Ho trovato piu' di una copia del gioco:")
        for i, c in enumerate(candidati, 1):
            print(f"  {i}) {c}")
        scelta = input("Numero della copia da tradurre: ").strip()
        try:
            return candidati[int(scelta) - 1]
        except (ValueError, IndexError):
            raise Errore("Scelta non valida.")
    print("Non ho trovato il gioco da solo.")
    print("Scrivi (o trascina qui) la cartella del gioco, quella che contiene ZeroParades.exe:")
    try:
        risposta = input("> ")
    except EOFError:
        risposta = ""
    if not risposta.strip():
        raise Errore("Nessuna cartella indicata.")
    return cerca_gioco(risposta)


# ------------------------------------------------------------------ CRC del bundle
def _cstr(f):
    b = b""
    while True:
        c = f.read(1)
        if c in (b"\0", b""):
            return b.decode("utf-8", "replace")
        b += c


def crc_bundle(percorso):
    """CRC32 dei dati non compressi di un file UnityFS: e' il valore che Addressables
    tiene in catalogo e confronta al caricamento."""
    import lz4.block

    with open(percorso, "rb") as f:
        if _cstr(f) != "UnityFS":
            raise Errore(f"{Path(percorso).name} non e' un bundle UnityFS.")
        versione = struct.unpack(">I", f.read(4))[0]
        _cstr(f)
        _cstr(f)
        dimensione, c_info, u_info, flag = struct.unpack(">qIII", f.read(20))
        if versione >= 7:
            f.seek((f.tell() + 15) // 16 * 16)
        if flag & 0x80:
            pos = f.tell()
            f.seek(dimensione - c_info)
            info = f.read(c_info)
            f.seek(pos)
        else:
            info = f.read(c_info)
        comp = flag & 0x3F
        if comp in (2, 3):
            info = lz4.block.decompress(info, uncompressed_size=u_info)
        elif comp != 0:
            raise Errore(f"Compressione del bundle non gestita (tipo {comp}).")
        b = io.BytesIO(info)
        b.read(16)
        n = struct.unpack(">i", b.read(4))[0]
        blocchi = [struct.unpack(">IIH", b.read(10)) for _ in range(n)]
        if flag & 0x200:
            f.seek((f.tell() + 15) // 16 * 16)
        crc = 0
        for u, c, fl in blocchi:
            d = f.read(c)
            k = fl & 0x3F
            if k in (2, 3):
                d = lz4.block.decompress(d, uncompressed_size=u)
            elif k != 0:
                raise Errore(f"Compressione dei blocchi non gestita (tipo {k}).")
            crc = zlib.crc32(d, crc)
    return crc & 0xFFFFFFFF


# ------------------------------------------------------------------------ catalogo
def trova_crc_bin(dati, nome_bundle, crc):
    """Posizioni in catalog.bin dei 4 byte del CRC, vicino al nome del bundle."""
    ago = struct.pack("<I", crc)
    nomi = [m.start() for m in re.finditer(re.escape(nome_bundle.encode("ascii")), dati)]
    pos = [m.start() for m in re.finditer(re.escape(ago), dati)]
    vicine = [p for p in pos if any(abs(p - n) <= 4096 for n in nomi)]
    return vicine


def azzera_crc_json(percorso, nome_bundle):
    """Vecchie versioni del gioco: catalog.json con i CRC dentro m_ExtraDataString
    (base64, testo UTF-16LE). Azzera tutti i campi m_Crc mantenendo le lunghezze."""
    cat = json.loads(Path(percorso).read_text(encoding="utf-8"))
    extra = base64.b64decode(cat["m_ExtraDataString"])
    campo = '"m_Crc":'.encode("utf-16-le")
    schema = re.compile(re.escape(campo) + b"(?:[0-9]\x00)+")

    def zero(m):
        cifre = (len(m.group(0)) - len(campo)) // 2
        return campo + " ".encode("utf-16-le") * (cifre - 1) + "0".encode("utf-16-le")

    nuovo, n = schema.subn(zero, extra)
    if n == 0:
        return False
    cat["m_ExtraDataString"] = base64.b64encode(nuovo).decode("ascii")
    Path(percorso).write_text(json.dumps(cat, separators=(",", ":")), encoding="utf-8")
    return True


# -------------------------------------------------------------------------- lavoro
def trova_file(gioco):
    aa = gioco / AA
    cartelle = [d for d in aa.iterdir() if d.is_dir()]
    bundle = [b for d in cartelle for b in d.glob(BUNDLE_GLOB)]
    if len(bundle) != 1:
        raise Errore(
            f"Mi aspettavo un solo file {BUNDLE_GLOB} in {aa}, ne ho trovati {len(bundle)}. "
            "Forse questa versione del gioco e' organizzata in modo diverso."
        )
    catalogo = aa / "catalog.bin"
    if not catalogo.exists():
        catalogo = aa / "catalog.json"
    if not catalogo.exists():
        raise Errore(f"Non trovo catalog.bin (ne' catalog.json) in {aa}.")
    return bundle[0], catalogo


def leggi_stato(gioco):
    p = gioco / BACKUP / STATO
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def carica_traduzione():
    if not FILE_TRADUZIONE.exists():
        raise Errore(f"Manca {FILE_TRADUZIONE.name}: deve stare accanto a installa.py.")
    d = json.loads(FILE_TRADUZIONE.read_text(encoding="utf-8"))
    testi = d.get("testi")
    if not isinstance(testi, dict) or not testi:
        raise Errore(f"{FILE_TRADUZIONE.name} non ha il formato atteso.")
    return d.get("meta", {}), testi


def scrivi_tabella(bundle, testi):
    import UnityPy

    env = UnityPy.load(str(bundle))
    if TABELLA not in env.container:
        raise Errore("Nel bundle non c'e' la tabella della lingua tedesca: versione del gioco non supportata.")
    tab = env.container[TABELLA].read()
    chiavi = list(tab.m_data.m_keys)
    vecchi = list(tab.m_data.m_values)
    nuovi = [testi.get(k, v) for k, v in zip(chiavi, vecchi)]
    coperte = sum(1 for k in chiavi if k in testi)
    tab.m_data.m_values = nuovi
    tab.save()
    dati = env.file.save(packer="lz4")
    tmp = bundle.with_name(bundle.name + ".tmp")
    tmp.write_bytes(dati)
    # rilettura di controllo prima di sostituire il file del gioco
    controllo = UnityPy.load(str(tmp)).container[TABELLA].read()
    if list(controllo.m_data.m_keys) != chiavi or list(controllo.m_data.m_values) != nuovi:
        tmp.unlink()
        raise Errore("Il bundle riscritto non supera la rilettura di controllo: non ho toccato il gioco.")
    os.replace(tmp, bundle)
    return len(chiavi), coperte, len(set(testi) - set(chiavi))


def stato_file(gioco, bundle, catalogo):
    """Ritorna (situazione, crc, posizioni) con situazione in:
    'originale'  il CRC del bundle e' in catalogo: file non modificati
    'tradotto'   installato da questo script (c'e' stato.json coerente)
    'ignoto'     bundle modificato da altro, catalogo non riconosciuto"""
    crc = crc_bundle(bundle)
    stato = leggi_stato(gioco)
    if catalogo.suffix == ".bin":
        pos = trova_crc_bin(catalogo.read_bytes(), bundle.name, crc)
        if len(pos) == 1:
            return "originale", crc, pos
        if len(pos) > 1:
            raise Errore("Ho trovato il CRC del bundle in piu' punti del catalogo: preferisco non toccare nulla.")
    else:
        # catalog.json: non si puo' riconoscere il singolo bundle, ci si affida a stato.json
        if not stato:
            return "originale", crc, []
    if stato and stato.get("bundle") == bundle.name:
        return "tradotto", crc, []
    return "ignoto", crc, []


def installa(gioco, forza=False):
    bundle, catalogo = trova_file(gioco)
    meta, testi = carica_traduzione()
    print(f"Gioco:      {gioco}")
    print(f"Bundle:     {bundle.name}")
    print(f"Traduzione: versione {meta.get('versione', '?')} del {meta.get('data', '?')}, {len(testi)} testi")
    print("Controllo i file del gioco (qualche secondo)...")
    situazione, crc, pos = stato_file(gioco, bundle, catalogo)
    cartella_bk = gioco / BACKUP

    if situazione == "ignoto" and not forza:
        raise Errore(
            "Il bundle dei testi non corrisponde al catalogo del gioco: sembra gia' modificato da un altro "
            "strumento o da una vecchia installazione.\n"
            "Ripristina i file originali (Steam: Proprieta' > File installati > Verifica integrita' dei file; "
            "GOG Galaxy: Gestisci installazione > Verifica/Ripara) e rilancia l'installer.\n"
            "Se sai che il catalogo e' gia' stato sistemato, puoi procedere lo stesso con --forza "
            "(in quel caso non verra' fatto alcun backup)."
        )

    if situazione == "originale":
        if cartella_bk.exists():
            vecchio = gioco / f"{BACKUP}_vecchio_{time.strftime('%Y%m%d_%H%M%S')}"
            cartella_bk.rename(vecchio)
            print(f"Il gioco e' stato aggiornato o riparato: il vecchio backup e' ora in {vecchio.name}")
        cartella_bk.mkdir()
        shutil.copy2(bundle, cartella_bk / bundle.name)
        shutil.copy2(catalogo, cartella_bk / catalogo.name)
        print(f"Backup degli originali in {cartella_bk}")
    elif situazione == "tradotto":
        print("La traduzione e' gia' installata: aggiorno i testi (backup e catalogo restano come sono).")
    else:
        print("ATTENZIONE: procedo con --forza, senza backup e senza toccare il catalogo.")

    print("Scrivo i testi italiani nel bundle (puo' volerci un minuto)...")
    totale, coperte, estranee = scrivi_tabella(bundle, testi)

    if situazione == "originale":
        if catalogo.suffix == ".bin":
            dati = bytearray(catalogo.read_bytes())
            dati[pos[0]:pos[0] + 4] = b"\0\0\0\0"
            catalogo.write_bytes(bytes(dati))
        else:
            if not azzera_crc_json(catalogo, bundle.name):
                print("ATTENZIONE: nel catalog.json non ho trovato campi m_Crc da azzerare.")
        (cartella_bk / STATO).write_text(
            json.dumps(
                {
                    "bundle": bundle.name,
                    "catalogo": catalogo.name,
                    "crc_originale": crc,
                    "posizione_crc": pos[0] if pos else None,
                    "versione_traduzione": meta.get("versione"),
                    "installato": time.strftime("%Y-%m-%d %H:%M:%S"),
                },
                indent=1,
            ),
            encoding="utf-8",
        )
        print("Catalogo aggiornato: il gioco accettera' il bundle modificato.")
    elif situazione == "tradotto":
        st = leggi_stato(gioco) or {}
        st["versione_traduzione"] = meta.get("versione")
        st["aggiornato"] = time.strftime("%Y-%m-%d %H:%M:%S")
        (cartella_bk / STATO).write_text(json.dumps(st, indent=1), encoding="utf-8")

    print()
    print(f"Fatto. Testi italiani scritti: {coperte} su {totale} voci della tabella.")
    if totale - coperte:
        print(f"  {totale - coperte} voci non hanno traduzione e restano in tedesco (testi non usati dal gioco")
        print("  o aggiunti da una versione piu' recente di questa traduzione).")
    if estranee:
        print(f"  {estranee} testi della traduzione non esistono in questa versione del gioco e sono stati ignorati.")
    print()
    print("Nel gioco: Settings > Text Language > scegli 'Deutsch'.")
    print("Da quel momento la voce comparira' come 'Italiano'.")


def ripristina(gioco):
    bundle, catalogo = trova_file(gioco)
    cartella_bk = gioco / BACKUP
    stato = leggi_stato(gioco)
    if not stato or not (cartella_bk / stato.get("bundle", "")).is_file():
        raise Errore(
            f"Non trovo un backup valido in {cartella_bk}.\n"
            "Per tornare ai file originali usa la verifica dei file di Steam o di GOG Galaxy."
        )
    if stato["bundle"] != bundle.name:
        raise Errore(
            "Il backup appartiene a un'altra versione del gioco (il gioco e' stato aggiornato): non lo ripristino.\n"
            "Se i testi sono tornati in tedesco non devi fare nulla; altrimenti usa la verifica dei file di Steam/GOG."
        )
    shutil.copy2(cartella_bk / stato["bundle"], bundle)
    bk_cat = cartella_bk / stato.get("catalogo", catalogo.name)
    if bk_cat.is_file():
        shutil.copy2(bk_cat, catalogo)
    shutil.rmtree(cartella_bk)
    print("File originali ripristinati e backup rimosso. Il tedesco e' tornato al suo posto.")


def verifica(gioco):
    bundle, catalogo = trova_file(gioco)
    situazione, crc, _ = stato_file(gioco, bundle, catalogo)
    print(f"Gioco:   {gioco}")
    print(f"Bundle:  {bundle.name}  (CRC {crc:08x})")
    testo = {
        "originale": "file originali, traduzione non installata",
        "tradotto": "traduzione italiana installata",
        "ignoto": "bundle modificato da un altro strumento o stato non riconosciuto",
    }[situazione]
    print(f"Stato:   {testo}")
    st = leggi_stato(gioco)
    if st:
        print(f"Backup:  presente (installato il {st.get('installato', '?')}, traduzione {st.get('versione_traduzione', '?')})")


def main():
    ap = argparse.ArgumentParser(description="Traduzione italiana amatoriale di ZERO PARADES: For Dead Spies")
    ap.add_argument("cartella", nargs="?", help="cartella del gioco (quella con ZeroParades.exe)")
    ap.add_argument("--ripristina", action="store_true", help="rimette i file originali dal backup")
    ap.add_argument("--verifica", action="store_true", help="mostra lo stato dei file senza modificare nulla")
    ap.add_argument("--forza", action="store_true", help="installa anche se il bundle risulta gia' modificato")
    args = ap.parse_args()
    print(f"ZERO PARADES - traduzione italiana amatoriale, installer {VERSIONE}\n")
    try:
        try:
            import UnityPy  # noqa: F401
            import lz4.block  # noqa: F401
        except ImportError:
            raise Errore(
                "Manca la libreria UnityPy. Installala una volta sola con:\n"
                "    Windows:  py -m pip install UnityPy==1.25.4\n"
                "    Linux:    python3 -m venv .venv && .venv/bin/python -m pip install -r requisiti.txt\n"
                "poi rilancia l'installer. I passaggi sono spiegati in LEGGIMI.md."
            )
        gioco = cerca_gioco(args.cartella)
        if args.verifica:
            verifica(gioco)
        elif args.ripristina:
            ripristina(gioco)
        else:
            installa(gioco, forza=args.forza)
        esito = 0
    except Errore as e:
        print(f"\nERRORE: {e}")
        esito = 1
    except PermissionError as e:
        print(f"\nERRORE: non ho i permessi per scrivere ({e}).")
        print("Chiudi il gioco e riprova; su Windows, se il gioco e' in 'Program Files', avvia come amministratore.")
        esito = 1
    chiedi_invio()
    return esito


if __name__ == "__main__":
    sys.exit(main())
