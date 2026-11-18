"""Outils proposés au modèle : lire et écrire une fiche, dans les limites fixées."""
import json
from pathlib import Path

DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "lire_fiche",
            "description": "Lit une fiche de procédure et renvoie son contenu Markdown.",
            "parameters": {
                "type": "object",
                "properties": {"nom": {"type": "string", "description": "Nom du fichier, par exemple modifier-taux-tva.md"}},
                "required": ["nom"],
            },
        },
    },
    # À faire (étape 4) : décrire l’outil ecrire_fiche.
]


class AccesRefuse(Exception):
    """Une limite fixée par l’équipe interdit l’opération demandée."""


def lister_fiches(limites):
    """Renvoie les noms des fiches du dossier, triés."""
    # Comme une compréhension de liste, sans crochets : sorted reçoit directement chaque nom.
    return sorted(chemin.name for chemin in Path(limites["dossier_fiches"]).glob("*" + limites["extension"]))


def chemin_autorise(nom, limites):
    """Renvoie le chemin de la fiche si elle reste dans le dossier des fiches, sinon lève AccesRefuse."""
    if not isinstance(nom, str) or not nom.strip():
        raise AccesRefuse("Nom de fiche invalide.")
    chemin = Path(nom)
    #Chemin absolu = à la racine du systeme donc hors du dossier de travail
    # .. renvoie au dossier parent donc même remarque
    if chemin.is_absolute() or ".." in chemin.parts:
        raise AccesRefuse("Accès refusé : chemin hors du dossier des fiches.")
    #vérifier l'extension
    if chemin.suffix != limites["extension"]:
        raise AccesRefuse(
            f"Accès refusé : seule l'extension {limites['extension']} est autorisée."
        )
    dossier = Path(limites["dossier_fiches"]).resolve()
    cible = (dossier / chemin).resolve()
    if not cible.is_relative_to(dossier):
        raise AccesRefuse("Accès refusé : chemin hors du dossier des fiches.")
    return cible


def lire_fiche(nom, limites):
    """Renvoie le contenu de la fiche, ou lève AccesRefuse."""
    # À faire (étape 3) : contrôler le chemin et la taille, puis lire la fiche.
    chemin = chemin_autorise(nom,limites)
    with open(chemin, "r", encoding="utf-8") as fiche:
        return fiche.read()

def ecrire_fiche(nom, contenu, limites, confirmer):
    """Enregistre la fiche ; confirmer(nom) décide d’un écrasement. Lève AccesRefuse sinon."""
    # À faire (étape 4) : contrôler le chemin et la taille, demander confirmation avant d’écraser.
    raise NotImplementedError("Étape 4 : ecrire_fiche")


def executer(appel, limites, confirmer):
    """Exécute un appel d’outil du modèle et renvoie le texte de son résultat, ou lève AccesRefuse."""
    # À faire (étape 3) : lire les arguments JSON de appel.function.arguments,
    # puis lancer l’outil nommé appel.function.name ; tout appel invalide est refusé. 
    try:
        arguments = json.loads(appel.function.arguments)
    except (json.JSONDecodeError, TypeError):
        raise AccesRefuse("Arguments invalides pour l'outil.")
    nom = appel.function.name
    if nom == "lire_fiche":
        nom = arguments.get("nom")
        if not nom :
            raise AccesRefuse("Argument 'nom' manquant pour lire fiche")
        return lire_fiche(arguments.get("nom"), limites)

    # if appel.function.name == "ecrire_fiche":
    #     user_input = input()
    #     ecrire_fiche(appel,user_input,limites)

