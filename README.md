# DroMo Project

DroMo is an automated 3D model generation system designed to streamline and automate the process of creating 3D models from captured visuals.

## Getting Started

These instructions will help you set up and run the project on your local machine for development and testing purposes.

### Prerequisites

- Python 3.9+
- Docker
- MongoDb

### Installation

1. Clone the repository:
2. Open MongoDB and Docker
3. ```docker compose build```
4. ```docker compose up```
5. `localhost:5000`

### Test

1. run: ```docker compose run test pytest```

# DEV:

### API Chart

### Structure
```
dromo/
│
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── video.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── video_service.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py
│   └── db/
│       ├── __init__.py
│       └── mongodb.py
├── tests/
│   ├── __init__.py
│   └── test_api.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── run.py
```