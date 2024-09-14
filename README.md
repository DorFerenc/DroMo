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

### API Endpoint Chart
| Resource | Address | Method | Parameters | Responses | Status Codes |
| -------- | ------- | ------ | ---------- | --------- | ------------ |
| Upload Visual Data | `/api/upload` | POST | - `title`: String<br>- `file`: Multipart Video | - `message`: Upload success<br>- `video_id`: MongoDB ID | 200, 400, 500 |
| List all videos | `/api/videos` | GET | None | Array of video objects | 200, 500 |
| Get video details | `/api/videos/<id>` | GET | - `id`: String (Video ID) | Video object | 200, 404, 500 |
| Delete a video | `/api/videos/<id>` | DELETE | - `id`: String (Video ID) | - `message`: Deletion success | 200, 404, 500 |
| Monitor Progress | `/api/progress/<id>` | GET | - `id`: String (Video ID) | - `video_id`: String<br>- `progress`: int (0-100)<br>- `status`: String | 200, 404, 500 |
| Preprocess Visual Data | `/api/preprocess/<id>` | POST | - `id`: String (Video ID) | - `message`: Preprocessing started<br>- `preprocessed_data_id`: String | 200, 404, 500 |
| Monitor Preprocessing Progress | `/api/preprocess/progress/<id>` | GET | - `id`: String (Preprocessed Data ID) | - `preprocessed_data_id`: String<br>- `progress`: int (0-100)<br>- `status`: String | 200, 404, 500 |
| Reconstruct 3D Model | `/api/reconstruct/<id>` | POST | - `id`: String (Preprocessed Data ID) | - `message`: Reconstruction started<br>- `model_id`: String | 200, 404, 500 |
| Monitor Reconstruction Progress | `/api/reconstruct/progress/<id>` | GET | - `id`: String (Model ID) | - `model_id`: String<br>- `progress`: int (0-100)<br>- `status`: String | 200, 404, 500 |
| Export 3D Model | `/api/export/<id>` | GET | - `id`: String (Model ID) | - `model_id`: String<br>- `file_path`: String<br>- `metadata`: Object | 200, 404, 500 |

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