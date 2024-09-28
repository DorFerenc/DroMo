import DromoUtils from './DromoUtils.js';
import PointCloudProcessVisualization from './PointCloudProcessVisualization.js';

class PointCloudManager {
    constructor(apiService, notificationSystem) {
        this.apiService = apiService;
        this.notificationSystem = notificationSystem;
        this.pointCloudList = document.getElementById('pointCloudList');
        this.pointCloudDetails = document.getElementById('pointCloudDetails');
        this.processVisualization = new PointCloudProcessVisualization('point-cloud-process-container', apiService);
        this.activePointCloudId = null;
        this.initEventListeners();
    }

    init() {
        this.initEventListeners();
        this.listPointClouds();
    }

    initEventListeners() {
        const uploadBtn = document.getElementById('uploadPointCloudBtn');
        const refreshBtn = document.getElementById('refreshPointCloudListBtn');

        if (uploadBtn) {
            uploadBtn.addEventListener('click', () => this.uploadPointCloud());
        }

        if (refreshBtn) {
            refreshBtn.addEventListener('click', () => this.listPointClouds());
        }
    }

    async uploadPointCloud() {
        const name = document.getElementById('pointCloudName').value;
        const file = document.getElementById('pointCloudFile').files[0];

        if (!name || !file) {
            this.notificationSystem.show('Please provide both name and file', 'error');
            return;
        }

        try {
            DromoUtils.validateFileSize(file, 100); // 100MB max file size

            const formData = new FormData();
            formData.append('name', name);
            formData.append('file', file);

            await this.apiService.post('/point_clouds', formData, {
                headers: { 'Content-Type': 'multipart/form-data' }
            });
            this.notificationSystem.show('Point cloud uploaded successfully!', 'success');
            this.listPointClouds();
        } catch (error) {
            this.notificationSystem.show('Error uploading point cloud: ' + error.message, 'error');
        }
    }

    async listPointClouds() {
        try {
            const pointClouds = await this.apiService.get('/point_clouds');
            this.pointCloudList.innerHTML = '';
            pointClouds.forEach(pc => {
                const li = document.createElement('li');
                li.innerHTML = `
                    <span>${DromoUtils.truncateString(pc.name, 30)}</span>
                    <div>
                        <button onclick="pointCloudManager.getPointCloudDetails('${pc.id}')">Details</button>
                        <button onclick="pointCloudManager.visualizePointCloud('${pc.id}')">Visualize</button>
                        <button onclick="pointCloudManager.reconstructPointCloud('${pc.id}')">Reconstruct</button>
                        <button onclick="pointCloudManager.downloadPointCloud('${pc.id}')">Download CSV</button>
                        <button class="delete" onclick="pointCloudManager.deletePointCloud('${pc.id}')">Delete</button>
                    </div>
                `;
                this.pointCloudList.appendChild(li);
            });
        } catch (error) {
            this.notificationSystem.show('Error listing point clouds: ' + error.message, 'error');
        }
    }

    async getPointCloudDetails(id) {
        try {
            const pc = await this.apiService.get(`/point_clouds/${id}`);
            this.pointCloudDetails.innerHTML = `
                <h3>${pc.name}</h3>
                <p>ID: ${pc.id}</p>
                <p>Number of Points: ${pc.num_points}</p>
                <p>Has Colors: ${pc.has_colors}</p>
                <p>Timestamp: ${DromoUtils.formatDate(pc.timestamp)}</p>
            `;
        } catch (error) {
            this.notificationSystem.show('Error getting point cloud details: ' + error.message, 'error');
        }
    }

    async reconstructPointCloud(id) {
        try {
            const response = await this.apiService.post(`/reconstruct/${id}`);
            this.notificationSystem.show(`Reconstruction started. Model ID: ${response.model_id}`, 'success');
        } catch (error) {
            this.notificationSystem.show('Error starting reconstruction: ' + error.message, 'error');
        }
    }

     async visualizePointCloud(id) {
            try {
                const pointCloudDetails = await this.apiService.get(`/point_clouds/${id}`);

                // Clear old visualization data
                this.processVisualization.clearVisualization();

                // Update the active point cloud ID
                this.activePointCloudId = id;

                // Trigger the point cloud process visualization
                this.processVisualization.showProcess(id);

                // Switch to the PointCloudTab
                const pointCloudTab = document.querySelector('[data-tab="PointCloudTab"]');
                if (pointCloudTab) {
                    pointCloudTab.click();
                }
            } catch (error) {
                this.notificationSystem.show('Error visualizing point cloud: ' + error.message, 'error');
            }
    }

    downloadPointCloud(id) {
        window.location.href = `${this.apiService.baseUrl}/point_clouds/${id}/download`;
    }

    async deletePointCloud(id) {
        if (confirm('Are you sure you want to delete this point cloud?')) {
            try {
                await this.apiService.delete(`/point_clouds/${id}`);
                this.notificationSystem.show('Point cloud deleted successfully', 'success');
                this.listPointClouds();
            } catch (error) {
                this.notificationSystem.show('Error deleting point cloud: ' + error.message, 'error');
            }
        }
    }

    hasActiveVisualization() {
        return this.activePointCloudId !== null;
    }

    // restore the point cloud process visualization
    restoreProcessVisualization() {
        if (this.hasActiveVisualization()) {
            this.processVisualization.showProcess(this.activePointCloudId);
        }
    }

}

export default PointCloudManager;