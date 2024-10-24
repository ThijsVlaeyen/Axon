# Ankathi

Ankathi is a Flask-based web application that tracks the Spotify songs played in our office and logs the ones our boss whistles along to! This fun project integrates with the Spotify API and uses a lightweight SQLite database to store song history.

## Features

- **Track Song Whistles**: Automatically logs songs when the boss whistles along.
- **Spotify Integration**: Uses the Spotify API to fetch currently playing songs.
- **Song History**: Stores and manages song history in an SQLite database.
- **Multiple Accounts**: Support for tracking multiple Spotify accounts.

## TODO

- [ ] Refactor models/database architecture
- [ ] Finish spotify authentication page / refactor auth_services
- [x] Start statistics screen
    - [ ] Clean up statistics screen
    - [ ] Filter on date in statistics
    - [ ] Show whistles per day
- [ ] Only ask questions between 8AM and 17PM
- [ ] Clean up overview screen
- [ ] Visualise data?
- [ ] Predictive model for whistle chance
- [ ] Security whitelist
- [ ] Utils get recommendations of current song playing

## Technologies Used 

- **Flask**: Backend framework for routing and server-side logic.
- **Spotipy**: A lightweight Python library for the Spotify Web API.
- **SQLite**: Local database to store song history.
- **Python-dotenv**: For managing environment variables securely.
