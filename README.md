# DOCKER DEMO

## Introduction

Docker est une plateforme de conteneurisation qui permet d'exécuter une application dans un environnement isolé et identique sur différentes machines. Une **image Docker** est un modèle qui contient l'application, ses dépendances et sa configuration. Un **conteneur** est une instance d'une image en cours d'exécution. Le **Docker Engine** est le logiciel qui crée, lance et gère les images et les conteneurs sur la machine hôte.

L'objectif est donc de détailler le contenu d'une image grâce à un fichier courrament appelé `Dockerfile`, qui sera utilisé par le moteur Docker pour créé une image. Cette image est peut ensuite être utilisé pour créé un conteneur. Pour utiliser un conteneur, il faut passer son status à up. Il y a deux utilisations d'un conteneur : une utilisation ponctuelle (le conteneur est up, effectue sa tâche, puis est down automatiquement) ou une utilisation continue (le conteneur est up, effectue des tâches de fond et est down par l'utilisateur).

## Installation

Le seul prérequis pour utiliser Docker est d'installer le Docker Engine : 
- Pour linux, il faut directement l'installer https://docs.docker.com/engine/install/.
- Pour WSL, il faut installer Docker Desktop https://docs.docker.com/desktop/setup/install/windows-install/ puis aller dans paramètre en haut à droite > Ressources > WSL Integration

## Dockerfile

Le Dockerfile constitue la base de Docker. Il existe des variations comme le docker-compose même si celui-ci peut être vu comme une manière de gérer plusieurs Dockerfile et enfin il y a Kubernetes qui est le stade la plus avancée de l'utilisation de Docker. Une liste non exauhstive de termes utile à la compréhension et l'écriture d'un Dockerfile sont présentés ici même si en toute transparence, il y a de fortes chances que vos Dockerfile seront écris par quelqu'un d'autre ou par un LLM plus tard. 

Vous pouvez directement sauté cette section et passé à la prochaine si vous pensez déjà connaître ces mots clés ou si vous voulez apprendre Docker directement par de la pratique puis revenir plus tard pour approfondir vos connaissances.

### FROM

Ceci est le premier mot clé de chaque Dockerfile car il définit l'image de base qui sera utilisé. Afin de s'éviter la construction à la main d'une architecture linux complète qui contient tous les logiciels et toutes les installations dont nous pourrions avoir besoin, nous préférons commencer d'un point de départ créé par quelqu'un d'autre. Ces points de départ peuvent être trouvé ici https://hub.docker.com/search?badges=official. **_L'idée d'un Dockerfile est donc d'enrichir une image de base pour atteindre un objectif._**

### RUN

Ce mot clé est omniprésent dans les Dockerfile car il permet d'utiliser des commandes directement dans le conteneur. Il faut voir un Dockerfile comme une séquence d'action qui seront appliqués les une après les autres à la création du conteneur grâce à l'image.

### COPY

Avec `FROM` vous définissez votre base et avec `RUN` vous enrichissez la forme de votre conteneur. Il ne manque plus que pouvoir rajouter du contenu à ce conteneur. Ce mot clé permet de copier un document de la machine hôte pour l'inscrire dans l'image. De cette manière, quand le conteneur sera crée, le même fichier se trouvera dans le conteneur. **_Ces trois mots clés permettent de comprendre 80% du contenu d'un Dockerfile en présupposant certaines bases en `bash`._**

### CMD / ENTRYPOINT

Ces mots clés sont présentés ensemble car leur différence est très subtil donc il est plus simple de les présenter d'un coup puis de comprendre plus tard quand est ce qu'il faut utiliser l'un ou l'autre. Ils s'utilisent tous les deux comme dernier mot clé d'un Dockerfile et ils définissent l'objectif d'un Dockerfile. Il n'est pas autorisé d'utiliser plusieurs de ces mots clés, si vous écrivez deux `CMD` dans un Dockerfile, uniquement le dernier sera utilisé.

## Pratique

Le meilleur moyen d'apprendre ou de se souvenir passe par la pratique. Dans cette section, nous présentons une série de Docker qui permettent de faire un tour de ce qui peut se faire.

### Hello World !

Il est impossible de parler d'un tutoriel de programmation sans faire un `Hello World !`. Le fichier `Dockerfile` qui se trouve dans le dossier `HelloWorld` permet justement de réaliser ça. Il n'est composé que de deux mots clé : `FROM` et `CMD`. L'image de base est `Alpine`, c'est une distribution Linux ultra légère (5MB) car nous ne voulons utiliser uniquement la commande `echo` de bash. Cette dernière est réalisé grâce au mot clé `CMD`.
Commençons par construire (`build`) l'image docker. Vous pouvez exécuter cette commande où `HelloWorld` est le dossier qui contient le Dockerfile : 
```bash
docker build HelloWorld/
```
Si tout se passe bien, vous devriez voir apparaître une ligne indiquant `=> exporting to image`. Vous pouvez donc vérifier que votre image a bien été créé grâce à la commande : 
```bash
docker images
```
Sauf que là, vous devriez ne rien voir. En effet, lorsque vous avez construit votre image, vous ne lui avez pas donné de nom (`tag`). Nous allons donc nommer notre image grâce à l'option `--tag` (-t) suivi du nom de l'image : 
```bash
docker build -t helloworld HelloWorld/
```
Et maintenant, si vous rééssayez cette commande : 
```bash
docker images
```
Vous devriez voir votre image. Super ! Essayons maintenant de lancer un conteneur : 
```bash
docker run helloworld
```
Normalement, vous devriez obtenir un log dans votre terminal.
