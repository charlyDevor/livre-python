.. _hug-tutorial:


=======
``hug``
=======


.. image:: hug.png
   :scale: 50%
   :align: center
   :alt: hug
   

Par Charles Ombang Ndo [#co]_

Introduction
============

Une API (Application Programming Interface) est une façade regroupant des
services qu'une application, offre à d'autres. Ces services sont définis sous
forme de classes, de méthodes et généralement suivis d'une documentation
décrivant le rôle de chaque composant de l'interface, exposant les utilisations
possibles et les normes d'utilisation. La plupart des applications actuelles
offrent ces *web services* plus connues sous RESTful web service.

Dans l'univers Python, la bibliothèque hug_ est un outil assez puissant
permettant d'implémenter une API. L'utilisation de la technologie hug_ pour
créer des APIs en Python est motivée par de nombreux avantages qui seront
détaillés dans un chapitre dédié.


RESTful web service et ``hug``
------------------------------

A l'origine REST (Representational State Transfer) est l'idée de définir un
ensemble de règles qui mises ensemble, permettent de construire une API et
décrivent la manière, donc la communication se passe entre le client et le
serveur. Les dévéloppeurs n'ont plus à écrire leur propre méthode HTTP (GET,
POST..) pour récupérer des données, c'est REST qui va définir de manière unique
les méthodes à utiliser. La conséquence directe est que quelque soit la
technologie employée côté serveur, les règles ne changeront pas, elles seront
tout le temps les mêmes.

Le concept RESTful web service repose sur les ressources qui sont représentées
par les `URLs`. Le client envoie des requêtes via ces URLs au moyen des
méthodes du protocole HTTP, ce sont les verbes:

   - GET: récupération de données,
   - POST: ajout de données
   - PUT: modifications de données
   - DELETE: suppression de données.


Les formats d'échanges sont nombreux. Dans ce chapitre, nous resterons sur du
:ref:`JSON <json-tutorial>`.

Pourquoi choisir ``hug``
------------------------

Les très célèbres frameworks que sont Flask_ et Django_ sont bousculés par les
performances qu'apportent hug_. La bibliothèque hug_ permet d'écrire une API de manière
simplifiée. Les APIs implémentées dans d'autres frameworks peuvent l'être en
quelques lignes avec hug. hug supporte le versioning, il permet la
documentation par le code et il intègre la validation des données.


Fonctionnement
==============

Supposons une simple fonction permettant de faire la somme de deux nombres passés en paramètre.

.. code-block:: python3

    """Simple application effectuant une somme de deux nombres"""

    def somme(val1, val2):
        """Retourne la somme des deux nombres passés en paramètre"""
        return val1 + val2

Pour transformer cette fonction en une simple API, il suffit d'importer la
bibliothèque hug_ et le tour est joué. Le code du fichier ``somme.py``.

.. code-block:: python3

    """Simple application effectuant une somme de deux nombres"""
    import hug

    @hug.get()
    def somme(val1, val2):
      """Retourne la somme des deux nombres passés en paramètre"""
      return val1 + val2


L'exécution du code ci-dessus via la commande.

.. code-block:: console

    $ hug -f somme.py

hug_ lance le serveur sur le port 8000. En entrant l'adresse
``http://localhost:8000`` on a une réponse au format :ref:`JSON <json-tutorial>`. Dans notre exemple

on obtient:


.. code-block:: json

    {
        "404": "The API call you tried to make was not defined. Here's a definition of the API to help you get going :)",
        "documentation": {
        "overview": "Simple API permettant la somme de deux nombres",
            "handlers": {
                "/somme": {
                    "GET": {
                        "usage": "La fonction retourne le résultat obtenu de la somme des deux nombres en param\u00e8tres",
                        "outputs": {
                            "format": "JSON (Javascript Serialized Object Notation)",
                            "content_type": "application/json"
                        },
                        "inputs": {
                            "val1": {
                                "type": "Basic text / string value"
                            },
                            "val2": {
                                "type": "Basic text / string value"
                            }
                        }
                    }
                }
            }
        }
    }


On peut remarquer que la documentation est très claire, la clé overview nous renseigne sur l'objectif de notre API, La clé usage renseigne sur le type de données renvoyées par l'API, dans notre cas, la ligne de code ``@hug.get()`` indique qu'il s'agit d'une requête GET. La suite du bloc :ref:`JSON <json-tutorial>` ci-dessus nous renseigne sur les paramètres de l'API, leurs types et le format de retour.

Maintenant pour voir le résultat de notre (petite) API, il suffit d'entrer dans le navigateur l'adresse suivante:
``localhost:8000/somme?val1=..&val2= ..`` et de passer les valeurs aux paramètres.

``Important``: Les APIs écrit avec hug_ peuvent être accédées depuis la console, pour
cela, il suffit de rajouter ``@hug.cli()`` comme nous l'avons fait avec ``@hug.get()``.


hug et le versioning
====================


Comme souligné auparavant, hug_ supporte et gère très bien le versioning. On peut avoir plusieurs versions de l'API dans la même application.



