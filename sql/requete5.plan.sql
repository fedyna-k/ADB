-- QUERY PLAN

explain query plan

-- On stocke dans une table temporaire les personnes
-- connus avant la sortie d'Avatar
with connusav as (
    select distinct pid from
        persons natural join principals natural join movies natural join ratings
    where numvotes > 200000 and startyear < 2009
),
-- On stocke dans une table temporaire les personnes
-- connus après la sortie d'Avatar
connusap as (
    select distinct pid from
        persons natural join principals natural join movies natural join ratings
    where numvotes > 200000 and startyear > 2009
),
-- Les nouveaux connus sont la différence entre les connus après
-- et les connus avant Avatar
connus as (
    select distinct pid from connusap except select distinct pid from connusav
)
-- On récupère parmis ces gens, ceux qui ont travaillé sur Avatar
select primaryName from
     persons natural join principals natural join movies
where pid in connus and (primaryTitle = 'Avatar')
-- Le order by ne sert que pour comparer avec MongoDB
order by primaryName;