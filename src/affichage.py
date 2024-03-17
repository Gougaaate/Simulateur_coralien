"""Module contenant l'interface graphique qui permet de contrôler la simulation selon plusieurs modes
"""

# EXÉCUTER CE MODULE AFIN DE LANCER LA SIMULATION

import simulation as s
import pygame.locals
import matplotlib.pyplot as plt
import organismes as org

####################### Lecture des paramètres d'affichage #############################################################

with open("parametres.txt", "r") as parametres:  # Ouvre le fichier texte contenant les paramètres
    L = parametres.readlines()
    M = []
    for i in L:
        j = i.split(' ')
        M.append(j)
    parametres.close()

r_plancton = int(M[8][0])               # Rayon du plancton
dimx = int(M[9][0])                     # Longueur de l'aquarium
dimy = int(M[10][0])                    # Largeur de l'aquarium
r_larve = float(M[5][0])                # Rayon des larves
nb_tours_multi = int(M[25][0])          # Limite de tours pour le mode jeu
limite_larves =  int(M[2][0])                  # Limite de larves par joueur en mode jeu

#################### Classe bouton pour le menu ###############################################################

class Bouton:
    def __init__(self, x, y, img, scale):
        """Constructeur de la classe Bouton
        """
        largeur = img.get_width()
        hauteur = img.get_height()
        self.img = pygame.transform.scale(img,(int(largeur * scale), int(hauteur * scale)))     # Ajuste la taille de l'image
        self.rect = self.img.get_rect()
        self.rect.topleft = (x, y)
        self.click = False

    def draw(self):
        """Dessine le bouton sur l'écran et permet de cliquer dessus
        """
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):                             # Vérifie que la souris est au dessus d'un des deux boutons et clique
            if pygame.mouse.get_pressed()[0] and not self.click:
                self.click = True                                   # Empêche les clicks en continu
                action = True                                       # Permet de différencier les boutons
        if not pygame.mouse.get_pressed()[0]:
            self.click = False

        screen.blit(self.img, (self.rect.x, self.rect.y))
        return action

############### Initialisation ############################################################################"


pygame.init()
screen = pygame.display.set_mode((dimx, dimy))
clic = pygame.mixer.Sound("clic.ogg")                                          # Son du clic
fond = pygame.image.load("Fond.jpg").convert_alpha()                           # Image de fond

fond = pygame.transform.scale(fond, (dimx, dimy))
pygame.display.set_caption("Simulateur coralien")
solo_img = pygame.image.load('mode_solo.png').convert_alpha()                  # Image de boutons
duo_img = pygame.image.load('mode_duo.png').convert_alpha()
jeu_img = pygame.image.load('mode_jeu.png').convert_alpha()
reset_img = pygame.image.load('reset.png').convert_alpha()
reprendre_img = pygame.image.load('reprendre.png').convert_alpha()
mode_sol = Bouton(150, 230, solo_img, 1)                                       # Création des boutons
mode_du = Bouton(600, 230, duo_img, 1)
mode_je = Bouton(373, 400, jeu_img,0.65)
texte1 = "By Titouan Maréchal and Adam Goux--Gateau                                                                                       All rights reserved"
texte2 = "CORAL SIMULATOR"
texte3 = "TM"
font = pygame.font.SysFont('robotto', 25)                                     # Affichage du titre et des auteurs
font2 = pygame.font.SysFont('robotto', 60)
coordonnees1 = (10, 10)
coordonnees2 = (300, 130)
coordonnees3 = (705, 115)
couleur = (255, 255, 255)
texte_1 = font.render(texte1, False, couleur)
titre = font2.render(texte2, False, couleur)
tm = font.render(texte3, False, couleur)

############ mode solo #################################################################################################

