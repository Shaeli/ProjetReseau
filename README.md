# Projet système et réseau
## Application coopérative médicale

***

##Fonctionnalités de base

### Client
- [ ] Saisie Login et mdp
- [ ] Execution des commandes classiques (ls, mv etc..)

### Serveur
- [ ] Authentification des clients
- [ ] Reception et execution des commandes reçues par le(s) client(s)

***

## Fonctionnalités additionnelles
- [ ] Le client peut accepter les flux graphiques du serveur (RDP ou VNC)
- [ ] Création de dossiers ou fichiers avec certains privilèges
- [ ] Utilisation de connexions chiffrées pour le client et le serveur (utilisation de certificats par exemple)
- [ ] Le client peut stocker localement des fichiers chiffrés et les ouvrir sans qu'ils apparaissent en clair sur le poste client
- [ ] Client et Serveur sous Windows
- [ ] Client et serveur sur des systèmes hétérogènes (serveur linux et client windows)

## Roadmap

Deux équipes travaillent en parallèle, l'une sur tout ce qui est connection entre les deux entités, l'autre sur la partie fonctionnement.
- [ ] Etape 1 : Serveur multithreadé et connection client basique (echo sans authentification)    (Moins d'une semaine)
- [ ] Etape 2 : Connection par mot de passe - Implémentation des commandes classiques             (1 semaine)
- [ ] Etape 3 : Connection chiffrée via certificat - Dépot de documents                           (2 semaines)
- [ ] Etape 4 : Chiffrement local des documents - Editions de documents                           (1-2 semaines)
- [ ] Etape 5 : Envoit de flux graphiques - Gestion des droits utilisateurs                       (2 semaines)
- [ ] Etape 6 : Ajout de fonctionnalités
