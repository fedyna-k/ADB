<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>IMDb Explorer - {{movie["titles"]["primary"]}}</title>

    <link rel="stylesheet" href="../assets/styles/main.css">
    <link rel="stylesheet" href="../assets/styles/header.css">
    <link rel="stylesheet" href="../assets/styles/footer.css">
    <link rel="stylesheet" href="../assets/styles/movie.css">

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
        <div id="card">
            <img src="{{image}}" alt="{{movie['titles']['primary']}}">
            <div class="info">
                % if movie["isAdult"]:
                <h2>{{movie["titles"]["primary"]}} <span id="adult-tag">ADULT</span></h2>
                % else:
                <h2>{{movie["titles"]["primary"]}}</h2>
                % end
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
                <p>Writers:</p>
                <p>{{", ".join([w["name"] for w in movie["writers"]])}}</p>
                <p>Directors:</p>
                <p>{{", ".join([w["name"] for w in movie["directors"]])}}</p>
                <h3>Characters</h3>
                % for char in movie["characters"]:
                <p>{{char["actor"]}}</p>
                <p>{{char["name"]}}</p>
                % end
            </div>
        </div>

        % if "episodes" in movie and len(movie["episodes"]):
        <h3>Episodes:</h3>
        <div id="episodes">
            % season = 0
            % for episode in sorted(sorted(movie["episodes"], key=lambda a: a["episodeNumber"]), key=lambda a: a["seasonNumber"]):
            
            % if season != episode["seasonNumber"]:
            % season += 1
            <h4>Season {{season}}</h4>
            % end
            <p>{{episode["episodeNumber"]}}</p>
            <a href="{{episode['mid']}}">{{episode["primaryTitle"]}}</a>
            <p>Released: {{episode["startYear"]}}</p>
            % if episode["runtimeMinutes"]:
            % if int(episode["runtimeMinutes"]) > 60:
            <p>Runtime: {{episode["runtimeMinutes"] // 60}}h{{episode["runtimeMinutes"] % 60}}min</p>
            % else:
            <p>Runtime: {{episode["runtimeMinutes"]}}min</p>
            % end
            % else:
            <p></p>
            % end
            % end
        </div>
        % end

        <h3>Locale:</h3>
        <div id="locale">
            % from flag import get_flag_emoji
            % for locale in sorted(movie["titles"]["locale"], key=lambda a: a["region"]):
            % if len(locale["region"]) == 2:
            <div>
                <p>{{get_flag_emoji(locale["region"])}}</p>
                <p>{{locale["title"]}}</p>
            </div>
            % end
            % end
        </div>
    </section>

    <footer>
        <p>Made with love & coffee by Kevin Fedyna</p>
    </footer>
</body>
</html>