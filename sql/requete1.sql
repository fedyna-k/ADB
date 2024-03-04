-- REQUETE QUESTION 1

select distinct primaryTitle, originalTitle from
    movies natural join persons natural join characters
where primaryName = 'Jean Reno';