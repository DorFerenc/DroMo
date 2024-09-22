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
2. Add a `.env` file in root project with this info:
```
FLASK_APP=run.py
FLASK_ENV=development
MONGODB_URI=mongodb://localhost:27017/dromo
SECRET_KEY=your-secret-key-here
UPLOAD_FOLDER=/app/uploads
```
3. Open MongoDB and Docker
4. ```docker compose build```
5. ```docker compose up```
6. `localhost:5000`

### Test

1. run: ```docker compose run test pytest```

# DEV:

### API Endpoint Chart

| Endpoint | Method | Parameters | Response | Codes |
|----------|--------|------------|----------|-------|
| `/api/upload` | POST | `title`: Str (opt)<br>`file`: File | `message`, `video_id` | 200, 400 |
| `/api/videos` | GET | - | Array of video objects | 200 |
| `/api/videos/<id>` | GET | `id`: Str | Video object | 200, 404 |
| `/api/videos/<id>` | DELETE | `id`: Str | `message` | 200, 404 |
| `/api/preprocess/<id>` | POST | `id`: Str | Processed video data | 200, 404 |
| `/api/preprocess/progress/<id>` | GET | `id`: Str | Progress info | 200, 404 |
| `/api/point_clouds` | POST | `name`: Str (opt)<br>`file`: File | `message`, `point_cloud_id` | 200, 400 |
| `/api/point_clouds` | GET | - | Array of point cloud objects | 200 |
| `/api/point_clouds/<id>` | GET | `id`: Str | Point cloud object | 200, 400, 404 |
| `/api/point_clouds/<id>` | DELETE | `id`: Str | `message` | 200, 400, 404 |
| `/api/point_clouds/<id>/download` | GET | `id`: Str | CSV file | 200, 404, 500 |
| `/api/reconstruct/<id>` | POST | `id`: Str | `message`, `model_id` | 200, 404, 500 |
| `/api/models` | GET | - | Array of 3D model objects | 200 |
| `/api/models/<id>` | GET | `id`: Str | 3D model object | 200, 404 |
| `/api/models/<id>` | DELETE | `id`: Str | `message` | 200, 404, 500 |
| `/api/models/<id>/download` | GET | `id`: Str | OBJ file | 200, 404 |
| `/api/models/<id>/texture` | GET | `id`: Str | Texture file | 200, 404 |
| `/api/models/<id>/material` | GET | `id`: Str | MTL file | 200, 404 |
| `/api/models/<id>/obj` | GET | `id`: Str | OBJ file | 200, 404 |

### Structure
```
├── app
│   ├── __init__.py
│   ├── api
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── config.py
│   ├── db
│   │   ├── __init__.py
│   │   └── mongodb.py
│   ├── models
│   │   ├── __init__.py
│   │   ├── ply.py
│   │   ├── point_cloud.py
│   │   ├── threed_model.py
│   │   └── video.py
│   ├── preprocess
│   │   ├── ply_preprocess.py
│   │   └── videos_to_frames.py
│   ├── reconstruction
│   │   ├── __init__.py
│   │   ├── mesh_to_obj_converter.py
│   │   ├── point_cloud_to_mesh.py
│   │   ├── reconstruction_utils.py
│   │   └── texture_mapper.py
│   ├── services
│   │   ├── __init__.py
│   │   ├── ply_service.py
│   │   ├── preprocess_service.py
│   │   ├── reconstruction_service.py
│   │   └── video_service.py
│   └── static
│       └── index.html
├── Dockerfile
├── README.md
├── docker-compose.yml
├── outputs
├── requirements.txt
├── run.py
├── tests
│   ├── __init__.py
│   ├── ply
│   │   └── input.ply
│   ├── test_api.py
│   ├── test_point_cloud.py
│   ├── test_preprocess.py
│   ├── test_reconstruction_api.py
│   └── test_threed_model_api.py
└── uploads
    └── Mouse-floor.ply
```

### 🚀 Build smarter, not harder! → Upgrade docker speed
To supercharge your Docker builds with faster performance and advanced optimizations, you can enable Docker BuildKit in PowerShell. Here’s how to unlock this feature:

First, activate BuildKit for your current session by running:
```
$env:DOCKER_BUILDKIT=1
```
Then, kick off your Docker build like a pro:
```
docker compose build
```
Want BuildKit always at your fingertips? Add DOCKER_BUILDKIT=1 to your system’s environment variables to ensure your builds are lightning fast—every single time you open a terminal.




### Check in docker mongo
1. Open Docker Desktop on your Windows machine.
2. In the Docker Desktop interface, go to the "Containers" tab.
3. Find the container running your MongoDB instance. It should be named something like "dromo-mongo-1" or similar, based on your docker-compose configuration.
4. Click on the container name to open its details.
5. In the container details view, click on the "Terminal" tab.
6. In the command input field, type `mongosh` and press Enter. This will open a MongoDB shell inside the container.
Once in the MongoDB shell, type the following commands:
```
use dromo
show collections
db.videos.find()
db.point_clouds.find()
db.point_clouds.find({}, {name: 1, _id: 0})
```