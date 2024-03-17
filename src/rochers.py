"""Ce module contient la classe Rocher qui permet d'instancier les éléments naturels inertes 
dans l'aquarium (roche, calcaire)
"""

from random import uniform

class Rocher:          
    def __init__(self,abscisse,ordonnee,rayon, color = (150,150,150)):
        """Constructeur classe rocher
        """
        self.x = abscisse
        self.y = ordonnee
        self._pos = (abscisse,ordonnee)
        self.r = rayon
        self.color = color

    @property
    def pos(self):
        return self._pos

    def car(self):
        """ Affiche le caractère R pour identifier la classe rocher
        """
        return 'R'

def creation_rochers(n,L,h,R_max,R_min=0):
    """Crée n rochers de rayons compris dans [R_min, R_max] dans un espace de dimension L*h
    """
    listeRochers=[]
    for i in range(n):
        r = uniform(R_min,R_max)
        x = uniform(3*r, L-3*r)                        # Centre les rochers pour éviter les effets de bord
        y = uniform(2*r, h-2*r)
        R = Rocher(x,y,r)
        listeRochers.append(R)
    return listeRochers