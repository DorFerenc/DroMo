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
| List all Point Cloud Data | `/api/pointclouds` | GET | None | Array of point cloud objects | 200, 500 |
| Get Point Cloud details | `/api/pointclouds/<id>` | GET | - `id`: String (Point Cloud ID) | Point cloud object | 200, 404, 500 |
| Delete a Point Cloud | `/api/pointclouds/<id>` | DELETE | - `id`: String (Point Cloud ID) | - `message`: Deletion success | 200, 404, 500 |
| Reconstruct 3D Model | `/api/reconstruct/<id>` | POST | - `id`: String (Point Cloud ID) | - `message`: Reconstruction started<br>- `model_id`: String | 200, 404, 500 |
| Monitor Reconstruction Progress | `/api/reconstruct/progress/<id>` | GET | - `id`: String (Model ID) | - `model_id`: String<br>- `progress`: int (0-100)<br>- `status`: String | 200, 404, 500 |
| List all 3D Models | `/api/models` | GET | None | Array of 3D model objects | 200, 500 |
| Get 3D Model details | `/api/models/<id>` | GET | - `id`: String (Model ID) | 3D model object | 200, 404, 500 |
| Display 3D Model | `/api/models/<id>/display` | GET | - `id`: String (Model ID) | - `model_id`: String<br>- `display_data`: Object | 200, 404, 500 |
| Export 3D Model | `/api/models/<id>/export` | GET | - `id`: String (Model ID) | - `model_id`: String<br>- `file_path`: String<br>- `metadata`: Object | 200, 404, 500 |
| Delete a 3D Model | `/api/models/<id>` | DELETE | - `id`: String (Model ID) | - `message`: Deletion success | 200, 404, 500 |

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
db.videos.find()
```