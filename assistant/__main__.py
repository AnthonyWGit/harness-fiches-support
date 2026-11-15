"""Point d’entrée : python -m assistant, ou python -m assistant --verifier."""

import sys

from assistant.interface import lancer

# sys.argv : mots de la ligne de commande ; sys.exit termine le programme avec le code renvoyé.
sys.exit(lancer(verifier="--verifier" in sys.argv[1:]))
