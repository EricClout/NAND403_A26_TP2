# Le IMPORT OS permet entr'autre de vérifier si le fichier JSON existe dans le système. (même rôle que "sys" en C++)
#   en lien avec : os.path.exists & os.path.basename(chemin)
import json
import os
from maya import cmds
import maya.cmds as cmds

from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,      # Utilisé pour le champ texte pour entrer le json
    QCheckBox,      # Utilisé pour les cases à cocher
    QVBoxLayout,
    QPushButton
)

# ------------------------------------------------------------------------------------------
#   Note à moi-même :  À l'Ext. d'une classe --> Fonction ex : main()
#                      À l'Int. d'une classe --> Méthode tjs (self) qui vien avec ex :soit en paramètre (self) ou self.create_ui()

# Classe personnalisée pour gérer l'organisation des objs dans le outliner de Maya
class OutlinerOrganiser(QWidget):

    def __init__(self):
        super().__init__()
        # Titre de la fenêtre & ses dimansions
        self.setWindowTitle("Organizté ch'it")
        self.resize(380, 220)
        self.create_ui()

         #                       --------------------

    # Création de l'interface utilisateur PySide6
    def create_ui(self):
        # Layout principal vertical
        layout = QVBoxLayout(self)

        # ----------- (QLineEdit) !!! C'est nouveau ça !!! ----------- #
        # Crée (Layout horizontal) pour champ texte du fichier json
        chemin_fichier = QLabel("entre ton chemin d'accès du json rule")
        self.path_input = QLineEdit()
        
        # Le r = Raw String. En gros c'est pour dire à Python de lire les \ normalement comme du texte
        self.path_input.setText(r"C:\Users\eric\repos\NAND403_A26_cours\TP2\rules.json")    # Valeur par défaut à type d'exemple
        
        layout.addWidget(chemin_fichier)
        layout.addWidget(self.path_input)                                                   # Ceci ajoute les 3 lignes ci-dessus au layout principal

        # ----------- (QLineEdit) !!! C'est nouveau ça !!! ----------- #
        # Crée la case à cocher : Aplication de la sélection
        self.selection_only_box = QCheckBox("Applique juste ta sélection")                   # Texte explicatif de la case
        self.selection_only_box.setChecked(True)                                             # Indication de la case (True = cochée, False = décochée)
        layout.addWidget(self.selection_only_box)                                            # Ceci ajoute les 2 lignes ci-dessus au layout principal
                                                                                             # ________________________________________________________
        # Crée la case à cocher : Couleurs                                                                           |
        self.apply_colors_box = QCheckBox("Applique les couleurs")                           #                       |
        self.apply_colors_box.setChecked(True)                                               #                       |
        layout.addWidget(self.apply_colors_box)                                              #                       |
                                                                                             #                       |
        # Crée la case à cocher : Appliquer la réorganisation                                #                       |
        self.apply_reorder_box = QCheckBox("Applique la réorganisation")                     #                       |
        self.apply_reorder_box.setChecked(True)                                              #                       |
        layout.addWidget(self.apply_reorder_box)                                             #                       |
                                                                                             #                       |
        # Bouton principal pour accepter                                                     #                       |
        self.organize_button = QPushButton("Organises-moé donc ça pour voir !")              #                       |
        layout.addWidget(self.organize_button)                                               #                       V

        # Connexion entre le clic du bouton vers la fonction "on_organize_clicked"
        self.organize_button.clicked.connect(self.on_organize_clicked)

    # Fonction exécutée lors du clic sur le bouton
    def on_organize_clicked(self):
        pass


# ------------------------------------------------------------------------------------------
#                        Cette partie est pour le chargement du json.
# ------------------------------------------------------------------------------------------
#   Info utile à savoir :
#   - os.path.exists() = Vérifie si le fichier indiqué dans le champ texte
#   - self.path_input.text() = Récupère le chemin en entier dans le champ texte
#   - os.path.basename(chemin) = Récupère uniquement le nom du fichier "rules.json" au lieu du chemin complet
#   - json.load() = Charge le contenu du json
#   - cmds.undoInfo(openChunk=True) = Sert à stocker les actions qui seront faites dans Maya pour permettre de faire CTRL+Z one shot
#   - cmds.undoInfo(closeChunk=True) = Ferme le stockage des actions pour appliquer le CTRL+Z one shot






    # ------------------------------------------------------------------------------------------

def main():
    global widget               # Ça tool_window ou widget.close ça fait la même chose
    try:
        widget.close()
    except Exception:
        pass
    widget = OutlinerOrganiser()
    widget.show()

main()