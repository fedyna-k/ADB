<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>IMDb Explorer - Search</title>

    <link rel="stylesheet" href="../assets/styles/main.css">
    <link rel="stylesheet" href="../assets/styles/header.css">
    <link rel="stylesheet" href="../assets/styles/footer.css">

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
        % for movie in movies:
        <h3>{{movie["titles"]["primary"]}}</h3>
        % end
    </section>

    <footer>
        <p>Made with love & coffee by Kevin Fedyna</p>
    </footer>
</body>
</html>