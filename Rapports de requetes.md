# Rapport de requêtes

> L'ensemble des requêtes a été effectué sur le même ordinateur sur la base `imdb-full` afin de ne pas induire de biais dans les mesures.

## Requete 1

### Sans index

**Temps d'execution** : 203.829 secondes

**Plan de requête** :
```
QUERY PLAN
|--SCAN characters     <-- Optimisable
|--SEARCH persons USING INDEX sqlite_autoindex_PERSONS_1 (pid=?)
|--SEARCH movies USING INDEX sqlite_autoindex_MOVIES_1 (mid=?)
`--USE TEMP B-TREE FOR DISTINCT
```

### Indexée

On rajoute deux index :
|Table|colonne|
|:-:|:-:|
|persons|primaryname|
|characters|pid|

**Temps d'execution** : 0.024 secondes

**Plan de requête** :
```
QUERY PLAN
|--SEARCH persons USING INDEX nom (primaryName=?)
|--SEARCH characters USING INDEX pidind (pid=?)
|--SEARCH movies USING INDEX sqlite_autoindex_MOVIES_1 (mid=?)
`--USE TEMP B-TREE FOR DISTINCT
```

## Requete 2

### Sans index

**Temps d'execution** : 3.638 secondes

**Plan de requête** :
```
QUERY PLAN
|--SCAN genres <-- Optimisable
|--SEARCH movies USING INDEX sqlite_autoindex_MOVIES_1 (mid=?)
|--SEARCH ratings USING AUTOMATIC COVERING INDEX (mid=?)
`--USE TEMP B-TREE FOR ORDER BY
```

### Indexée

On rajoute deux index :
|Table|colonne|
|:-:|:-:|
|genres|genre|
|ratings|mid|

**Temps d'execution** : 0.795 secondes

**Plan de requête** : 
```
QUERY PLAN
|--SEARCH genres USING INDEX genreind (genre=?)
|--SEARCH movies USING INDEX sqlite_autoindex_MOVIES_1 (mid=?)
|--SEARCH ratings USING INDEX midind (mid=?)
`--USE TEMP B-TREE FOR ORDER BY
```

## Requete 3

### Non indexée

**Temps d'execution** : 146.885 secondes (avec `.output out.txt`)

**Plan de requête** :
```
QUERY PLAN
|--MATERIALIZE espagnols
|  `--SCAN titles
|--SCAN persons USING INDEX nom
|--SEARCH writers USING AUTOMATIC COVERING INDEX (pid=?)
`--SEARCH espagnols USING AUTOMATIC COVERING INDEX (mid=?) LEFT-JOIN
```

### Indexée

On rajoute deux index :
|Table|colonne|
|:-:|:-:|
|titles|region|
|writers|pid|

> La requête utilise l'index `nom` créé pour la requête 1 lors de son scan des `primaryName`

**Temps d'execution** : 6.885 secondes

**Plan de requête** :
```
QUERY PLAN
|--MATERIALIZE espagnols
|  `--SEARCH titles USING INDEX title_reg (region=?)
|--SCAN persons USING INDEX nom
|--SEARCH writers USING INDEX writer_pid (pid=?)
`--SEARCH espagnols USING AUTOMATIC COVERING INDEX (mid=?) LEFT-JOIN
```

## Requete 4

### Non indexée

**Temps d'exécution** : 258.720 secondes

**Plan de requête** : 
```
QUERY PLAN
|--MATERIALIZE differentroles
|  |--SCAN characters
|  |--SEARCH persons USING INDEX sqlite_autoindex_PERSONS_1 (pid=?)
|  `--USE TEMP B-TREE FOR GROUP BY
|--SCAN differentroles
|--LIST SUBQUERY 3
|  |--MATERIALIZE maxroles
|  |  `--SEARCH differentroles
|  `--SCAN maxroles 
`--USE TEMP B-TREE FOR DISTINCT
```

> `maxroles` étant de taille 1, un `SCAN` effectué dessus est en réalité un test d'égalité.

### Indexée

On rajoute un index :
|Table|colonne|
|:-:|:-:|
|characters|(mid, pid)|

