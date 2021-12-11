# Puissance4-IA

**Date de réalisation :** Mai 2020

**Cadre du projet :* Cours "Introduction à l’Intelligence Artificielle" en 3ème année à l’ESILV (1ère année du cycle ingénieur), réalisé en groupe avec Dimitri, Stéphane et Alban

**Langage utilisé :** Python

Le Puissance 4 est un jeu à deux joueurs en tour par tour. Les joueurs disposent de 21 pions de couleur et doivent les placer chacun leur tour dans une colonne de la grille du jeu, qui compte 6 rangées et 7 colonnes. Les pions coulissent alors jusqu’à la position la plus basse de la colonne. Le but du jeu est d’aligner une suite de 4 pions de même couleur sur cette grille.

J’ai développé une Intelligence Artificielle capable de jouer au Puissance 4 contre un utilisateur. La taille de la grille a été agrandie en 12 colonnes et 6 rangées afin de complexifier le problème. En effet, dans le cas où le premier joueur jouerait au milieu de la petite grille (colonne 4) et ne ferait pas d’erreur, le deuxième joueur ne pourrait jamais gagner. Pour limiter le temps du jeu, il suffit toujours de n’aligner que 4 pions pour remporter la partie et chaque joueur ne dispose que de 21 pions au total.

L’IA développée repose sur un algorithme Minimax avec élagage Alpha-Beta, ainsi qu’une heuristique dont le principe est expliqué dans le rapport.

Afin de jouer, il vous suffit de lancer le programme python. Il vous sera alors demandé de choisir quel joueur commence. Dans tous les cas, l'IA a les pions représentés par X et vous aurez les pions représentés par O.
