"""
Module principal contenant les fonctions permettant d'effectuer un tour de simulation en mode
solo (une seule colonie) ou en mode affrontement (2 colonies concurrentes)
"""

import organismes as org
import random as rd
import rochers

############# définition des paramètres de la simulation ###############################################################

with open("parametres.txt","r") as parametres:   # les paramètres sont stockés dans le fichier parametres.txt
    L=parametres.readlines()
    M=[]
    for i in L:
        j=i.split(' ')
        M.append(j)

nb_rochers = int(M[3][0])           # nombre de rochers générés dans l'aquarium
r_larve = float(M[5][0])            # rayon des larves
nb_plancton_init = int(M[6][0])     # quantité initiale de plancton
nb_plancton_r = int(M[7][0])        # quantité de plancton ajoutée à chaque tour
r_plancton = float(M[8][0])         # rayon du plancton
dimx = int(M[9][0])                 # longueur de l'aquarium
dimy = int(M[10][0])                # largeur de l'aquarium
r_min = float(M[11][0])             # rayon minimal des rochers
r_max = float(M[12][0])             # rayon maximal des rochers
nb_coraux_r = int(M[13][0])         # nombre maximal de larves rajoutées à chaque tour
dific_app = int(M[16][0])           # coefficient qui caractérise la difficulté d'apparition des larves
dific_ponte = int(M[15][0])         # coefficient qui caractérise la dificulté des coraux à pondre des larves
prix_ponte = int(M[19][0])          # coefficient modélisant la baisse de santé induite par la ponte d'une larve
visib = int(M[17][0])               # coefficient modélisant la capacité des larves à s'orienter (visibilité)
nb_coraux = int(M[4][0])            # nombre de larves initialement générées
capa = int(M[14][0])                # capacité de nourriture des larves (quantité servant de référence)
vitesse_l = float(M[1][0])          # Vitesse maximale des larves
vitesse_p = float(M[0][0])          # Vitesse maximale du plancton
endurance = int(M[18][0])           # coefficent qui modélise la capacité des coraux à se déplacer longtemps sans manger
pH = int(M[24][0])                  # pH de l'eau

###### paramètres de le seconde colonie en mode affrontement #########

endurance2 = int(M[21][0])          # endurance de la seconde colonie (en mode affrontement)
vitesse_l2 = int(M[22][0])          # vitesse des larves de la seconde colonie (en mode affrontement)
capa2 = int(M[20][0])               # capacité des coraux de la seconde colonie en mode affrontement
visib2 = int (M[23][0])             # visibilité des larves de la deuxième colonie


############### mode solo ########################################################################################

def initialisation_solo():
    """Fonction permettant de créer les listes contenant les rochers, le plancton et les coraux
    """
    R = rochers.creation_rochers(nb_rochers, dimx, dimy, r_max, r_min)
    P = org.creation_plancton(nb_plancton_init, dimx, dimy, R)
    C = org.creation_corail(nb_coraux, dimx, dimy, r_larve, R, capa)
    return R,C,P

def un_tour_solo(R,C,P):
    """Fonction permettant d'effectuer un tour de simulation en mode solo
    """
    if len(P) <=  2*nb_plancton_init:                                                       # On s'assure qu'il n'y ait pas trop de plancton dans l'aquarium
        org.apparition_plancton(P, dimx, dimy, nb_plancton_r, R)                            # On fait alors réapparaitre du plancton
    alea = rd.randint(0, dific_app)
    if not alea:                                                                            # On fait apparaître des larves plus ou moins difficilement
        org.apparition_corail(C, dimx, dimy, nb_coraux_r, R, r_larve)

    for corail in C:                                                                        # Le corail bouge et se fixe éventuellement à un rocher
        corail.bouger_int(P, C, R, endurance, visib, vitesse_l)
        corail.accrocher(R)
        if corail.sante <= 0 or corail.age >= 5:                                            # On fait mourir le corail s'il est trop vieux ou trop affamé
            corail.mourir(R, C, pH)                                                         # Le corail va éventuellment devenir du calcaire
        corail.grossir()                                                                    # Le corail peut augmenter sa taille s'il est fixé et bien nourri
        corail.pondre(C, r_larve, (200, 5, 170), R, dific_ponte, prix_ponte)                # Les coraux fixés peuvent pondre

    for plancton in P:                                                                      # Le plancton bouge et se fait manger éventuellement
        plancton.bouger(R, vitesse_p)
        plancton.choix_mangeur(C, P)                                                        # On détermine quel corail peut manger le plancton



############### mode affrontement ######################################################################################

def initialisation_multi():
    """Cette fonction sert à créer les listes contenant les organismes en mode affrontement
    """
    R = rochers.creation_rochers(nb_rochers, dimx, dimy, r_max, r_min)                      # Création de la liste contenant les rochers
    P = org.creation_plancton(nb_plancton_init, dimx, dimy, R)                              # Création de la liste contenant le plancton
    C1 = org.creation_corail(10, dimx, dimy, r_larve, R, capa)                              # Colonie bleue
    C2 = org.creation_corail(10, dimx, dimy, r_larve, R, capa2, (190, 90, 50))              # Colonie rouge
    return R, P, C1, C2


