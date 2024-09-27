from datetime import datetime
from bson import ObjectId
from app.db.mongodb import get_db
import numpy as np

class PointCloud:
    """Represents a point cloud in the system."""

    def __init__(self, name, points, colors=None):
        """
        Initialize a new PointCloud instance.

        Args:
            name (str): The name of the point cloud.
            points (np.ndarray): Array of shape (N, 3) containing the x, y, z coordinates.
            colors (np.ndarray, optional): Array of shape (N, 3) containing the r, g, b values.
        """
        self.name = name
        self.points = np.array(points)
        self.colors = np.array(colors) if colors is not None else None
        self.timestamp = datetime.utcnow()

    @classmethod
    def from_string(cls, name, data_string):
        """
        Create a PointCloud instance from a string representation.

        Args:
            name (str): The name of the point cloud.
            data_string (str): String representation of the point cloud data.

        Returns:
            PointCloud: A new PointCloud instance.
        """
        lines = data_string.strip().split('\n')[1:]  # Skip header
        data = np.array([list(map(float, line.split(','))) for line in lines])

        if data.shape[1] == 3:
            return cls(name, data)
        elif data.shape[1] == 6:
            return cls(name, data[:, :3], data[:, 3:])
        else:
            raise ValueError("Invalid data format")

    def save(self):
        """
        Save the point cloud to the database.

        Returns:
            str: The ID of the inserted point cloud document.
        """
        db = get_db()
        data = {
            'name': self.name,
            'points': self.points.tolist(),  # Convert numpy array to list
            'timestamp': self.timestamp
        }
        if self.colors is not None:
            data['colors'] = self.colors.tolist()  # Convert numpy array to list

        result = db.point_clouds.insert_one(data)
        return str(result.inserted_id)

    @staticmethod
    def get_by_id(point_cloud_id):
        """
        Retrieve a point cloud by its ID.

        Args:
            point_cloud_id (str): The ID of the point cloud to retrieve.

        Returns:
            PointCloud: The PointCloud instance if found, None otherwise.
        """
        db = get_db()
        try:
            data = db.point_clouds.find_one({'_id': ObjectId(point_cloud_id)})
            if data:
                points = np.array(data['points'])
                colors = np.array(data['colors']) if 'colors' in data else None
                pc = PointCloud(data['name'], points, colors)
                pc.timestamp = data['timestamp']
                return pc
        except:
            return None
        return None

    def to_string(self):
        """
        Convert the point cloud to a string representation.

        Returns:
            str: String representation of the point cloud.
        """
        header = 'x,y,z' if self.colors is None else 'x,y,z,r,g,b'
        data = self.points if self.colors is None else np.hstack((self.points, self.colors))
        return header + '\n' + '\n'.join(','.join(map(str, row)) for row in data)

    def to_csv(self):
        """Convert the point cloud to a CSV string."""
        header = 'x,y,z'
        if self.colors is not None:
            header += ',r,g,b'

        csv_rows = [header]
        for i in range(len(self.points)):
            row = f"{self.points[i][0]},{self.points[i][1]},{self.points[i][2]}"
            if self.colors is not None:
                row += f",{self.colors[i][0]},{self.colors[i][1]},{self.colors[i][2]}"
            csv_rows.append(row)

        return '\n'.join(csv_rows)

    @staticmethod
    def list_all():
        """
        Retrieve all point clouds from the database.

        Returns:
        pymongo.cursor.Cursor: A cursor for all point clouds in the database.
        """
        db = get_db()
        return db.point_clouds.find()


###########################################################################################
# This PointCloud class is designed to handle both colored and non-colored point clouds. Here's a breakdown of its features:

# The __init__ method initializes a PointCloud with a name, points, and optional colors.
# The from_string class method allows creating a PointCloud instance from a string representation, handling both colored and non-colored formats.
# The save method stores the point cloud in the MongoDB database.
# The get_by_id static method retrieves a point cloud from the database by its ID.
# The to_string method converts the point cloud back to its string representation.
###########################################################################################
###########################################################################################