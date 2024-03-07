-- QUERY PLAN

-- Cette requête ne peut pas plus être optimisée par index
-- Après plusieurs tentives sur des requêtes différentes
-- - Utilisation de not in
-- - Jointure gauche exclusive
-- - Operateur except
-- Cette méthode est celle qui fonctionne le plus vite sur la full.

explain query plan

-- Table temporaire contenant tout les films sortis en Espagne
with espagnols as (
    select mid from titles
    -- Cette recherche peut être optimisée par index
    where region = 'ES'
)

-- On effectue une jointure gauche exclusive pour récuperer
-- tous les scénaristes qui n'ont pas écris de films sorti
-- en Espagne
select distinct primaryName from
   writers left join espagnols on espagnols.mid = writers.mid
   natural join persons
where espagnols.mid is null;