import cv2
import numpy as np
import os
from datetime import datetime
from bson import ObjectId
from app.db.mongodb import get_db
from app.models.point_cloud import PointCloud


class StructureFromMotion:
    def __init__(self, image_folder, K=None):
        self.image_folder = image_folder
        self.K = K if K is not None else np.array([[1000, 0, 500], [0, 1000, 500], [0, 0, 1]])
        self.images = []
        self.features = []

    def load_images(self):
        for filename in os.listdir(self.image_folder):
            if filename.endswith(('.png', '.jpg', '.jpeg')):
                img = cv2.imread(os.path.join(self.image_folder, filename))
                if img is not None:
                    self.images.append(img)
        print(f"Loaded {len(self.images)} images.")

    def find_features(self, image):
        sift = cv2.SIFT_create()
        kp, des = sift.detectAndCompute(image, None)
        return kp, des

    def match_features(self, des1, des2):
        bf = cv2.BFMatcher()
        matches = bf.knnMatch(des1, des2, k=2)
        good = [m for m, n in matches if m.distance < 0.7 * n.distance]
        return good

    def triangulate_points(self, P1, P2, pts1, pts2):
        pts1 = np.float32(pts1).reshape(-1, 1, 2)
        pts2 = np.float32(pts2).reshape(-1, 1, 2)
        points_4d = cv2.triangulatePoints(P1, P2, pts1, pts2)
        points_3d = points_4d[:3, :] / points_4d[3, :]
        return points_3d.T

    def reconstruct_3d(self):
        self.features = [self.find_features(img) for img in self.images]
        all_points_3d = []

        for i in range(len(self.images) - 1):
            matches = self.match_features(self.features[i][1], self.features[i + 1][1])
            print(f"Found {len(matches)} matches between images {i} and {i + 1}")

            if len(matches) < 8:
                print(f"Not enough matches between images {i} and {i + 1}. Skipping this pair.")
                continue

            src_pts = np.float32([self.features[i][0][m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
            dst_pts = np.float32([self.features[i + 1][0][m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)

            F, mask = cv2.findFundamentalMat(src_pts, dst_pts, cv2.FM_RANSAC)

            if F is None:
                print(f"Failed to compute fundamental matrix for images {i} and {i + 1}. Skipping this pair.")
                continue

            src_pts = src_pts[mask.ravel() == 1]
            dst_pts = dst_pts[mask.ravel() == 1]

            print(f"Using {src_pts.shape[0]} inlier points for reconstruction between images {i} and {i + 1}")

            E = np.dot(np.dot(np.transpose(self.K), F), self.K)
            _, R, t, _ = cv2.recoverPose(E, src_pts, dst_pts, self.K)

            P1 = np.dot(self.K, np.hstack((np.eye(3), np.zeros((3, 1)))))
            P2 = np.dot(self.K, np.hstack((R, t)))

            points_3d = self.triangulate_points(P1, P2, src_pts, dst_pts)
            all_points_3d.extend(points_3d)

        print(f"Reconstructed {len(all_points_3d)} 3D points in total.")
        return np.array(all_points_3d)

    def save_to_db(self, name='point_cloud'):
        points_3d = self.reconstruct_3d()
        # Convert the points_3d array to a list of dictionaries
        formatted_points = np.array([[float(p[0]), float(p[1]), float(p[2])] for p in points_3d])

        point_cloud = PointCloud(name, formatted_points)
        # Write the point cloud data to a CSV file

        with open('app/points/3d_points.csv', 'w') as f:
            f.write(point_cloud.to_string())

        point_cloud_id = point_cloud.save()
        print(f"3D reconstruction complete. {len(formatted_points)} points saved to the database with ID {point_cloud_id}.")

        return len(formatted_points)