.. code-block:: python3

    """Simple Exemple du versioning avec hug"""
    import hug

    @hug.get('/echo', versions=1)
    def echo(text):
        return text


    @hug.get('/echo', versions=range(2, 5))
    def echo(text):
        return "Echo: {text}".format(**locals())



Le code ci-dessus montre la façon dont hug_ gère le versioning. Il suffit pour cela d'ajouter dans la méthode GET les versions que l'on veut. C'est une fois de plus assez claire, simple et compréhensible.

On peut déduire du code précédent que l'on a 4 versions. Pour le vérifier, il suffit de mettre dans le navigateur l'adresse http://localhost:8000, on a alors la documentation au format JSON suivante:

.. code-block:: json

    {
        "404": "The API call you tried to make was not defined. Here's a definition of the API to help you get going :)",
        "documentation": {
            "overview": "Simple Exemple du versioning avec hug",
            "version": 4,
            "versions": [
                1,
                2,
                3,
                4
            ],
            "handlers": {
                "/echo": {
                    "GET": {
                        "outputs": {
                            "format": "JSON (Javascript Serialized Object Notation)",
                            "content_type": "application/json"
                        },
                        "inputs": {
                            "text": {
                                "type": "Basic text / string value"
                            }
                        }
                    }
                }
            }
        }
    }


Si on compare ce rendu :ref:`JSON <json-tutorial>` au précédent, on remarque la présence du champ
``version``. La clé ``version`` de valeur 4 indique la version actuelle de l'API et
la clé ``versions`` prend en valeur un tableau listant les différentes versions
de notre API. Pour tester le bon fonctionnement du versioning, on peut écrire
http://localhost:8000/v1/echo?text=toto. Dans cette URL, on spécifie la version
que l'on souhaite utiliser, ici la version v1. En sortie on aura ``toto``, ce qui
correspond bien à la sortie attendue de la version 1. En changeant dans l'URL
juste la version en la remplaçant par v2, v2 ou v4, la sortie est naturellement
celle attendue suivant la version indiquée ``Echo:toto``.


Validation automatique des données
==================================

Il est possible d'ajouter des fonctions aux paramètres de nos méthodes, pour
expliciter comment ils sont validés et transcris en type python. Pour cela, il suffit
de mettre les arguments sous la forme suivante: ``argument:type``. L'avantage de l'utilisation d'une telle
spécification est de clairement indiquer au niveau de la documentation le type
de données attendues. Ceci est connu sous le terme annotations_ en python.

.. code-block:: python3

    """Test de la validation automatique des données"""
    import hug

    @hug.get()
    def annota(text:int):
        return text


Le code ci-dessus montre comment valider les données automatiquement. L'argument de la
fonction ``annota(...)`` est suivi du type int soit ``text::int``. On comprend
aisément que l'argument text est de type int. Vérifions la sortie suivant
l'adresse <http://localhost:8000>.



.. code-block:: json

    {
        "404": "The API call you tried to make was not defined. Here's a definition of the API to help you get going :)",
        "documentation": {
            "overview": "Test de la validation automatique des données",
            "handlers": {
                "/annota": {
                    "GET": {
                        "outputs": {
                            "format": "JSON (Javascript Serialized Object Notation)",
                            "content_type": "application/json"
                        },
                        "inputs": {
                            "text": {
                                "type": "int(x=0) -> integer\nint(x, base=10) -> integer\n\nConvert a number or string to an integer, or         return 0 if no arguments\nare given   If x is a number, return x __int__()   For floating point\nnumbers, this truncates towards zero \n\nIf x is not a number or if base is given, then x must be a string,\nbytes, or bytearray instance representing an integer literal in the\ngiven base   The literal can be preceded by '+' or '-' and be surrounded\nby whitespace   The base defaults to 10   Valid bases are 0 and 2-36 \nBase 0 means to interpret the base from the string as an integer literal \n>>> int('0b100', base=0)\n4"
                            }
                        }
                    }
                }
            }
        }
    }


On voit bien dans le bloc inputs la clé type, on peut clairement voir que
l'entrée est de type int.

Si on entre l'adresse http://localhost:8000/annota?text=salut on a en retour
une belle erreur comme celle ci-dessous:

.. code-block:: json

    {
        "errors": {
            "text": "invalid literal for int() with base 10: 'salut'"
        }
    }


Cette technique qu'apporte la bibliothèque hug_ permet de valider les données automatiquement. Cela est fait
implicitement.



Les directives
==============

Les directives sont globalement des arguments enregistrés pour fournir
automatiquement des valeurs. Un exemple serait meilleur pour expliquer le rôle
des directives. hug_ possède des directives prédéfinies, mais il donne la
possibilité de créer des directives personnalisées.

.. code-block:: python3

    import hug

    @hug.directive()
    def salutation_general(greeting='hi', **kwargs):
        return greeting + ' there!'
    @hug.get()
    def salut_anglais(greeting: salutation_general='hello'):
        return greeting
    @hug.get()
    def salut_americain(greeting: salutation_general):
        return greeting


