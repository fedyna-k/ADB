-- REQUETE QUESTION 3

with espagnols as (
    select mid from titles
    where region = 'ES'
)
select distinct primaryName from
   writers left join espagnols on espagnols.mid = writers.mid
   natural join persons
where espagnols.mid is null;
