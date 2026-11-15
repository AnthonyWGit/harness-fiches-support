# Organisation du code Python

Comment les fichiers de `assistant/` se trouvent entre eux, et comment lancer l’assistant sans erreur d’import.

## Ton projet est un package

Un module est un fichier `.py` ; un package est un dossier de modules. `assistant/` est un package, écrit par l’équipe plutôt qu’installé avec `pip` :

```text
harness-fiches-support/        ← racine du dépôt : tout se lance d’ici
├── assistant/
│   ├── __init__.py            fait de assistant/ un package
│   ├── __main__.py            ce que lance python -m assistant
│   ├── interface.py           échanges dans le terminal
│   ├── conversation.py        boucle de conversation avec le service
│   ├── outils.py              lecture et écriture des fiches
│   ├── client.py              connexion au service d’IA
│   ├── configuration.py       lecture de .env et limites.toml
│   └── service_simule.py      service d’IA simulé pour les tests
├── tests/
└── pyproject.toml
```

## Importer un fichier du projet

Les formes d’`import` sont celles que tu connais déjà :

```python
import json                              # un module
from math import sqrt                    # une fonction d’un module
from babel.dates import format_date      # une fonction du module dates, dans le package babel
```

Ton package s’importe comme `babel` : le package, un point, le module.

```python
from assistant.outils import lire_fiche  # la fonction lire_fiche du module outils, dans le package assistant
from assistant import client, outils     # deux modules du package assistant
```

Ce nom complet s’écrit toujours, depuis n’importe quel fichier du projet, tests compris.

## `__init__.py`

Sa présence fait de `assistant/` un package ordinaire. Le fichier est vide : il n’a rien d’autre à faire. Ne pas le supprimer.

## `__main__.py` et `python -m`

`-m` signifie *module* : `python -m venv .venv` exécute le module `venv` de Python comme un programme. `python -m assistant` fait de même avec ton package : Python exécute son fichier `__main__.py`, qui appelle `lancer()` dans `interface.py`.

## Lancer depuis la racine du dépôt

Python cherche `assistant` à partir du dossier d’où tu lances la commande. Se placer à la racine du dépôt, environnement virtuel activé :

```sh
python -m assistant
python -m assistant --verifier
python -m pytest
```

Ne pas lancer un fichier du package directement, comme `python assistant/interface.py` : Python cherche alors `assistant` dans le dossier `assistant/` lui-même, et ne le trouve pas.

pytest trouve le package grâce à `pythonpath = ["."]` dans `pyproject.toml`.

## Erreurs fréquentes

| Message | Cause | Correction |
| --- | --- | --- |
| `No module named assistant` ou `ModuleNotFoundError: No module named 'assistant'` | Lancé hors de la racine, ou fichier lancé directement | Revenir à la racine et utiliser `python -m assistant` |
| `ModuleNotFoundError: No module named 'rich'` (ou `'openai'`, `'dotenv'`) | Environnement virtuel non activé, ou dépendances non installées | `source .venv/bin/activate`, puis `pip install -r requirements.txt` |
