# Projet système et réseau
## Application coopérative médicale

***

##Fonctionnalités de base

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
- [ ] Client et Serveur sous Windows
- [ ] Client et serveur sur des systèmes hétérogènes (serveur linux et client windows)

## LIB NECESSAIRES :


  -PyCrypto


## Roadmap

Deux équipes travaillent en parallèle, l'une sur tout ce qui est connection entre les deux entités, l'autre sur la partie fonctionnement.

Etapes achevés:

- [X] Etape 1 : Serveur multithreadé et connection client basique (echo sans authentification)   
- [X] Etape 2 : Connection par mot de passe - Implémentation des commandes classiques            
- [X] Etape : Comptabilité Windows (client seulement)
- [X] Etape : Ergonomie dans les commandes + test d'exception
- [X] Etape 3 : Connection chiffrée via certificat   
- [X] Etape : Le client peut ajouter des donnees dans les fichiers ~ en mode console
- [X] Etape : Rajouter mkdir et rm
- [X] Autocomplétion
- [X] Dépot de documents
- [X] Création de dossiers ou fichiers avec certains privilèges
- [X] Chiffrement local des documents - Editions de documents 

Etapes en cours:

- [ ] Adaptation windows
- [ ] Client graphique
- [ ] Faire de la place au niveaux des thread
- [ ] Regler probleme de cd : differencier les dossiers /fichier? + si cd dans un fichier -> NOP.
- [ ] commande clear

Etapes futures:

- [ ] Faire de la place au niveaux des thread                
- [ ] Etape : Envoit de flux graphiques             
- [ ] Etape : Ajout de fonctionnalités
