import DromoUtils from './DromoUtils.js';
import PointCloudProcessVisualization from './PointCloudProcessVisualization.js';

class PointCloudManager {
    constructor(apiService, notificationSystem, processVisualization) {
        this.apiService = apiService;
        this.notificationSystem = notificationSystem;
        this.processVisualization = processVisualization;
        this.pointCloudList = document.getElementById('pointCloudList');
        this.pointCloudDetails = document.getElementById('pointCloudDetails');
        this.uploadArea = document.getElementById('pointCloudUploadArea');
        this.uploadBtn = document.getElementById('uploadPointCloudBtn');
        this.refreshBtn = document.getElementById('refreshPointCloudListBtn');
        this.fileInput = document.getElementById('pointCloudFile');
        this.nameInput = document.getElementById('pointCloudName');
        this.fileNameElement = this.uploadArea.querySelector('.file-name');
        this.isUploading = false;
        this.activePointCloudId = null;

    }

    init() {
        this.initEventListeners();
        this.listPointClouds();
    }

    initEventListeners() {
        if (this.uploadArea) {
            this.uploadArea.addEventListener('click', () => this.fileInput.click());
            this.uploadArea.addEventListener('dragover', this.handleDragOver.bind(this));
            this.uploadArea.addEventListener('dragleave', this.handleDragLeave.bind(this));
            this.uploadArea.addEventListener('drop', this.handleDrop.bind(this));
        }

        if (this.fileInput) {
            this.fileInput.addEventListener('change', (e) => this.handleFiles(e.target.files));
        }

        if (this.uploadBtn) {
            this.uploadBtn.addEventListener('click', () => this.uploadPointCloud());
        }

        if (this.refreshBtn) {
            this.refreshBtn.addEventListener('click', () => this.listPointClouds());
        }
    }

    handleDragOver(e) {
        e.preventDefault();
        this.uploadArea.classList.add('dragover');
    }

    handleDragLeave() {
        this.uploadArea.classList.remove('dragover');
    }

    handleDrop(e) {
        e.preventDefault();
        this.uploadArea.classList.remove('dragover');
        this.handleFiles(e.dataTransfer.files);
    }

    handleFiles(files) {
        if (files.length > 0) {
            const fileName = files[0].name;
            this.fileNameElement.textContent = fileName;
            this.fileNameElement.style.display = 'block';
            this.fileInput.files = files;
        }
    }

    async uploadPointCloud() {
        if (this.isUploading) {
            this.notificationSystem.show('Upload already in progress', 'info');
            return;
        }

        const name = this.nameInput.value;
        const file = this.fileInput.files[0];

        if (!name || !file) {
            this.notificationSystem.show('Please provide both name and file', 'error');
            return;
        }

        try {
            this.isUploading = true;
            this.uploadBtn.disabled = true;
            this.uploadBtn.textContent = 'Uploading...';

            DromoUtils.validateFileSize(file, 100); // 100MB max file size

            const formData = new FormData();
            formData.append('name', name);
            formData.append('file', file);

            await this.apiService.post('/point_clouds', formData, {
                headers: { 'Content-Type': 'multipart/form-data' }
            });
            this.notificationSystem.show('Point cloud: ' +name + ' uploaded successfully!', 'success');
            this.resetForm();
            this.listPointClouds();
        } catch (error) {
            this.notificationSystem.show('Error uploading point cloud: ' + error.message, 'error');
        } finally {
            this.isUploading = false;
            this.uploadBtn.disabled = false;
            this.uploadBtn.textContent = 'Upload';
        }
    }

    resetForm() {
        this.fileInput.value = '';
        this.nameInput.value = '';
        this.fileNameElement.textContent = '';
        this.fileNameElement.style.display = 'none';
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

                        <button onclick="window.pointCloudManager.getPointCloudDetails('${pc.id}')">Details</button>
                        <button onclick="pointCloudManager.visualizePointCloud('${pc.id}')">Visualize</button>
                        <button onclick="window.pointCloudManager.reconstructPointCloud('${pc.id}')">Reconstruct</button>
                        <button onclick="window.pointCloudManager.downloadPointCloud('${pc.id}')">Download CSV</button>
                        <button class="delete" onclick="window.pointCloudManager.deletePointCloud('${pc.id}')">Delete</button>
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
            this.notificationSystem.show(`Reconstruction completed. Model ID: ${response.model_id}`, 'success');
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
                this.notificationSystem.show('Point cloud:' + id + ' deleted successfully', 'success');
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