def mode_solo():
    """Cette fonction permet de gérer l'affichage de la simulation en mode solo (une seule colonie),
    elle permet aussi de tracer l'évolution des populations au fil de la simulation lorsque l'utilisateur ferme
    la fenêtre pygame.
    """
    ecran = pygame.display.set_mode((dimx, dimy))                               # Création de l'écran et des paramètres graphiques initiaux
    R, C, P = s.initialisation_solo()                                           # Initialisation de la simulation
    populationPlancton = []
    populationCoraux = []
    tourSimulation = []
    popTot = []
    pygame.display.set_caption("Simulateur corallien")

    continuer = True
    while continuer:
        pygame.draw.rect(ecran, (255, 255, 255), (0, 0, dimx, dimy))            # On dessine un rectangle de fond

        for event in pygame.event.get():
            if event.type == pygame.QUIT:                                           # La croix fait quitter pygame
                continuer = False

            if pygame.mouse.get_pressed()[0]:                                       # Le click gauche ajoute une larve
                a = pygame.mouse.get_pos()
                org.ajouter_larve(a, r_larve, C, (0,0,255))

            if pygame.mouse.get_pressed()[2]:                                       # Le click droit ajoute du plancton
                a = pygame.mouse.get_pos()
                org.ajouter_plancton_pos(P,R, a, 15, 15, 10)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:                                # Si on appuie sur espace....
                    plt.plot(tourSimulation, populationPlancton, label="plancton /5",color='green')            # Affichage des populations en fonction du temps
                    plt.plot(tourSimulation, populationCoraux, label="coraux", color='blue')
                    plt.title("Populations en fonction du temps")
                    plt.xlabel("Nombre de tours")
                    plt.ylabel("Nombre d'organismes")
                    plt.legend()
                    plt.show()

                if event.key == pygame.K_RETURN:                                                    # Si on appuie sur Entrée : pause
                    while True:

                        screen.blit(fond, (0, 0))
                        bouton_reset = Bouton(70, 200, reset_img, 1)                                # Bouton de reprise
                        bouton_reprendre = Bouton(550, 200, reprendre_img, 1)                       # Bouton pour réinitialiser la simulation
                        ev = pygame.event.wait()

                        if bouton_reprendre.draw():                                         # Reprise de la simulation
                            clic.play()
                            plt.close()
                            break

                        if bouton_reset.draw():
                            clic.play()
                            C.clear()                                                        # On vide toutes les listes
                            P.clear()
                            populationPlancton.clear()
                            populationCoraux.clear()
                            tourSimulation.clear()
                            R, C, P = s.initialisation_solo()                               # On reprend d'autres paramètres initiaux
                            break

                        if ev.type == pygame.KEYDOWN and ev.key == pygame.K_RETURN:
                            plt.close()
                            break
                        if ev.type == pygame.QUIT:
                            continuer = False
                            break
                        pygame.display.update()

        s.un_tour_solo(R, C, P)                                          # On effectue un tour de simulation
        font = pygame.font.SysFont('comicsansms', 20)                    # Affiche le nombre de tours
        texte = "tour " + str(len(populationPlancton))
        coordonnees = (5, 565)
        couleur = (0, 0, 0)
        nombre_tours = font.render(texte, False, couleur)
        screen.blit(nombre_tours, coordonnees)

        populationPlancton.append(len(P)/8)                                                 # Listes contenant l'effectif des populations
        populationCoraux.append(len(C))
        tourSimulation.append(len(populationPlancton))
        popTot.append(len(P)/5 + len(C))
        for c in C:                                                                          # Représentation graphiques des rochers, coraux et planctons
            pygame.draw.circle(ecran, c.color, (round(c.x), round(c.y)), round(c.r))
        for p in P:
            pygame.draw.circle(ecran, (0, 250, 0), (round(p.x), round(p.y)), r_plancton)
        for rocher in reversed(R):
            pygame.draw.circle(ecran, rocher.color, (round(rocher.x), round(rocher.y)), round(rocher.r))

        pygame.display.update()                                                      # On rafraîchit l'affichage

    plt.plot(tourSimulation, populationPlancton, label="plancton /5", color='green')  # Affichage des populations en fonction du temps
    plt.plot(tourSimulation, populationCoraux, label="coraux", color='blue')
    plt.title("Populations en fonction du temps")
    plt.xlabel("Nombre de tours")
    plt.ylabel("Nombre d'organismes")
    plt.legend()
    plt.show()


############### mode affrontement #####################################################################################

