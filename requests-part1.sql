-- REQUETE QUESTION 1

-- select distinct primaryTitle, originalTitle from
--     movies natural join persons natural join characters
-- where primaryName = "Jean Reno";

-- REQUETE QUESTION 2

-- select primaryTitle, originalTitle, genre, averageRating from
--     ratings natural join movies natural join genres
-- where
--     genre = "Horror" and
--     startyear between 2000 and 2009
-- order by averageRating desc
-- limit 3;

-- REQUETE QUESTION 3

-- with espagnols as (
--     select mid from 
--         movies natural join titles
--     where region = "ES"
-- )
-- select distinct primaryName from
--     persons natural join writers natural join movies
-- where mid not in espagnols;

-- REQUETE QUESTION 4

-- with differentroles as (
--     select count(*) as nbroles, primaryname from
--         persons natural join characters
--     group by mid, pid
-- ), maxroles as (
--     select max(nbroles) from differentroles limit 1
-- )
-- select distinct primaryname from differentroles
-- where nbroles in maxroles;

-- REQUETE QUESTION 5

-- with pasconnus as (
--     select distinct pid from
--         persons natural join principals natural join movies natural join ratings
--     where numvotes < 200000 and startyear < 2009
-- ),
-- connus as (
--     select distinct pid from
--         persons natural join principals natural join movies natural join ratings
--     where numvotes > 200000 and startyear > 2009
-- )
-- select primaryName from
--     persons natural join principals natural join movies
-- where pid in pasconnus and pid in connus and primaryTitle = "Avatar"
-- order by primaryName