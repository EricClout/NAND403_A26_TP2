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
        self.resize(450, 220)
        self.create_ui()

#                       --------------------

    # Création de l'interface utilisateur PySide6
    def create_ui(self):
        # Layout principal vertical
        layout = QVBoxLayout(self)

        # ----------- (QLineEdit) !!! C'est nouveau ça !!! ----------- #
        # Crée (Layout horizontal) pour champ texte du fichier json
        chemin_fichier = QLabel("Copie/Colle ton chemin d'accès pour rule.json.         Auppuez sur ENTER pour confirmer")
        self.path_input = QLineEdit()
        
        # Le r = Raw String. En gros c'est pour dire à Python de lire les \ normalement comme du texte
        self.path_input.setText(r"C:\Users\BLA BLA BLA\rules.json")                           # Valeur par défaut à type d'exemple
        
        layout.addWidget(chemin_fichier)
        layout.addWidget(self.path_input)                                                     # Ceci ajoute les 3 lignes ci-dessus au layout principal

        # ----------- (QLineEdit) !!! C'est nouveau ça !!! ----------- #
        # Crée la case à cocher : Aplication de la sélection
        self.selection_seule_box = QCheckBox("Applique sur ta sélection")                     # Texte explicatif de la case
        self.selection_seule_box.setChecked(True)                                             # Indication de la case (True = cochée, False = décochée)
        layout.addWidget(self.selection_seule_box)                                            # Ceci ajoute les 2 lignes ci-dessus au layout principal
                                                                                              # ________________________________________________________
        # Crée la case à cocher : Couleurs                                                                            |
        self.applique_colors_box = QCheckBox("Applique les couleurs")                         #                       |
        self.applique_colors_box.setChecked(True)                                             #                       |
        layout.addWidget(self.applique_colors_box)                                            #                       |
                                                                                              #                       |
        # Crée la case à cocher : Appliquer la réorganisation                                 #                       |
        self.applique_reorder_box = QCheckBox("Applique la réorganisation")                   #                       |
        self.applique_reorder_box.setChecked(True)                                            #                       |
        layout.addWidget(self.applique_reorder_box)                                           #                       |
                                                                                              #                       |
        # Bouton principal pour accepter                                                      #                       |
        self.organize_button = QPushButton("Organises-moé donc ça pour voir !")               #                       |
        layout.addWidget(self.organize_button)                                                #                       V

        # Connexion entre le clic du bouton vers la fonction "on_organize_clicked"
        self.organize_button.clicked.connect(self.on_organize_clicked)

    
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

    # Méthode exécutée quand on clic sur le bouton d'organisation *VOIR NOTES CI-HAUT
    def on_organize_clicked(self):
        json_path = self.path_input.text()

        # Vérification du fichier *VOIR NOTES CI-HAUT
        if not os.path.exists(json_path):
            cmds.warning(f"Je ne trouve pas ton ficher json mon p'tit pit : {json_path}")
            return

        # Chargement sécurisé du fichier json
        try:
            file = open(json_path, "r", encoding="utf-8")
            rules_data = json.load(file)
            file.close()
        except Exception as error:
            cmds.warning(f"OUPSY !! Y'a eu uen erreur et j'ai pas pu lire ton fichier json : \n {error}")
            return

        # CTRL+Z ouverture du stockage *VOIR NOTES CI-HAUT
        cmds.undoInfo(openChunk=True, chunkName="OrganiseOutliner")

        try:
            # Récupère l'info de si oui ou non le cases est cochée
            applique_selection = self.selection_seule_box.isChecked()
            applique_colors = self.applique_colors_box.isChecked()
            applique_reorder = self.applique_reorder_box.isChecked()

            # Message pour informer l'utilisateur des choix possible
            print(f"Pour que ça marche tu dois faire :\n{len(rules_data)} Options possible.\n")
            print(f"Options A : Sélection={applique_selection} Applique les modifs sur la sélection active±\n (Doit avoir au moins une autre case de cochée),\n Options B : Couleurs={applique_colors} : Applique la couleur sur les noms des éléements de ta scène,\n Options C : Tri={applique_reorder} : Tri les élément de ta scène en fonction de leur suffix")

            

