# Fiches support : consulter et rédiger les fiches depuis la ligne de commande

La responsable du support de Batifact a validé tes critères d’acceptation. Tu réalises un prototype d’assistant IA en ligne de commande qui répond aux questions de l’équipe à partir des fiches de procédure et rédige de nouvelles fiches, sans agir hors de leur dossier.

## Contenu du dépôt

| Fichier | Rôle |
| --- | --- |
| [`assistant/`](assistant/) | Code de départ : chaque `À faire (étape n)` indique ce qui reste à écrire |
| [`assistant/service_simule.py`](assistant/service_simule.py) | Service d’IA simulé, pour essayer et tester sans réseau ni quota : `SERVICE=simule` dans `.env` l’active ; ses questions spéciales sont listées en tête du fichier |
| [`limites.toml`](limites.toml) | Limites fixées par l’équipe |
| [`fiches/`](fiches/) | Fiches de procédure de l’équipe support |
| [`tests/`](tests/) | Tests pytest, dont un premier test fourni, qui réussit une fois l’étape 3 faite |
| [`docs/schema-cadre-technique.md`](docs/schema-cadre-technique.md) | Schéma du cadre technique retenu par l’équipe |
| [`docs/organisation-du-code.md`](docs/organisation-du-code.md) | Package `assistant`, imports et lancement avec `python -m` |
| [`docs/scenario-demonstration.md`](docs/scenario-demonstration.md) | Scénario de la démonstration du vendredi |
| [`.env.example`](.env.example) | Modèle de configuration du service d’IA |
| [`resoudre.py`](resoudre.py) | Rattraper une étape |

## Pour commencer

