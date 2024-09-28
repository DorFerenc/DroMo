"""Service layer for visual_data-related operations."""

from app.models.visual_data import VisualData
from bson import ObjectId
from bson.errors import InvalidId
from app.db.mongodb import get_db

class VisualDataService:
    """Handles business logic for visual_data operations."""

    @staticmethod
    def create_visual_data(title, file_path):
        """
        Create a new visual_data entry.

        Args:
            title (str): The title of the visual_data.
            file_path (str): The path where the visual_data file is stored.

        Returns:
            str: The ID of the created visual_data.
        """
        visual_data = VisualData(title=title, file_path=file_path)
        return visual_data.save()

    @staticmethod
    def get_visual_data(visual_data_id):
        """
        Retrieve a visual_data by its ID.

        Args:
            visual_data_id (str): The ID of the visual_data to retrieve.

        Returns:
            dict: The visual_data data if found, None otherwise.
        """
        try:
            return VisualData.get_by_id(visual_data_id)
        except InvalidId:
            return None
        # return visual_data.get_by_id(visual_data_id)

    @staticmethod
    def get_all_visual_datas():
        """Retrieve all visual_datas."""
        db = get_db()
        return list(db.visual_datas.find())

    @staticmethod
    def delete_visual_data(visual_data_id):
        """Delete a visual_data by its ID."""
        try:
            db = get_db()
            result = db.visual_datas.delete_one({'_id': ObjectId(visual_data_id)})
            return result.deleted_count > 0
        except InvalidId:
            return False