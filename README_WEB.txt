SKYJUMP - VERSIONE WEB (PYGBAG)
===============================

Questa versione mantiene il gioco Python/Pygame e aggiunge il ciclo asincrono
richiesto per provare la compilazione con Pygbag. Usa pygame-ce.

PROVA LOCALE (Windows / PowerShell)
----------------------------------
Apri il terminale nella cartella del progetto e lancia:

    py -3.13 -m venv .venv313
    .\.venv313\Scripts\Activate.ps1
    python -m pip install --upgrade pip
    python -m pip install pygame-ce pygbag
    python -m pygbag .

Pygbag dovrebbe avviare un server locale. Apri l'indirizzo che mostra nel
terminale (spesso http://localhost:8000). Non chiudere il terminale mentre provi.

PUBBLICAZIONE SU GITHUB PAGES
-----------------------------
1. Crea un repository pubblico su GitHub, per esempio SkyJump.
2. Estrai il contenuto di questo ZIP e carica TUTTI i file, inclusa la cartella
   nascosta .github/workflows/deploy.yml, nel ramo main del repository.
3. Su GitHub, apri Settings > Pages.
4. In "Build and deployment", seleziona "GitHub Actions" come source.
5. Apri la scheda Actions e attendi che "Build and deploy SkyJump to GitHub Pages"
   finisca con esito verde.
6. L'indirizzo pubblico sarà simile a https://TUONOME.github.io/NOME-REPOSITORY/

NOTE IMPORTANTI
----------------
- La pubblicazione richiede un account GitHub.
- Il workflow tenta di compilare automaticamente il gioco. Se il build fallisce,
  apri Actions, seleziona l'esecuzione rossa e condividi qui il messaggio d'errore.
- Il codice originale usa input mouse; i browser mobili spesso li traducono in
  eventi pointer/mouse, ma il controllo touch va testato sul telefono.
- Il layout attuale ha dimensioni fisse 480x800. Può essere necessario rifinire
  scaling e controlli touch per alcuni dispositivi.
