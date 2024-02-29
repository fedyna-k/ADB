-- QUERY PLAN

explain query plan with espagnols as (
    select mid from titles
    where region = 'ES'
)
select distinct primaryName from
    persons natural join writers
where mid not in espagnols;

-- REQUETE QUESTION 3

with espagnols as (
    select mid from titles
    where region = 'ES'
)
select distinct primaryName from
    persons natural join writers
where mid not in espagnols;
