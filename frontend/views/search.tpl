<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>IMDb Explorer - Search</title>

    <link rel="stylesheet" href="../assets/styles/main.css">
    <link rel="stylesheet" href="../assets/styles/header.css">
    <link rel="stylesheet" href="../assets/styles/footer.css">
    <link rel="stylesheet" href="../assets/styles/search.css">

    <script src="../assets/scripts/searchbar.js" defer></script>
</head>
<body>
    <header>
        <h1><a href="/">IMDb Explorer</a></h1>
        <div id="searchbar">
            <input type="text" placeholder="Search for a movie...">
            <img src="../assets/images/search.svg" alt="search">
        </div>
    </header>

    <section>
        <h2>Search result for {{pattern}}...</h2>
        % if len(movies) == 0:
        <p>No result found...</p>
        % end

        % for movie in movies:
        <article>
            <a href="/{{movie['mid']}}"><img src="{{images[movie['mid']]}}"></a>
            <div>
                % if movie["isAdult"]:
                <h3><a href="/{{movie['mid']}}">{{movie["titles"]["primary"]}}</a><span class="adult-tag">ADULT</span></h3>
                % else:
                <h3><a href="/{{movie['mid']}}">{{movie["titles"]["primary"]}}</a></h3>
                % end
                <div class="info">
                    % if movie["runtimeMinutes"]:
                    % if int(movie["runtimeMinutes"]) > 60:
                    <p>Runtime: </p>
                    <p>{{movie["runtimeMinutes"] // 60}}h{{movie["runtimeMinutes"] % 60}}min</p>
                    % else:
                    <p>Runtime: </p>
                    <p>{{movie["runtimeMinutes"]}}min</p>
                    % end
                    % end
                    % if movie["endYear"]:
                    <p>First aired: </p>
                    <p>{{movie["startYear"]}}</p>
                    <p>Last aired: </p>
                    <p>{{movie["endYear"]}}</p>
                    % else:
                    <p>Release date: </p>
                    <p>{{movie["startYear"]}}</p>
                    % end
                    <p>Genres: </p>
                    <p>{{", ".join(movie["genres"])}}</p>
                    <p>Average rating: </p>
                    % if "averageRating" in movie:
                    <p>{{movie["averageRating"]}}/10 (on {{movie["numVotes"]}} votes)</p>
                    % else:
                    <p>No rating yet...</p>
                    % end
                </div>
            </div>
        </article>
        % end
    </section>

    <footer>
        <p>Made with love & coffee by Kevin Fedyna</p>
    </footer>
</body>
</html>