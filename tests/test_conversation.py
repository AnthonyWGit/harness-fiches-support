
from assistant import conversation
from assistant.service_simule import ServiceSimule, texte


def refuser(nom):
    """Refuse tout écrasement de fiche."""
    return False


def ignorer(texte):
    """N'affiche rien (pas d'interface en test)."""
    pass


def test_renvoie_la_reponse_du_modele(limites):
    # Le service simulé renverra ce texte, puis s'arrêtera.
    service = ServiceSimule([texte("Bonjour, que puis-je faire ?")])

    messages = conversation.nouvelle_conversation(limites)
    reponse = conversation.poser(
        "Bonjour", messages, service, "simule", limites, refuser, ignorer
    )