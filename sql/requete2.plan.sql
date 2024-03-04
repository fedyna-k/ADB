-- QUERY PLAN

explain query plan select primaryTitle, originalTitle, genre, averageRating from
    ratings natural join movies natural join genres
where
    genre = 'Horror' and
    startyear between 2000 and 2009
order by averageRating desc
limit 3;