# ------------------------------------------------------------------------------------------
#               Cette partie est pour configuer l'effet d'est case à cocher.
# ------------------------------------------------------------------------------------------
            # CASE 1 - Applique les modif sur la Sélection active
            # (doit avoir au moins 1 des 2 autres case de coché pour marcher)
            if not applique_colors and not applique_reorder:
                cmds.warning("Heille wow une chance que je suis là! Pour que je puisse appliquer les modifs tu dois cocher au moins une des deux cases d'action (Couleurs ou Réorganisation).")
                return

            # Obtient la liste des objets à traiter selon la case Sélection
            if applique_selection:
                objets_cible = cmds.ls(selection=True, dag=True)
            else:
                objets_cible = cmds.ls(dag=True, transforms=True)
             
            # Sécurité si aucun objet n'est trouvé ou sélectionné
            if not objets_cible:
                cmds.warning("Heille wow ! J'ai peut-être pas d'œil, mais je sais que t'as rien de sélectionné dans ton projet Maya !")
                return
#                       --------------------
            
            # CASE 2 seulement - Couleur est cochée
            # *ATTENTION* Le objs dans Maya sont nommé avec un namespace " TP2: " devant
            # Fack faut bypasser les 3 premiers caratères avec ce que Python nous offre .split(":")[-1]
            if applique_colors:
                for objet in objets_cible:
                    # Sécurité : Si c'est une Shape, on récupère la transform du parent
                    if cmds.nodeType(objet) == "mesh" or "Shape" in objet:
                        parents = cmds.listRelatives(objet, parent=True)
                        if parents:
                            objet = parents[0]

                    nom_sans_namespace = objet.split(":")[-1]

                    # On lit les préfixes du json ("SM_", "FX_", "LGT_")
                    for prefixe, couleur_rgb in rules_data.items():
                        if nom_sans_namespace.startswith(prefixe):
                            # Valide si True ou False pour la sélectionner
                            cmds.setAttr(f"{objet}.useOutlinerColor", True)
                            # Applique la couleur RGB selon le json
                            cmds.setAttr(f"{objet}.outlinerColor", couleur_rgb[0], couleur_rgb[1], couleur_rgb[2], type="double3")
                            # *Explication du pourquoi du comment avec les paramètres du cmds.setAttr(f" ")
                            # Maya prendre les vector 3 (RGB) faut les associés au 0, 1, 2.
                            # De plus, Maya n'a pas qu'une seule attribue (int, text, bool)
                            # L'utilisation du " type="double3 " devient donc nécessaire
#                       --------------------

            # CASE 3 seulement - Réorganisation est cochée
            if applique_reorder:
                # Filtrage effecturé dans la liste d'objets sélectionnés qui correspondent
                # à au moins une règle inclus dans le json
                objets_a_trier = []                                 # Toujours initialiser la liste

                for objet in objets_cible:
                    nom_sans_namespace = objet.split(":")[-1]
                    for prefixe in rules_data.keys():
                        if nom_sans_namespace.startswith(prefixe):
                            objets_a_trier.append(objet)
                            break
                          
                # Tri par ordre alphabétique croissant
                objets_tries = sorted(list(set(objets_a_trier)))    # Le set() évite les doublons dans l'hiérarchie

                # Déplacement dans l'Outliner
                for objet in objets_tries:
                    cmds.reorder(objet, back=True)

            print(f"Organiseté ch'it avec SUCCÈS !! {len(objets_cible)} objet(s) traités !")


        # *** DOIT ÊTRE À LA TOUTE FIN *** les modifs doivent être entre l'ouverture " try "
        #                                  et la fermeture " finally " pour que les CTRL+Z marche
        finally:
            # Le stockage ferme pour ne pas bloquer Maya
            cmds.undoInfo(closeChunk=True)
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