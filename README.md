# TFA

### **Concept du jeu :**

Création d'un jeu au design du manga Dragon Ball avec Python (PyGame). Le concept du jeu est de voyager dans une carte en 2D où il y a des personnages avec lesquels on peut interagir. Un système basique de combat est mis en place entre deux personnages. Il est possible de découvrir des objets dans la carte.

### **Fonctionnalités :**
- Système de map 2D
- Interaction avec d'autres entités
- Système de combat 2D (personnage VS personnage IA, coups, temps, vie, ki)
- Création d'une IA
- Menu de démarrage
- Animation des personnages
- Histoire basique
- Son de fond lors du jeu
- (Trouver des objets dans la carte + système de monnaie + boutique pour achat de cartes)
- (Sauvegarde via base de données)
- (Sytème de socket multijoueur)

### **Problèmes :**
- Manque de connaissance sur PyGame
- Collision dans la carte
- IA du second personnage dans un combat
- Sauvegarde de l'avancement du personnage
- Animation du personnage (tomber, sauter, frapper)
- Changement d'une map à une autre map.
- Meilleure possibilité de maintenir un code PyGame
- Interaction avec les personnages

### **Acquis :**
- Image des animations (sprites) récupérée
- Sons récupérés
- Logiciel de création de la map 2D

### **Technologies :**
- PyGame
- Mysql

### **Par où commencer :**
- Idée de l'histoire
- Se renseigner PyGame et l'import d'une map avec Tiled Map Editor
- Création de la map :
    - Monde général
    - Kamé House
    - Tour de Karin
    - Capitale de l'Ouest
- Ajout des collisions
- Importation des maps + personnages
- Ajout du moyen de discussions
- Création de l'espace de combat (map + intégration des deux personnages et animations + barre de vie)
- Création du système de combat (vie, Ki, arrêt du jeu, temps de jeu + coups et animations)
- Création de l'IA
- Menu de démarrage
- Ajout des musiques
- Sauvegarde de l'évolution du jeu en base de données
- (Trouver des objets dans la carte + système de monnaie + boutique pour achat de cartes)
- (Sytème de socket multijoueur)

### **Avancement :**
- [11/10/18] : Création de l'objectif du projet
- [18/10/18] : Tester le module TMX + test des collisions + renseignements sur PyGame (tutoriels)
- [25/10/18] : Exercices sur PyGame et fin des tutoriels basiques
- [31/10/18] : Première carte, gestion des collisions + squelette d'une MAP (Player (sprites) + événements)
- [08/11/18] : Vérification des fonctionnalités sur Windows + adaptations
- [15/11/18] : Renseignement sur les sockets
- [18/11/18] : Map moins carrée, commentaires ajoutés + collisions V0.1
- [22/11/18] : Recherche sur les différences de traitements du CPU + les différences avec Windows 
- [27/11/18] : Refonte du système de collision, librairie TMX modifiée, chemins des fichiers adaptés
- [28/11/18] : Refactoring (class), gestion des collisions, optimisation des images, mise en place de fonctions, commentaires ajoutés, favicon + titre du jeu et gestion des FPS en fonction du CPU
- [09/01/19] : Collisions totalement fonctionnelles + totalité du code modifié et optimisé
- [16/01/19] : Nouvelles conditions d'importation des librairies sous Windows
- [23/01/19] : Corrections liées aux FPS sous Windows qui se traitaient différemment
- [30/01/19] : Renseignements sur le passage d'une map à l'autre
- [06/02/19] : Demande d'aide auprès de développeurs Python pour adopter une nouvelle logique de code
- [13/02/19] : Conception schématique des nouvelles informations à prendre en compte pour le transfert d'entités
- [20/02/19] : Re-développement des traitements mis en place sur le disque public (inaccessible)
- [27/02/19] : Fin du développement des informations mises en place sur le disque public (toujours inaccessible)
- [03/03/19] : Mise en place des Sprites animés lors de la marche