def mode_duo():
    """Cette fonction permet de gérer l'affichage de la simulation en mode affrontement, elle permet également
    de tracer le graphe indiquant la quantité de chaque organisme au fil de la simulation. Elle permet de
    comparer le développement de deux colonies qui possèdent chacunes des paramètres différents.
    """

    ecran = pygame.display.set_mode((dimx, dimy))                                 # Création de l'écran et des paramètres graphiques initiaux
    R, P, C1, C2 = s.initialisation_multi()                                       # Initialisation de la simulation
    populationPlancton = []
    populationCoraux1 = []
    populationCoraux2 = []
    tourSimulation = []
    pygame.display.set_caption("Simulateur corallien")

    continuer = True
    while continuer:
        pygame.draw.rect(ecran, (250, 250, 250), (0, 0, dimx, dimy))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:                                       # Cliquer sur la croix fait sortir de pygame
                continuer = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:                                                       # Si on appuie sur espace...
                    plt.plot(tourSimulation, populationPlancton, label="plancton /5", color='green')  # Affichage des populations en fonction du temps
                    plt.plot(tourSimulation, populationCoraux1, label="coraux 1", color='blue')
                    plt.plot(tourSimulation, populationCoraux2, label="coraux 2", color='red')
                    plt.title("Populations en fonction du temps")
                    plt.xlabel("Nombre de tours")
                    plt.ylabel("Nombre d'organismes")
                    plt.legend()
                    plt.show()
                if event.key == pygame.K_RETURN:                                                        # Si on appuie sur entrée : pause
                    while True:

                        screen.blit(fond, (0, 0))
                        bouton_reset = Bouton(70, 200, reset_img, 1)            # Bouton de reprise
                        bouton_reprendre = Bouton(550, 200, reprendre_img, 1)   # Bouton pour réinitialiser la simulation
                        ev = pygame.event.wait()

                        if bouton_reprendre.draw():                                 # Reprise de la simulation
                            clic.play()
                            plt.close()
                            break

                        if bouton_reset.draw():
                            clic.play()
                            C1.clear()                                              # On vide toutes les listes
                            C2.clear()
                            P.clear()
                            populationPlancton.clear()
                            populationCoraux1.clear()
                            populationCoraux2.clear()
                            tourSimulation.clear()
                            R, P, C1, C2 = s.initialisation_multi()                # On reprend d'autres paramètres initiaux
                            break

                        if ev.type == pygame.KEYDOWN and ev.key == pygame.K_RETURN:
                            plt.close()
                            break
                        if ev.type == pygame.QUIT:
                            continuer = False
                            break
                        pygame.display.update()
        s.un_tour_multi(R, C1, C2, P)                                                         # On effectue un tour de simulation

        font = pygame.font.SysFont('comicsansms', 20)                                         # Affichage du nombre de tours
        texte = "tour " + str(len(populationPlancton))
        coordonnees = (5, 565)
        couleur = (0, 0, 0)
        nombre_tours = font.render(texte, False, couleur)
        screen.blit(nombre_tours, coordonnees)

        populationPlancton.append(len(P)/5)                                                   # Liste contenant l'effectif de chaque population
        populationCoraux1.append(len(C1))
        populationCoraux2.append(len(C2))
        tourSimulation.append(len(populationPlancton))

        for p in P:                                                                          # Représentation graphiques des rochers, coraux et planctons
            pygame.draw.circle(ecran, (0, 250, 0), (round(p.x), round(p.y)), r_plancton)
        for c in C1:
            pygame.draw.circle(ecran, c.color, (round(c.x), round(c.y)), round(c.r))
        for c in C2:
            pygame.draw.circle(ecran, c.color, (round(c.x), round(c.y)), round(c.r))
        for rocher in reversed(R):
            pygame.draw.circle(ecran, rocher.color, (round(rocher.x), round(rocher.y)), round(rocher.r))
        pygame.display.update()                                                                               # On rafraîchit l'affichage

    plt.plot(tourSimulation, populationPlancton, label="plancton/5", color='green')         # Affichage des populations en fonction du temps
    plt.plot(tourSimulation, populationCoraux1, label="Coraux 1", color='blue')
    plt.plot(tourSimulation, populationCoraux2, label="Coraux 2", color='red')
    plt.title("Populations en fonction du temps")
    plt.xlabel("Nombre de tours")
    plt.ylabel("Nombre d'organismes")
    plt.legend()
    plt.show()


################### Mode jeu (2 joueurs) ###############################################################################

