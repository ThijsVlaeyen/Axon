# WhistleWarden

WhistleWarden is a Flask-based web application that tracks the Spotify songs played in our office and logs the ones our boss whistles along to! This fun project integrates with the Spotify API and uses a lightweight SQLite database to store song history.

## Features

- **Track Song Whistles**: Automatically logs songs when the boss whistles along.
- **Spotify Integration**: Uses the Spotify API to fetch currently playing songs.
- **Song History**: Stores and manages song history in an SQLite database.
- **Multiple Accounts**: Support for tracking multiple Spotify accounts.

## Technologies Used 

- **Flask**: Backend framework for routing and server-side logic.
- **Spotipy**: A lightweight Python library for the Spotify Web API.
- **SQLite**: Local database to store song history.
- **Python-dotenv**: For managing environment variables securely.
