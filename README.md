# Projet système et réseau
## Application coopérative médicale

***

## Fonctionnalités de base

### Client
- [X] Saisie Login et mdp
- [X] Execution des commandes classiques (ls, mv etc..)

### Serveur
- [X] Authentification des clients
- [X] Reception et execution des commandes reçues par le(s) client(s)

***

## Fonctionnalités additionnelles
- [ ] Le client peut accepter les flux graphiques du serveur (RDP ou VNC)
- [X] Création de dossiers ou fichiers avec certains privilèges
- [X] Utilisation de connexions chiffrées pour le client et le serveur (utilisation de certificats par exemple)
- [X] Le client peut stocker localement des fichiers chiffrés et les ouvrir sans qu'ils apparaissent en clair sur le poste client
- [X] Client et Serveur sous Windows
- [X] Client et serveur sur des systèmes hétérogènes (serveur linux et client windows)

## LIB NECESSAIRES :
  
  -pip
  -Tkinter 
  -Tix
  -PyCrypto
  -readchar

## Roadmap

Deux équipes travaillent en parallèle, l'une sur tout ce qui est connection entre les deux entités, l'autre sur la partie fonctionnement.

### Etapes achevés:

- [X] Etape 1 : Serveur multithreadé et connection client basique (echo sans authentification)   
- [X] Etape 2 : Connection par mot de passe - Implémentation des commandes classiques            
- [X] Etape 3 : Comptabilité Windows (client seulement)
- [X] Etape 4 : Ergonomie dans les commandes + test d'exception
- [X] Etape 5 : Connection chiffrée via certificat   
- [X] Etape 6 : Le client peut ajouter des donnees dans les fichiers ~ en mode console
- [X] Etape 7 : Rajouter mkdir et rm
- [X] Etape 8 : Autocomplétion
- [X] Etape 9 : Dépot de documents
- [X] Etape 10 : Création de dossiers ou fichiers avec certains privilèges
- [X] Etape 11 : Chiffrement local des documents - Editions de documents 
- [X] Etape 12 : Adaptation windows
- [X] Etape 13 : Client graphique
- [X] Etape 14 : Faire de la place au niveaux des threads             
- [X] Etape 15 : Envoit de flux graphiques             
- [X] Etape 16 : Ajout de fonctionnalités
- [X] Etape 17 : Regler probleme de cd : differencier les dossiers /fichier? + si cd dans un fichier -> NOP.
- [X] Etape 18 :commande clear

### Etapes en cours:

### Etapes futures:
