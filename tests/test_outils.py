import pytest

from assistant.outils import AccesRefuse, lire_fiche


def test_refuse_une_fiche_hors_du_dossier(limites):
    with pytest.raises(AccesRefuse):
        lire_fiche("../.env.md", limites)

def test_lit_une_fiche_du_dossier(limites):
    assert lire_fiche("modifier-taux-tva.md", limites) == "# Modifier le taux de TVA\n"