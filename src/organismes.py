"""Ce module contient la classe Organisme, les sous classes Corail et Plancton ainsi que les méthodes
permettant de créer les êtres-vivants dans l'aquarium"""

from abc import abstractmethod
import numpy as np
from rochers import Rocher
import random as rd

############## lecture des paramères utiles ############################################################################


with open("parametres.txt", "r") as parametres:    # on a besoin des dimensions de l'aquarium pour l'affichage
    L=parametres.readlines()
    M=[]
    for i in L:
        j=i.split(' ')
        M.append(j)

dimx = int(M[9][0])
dimy = int(M[10][0])


############# Classe Organisme #########################################################################################

class Organisme():
    """Ceci est la classe mère qui englobe tous les êtres vivants
    """
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.pos = (x,y)

    @property
    def pos(self):
        return self.__pos

    @property
    def x(self):
        return self.__x

    @pos.setter                                     # on ne peut pas positionner une larve hors de l'aquarium
    def pos(self,new_pos):
        nx,ny = new_pos
        if nx < 0:
            nx = 0
        elif nx > dimx:
            nx = dimx
        self.x = nx
        if ny < 0:
            ny = 0
        elif ny > dimy:
            ny = dimy
        self.y  = ny
        self.__pos = nx,ny

    @x.setter
    def x(self, new_pos):
        nx = new_pos
        if nx < 0:
            nx = 0
        elif nx > dimx:
            nx = dimx
        self.__x = nx

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, new_pos):
        ny = new_pos
        if ny < 0:
            ny = 0
        elif ny > dimy:
            ny = dimy
        self.__y = ny

    @abstractmethod                                # Toutes les sous-classes de Animal doivent avoir une méthode 'bouger', sinon elles ne peuvent pas être instanciées
    def car(self):
        pass


###################### Classe Corail ###################################################################################