**Temps d'exécution** : 202.248 secondes

**Plan de requête** : 
```
QUERY PLAN
|--MATERIALIZE differentroles
|  |--SCAN characters USING COVERING INDEX charac_pmid
|  |--SEARCH persons USING INDEX sqlite_autoindex_PERSONS_1 (pid=?)
|  `--USE TEMP B-TREE FOR GROUP BY
|--SCAN differentroles
|--LIST SUBQUERY 3
|  |--MATERIALIZE maxroles
|  |  `--SEARCH differentroles
|  `--SCAN maxroles
`--USE TEMP B-TREE FOR DISTINCT
```

## Requete 5

### Non indexée

**Temps d'exécution** : 339.564 secondes

**Plan de requête** : 
```
QUERY PLAN
|--SCAN principals
|--SEARCH persons USING INDEX sqlite_autoindex_PERSONS_1 (pid=?)
|--LIST SUBQUERY 5
|  |--MATERIALIZE connus
|  |  `--COMPOUND QUERY
|  |     |--LEFT-MOST SUBQUERY
|  |     |  |--MATERIALIZE connusap
|  |     |  |  |--SCAN ratings
|  |     |  |  |--SEARCH movies USING INDEX sqlite_autoindex_MOVIES_1 (mid=?)
|  |     |  |  |--SEARCH principals USING AUTOMATIC COVERING INDEX (mid=?)
|  |     |  |  `--USE TEMP B-TREE FOR DISTINCT
|  |     |  `--SCAN connusap
|  |     `--EXCEPT USING TEMP B-TREE
|  |        |--MATERIALIZE connusav
|  |        |  |--SCAN ratings
|  |        |  |--SEARCH movies USING INDEX sqlite_autoindex_MOVIES_1 (mid=?)
|  |        |  |--SEARCH principals USING AUTOMATIC COVERING INDEX (mid=?)
|  |        |  `--USE TEMP B-TREE FOR DISTINCT
|  |        `--SCAN connusav
|  `--SCAN connus
|--SEARCH movies USING INDEX sqlite_autoindex_MOVIES_1 (mid=?)
`--USE TEMP B-TREE FOR ORDER BY
```

### Indexée

On rajoute deux index :
|Table|colonne|
|:-:|:-:|
|ratings|numVotes|
|principals|pid|

**Temps d'execution** : 18.714 secondes

**Plan de requête** : 
```
QUERY PLAN
|--SEARCH persons USING INDEX sqlite_autoindex_PERSONS_1 (pid=?)
|--LIST SUBQUERY 5
|  |--MATERIALIZE connus
|  |  `--COMPOUND QUERY
|  |     |--LEFT-MOST SUBQUERY
|  |     |  |--MATERIALIZE connusap
|  |     |  |  |--SEARCH ratings USING INDEX rat_num (numVotes>?)
|  |     |  |  |--SEARCH movies USING INDEX sqlite_autoindex_MOVIES_1 (mid=?)
|  |     |  |  |--SEARCH principals USING INDEX prin_mid (mid=?)
|  |     |  |  `--USE TEMP B-TREE FOR DISTINCT
|  |     |  `--SCAN connusap
|  |     `--EXCEPT USING TEMP B-TREE
|  |        |--MATERIALIZE connusav
|  |        |  |--SEARCH ratings USING INDEX rat_num (numVotes>?)
|  |        |  |--SEARCH movies USING INDEX sqlite_autoindex_MOVIES_1 (mid=?)
|  |        |  |--SEARCH principals USING INDEX prin_mid (mid=?)
|  |        |  `--USE TEMP B-TREE FOR DISTINCT
|  |        `--SCAN connusav
|  `--SCAN connus
|--SEARCH principals USING INDEX prin_pid (pid=?)
|--SEARCH movies USING INDEX sqlite_autoindex_MOVIES_1 (mid=?)
`--USE TEMP B-TREE FOR ORDER BY
```

## Conclusion

Les requêtes 3 et 4 ont été mal optimisées par index surement car la structure de la requête SQL en elle même ne permet pas une bonne optimisation.