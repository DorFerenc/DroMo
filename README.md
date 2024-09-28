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
3. Open Docker - [(Download separately)](https://www.docker.com/)
4. Run: ```docker compose up --build```
5. GoTo: `localhost:5000`

### Test

1. run: ```docker compose run test pytest```


</br>
</br>
</br>
</br>

# DEV:

### API Endpoint Chart

| Endpoint | Method | Parameters | Response | Codes |
|----------|--------|------------|----------|-------|
| `/api/upload` | POST | `title`: Str (opt)<br>`file`: File | `message`, `visual_data_id` | 200, 400 |
| `/api/visual_datas` | GET | - | Array of visual_data objects | 200 |
| `/api/visual_datas/<id>` | GET | `id`: Str | visual_data object | 200, 404 |
| `/api/visual_datas/<id>` | DELETE | `id`: Str | `message` | 200, 404 |
| `/api/preprocess/<id>` | POST | `id`: Str | Processed visual_data data | 200, 404 |
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
| `/api/models/<id>/obj` | GET | `id`: Str | OBJ file | 200, 404, 500 |
| `/api/reconstruction/point_cloud/<id>` | GET | `id`: Str | Point cloud data | 200, 404 |
| `/api/reconstruction/initial_mesh/<id>` | GET | `id`: Str | Initial mesh data | 200, 400, 404 |
| `/api/reconstruction/refined_mesh/<id>` | GET | `id`: Str | Refined mesh data | 200, 404 |
| `/api/reconstruction/textured_mesh/<id>` | GET | `id`: Str | Textured mesh data | 200, 404 |

### Structure
```
Dromo_Structure/
├── app
│   ├── __init__.py
│   ├── config.py
│   ├── api
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── db
│   │   ├── __init__.py
│   │   └── mongodb.py
│   ├── models
│   │   ├── __init__.py
│   │   ├── point_cloud.py
│   │   ├── threed_model.py
│   │   └── visual_data.py
│   ├── preprocess
│   │   ├── ply_preprocess.py
│   │   └── visual_datas_to_frames.py
│   ├── reconstruction
│   │   ├── __init__.py
│   │   ├── mesh_to_obj_converter.py
│   │   ├── point_cloud_to_mesh.py
│   │   ├── reconstruction_utils.py
│   │   └── texture_mapper.py
│   ├── services
│   │   ├── __init__.py
│   │   ├── preprocess_service.py
│   │   ├── recon_proc_visualization_service.py
│   │   ├── reconstruction_service.py
│   │   └── visual_data_service.py
│   └── static
│       ├── index.html
│       ├── css
│       │   ├── reconstruction-process.css
│       │   └── styles.css
│       └── js
│           ├── ApiService.js
│           ├── DromoUtils.js
│           ├── ModelManager.js
│           ├── ModelViewer.js
│           ├── NotificationSystem.js
│           ├── PointCloudManager.js
│           ├── ReconstructionProcess.js
│           ├── VisualDataManager.js
│           └── main.js
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
│   ├── test_recon_proc_visualization_service.py
│   ├── test_reconstruction_api.py
│   ├── test_reconstruction_service.py
│   ├── test_threed_model_api.py
│   └── test_visualization_api.py
└── uploads
    └── test_ply.ply
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
db.visual_data.find()
db.point_clouds.find()
db.point_clouds.find({}, {name: 1, _id: 0})
```