def un_tour_multi(R, C1, C2, P):
    """Fonction permettant d'effectuer un tour de simulation en mode affrontement, elle prend 2 listes
    en argument plutôt qu'une seule
    """
    if len(P) <=  2*nb_plancton_init:                                                   # On régule le quantité de plancton dans l'aquarium
        org.apparition_plancton(P, dimx, dimy, nb_plancton_r, R)
    for corail in C1:                                                                   # On gère les déplacements de la première colonie
        corail.bouger_int(P, C1+C2, R, endurance, visib, vitesse_l)
        corail.accrocher(R)
        alea = rd.randint(0, dific_app)

        if not alea:                                                                   # On fait apparaître des larves plus ou moins difficilement
            org.apparition_corail(C1, dimx, dimy, nb_coraux_r, R, r_larve)
        if corail.sante <= 0 or corail.age >= 5:
            corail.mourir(R, C1, pH)

        corail.grossir()
        corail.pondre(C1, r_larve, corail.color, R, dific_ponte, prix_ponte)

    for corail in C2:                                                                  # On effectue les mêmes actions pour la seconde colonie
        corail.bouger_int(P, C1 + C2, R, endurance2, visib, vitesse_l2)
        corail.accrocher(R)
        alea = rd.randint(0, dific_app)

        if not alea:                                                                   # On fait apparaître des larves plus ou moins difficilement
            org.apparition_corail(C2, dimx, dimy, nb_coraux_r, R, r_larve, (190, 90, 50))
        if corail.sante <= 0 or corail.age >= 5:
            corail.mourir(R, C2, pH)

        corail.grossir()
        corail.pondre(C2, r_larve, corail.color, R, dific_ponte, prix_ponte)
    for plancton in P:                                                                 # Le plancton bouge et se fait éventuellement manger
        plancton.bouger(R, vitesse_p)
        plancton.choix_mangeur(C1+C2, P)


############# mode jeu à deux joueurs ##################################################################################

def initialisation_jeu2():
    """Cette fonction sert à créer les listes contenant les organismes en mode jeu à deux joueurs
    """
    R = rochers.creation_rochers(nb_rochers, dimx, dimy, r_max, r_min) # création de la liste contenant les rochers
    P = org.creation_plancton(nb_plancton_init, dimx, dimy, R)     # création de la liste contenant le plancton
    C1 = org.creation_corail(10, dimx, dimy, r_larve, R, capa)  # colonie bleue
    C2 = org.creation_corail(10, dimx, dimy, r_larve, R, capa2, (190, 90, 50))   # colonie rouge
    return R, P, C1, C2

def un_tour_jeu2(R, C1, C2, P):
    """Fonction permettant d'effectuer un tour de simulation en mode jeu à deux joueurs, elle prend 2 listes
    en argument plutôt qu'une seule. Les coraux ennemis qui passent à proximité l'un de l'autre s'infligent
    des dégâts mutuels en focntion de leur différence de santé
    """
    if len(P) <=  1.3*nb_plancton_init:                                          # On régule le quantité de plancton dans l'aquarium
        org.apparition_plancton(P, dimx, dimy, nb_plancton_r, R)
    for corail in C1:                                                            # On gère les déplacements de la première colonie
        corail.bouger_int(P, C1+C2, R, endurance, visib, vitesse_l)
        corail.accrocher(R)
        for ennemi in C2:                                                        # Affrontement entre larves
            if org.distance(corail, ennemi) < 3*corail.r:
                perte = abs(corail.sante - ennemi.sante)                         # Perte de santé selon la différence entre les 2 santés
                corail.sante = corail.sante - perte
                ennemi.sante = ennemi.sante - perte

        alea = rd.randint(0, dific_app)
        if not alea:                                                            # On fait apparaître des larves plus ou moins difficilement
            org.apparition_corail(C1, dimx, dimy, nb_coraux_r, R, r_larve)

        if corail.sante <= 0 or corail.age >= 5:
            corail.mourir(R, C1, pH)
        corail.grossir()
        corail.pondre(C1, r_larve, corail.color, R, dific_ponte, prix_ponte)

    for corail in C2:                                                          # On effectue les mêmes actions pour la seconde colonie
        corail.bouger_int(P, C1 + C2, R, endurance2, visib, vitesse_l2)
        corail.accrocher(R)

        for ennemi in C1:
            if org.distance(corail, ennemi) < 3*corail.r:
                perte = abs(corail.sante - ennemi.sante)
                corail.sante = corail.sante - perte
                ennemi.sante = ennemi.sante - perte

        alea = rd.randint(0, dific_app)
        if not alea:                                                                            # On fait apparaître des larves plus ou moins difficilement
            org.apparition_corail(C2, dimx, dimy, nb_coraux_r, R, r_larve, (190, 90, 50))
        if corail.sante <= 0 or corail.age >= 5:
            corail.mourir(R, C2, pH)
        corail.grossir()
        corail.pondre(C2, r_larve, corail.color, R, dific_ponte, prix_ponte)

    for plancton in P:                                               # Le plancton bouge et se fait éventuellement manger
        plancton.bouger(R, vitesse_p)
        plancton.choix_mangeur(C1+C2, P)