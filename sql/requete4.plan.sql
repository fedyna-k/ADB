-- QUERY PLAN

explain query plan

-- Table temporaire qui compte le nombre de rôles
-- différents dans un même film, pour un même acteur
with differentroles as (
    select count(*) as nbroles, primaryname from
        persons natural join characters
    group by mid, pid
),
-- On stocke le maximum de la table d'au dessus
-- dans une table temporaire
maxroles as (
    select max(nbroles) from differentroles limit 1
)
select distinct primaryname from differentroles
-- Ici le "in" est en réalité un simple test d'égalité
-- l'opérateur SCAN est donc rapide.
where nbroles in maxroles;