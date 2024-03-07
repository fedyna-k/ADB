-- QUERY PLAN

explain query plan

-- Recherche des titres, genres et notes de films
select primaryTitle, originalTitle, genre, averageRating from
    ratings natural join movies natural join genres
where
    -- Films d'horreur de la décénie 2000
    -- La recherche peut être optimisée par index
    genre = 'Horror' and
    -- Celle-ci aussi
    startyear between 2000 and 2009
-- Récupération des trois meilleurs
order by averageRating desc
limit 3;