1. Forke ce dépôt, clone ton fork et ouvre ta demande de fusion (Pull Request) vers ta branche `rendu/<prenom>`, comme au brief précédent : [Fork et demande de fusion](https://github.com/SIMPLON-DIST-DEVIA-P1-199833/assistant-fiches-support/blob/main/docs/github-demande-de-fusion.md) et [Commandes Git](https://github.com/SIMPLON-DIST-DEVIA-P1-199833/assistant-fiches-support/blob/main/docs/git-commandes.md). Pour ce dépôt, les quatre listes de la demande de fusion sont :
   - **base repository :** `SIMPLON-DIST-DEVIA-P1-199833/harness-fiches-support` ;
   - **base :** `rendu/<prenom>`, ta branche ;
   - **head repository :** `<ton-compte>/harness-fiches-support` ;
   - **compare :** `main`.
2. Lis le [schéma du cadre technique](docs/schema-cadre-technique.md) et l’[organisation du code](docs/organisation-du-code.md), puis parcours le code de départ.
3. Termine chaque étape par un commit et un push.

## Limites fixées par l’équipe

Le modèle choisit quoi lire et quoi écrire, mais une fiche ou une question peut l’induire en erreur. C’est donc ton code Python qui applique ces limites, avec les valeurs de [`limites.toml`](limites.toml).

| Limite | Pourquoi | Au-delà |
| --- | --- | --- |
| Dossier `fiches/` | Le modèle ne doit lire ni `.env` ni le code | Lecture ou écriture refusée, avec un message |
| Extension `.md` | Les fiches sont en Markdown | Refusée, avec un message |
| 20 Ko par fiche | Une fiche fait environ 1 Ko ; au-delà, elle consomme du quota et encombre la conversation | Lecture ou écriture refusée, jamais tronquée : une procédure coupée perd des étapes |
| 30 s par appel au service | Le technicien est au téléphone avec un client | Question abandonnée avec un message, sans nouvelle tentative ; la conversation continue |
| 10 appels d’outil par question | Un modèle peut tourner en boucle, et chaque appel renvoie toute la conversation | Question arrêtée avec un message ; la conversation continue |
| 60 000 jetons de conversation | Chaque appel renvoie toute la conversation : elle coûte de plus en plus cher et finit par dépasser ce que le modèle accepte | La conversation repart de zéro, avec un message |

## Étapes

### 1. Accès

Installe l’environnement et les dépendances, configure ta clé, vérifie un appel au service, puis décris l’installation dans la section [Ton assistant](#ton-assistant).

**Résultat :** `python -m assistant --verifier` affiche la réponse du service ; sans clé, un message explique quoi faire.

Lance toujours l’assistant et les tests depuis la racine du dépôt, avec `python -m`. En cas de `ModuleNotFoundError`, voir l’[organisation du code](docs/organisation-du-code.md#erreurs-fréquentes).

<details>
<summary>Indice : environnement</summary>

Créer un environnement virtuel dans le dépôt, l’activer, puis installer les dépendances :

```sh
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Voir [Environnements virtuels et paquets](https://docs.python.org/fr/3/tutorial/venv.html).

</details>

<details>
<summary>Indice : clé</summary>

Copier `.env.example` en `.env` et y coller la clé. Avant le premier commit, vérifier que `git status` n’affiche pas `.env`.

Le code de départ charge `.env` avec [python-dotenv](https://pypi.org/project/python-dotenv/) : chaque ligne devient une variable d’environnement du programme. `os.getenv("LITELLM_API_KEY")` renvoie alors ta clé, ou `None` si la variable n’existe pas.

</details>

<details>
<summary>Indice : clé versionnée par erreur</summary>

Supprimer le fichier ne suffit pas : la clé reste dans l’historique. Prévenir le formateur, qui révoque la clé et en donne une nouvelle.

</details>

### 2. Conversation

L’assistant répond aux questions en gardant l’historique. Il signale une clé refusée ou un service qui ne répond pas, sans planter.

**Résultat :** une deuxième question qui renvoie à la première obtient une réponse cohérente. Avec `SERVICE=simule`, les questions `panne`, `lent` et `refus` produisent chacune un message.

<details>
<summary>Indice : historique</summary>

Le service ne garde aucune mémoire entre deux appels. À chaque question, tu lui renvoies toute la conversation : la liste `messages`, à laquelle tu ajoutes la question (`"role": "user"`) puis sa réponse (`"role": "assistant"`).

Voir [l’utilisation du SDK OpenAI avec LiteLLM](https://docs.litellm.ai/docs/proxy/user_keys).

</details>

<details>
<summary>Indice : erreurs du service</summary>

Le SDK lève une exception différente pour chaque panne : voir [Handling errors](https://github.com/openai/openai-python#handling-errors). Les transformer en `ServiceIndisponible` avec un message clair, puis afficher ce message dans l’interface. Le principe, sur un autre exemple :

```python
class SaisieInvalide(Exception):
    """La saisie ne permet pas de continuer."""


def lire_age(saisie):
    try:
        return int(saisie)
    except ValueError:
        # Un raise dans le except remplace l’exception par celle du projet.
        raise SaisieInvalide(f"« {saisie} » n’est pas un nombre : saisir l’âge en chiffres.")


try:
    age = lire_age(saisie)
except SaisieInvalide as erreur:  # erreur : l’exception levée
    print(f"Erreur : {erreur}")  # affiche son message
```

</details>

<details>
<summary>Indice : lire un traceback</summary>

Le lire de bas en haut : la dernière ligne donne l’exception, la ligne au-dessus l’endroit du code où elle s’est produite. Formuler une hypothèse, puis la vérifier avec un `print` ou en relançant avec une seule modification.

</details>

### 3. Lecture

L’utilisateur joint d’abord une fiche à sa question avec `/joindre`. Ensuite, le modèle lit lui-même une fiche grâce à l’outil `lire_fiche`. Dans [Ton assistant](#ton-assistant), compare les deux approches en quelques lignes.

**Résultat :** une question sur la TVA obtient une réponse tirée de la fiche, et l’interface signale la lecture. Toute lecture hors du dossier des fiches est refusée, et tes tests de lecture (fiche du dossier, `..`, chemin absolu) réussissent avec `python -m pytest`.

<details>
<summary>Indice : appel d’outil</summary>

Voir [Function calling](https://platform.openai.com/docs/guides/function-calling), onglet **Chat Completions**. Le trajet :

1. tu envoies la conversation avec la description des outils (`tools`) ;
2. le modèle répond par des `tool_calls` : nom de l’outil et arguments en JSON ;
3. ton code vérifie les arguments, puis exécute l’outil, ou le refuse ;
4. tu ajoutes la réponse du modèle, puis le résultat (`"role": "tool"`, avec le `tool_call_id`) ;
5. tu renvoies le tout, jusqu’à une réponse sans `tool_calls`.

</details>

<details>
<summary>Indice : signaler et confirmer</summary>

`poser` reçoit deux fonctions de l’interface en paramètres, sans parenthèses : `conversation.poser(…, confirmer, signaler)`. Elles s’appellent comme toute fonction, par exemple `signaler("Fiche lue.")`. Ainsi, `conversation.py` informe l’utilisateur sans dépendre de Rich, et les tests lui passent leurs propres fonctions.

</details>

<details>
<summary>Indice : rester dans le dossier</summary>

Comparer des chaînes de caractères ne suffit pas : `..`, un chemin absolu ou un lien symbolique en sortent. Voir [`Path.resolve()`](https://docs.python.org/fr/3/library/pathlib.html#pathlib.Path.resolve) et [`PurePath.is_relative_to()`](https://docs.python.org/fr/3/library/pathlib.html#pathlib.PurePath.is_relative_to).

</details>

<details>
<summary>Indice : refus et réponses invalides</summary>

Un refus n’arrête pas le programme : il est renvoyé au modèle comme résultat de l’outil, pour que celui-ci puisse répondre à l’utilisateur. Les arguments viennent du modèle : [`json.loads`](https://docs.python.org/fr/3/library/json.html#json.loads), qui lit une chaîne JSON comme `json.load` lit un fichier, peut échouer, une clé peut manquer, l’outil peut ne pas exister. Pour essayer : `SERVICE=simule` et les questions `invalide` et `inconnu`.

</details>

<details>
<summary>Indice : pytest</summary>

Voir [Get Started](https://docs.pytest.org/en/stable/getting-started.html), [pytest.raises](https://docs.pytest.org/en/stable/how-to/assert.html#assertions-about-expected-exceptions) et [tmp_path](https://docs.pytest.org/en/stable/how-to/tmp_path.html). La fixture `limites` de [`tests/conftest.py`](tests/conftest.py) fournit un dossier de fiches temporaire : tes tests ne modifient pas les vraies fiches.

</details>

### 4. Écriture

Le modèle crée des fiches dans le dossier prévu et demande confirmation avant d’en écraser une. Le programme explique chaque refus et chaque arrêt dû à une limite.

**Résultat :** une nouvelle fiche est créée sans confirmation. L’écrasement d’une fiche existante demande confirmation, et un refus la laisse intacte. La question `boucle` du service simulé s’arrête au nombre d’appels fixé, et la conversation continue. Tes tests de création et d’écrasement refusé réussissent.

<details>
<summary>Indice : confirmation</summary>

C’est ton code qui demande la confirmation, pas le modèle. Voir [`Confirm.ask`](https://rich.readthedocs.io/en/stable/prompt.html) de Rich.

</details>

<details>
<summary>Indice : limites</summary>

Compter les appels d’outil d’une même question. Pour la taille de la conversation, chaque réponse du service indique les jetons consommés dans `usage.total_tokens`.

</details>

### 5. Tests et démonstration

Complète tes tests avec le service simulé : conversation, appel d’outil, écriture par le modèle, arrêt au nombre d’appels, panne du service. Puis présente ton assistant à Nadia Ferrand, responsable du support, selon le [scénario de démonstration](docs/scenario-demonstration.md).

**Résultat :** avec ceux des étapes 3 et 4, tes tests couvrent la lecture, le refus hors dossier, l’écriture, la confirmation, la conversation, l’arrêt au nombre d’appels et la panne du service, et réussissent tous.

<details>
<summary>Indice : tester avec le service simulé</summary>

Passer au service la liste des réponses qu’il doit renvoyer, dans l’ordre :

```python
from assistant.service_simule import ServiceSimule, appel_outil, texte

service = ServiceSimule([
    appel_outil("lire_fiche", nom="modifier-taux-tva.md"),
    texte("Voir la fiche modifier-taux-tva.md."),
])
```

`service.requetes` garde ensuite les messages reçus à chaque appel.

</details>

**Bonus :** afficher les différences avant un écrasement ([`difflib`](https://docs.python.org/fr/3/library/difflib.html)).

## Rattraper une étape

Si tu restes bloqué·e et que tu veux commencer l’étape suivante, demande le jeton d’accès au formateur, puis lance `python resoudre.py`, environnement du projet activé. Le script contrôle une copie de ton code, indique l’étape en cours et ce qui y manque, puis demande confirmation. Pour choisir l’étape toi-même : `python resoudre.py 3`.

Ton travail est d’abord enregistré dans un commit, puis un second commit corrige les fichiers de code de l’étape avec la version de référence. Tes commits restent dans ton historique ; ton README et les fichiers que tu as ajoutés sont conservés.

## Ton assistant

> À compléter au fil des étapes : installation, configuration de la clé (sans sa valeur), lancement, comportement aux limites, et comparaison de l’étape 3.