class Corail(Organisme):
    """Ceci est la classe corail qui hérite de la superclasse Organisme
    """

    def __init__(self, x, y, rayon, color = (0,110,190), capacite = 20, age = 0):
        super().__init__(x,y)
        self.capa = capacite
        self.sante = rd.randint(int(self.capa / 2), self.capa)
        self.age = age
        self.r = rayon
        self.color = color

    def car(self):
        """Cette méthode renvoie la chaîne de caractère idientifiant le corail
        """
        return 'C'

    def vieillir(self):
        """Méthode permettant d'augmenter l'âge d'un corail
        """
        self.age += 1

    def pondre(self, C, r, color, R, dific_ponte, prix_ponte):
        """Cette méthode permet à un corail fixé de pondre une nouvelle larve
        """
        aleatoire = rd.randint(0, dific_ponte)                                # Probabilité de ponte quantifiable
        if self.age >= 3 and not aleatoire:
            a = rd.uniform(self.r, self.r + 20)
            b = rd.uniform(self.r, self.r + 20)
            nouveau = Corail(self.x + a, self.y + b, r, color)

            ok = True
            for rocher in R:                              # Empêche de pondre dans un rocher
                d = distance(rocher, nouveau)
                if d < rocher.r:
                    ok = False
            for corail in C:                              # Empêche de pondre dans un corail
                if corail != nouveau:
                    d = distance(corail, nouveau)
                    if d < self.r + corail.r:
                        ok = False
            if ok:                                       # Ponte et perte de santé selon le paramètre
                C.append(nouveau)
                self.sante = self.sante - prix_ponte


    def grossir(self):
        """Cette méthode permet d'augmenter le volume d'un corail fixé et ayant suffisament mangé
        """
        if self.sante >= self.capa and self.age in [1, 2, 3, 4]:
            self.vieillir()                                          # On augmente l'âge
            self.sante = int(self.capa/2)
            self.r = self.r * 1.4                                    # On augmente la taille

    def mourir(self, R, C, pH):
        """Cette méthode fait disparaitre les larves affamées et transforme en calcaire les coraux fixés
        qui sont trop vieux ou affamés"""
        if self.age == 0:
            C.remove(self)                          # On retire les coraux morts de la liste
        else:
            a = rd.randint(0, int(abs(pH - 7)))  # L'acidité de l'eau peut bloquer la calcification
            if not a:
                R.append(Rocher(self.x, self.y, self.r, (253, 245, 145)))     # Les coraux morts intègrent la classe Rocher sous forme de calcaire
            C.remove(self)

    def accrocher(self, R):
        """Cette méthode permet à la larve de se fixer sur un rocher si elle est suffisament près
        """
        if self.age == 0:
            for rocher in R:                                    # On mesure la distance entre chaque rocher et la larve
                if distance(rocher, self) < rocher.r + self.r:
                    self.vieillir()                             # La larve passe à l'âge 1, elle ne pourra plus bouger
                    return True

    def bouger_int(self, P, C, R, endurance, visib, vitesse_l):
        """Cette méthode permet aux larves de se déplacer dans la direction présentant la plus forte
        densité de plancton, elle enlève de la vie à tous les coraux"""

        if not rd.randint(0, endurance):                                              # La larve peut perdre un point de vie car elle se fatigue
            self.sante = self.sante - 1
        if self.age == 0:                                                             # Il faut que le corail soit une larve pour se déplacer
            L = [0, 0, 0, 0]                                                          # On crée un compteur
            ok = 1
            for p in P:
                if distance(self, p) < visib:                                         # Le plancton doit être suffisament près pour être visible
                    if p.x < self.x and p.y < self.y:
                        L[0] += 1
                    if p.x > self.x and p.y < self.y:
                        L[1] += 1
                    if p.x < self.x and p.y > self.y:
                        L[2] += 1
                    if p.x > self.x and p.y > self.y:
                        L[3] += 1
            m = L.index(max(L))
            if L == [0, 0, 0, 0] or self.sante > 2*self.capa:                            # Si le corail ne voit aucun plancton ou a assez mangé
                self.bouger(R, C, vitesse_l, endurance)                                  # Alors il bouge au hasard
            else:                                                                        # Sinon il se déplace là où il a vu le plus de plancton
                if m == 0:
                    c = Corail(self.x - vitesse_l, self.y - vitesse_l, self.r)
                if m == 1:
                    c = Corail(self.x + vitesse_l, self.y - vitesse_l, self.r)
                if m == 2:
                    c = Corail(self.x - vitesse_l, self.y + vitesse_l, self.r)
                if m == 3:
                    c = Corail(self.x + vitesse_l, self.y + vitesse_l, self.r)

                for rocher in R:                # On vérifie que la nouvelle position n'est pas dans un rocher
                    d = distance(c, rocher)
                    if d < rocher.r:
                        ok = False

                for corail in C:                # On vérifie que la nouvelle position n'est pas dans un corail
                    if corail != self:
                        d = distance(corail, c)
                        if d < c.r + corail.r:
                            ok = False
                if ok:
                    self.x = c.x
                    self.y = c.y

    def bouger(self, R, C, vitesse_l, endurance):
        """Cette méthode permet à une larve de se déplacer aléatoirement dans l'eau suivant
        un mouvement brownien"""

        if not rd.randint(0, endurance):                                 # La larve peut perdre un point de vie car elle se fatigue
            self.sante = self.sante - 1

        if self.age == 0:                                   # Seule les larves bougent
            a = rd.uniform(-vitesse_l, vitesse_l)
            b = rd.uniform(-vitesse_l, vitesse_l)
            c = Corail(self.x + a, self.y + b, self.r)      # Coordonnées changées aléatoirement

            ok = True
            for rocher in R:             # Empêche de se déplacer dans un rocher
                d = distance(c, rocher)
                if d < rocher.r:
                    ok = False

            for corail in C:                 # Empêche de se déplacer dans un corail
                if corail != self:
                    d = distance(corail, c)
                    if d < self.r + corail.r:
                        ok = False
            if ok:
                self.x += a
                self.y += b


################# Classe Plancton ######################################################################################