Ci-dessus, on a créé une directive basée sur la fonction
``salutation_general(..)``. Cette fonction possède un paramètre avec une valeur
par défaut. Si on va à l'adresse http://localhost:8000/salut_anglais on aura en
retour ``hello there``, http://localhost:8000/salut_anglais retournera ``hi
there``. En effet, dans la fonction ``salut_anglais(..)``, on passe la
directive avec une nouvelle valeur par défaut qui est ``hello``. Cela a pour
effet d'écraser la valeur par défaut ``hi``. Par contre la fonction
``salut_americain(..)`` prend en argument la même directive, mais aucune valeur
n'est redéfinie, cela va conserver la valeur par défaut ``hi``.

Utilisation des directives
==========================

Pour utiliser les directives dans nos fonctions, il existe deux méthodes. La
première apparaît clairement, il s'agit de l'utilisation des types annotation
``greeting::directive``. On peut aussi utiliser le préfixe ``hug_`` ce qui
d'après notre exemple précédent deviendra avec la fonction
``salut_americain(...)`` :

.. code-block:: python3

    @hug.get()
    def salut_americain(hug_salutation_general='Yoo man'):
        pass


Il est aussi possible d'ajouter une valeur ``hug_salutation_general='Yoo man'``.

.. note:: il est important d'ajouter ``**kwargs``.

Format de sortie
================

hug_ utilise le JSON comme format par défaut. Heureusement, il offre
la possibilité de définir des formats autres que JSON. Il existe différentes
façons de spécifier le format que l'on veut utiliser

.. code-block:: python3

    hug.API(__name__).output_format = hug.output_format.html

    # Ou

    @hug.default_output_format()
    def my_output_formatter(data, request, response):
        """Format personnalisé."""

    # Ou encore

    @hug.get(output=hug.output_format.html)
    def my_endpoint():
        """Retourne du HTML."""


Il est possible de créer des formats de sortie personnalisés. Cela se passe
comme le montre le code ci-dessous

.. code-block:: python3

    @hug.format.content_type('text/plain')
    def format_as_text(data, request=None, response=None):
        return str(content).encode('utf-8')
        
Le format par défaut est le :ref:`JSON <json-tutorial>`. L'une des technique pour définir un nouveau format par défaut est

``hug.API(__name__).http.output_format = hug.<format cible>`` par exemple format_cible ``output_format.html``

Si on souhaite un format pour une url spécifique et pas toutes les urls, par exemple pour notre méthode somme, on
veut que le format soit en ``html`` on fera:


.. code-block:: python3

    """Simple application effectuant une somme de deux nombres"""
    import hug

    @hug.get(output = hug.output = hug.output_format.html)
    def somme(val1, val2):
      """Retourne la somme des deux nombres passés en paramètre"""
      return "<h1>{}</h1>".format(val1 + val2)
      
      
donc il suffit de spécifier le format dans le get ``@hug.get(output = hug.output = hug.<format cible>)``.

Le routage
----------

C'est la notion qu'on retrouve dans la plupart des frameworks. Il s'agit de
définir des chemins, urls d'accès aux données. Le mécanisme est simplifié, il y'a plusieurs manières
de faire le routage avec la bibliothèque hug_.

Exemple, on crée une route vers notre méthode somme du fichier ``somme.py``

.. code-block:: python3

    """Simple application effectuant une somme de deux nombres"""
    import hug

    @hug.get('/ajout')
    def somme(val1:int, val2:int):
      """Retourne la somme des deux nombres passés en paramètre"""
      return val1 + val2

Avant pour exécuter la méthode somme on entrait l'adresse suivante: http://localhost:8000/somme?val1=..&val2=..
Avec la route indiquée dans ``@hug.get()`` (/ajout) il suffit de remplace dans l'adresse précédente /somme par /ajout
http://localhost:8000/ajout?val1=..&val2=... 

Suivant la taille du projet, l'ajout des routes avec la méthode get peut surcharger le code. Il existe donc une solution,
on peut avoir un fichier dans lequel nos méthodes sont déclarées et un second pour créer des routes.

Dans un autre fichier on va importer la méthode somme du fichier somme.py et créer une route

.. code-block:: python3

    import hug
    import somme

    api = hug.API(__name__)
    hug.get('/ajout')(somme.somme)
    
 Le résultat est le même toujours en entrant cette url http://localhost:8000/ajout?val1=..&val2=..
 
 Un avantage du routage est qu'il permet de bien nommer les urls.
 

Conclusion
==========

La bibliothèque hug_ offre un moyen très simplifié d'écrire des APIs REST.
La syntaxe est assez claire, la documentation bien élaborée depuis le code, le
*versioning* est réalisé en une seule ligne de code.


Bibliographie
-------------

- Site de ``hug``: http://www.hug.rest/
- *Réaliser une API avec Python 3*, par Rémi Alvergnat, http://toilal.github.io/talk-python3-hug/

.. [#co] <charles.ombangndo@he-arc.ch>

.. liens externes.

.. _hug: http://www.hug.rest/
.. _Flask: http://flask.pocoo.org/
.. _Django: https://www.djangoproject.com/
.. _annotations: http://sametmax.com/les-annotations-en-python-3/

