
# Project Title

Sonder is a mobile app designed to help you make friends with your Spotify music taste. Made by the Gen Z for Gen Z. 


## Features
With Sonder, you will be able to:
- View Profiles with similar music tastes
- Add new Friends
- Chat with Friends
- View Friends Playlists

## Database Design
The ER diagram for the database entities and their relatonships can be viewed [here](https://drawsql.app/teams/polygon/diagrams/sonder)
## API Reference
The complete API documentation for this project can be found in on this [webpage](https://fortunethedev.notion.site/API-Reference-e66dd841f5e64bcabb66bf2bf2a83e13)

## Run Locally

1. Install Python on your machine if you haven't
2. Fork The Repo then clone
```bash
git clone https://github.com/Consumer-Watch/tinder-for-spotify-backend.git

cd tinder-for-spotify
```
3. Create a Virtual Environment for the project

4. Install the Dependencies
```
pip install -r requirements.txt
```

5. To run the project
```
python app.py
```

6. To make migrations on database models
```bash
flask db migrate -m "Migration message"
flask db upgrade
```

