-- REQUETE QUESTION 4

with differentroles as (
    select count(*) as nbroles, primaryname from
        persons natural join characters
    group by mid, pid
), maxroles as (
    select max(nbroles) from differentroles limit 1
)
select distinct primaryname from differentroles
where nbroles in maxroles;