class Plancton(Organisme):
    """La classe Plancton hérite de la superclasse Organisme
    """

    def car(self):
        return 'P'

    def bouger(self, R, vitesse_p):
        """La méthode bouger permet au plancton de se déplacer suivant un mouvement brownien à la vitesse
        vitesse_p"""
        a = rd.uniform(-vitesse_p, vitesse_p)
        b = rd.uniform(-vitesse_p, vitesse_p)
        t = Corail(self.x + a, self.y + b, 1)
        ok = True
        for rocher in R:               # On s'assure que la nouvelle position n'est pas dans un rocher
            d = distance(t, rocher)
            if d < rocher.r:
                ok = False
        if ok:
            self.x += a
            self.y += b

    def choix_mangeur(self, C, P):
        """Cette méthode permet de déterminer quel corail va pouvoir manger le plancton
        """
        mangeur = None
        dl = 100
        for corail in C:
            d = distance(corail, self)
            if d < 2 * corail.r + 2 * corail.age and d < dl:
                mangeur = corail
                dl = d                                                      # Le but est de trouver le corail qui correspond au plus petit dl
        if mangeur != None:
            P.remove(self)
            mangeur.sante += 1                                              # Le corail qui mange le plancton augmente sa santé de 1


################ Fonctions de création #################################################################################
# Les fonctions de créations permettent de générer les organismes dans l'aquarium

def creation_corail(N, L, h, r, R, capa, color = (0, 110, 190)):
    """Cette fonction crée et retourne la liste qui contiendra les coraux au cours de la simulation
    """
    ListeCorail = []
    while len(ListeCorail) < N:
        ajouter = True
        x = rd.uniform(0, L)
        y = rd.uniform(0, h)
        c = Corail(x, y, r, color, capa)

        for rocher in R:                            # On ne peut pas ajouter de corail dans un rocher...
            if distance(rocher, c) < rocher.r:
                ajouter = False
        for cor in ListeCorail:                     # ... ni dans un autre corail
            if distance(cor, c) < cor.r + c.r:
                ajouter = False
        if ajouter:
            ListeCorail.append(c)
    return ListeCorail


def creation_plancton(N, L, h, R):
    """Cette fonction crée et retourne la liste qui contiendra les planctons au cours de la simulation
    """
    ListePlancton = []
    for i in range(N):
        ajouter = True
        x = rd.uniform(0, L)
        y = rd.uniform(0, h)
        p = Plancton(x, y)

        for rocher in R:                            # Pas de plancton dans un rocher
            if distance(rocher, p) < rocher.r:
                ajouter = False
        if ajouter:
            ListePlancton.append(p)
    return ListePlancton

def apparition_plancton(Lp, L, h, nb, R):
    """Cette fonction permet de générer aléatoirement du plancton dans l'aquarium
    """
    for i in range(nb):
        ajouter = True
        x = rd.uniform(0, L)
        y = rd.uniform(0, h)
        p = Plancton(x, y)
        for rocher in R:                            # Pas de plancton dans un rocher
            if distance(rocher, p) < rocher.r:
                ajouter = False
        if ajouter:
            Lp.append(p)


def apparition_corail(C, L, h, nb, R, r, color=(0, 110, 190)):
    """Fait apparaitre du corail dans l'aquarium en ajoutant de nouveaux coraux à la liste C
    """
    for i in range(nb):
        ajouter = True
        x = rd.uniform(0, L)
        y = rd.uniform(0, h)
        c = Corail(x, y, r, color)

        for rocher in R:                        # Pas de corail dans un rocher
            if distance(rocher, c) < rocher.r:
                ajouter = False
        if ajouter:
            C.append(c)

def ajouter_larve(pos, r, C, color = (0,0,255)):
    """Ajoute une larve à un endroit de l'aquarium
    """
    c = Corail(pos[0], pos[1], r, color)
    C.append(c)

def ajouter_plancton_pos(P, R, pos, largeur, longueur, nb_planct = 10):
    """Ajoute un groupe de plancton autour d'une certaine position dans l'aquarium
    """
    L = []
    for i in range(nb_planct):
        ajouter = True
        x = rd.uniform(pos[0] - longueur/2, pos[0] + longueur/2)        # Planctons de coordonnées aléatoires autour du point considéré
        y = rd.uniform(pos[1] - largeur/2, pos[1] + largeur/2)
        p = Plancton(x, y)

        for rocher in R:                                    # Pas de plancton dans un rocher
            if distance(rocher, p) < rocher.r:
                ajouter = False
        if ajouter:
            P.append(p)

############## Autres fonctions ########################################################################################

def distance(obj1, obj2):
    """Fonction permettant de calculer la distance euclidienne entre deux objets
    """
    return np.sqrt((obj1.x - obj2.x)**2 + (obj1.y - obj2.y)**2)