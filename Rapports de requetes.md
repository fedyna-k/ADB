# Rapport de requêtes

## Requete 1

### Sans index

**Temps d'execution** : 123.983 secondes

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

**Temps d'execution** : 0.005 secondes

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

**Temps d'execution** : 0.717 secondes

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

**Temps d'execution** : 10.782 secondes (avec `.output out.txt`)

**Plan de requête** :
```
QUERY PLAN
|--SCAN writers
|--LIST SUBQUERY 2
|  |--SCAN titles
|  `--SEARCH movies USING COVERING INDEX sqlite_autoindex_MOVIES_1 (mid=?)
|--SEARCH persons USING INDEX sqlite_autoindex_PERSONS_1 (pid=?)
|--SEARCH movies USING COVERING INDEX sqlite_autoindex_MOVIES_1 (mid=?)
`--USE TEMP B-TREE FOR DISTINCT
```

