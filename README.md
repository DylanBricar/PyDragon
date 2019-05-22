# PyDragon

![Image de jeu](https://nsa40.casimages.com/img/2019/05/21/190521105547247473.png "image de jeu")

### **Concept du jeu :**

Création d'un jeu au design du manga Dragon Ball avec Python (PyGame). Le concept du jeu est de voyager dans une carte en 2D où il y a des personnages avec lesquels on peut interagir. Il est possible de découvrir des objets dans la carte et remplir des missions.

### **Fonctionnalités :**
- Système de map 2D
- Interaction avec d'autres entités
- Menu de démarrage
- Animation des personnages
- Histoire basique
- Son de fond lors du jeu
- Trouver des objets dans la carte
- (Sauvegarde via base de données)

### **Problèmes :**
- Manque de connaissance sur PyGame
- Collision dans la carte
- Sauvegarde de l'avancement du personnage
- Animation du personnage.
- Changement d'une map à une autre map.
- Meilleure possibilité de maintenir un code PyGame
- Interaction avec les personnages
- Placement des interfaces

### **Acquis :**
- Image des animations (sprites) récupérée
- Musique récupérée
- Logiciel de création de la map 2D

### **Technologies :**
- PyGame
- MySQL

### **Par où commencer :**
- Idée de l'histoire
- Se renseigner PyGame et l'import d'une map avec Tiled Map Editor
- Création de la map :
    - Monde général
    - Kamé House
- Ajout des collisions
- Importation des maps + personnages
- Ajout du moyen de discussion
- Ajout des musiques
- Création de l'histoire
- Recherche d'objets dans la carte
- Menu de démarrage
- Sauvegarde de l'évolution du jeu en base de données

### **Avancement :**
- [11/10/18] : Création de l'objectif du projet.
- [18/10/18] : Tester le module TMX + test des collisions + renseignements sur PyGame (tutoriels).
- [25/10/18] : Exercices sur PyGame et fin des tutoriels basiques.
- [31/10/18] : Première carte, gestion des collisions + squelette d'une MAP (Player (sprites) + événements).
- [08/11/18] : Vérification des fonctionnalités sur Windows + adaptations.
- [15/11/18] : Renseignement sur les sockets.
- [18/11/18] : Map moins carrée, commentaires ajoutés + collisions V0.1.
- [22/11/18] : Recherche sur les différences de traitements du CPU + les différences avec Windows.
- [27/11/18] : Refonte du système de collision, librairie TMX modifiée, chemins des fichiers adaptés.
- [28/11/18] : Refactoring (class), gestion des collisions, optimisation des images, mise en place de fonctions, commentaires ajoutés, favicon + titre du jeu et gestion des FPS en fonction du CPU.
- [09/01/19] : Collisions totalement fonctionnelles + totalité du code modifié et optimisé.
- [16/01/19] : Nouvelles conditions d'importation des librairies sous Windows.
- [23/01/19] : Corrections liées aux FPS sous Windows qui se traitaient différemment.
- [30/01/19] : Renseignements sur le passage d'une map à l'autre.
- [06/02/19] : Demande d'aide auprès de développeurs Python pour adopter une nouvelle logique de code.
- [13/02/19] : Conception schématique des nouvelles informations à prendre en compte pour le transfert d'entités.
- [20/02/19] : Redéveloppement des traitements mis en place sur le disque public (inaccessible).
- [27/02/19] : Fin du développement des informations mises en place sur le disque public (toujours inaccessible).
- [03/03/19] : Mise en place des Sprites animés lors de la marche, intérieur de la maison + collisions.
- [06/03/19] : Corrections de bugs liés à l'importation des sprites sur Windows.
- [13/03/19] : Plan de recherche sur la gestion du multimap et les informations qui y sont liées.
- [20/03/19] : Correction de la deuxième map au niveau des importations (globalisation du path).
- [27/03/19] : Demande d'aide auprès de développeurs Python pour le transfert de map.
- [24/04/19] : Relance de la demande d'aide auprès de développeurs.
- [08/05/19] : Projet de révision du jeu et nouvelle direction adoptée.
- [15/05/19] : Gestion des interfaces (menu), division en plusieurs class et ajout de collisions.
- [16/05/19] : Boucle sur les interfaces, sauvegarde des coordonnées, ajustement du personnage au niveau des sprites, division du code en plusieurs fichiers et ajout de commentaires.
- [17/05/19] : Ajout de la musique, d'un personnage, système d'interaction et première mission.
- [20/05/19] : Optimisation du code, ajout du personnage qui parle, transparence de la map et arrêt du sprite.
- [21/05/19] : Création d'une nouvelle map, collision et maison pour la mission n°1, appel des différentes maps et réaction, possibilité de discuter, optimisation du code, ajout de l'inventaire et mission 1 terminée.
- [22/05/19] : Ajout du menu de démarrage et modification de collisions dans la map.


### **Informations :**
Ce projet a été développé en sixième année secondaire dans le cadre du cours d'informatique de monsieur Bertocchi (http://explore-photo.com/) du Collège Roi Baudouin.