def mode_jeu_deux_joueurs(n = nb_tours_multi):
    """Cette fonction lance un mode multijoueur où les deux joueurs peuvent faire apparaître
    chacun leur tour une larve  à l'endroit souhaité. Le but est d'avoir la plus grande colonie
    au bout de n tours"""

    lim = limite_larves                                                       # limite de larves pour chaque joueur
    ecran = pygame.display.set_mode((dimx, dimy))                    # Paramètres initiaux d'affichage
    R, P, C1, C2 = s.initialisation_multi()
    C1 = []
    C2 = []
    populationPlancton = []
    populationCoraux1 = []
    populationCoraux2 = []
    tourSimulation = []
    pygame.display.set_caption("Simulateur coralien")

    continuer = True
    parite = 0
    while continuer:
        if len(tourSimulation) >= n:                                                        # Le jeu se finit au tour n
            continuer = False
        pygame.draw.rect(ecran, (250, 250, 250), (0, 0, dimx, dimy))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                continuer = False
            if pygame.mouse.get_pressed()[0] and parite < 2*lim:                           # Si click droit...
                a = pygame.mouse.get_pos()                                                 # On ajoute une larve tantôt bleue, tantôt rouge
                if parite %2:
                    org.ajouter_larve(a, r_larve, C1)
                elif not parite %2:
                    org.ajouter_larve(a, r_larve, C2, (255, 0, 0))
                parite += 1

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:                                        # Si on appuie sur entrée : pause

                    while True:
                        screen.blit(fond, (0, 0))
                        bouton_reprendre = Bouton(300, 200, reprendre_img, 1)                  # Bouton pour reprendre
                        ev = pygame.event.wait()

                        if bouton_reprendre.draw():                                            # Reprise si on clique sur le bouton
                            clic.play()
                            plt.close()
                            break

                        if ev.type == pygame.KEYDOWN and ev.key == pygame.K_RETURN:
                            plt.close()
                            break
                        if ev.type == pygame.QUIT:
                            continuer = False
                            break
                        pygame.display.update()

        s.un_tour_jeu2(R, C1, C2, P)                                       # On effectue un tour de simulation
        font = pygame.font.SysFont('comicsansms', 20)                       # Affichage du nombre de tours
        texte = "tour " + str(len(populationPlancton))
        coordonnees = (5, 565)
        couleur = (0, 0, 0)
        nombre_tours = font.render(texte, False, couleur)
        ecran.blit(nombre_tours, coordonnees)

        populationPlancton.append(len(P) / 5)                           # Liste contenant l'effectif de chaque population
        populationCoraux1.append(len(C1))
        populationCoraux2.append(len(C2))
        tourSimulation.append(len(populationPlancton))

        for p in P:                                                         # Représentation graphiques des rochers, coraux et planctons
            pygame.draw.circle(ecran, (0, 250, 0), (round(p.x), round(p.y)), r_plancton)
        for c in C1:
            pygame.draw.circle(ecran, c.color, (round(c.x), round(c.y)), round(c.r))
        for c in C2:
            pygame.draw.circle(ecran, c.color, (round(c.x), round(c.y)), round(c.r))
        for rocher in reversed(R):
            pygame.draw.circle(ecran, rocher.color, (round(rocher.x), round(rocher.y)), round(rocher.r))
        pygame.display.update()

    victoire(C1,C2)

    plt.plot(tourSimulation, populationPlancton, label="plancton/5", color='green')                             # Affichage des populations en fonction du temps
    plt.plot(tourSimulation, populationCoraux1, label="Coraux 1", color='blue')
    plt.plot(tourSimulation, populationCoraux2, label="Coraux 2", color='red')
    plt.title("Populations en fonction du temps")
    plt.xlabel("Nombre de tours")
    plt.ylabel("Nombre d'organismes")
    plt.legend()
    plt.show()

def victoire(C1, C2):
    """Cette fonction affiche le vainqueur de la partie
    """
    screen = pygame.display.set_mode((dimx, dimy))
    score1 = 0
    score2 = 0
    for c in C1:                                                                # Les coraux rapportent plus s'ils sont plus âgés
        score1 += c.age
    for c in C2:
        score2 += c.age
    if score1 > score2:                                                         # Comparaison des scores
        message = "La colonie 1 a remporté la partie !!! "
    elif score1 < score2:
        message = "La colonie 2 a remporté la partie !!! "
    else:
        message = "Ex Aequo"

    couleur = (250, 250, 250)
    coord_vainqueur = (130, 115)

    if message == "Ex Aequo":
        coord_vainqueur = (400, 115)

    font = pygame.font.SysFont('robotto', 60)
    message_vainqueur = font.render(message, False, couleur)
    fond_v = pygame.image.load('victoire.jpg').convert_alpha()
    fond_v = pygame.transform.scale(fond_v, (dimx, dimy))

    continuer = True                                                    # Affichage du message de fin
    while continuer:
        screen.blit(fond_v, (0, 0))
        screen.blit(message_vainqueur, coord_vainqueur)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                continuer = False
        pygame.display.update()


################### Programme principal: lancement du menu de la simulation ############################################

if __name__ == '__main__':

    continuer = True
    while continuer:
        screen.blit(fond,(0,0))                                         # Remplit l'écran et dessine les boutons
        screen.blit(tm, coordonnees3)
        screen.blit(titre, coordonnees2)
        screen.blit(texte_1, coordonnees1)

        if mode_sol.draw():                                             # Si on presse un bouton, le mode correspondant se lance
            clic.play()
            mode_solo()
        if mode_du.draw():
            clic.play()
            mode_duo()
        if mode_je.draw():
            clic.play()
            mode_jeu_deux_joueurs()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:                              # Quitte pygame si on clique sur la croix
                continuer = False

        pygame.display.update()

    pygame.quit()