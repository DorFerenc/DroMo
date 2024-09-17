from app.db.mongodb import get_db
from bson import ObjectId
from datetime import datetime

class ThreeDModel:
    def __init__(self, name, folder_path, point_cloud_id, obj_file, mtl_file, texture_file, id=None):
        self.id = id
        self.name = name
        self.folder_path = folder_path
        self.point_cloud_id = point_cloud_id
        self.obj_file = obj_file
        self.mtl_file = mtl_file
        self.texture_file = texture_file
        self.created_at = datetime.utcnow()

    def save(self):
        db = get_db()
        model_data = {
            "name": self.name,
            "folder_path": self.folder_path,
            "point_cloud_id": self.point_cloud_id,
            "obj_file": self.obj_file,
            "mtl_file": self.mtl_file,
            "texture_file": self.texture_file,
            "created_at": self.created_at
        }
        if self.id:
            db.threed_models.update_one({"_id": ObjectId(self.id)}, {"$set": model_data})
        else:
            result = db.threed_models.insert_one(model_data)
            self.id = str(result.inserted_id)
        return self.id

    @staticmethod
    def get_by_id(model_id):
        db = get_db()
        model_data = db.threed_models.find_one({"_id": ObjectId(model_id)})
        if model_data:
            return ThreeDModel(
                id=str(model_data["_id"]),
                name=model_data["name"],
                folder_path=model_data["folder_path"],
                point_cloud_id=model_data["point_cloud_id"],
                obj_file=model_data["obj_file"],
                mtl_file=model_data["mtl_file"],
                texture_file=model_data["texture_file"]
            )
        return None

    @staticmethod
    def get_all():
        db = get_db()
        models = []
        for model_data in db.threed_models.find():
            models.append(ThreeDModel(
                id=str(model_data["_id"]),
                name=model_data["name"],
                folder_path=model_data["folder_path"],
                point_cloud_id=model_data["point_cloud_id"],
                obj_file=model_data["obj_file"],
                mtl_file=model_data["mtl_file"],
                texture_file=model_data["texture_file"]
            ))
        return models

    @staticmethod
    def delete(model_id):
        db = get_db()
        result = db.threed_models.delete_one({"_id": ObjectId(model_id)})
        return result.deleted_count > 0