"""Service layer for PLY file-related operations."""

from app.models.ply import PLY
from bson import ObjectId
from bson.errors import InvalidId
from app.db.mongodb import get_db

class PLYService:
    """Handles business logic for PLY file operations."""

    @staticmethod
    def create_ply(title, file_path):
        """
        Create a new PLY file entry.

        Args:
            title (str): The title of the PLY file.
            file_path (str): The path where the PLY file is stored.

        Returns:
            str: The ID of the created PLY file.
        """
        ply = PLY(title=title, file_path=file_path)
        return ply.save()

    @staticmethod
    def get_ply(ply_id):
        """
        Retrieve a PLY file by its ID.

        Args:
            ply_id (str): The ID of the PLY file to retrieve.

        Returns:
            dict: The PLY file data if found, None otherwise.
        """
        try:
            return PLY.get_by_id(ply_id)
        except InvalidId:
            return None

    @staticmethod
    def get_all_ply_files():
        """Retrieve all PLY files."""
        db = get_db()
        return list(db.ply_files.find())

    @staticmethod
    def delete_ply(ply_id):
        """
        Delete a PLY file by its ID.

        Args:
            ply_id (str): The ID of the PLY file to delete.

        Returns:
            bool: True if deletion was successful, False otherwise.
        """
        try:
            db = get_db()
            result = db.ply_files.delete_one({'_id': ObjectId(ply_id)})
            return result.deleted_count > 0
        except InvalidId:
            return False
