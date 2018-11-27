# TFA

### **Concept du jeu :**

Création d'un jeu au design du manga Dragon Ball avec Python (PyGame). Le concept du jeu est de voyager dans une carte en 2D où il y a des personnages avec lesquels on peut interagir. Un système basique de combat est mit en place entre deux personnages. Il est possible de découvrir des objets dans la carte.

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
- [08/11/18] : Verification des fonctionnalités sur Windows + adaptations
- [15/11/18] : Renseignement sur les sockets
- [18/11/18] : Map moins carrée, commentaires ajoutés + collisions V0.1
- [22/11/18] : Recherche sur les différences de traitements du CPU + les différences avec Windows 
- [28/11/18] : Refonte du système de collision, librairie TMX modifiée, chemins des fichiers adaptés, mise en place de fonctions