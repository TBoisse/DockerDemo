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

Ces mots clés sont présentés ensemble car leur différence est très subtil donc il est plus simple de les présenter d'un coup puis de comprendre plus tard quand est ce qu'il faut utiliser l'un ou l'autre. Ils s'utilisent tous les deux comme dernier mot clé d'un Dockerfile et ils définissent l'objectif d'un Dockerfile. Il n'est pas autorisé d'utiliser plusieurs d'un de ces mots clés, si vous écrivez deux `CMD` dans un Dockerfile, uniquement le dernier sera utilisé.

Si les différences entre ces deux mots clés vous intéresse, une première est décrite dans la section [Contourner CMD](#contourner-cmd)

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

### Hello World ! 2

Bon, l'exemple d'avant était sympa mais l'image est un peu vide. Essayons de complexifier un peu cette image. Dans l'exemple précedent, nous avions lancer le build de l'image depuis la root de ce projet. Nous allons essayer une nouvelle approche en entrant dans le dossier de ce deuxième projet :
```bash
cd HelloWorld2
```
Nous avons deux fichiers : `main.py` et `Dockerfile`. Le fichier python effectue un simple print. Le Dockerfile récupère l'image `python:3.12-alpine3.23` qui est une image qui contient directement une version python (dans notre cas 3.12) et se base sur la version 3.23 de la distribution Alpine. À la différence du dernier exemple, nous retrouvons le mot clé `COPY`. Ce dernier copie le fichier python et l'intégre à l'image. Nous pouvons build cette image :
```bash
docker build -t helloworld2 .
docker run helloworld2
```

La commande `docker run` permet de mettre up un conteneur en se basant sur une image, cette utilisation est donc ponctuelle pour cette exemple car l'objectif associé à l'image ne demande pas de maintenir le conteneur up.

### L'intérieur d'un Docker

Si vous avez suivi les exemples dans l'ordre, vous devriez déjà être dans le dossier `HelloWorld2` sinon, effectuez cette commande :
```bash
cd HelloWorld2
```
Vous pouvez build l'image présente dans ce dossier :
```bash
docker build -t helloworld2 .
```
Lors de l'introduction, nous avions décrit un Docker comme capable d'exécuter un programme dans un environnement isolé. Nous allons essayer de rentrer à l'intérieur de cet environnement grâce à l'option `--interactive` (-i) qui permet de transmettre ce qui est écrit dans notre terminal au conteneur et à l'option `--tty` (-t) qui permet d'ouvrir un pseudo terminal qui récupère ce qui est envoyé grâce à -i. Le dernier mot de la commande est le terminal qui sera ouvert : sh pour les distributions légères en générale, et bash sinon.
```bash
docker run -it helloworld2 sh
```
Vous vous trouvez maintenant à l'intérieur du conteneur. Vous pouvez voir où vous vous trouver : 
```bash
ls
```
Vous devriez voir une liste de dossier ainsi que le fichier `main.py`. Vous pouvez essayer de l'utiliser : 
```bash
python main.py
```
Si tout s'est bien passé, vous avez obtenu le bon log ! Pour sortir du docker, la commande la plus répandue est `CTRL + D`.

### Contourner CMD

Dans l'explication de chaque mot clé, nous avions dit que `CMD` et `ENTRYPOINT` étaient très proches. Si CMD est utilisé seul, alors il contient toutes les informations pour réaliser l'objectif de l'image. Si ENTRYPOINT est utilisé seul, alors il contient toutes les informations pour réaliser l'objectif de l'image (oui c'est la même chose). Si ENTRYPOINT est présent et CMD est présent, alors CMD correspond aux arguments qui seront donnés à ENTRYPOINT. Par exemple : 
```Dockerfile
ENTRYPOINT ["python"]
CMD ["main.py"]
```
Dans ce cas, CMD contient le nom du fichier python qui est donné à ENTRYPOINT. Dans ce cas, si nous devons utiliser qu'un seul des deux, lequel choisir ?

