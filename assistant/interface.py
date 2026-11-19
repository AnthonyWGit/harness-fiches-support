"""Interface en ligne de commande de l’assistant."""

from rich.console import Console
from rich.markdown import Markdown
from rich.prompt import Prompt
from assistant import client, conversation, outils
from assistant.configuration import ConfigurationInvalide, charger_configuration, charger_limites

AIDE = """Pose ta question, puis valide avec Entrée.
/joindre <fiche.md> <question> : joindre une fiche à ta question
/nouvelle : repartir d’une conversation vide
/quitter : quitter"""

console = Console()

def confirmer(nom):
    """Demande à l’utilisateur s’il accepte d’écraser la fiche."""
    # À faire (étape 4).
    signaler("Ecraser la fiche ? [y] [n]")
    user_input = input()
    if user_input == "y":
        return True
    elif user_input == "n":
        return False
    else:
        raise outils.AccesRefuse("Mauvaise commande : répondre par y ou n")


def signaler(texte):
    """Affiche une opération ou un refus, sans l’enregistrer dans la conversation."""
    console.print(f"[italic]{texte}[/italic]")


def lancer(verifier=False):
    """Démarre l’assistant et renvoie le code de sortie du programme."""
    try:
        configuration = charger_configuration()
        limites = charger_limites()
        service = client.creer_client(configuration, limites)
    except ConfigurationInvalide as erreur:  # erreur : l’exception levée ; l’afficher donne son message
        console.print(f"Erreur : {erreur}")
        return 1
    if verifier:
        console.print(client.verifier_acces(service, configuration["modele"]))
        return 0

    messages = conversation.nouvelle_conversation(limites)
    console.print(f"Assistant des fiches support, modèle {configuration['modele']}.\n{AIDE}")
    while True:
        try:
            saisie = Prompt.ask("\nToi").strip()
        except (EOFError, KeyboardInterrupt):  # l’une ou l’autre : Ctrl+D ou Ctrl+C
            return 0
        if saisie == "/quitter":
            return 0
        if saisie == "/nouvelle":
            messages = conversation.nouvelle_conversation(limites)
            signaler("Nouvelle conversation.")
            continue
        if not saisie:
            continue
        question = saisie
        # Split() coupe sur les espaces
        parties = saisie.split(maxsplit=2)  # /joindre plus nom-de-fiche
        if parties and parties[0] == "/joindre":
            if len(parties) < 3:
                signaler("Usage : /joindre <fiche.md> <question>")
                continue
            nom_fiche = parties[1]
            question_utilisateur = parties[2]
            try:
                question = conversation.joindre_fiche(nom_fiche, question_utilisateur, limites)
            except outils.AccesRefuse as erreur:
                signaler(str(erreur))
                continue
        # À faire (étape 2) : afficher les erreurs du service sans quitter.
        signaler("Le service réfléchit…")
        # try/catch pour ne pas que l'app plante
        # Utile pour helpdesk pour avoir de soucis pendant intervention
        try:
            reponse = conversation.poser(
                question, messages, service, configuration["modele"], limites, confirmer, signaler
            )
        except client.ServiceIndisponible as erreur:
            console.print(f"[red]Erreur : {erreur}[/red]")
            continue
        console.print(Markdown(reponse))