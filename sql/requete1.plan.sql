-- QUERY PLAN

explain query plan

-- Recherche des titres principaux et originaux
select distinct primaryTitle, originalTitle from
    movies natural join persons natural join characters
-- dans lesquels Jean Reno a joué

-- Ce critère de recherche peut être optimisé avec
-- un index sur la colonne "primaryName"
where primaryName = 'Jean Reno';