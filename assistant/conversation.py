"""Cœur de l’assistant : la conversation et la boucle des appels d’outil."""

from assistant import client, outils

CONSIGNES = """Tu es l’assistant de l’équipe support de Batifact, éditeur d’un logiciel de facturation pour artisans.
Réponds en français, brièvement, à partir des fiches de procédure, et cite la fiche utilisée.
Utilise lire_fiche pour consulter une fiche et ecrire_fiche pour enregistrer un brouillon de fiche.
Fiches disponibles : {fiches}"""


class LimiteAtteinte(Exception):
    """La question en cours s’arrête sur une limite fixée par l’équipe."""


def nouvelle_conversation(limites):
    """Renvoie la liste des messages d’une nouvelle conversation."""
    fiches = ", ".join(outils.lister_fiches(limites))
    # format remplace {fiches} dans CONSIGNES par la valeur donnée.
    return [{"role": "system", "content": CONSIGNES.format(fiches=fiches)}]


def joindre_fiche(nom, question, limites):
    """Renvoie la question suivie du contenu de la fiche jointe, ou lève AccesRefuse."""
    # À faire (étape 3).
    raise NotImplementedError("Étape 3 : joindre_fiche")


def poser(question, messages, service, modele, limites, confirmer, signaler):
    """Ajoute la question aux messages, envoie la conversation et garde l'historique.

    confirmer et signaler seront utilisés aux étapes 3 et 4.
    """
    messages.append({"role": "user", "content": question})

    try:
        reponse = client.envoyer(service, modele, messages)
    except client.ServiceIndisponible:
        # On retire la question pour garder un historique cohérent, puis on propage.
        # En d'autres mots : nettoyer l'historique pour qu'il reste cohérent puis on laisse
        # l'interface gérer l'affichage de l'erreur
        messages.pop()
        raise

    message = reponse.choices[0].message

    # À faire (étape 3) : si message.tool_calls, exécuter les outils jusqu'à la réponse finale.
    # À faire (étape 4) : gérer les limites (appels d'outil, taille de conversation).
    if getattr(message, "tool_calls", None):
        messages.append(message.model_dump(exclude_none=True))
        return "Fonctionnalité à venir (étape 3) : exécution des outils."

    messages.append({"role": "assistant", "content": message.content})
    return message.content
