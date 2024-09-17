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

| Resource | Address | Method | Parameters | Responses | Status Codes |
| -------- | ------- | ------ | ---------- | --------- | ------------ |
| Upload Visual Data | `/api/upload` | POST | - `title`: String<br>- `file`: Multipart Video | - `message`: Upload success<br>- `video_id`: MongoDB ID | 200, 400, 500 |
| List all videos | `/api/videos` | GET | None | Array of video objects | 200, 500 |
| Get video details | `/api/videos/<id>` | GET | - `id`: String (Video ID) | Video object | 200, 404, 500 |
| Delete a video | `/api/videos/<id>` | DELETE | - `id`: String (Video ID) | - `message`: Deletion success | 200, 404, 500 |
| Monitor Video Processing Progress | `/api/progress/<id>` | GET | - `id`: String (Video ID) | - `video_id`: String<br>- `progress`: int (0-100)<br>- `status`: String | 200, 404, 500 |
| Preprocess Video to Point Cloud | `/api/preprocess/<id>` | POST | - `id`: String (Video ID) | - `message`: Preprocessing started<br>- `point_cloud_id`: String | 200, 404, 500 |
| Monitor Preprocessing Progress | `/api/preprocess/progress/<id>` | GET | - `id`: String (Point Cloud ID) | - `point_cloud_id`: String<br>- `progress`: int (0-100)<br>- `status`: String | 200, 404, 500 |
| Upload Point Cloud | `/api/point_clouds` | POST | - `name`: String<br>- `file`: Multipart File (.txt or .csv) | - `message`: Upload success<br>- `point_cloud_id`: MongoDB ID | 200, 400, 500 |
| List all Point Clouds | `/api/point_clouds` | GET | None | Array of point cloud objects | 200, 500 |
| Get Point Cloud details | `/api/point_clouds/<id>` | GET | - `id`: String (Point Cloud ID) | Point cloud object | 200, 400, 404 |
| Delete a Point Cloud | `/api/point_clouds/<id>` | DELETE | - `id`: String (Point Cloud ID) | - `message`: Deletion success | 200, 400, 404 |
| Reconstruct 3D Model | `/api/reconstruct/<id>` | POST | - `id`: String (Point Cloud ID) | - `message`: Reconstruction started<br>- `model_id`: String | 200, 404, 500 |
| Monitor Reconstruction Progress | `/api/reconstruct/progress/<id>` | GET | - `id`: String (Model ID) | - `model_id`: String<br>- `progress`: int (0-100)<br>- `status`: String | 200, 404, 500 |
| List all 3D Models | `/api/models` | GET | None | Array of 3D model objects | 200, 500 |
| Get 3D Model details | `/api/models/<id>` | GET | - `id`: String (Model ID) | 3D model object | 200, 404, 500 |
| Display 3D Model | `/api/models/<id>/display` | GET | - `id`: String (Model ID) | - `model_id`: String<br>- `display_data`: Object | 200, 404, 500 |
| Export 3D Model | `/api/models/<id>/export` | GET | - `id`: String (Model ID) | - `model_id`: String<br>- `file_path`: String<br>- `metadata`: Object | 200, 404, 500 |
| Delete a 3D Model | `/api/models/<id>` | DELETE | - `id`: String (Model ID) | - `message`: Deletion success | 200, 404, 500 |

### Structure
```
Dromo_Structure/
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
│   │   ├── point_cloud.py
│   │   ├── threed_model.py
│   │   └── video.py
│   ├── reconstruction
│   │   ├── __init__.py
│   │   ├── mesh_to_obj_converter.py
│   │   ├── point_cloud_to_mesh.py
│   │   ├── reconstruction_utils.py
│   │   └── texture_mapper.py
│   ├── services
│   │   ├── __init__.py
│   │   ├── reconstruction_service.py
│   │   └── video_service.py
│   └── static
│       └── index.html
├── Dockerfile
├── README.md
├── docker-compose.yml
├── requirements.txt
├── run.py
├── tests
│   ├── __init__.py
│   ├── test_api.py
│   ├── test_point_cloud.py
│   └── test_reconstruction_api.py
└── uploads
    └── test_video.mp4
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
```