Un élément de réponse est que CMD est très facilement remplacable dans le terminal. Si vous avez suivi tous les exemples, vous devriez être dans le dossier `HelloWorld2` et vous devriez avoir build l'image de ce dossier, sinon effectuez ces commande : 
```bash
cd HelloWorld2
docker build -t helloworld2 .
```
Cette image ne contient pas d'ENTRYPOINT et ne contient qu'un seul CMD. Si vous appelez :
```bash
docker run helloworld2
```
Vous devriez obtenir le print de "Hello World". Cependant, vous pouvez outrepasser CMD en indiquant une commande après le nom de l'image : 
```bash
docker run helloworld2 ls /
```
Vous devriez voir apparaître tous les dossiers et fichiers présents à la root du conteneur. Si vous avez suivi tous les exemples, vous avez aussi dû remarquer que cette commande est équivalente à être rentré dans le conteneur et d'avoir effectuer la commande ls.

### Projet Python

Petit spoiler avant de commencer cet exercice : vous n'obtiendrez pas les résultats de ce Dockerfile ici, vous devrez attendre l'exercice suivant. Avec cet exercice, nous avons enfin la possibilité de voir un projet Docker basique plutôt complet.

Vous pouvez aller dans le dossier `PythonProject` afin de pouvoir jeter un oeil à tous les fichiers qui seront nécessaire pour construire le projet. L'objectif de ce projet est de générer une image avec n (entier prédifini) points choisis aléatoirement. L'image de base est `python:3.14-slim`, nous utilisons donc la version 3.14 de python sur une distribution Debian Trixie Slim. Nous retrouvons un dossier `src` qui définit une fonction pour générer n points aléatoirement et un fichier `main.py` qui est appelé par CMD du Dockerfile et qui s'occupe d'afficher ces n points. L'affichage de ces points nécessite la librairie `matplotlib`, c'est pour cela que nous avons défini un fichier `requirements.txt` et qui est installé grâce au mot clé `RUN` qui appelle `pip`.

Vous pouvez construire cette image et la nommée `pythonproject`. Cependant, vous remarquerez que rien ne se produit. En tout cas, à première vue car nous allons voir qu'en réalité, il s'est bien passé quelque chose. Pour cela, rentrons dans le docker :
```bash
docker run -it pythonproject bash
```
Une première chose que nous pouvons remarquer est que le dossier dans lequel nous nous trouvons n'est plus `/` comme c'était le cas depuis le début des exemples. Maintenant, l'espace de travail se nomme `/app` et ceci a été défini grâce au mot clé `WORKDIR` dans le Dockerfile. Ceci est souvent une bonne pratique quand vous écrirez des Dockerfile. Vous pouvez effectuer la commande `ls` afin de voir la liste des fichiers présent dans l'espace de travail. Vous devriez voir 2 fichiers (un py et un txt) et un dossier src.

Si vous effectuez la commande 
```bash
python main.py
```
puis que vous effectuez de nouveau la commande `ls` vous verrez qu'un nouveau fichier vient d'apparaître : `random_points.png`. Pourtant, si vous sortez du conteneur et que vous effectuez `ls` vous ne verrez pas cette image png. En effet, nous rappelons qu'un conteneur est sensé être isolé de votre machine ! Comment faire pour récupèrer cette image ???

### Partage de volume

Il est important d'avoir réaliser l'exercice précedent pour réaliser cet exercice. Vous devriez toujours être dans le dossier `PythonProject` et vous devriez avoir une image docker `pythonproject`. Le problème soulevé par le dernier exercice est que le conteneur génère une image png mais qu'elle ne se retrouve pas sur notre machine. Or nous en avons besoin. Nous introduisons le concept de `volume`. En Docker, un volume permet de relier un dossier de la machine hôte avec un dossier du conteneur. De cette manière, tous les fichiers créés, supprimées ou modifées dans le dossier du conteneur se retrouve dans le dossier de la machine hôte et inversement. Nous allons donc utiliser ce concept pour récupèrer notre image png grâce à l'option --volume (-v) de Docker qui attend le dossier hôte puis le dossier conteneur séparé par un `:` :
```bash
docker run -v .:/app pythonproject
```
Normalement, si vous faîtes `ls` vous verrez l'image png sur votre machine !