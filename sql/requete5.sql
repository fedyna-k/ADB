-- REQUETE QUESTION 5

with connusav as (
    select distinct pid from
        persons natural join principals natural join movies natural join ratings
    where numvotes > 200000 and startyear < 2009
),
connusap as (
    select distinct pid from
        persons natural join principals natural join movies natural join ratings
    where numvotes > 200000 and startyear > 2009
),
connus as (
    select distinct pid from connusap except select distinct pid from connusav
)
select primaryName from
     persons natural join principals natural join movies
where pid in connus and (primaryTitle = 'Avatar')
order by primaryName;