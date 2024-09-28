import DromoUtils from './DromoUtils.js';

class VisualDataManager {
    constructor(apiService, notificationSystem) {
        this.apiService = apiService;
        this.notificationSystem = notificationSystem;
        this.visualDataList = document.getElementById('visualDataList');
        this.visualDataDetails = document.getElementById('visualDataDetails');
        this.uploadArea = document.getElementById('plyUploadArea');
        this.uploadBtn = document.getElementById('uploadPLYBtn');
        this.refreshBtn = document.getElementById('refreshVisualDataListBtn');
        this.fileInput = document.getElementById('plyFile');
        this.titleInput = document.getElementById('plyTitle');
        this.fileNameElement = this.uploadArea.querySelector('.file-name');
        this.isUploading = false;
    }

    init() {
        this.initEventListeners();
        this.listVisualDatas();
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
            this.uploadBtn.addEventListener('click', () => this.uploadPLY());
        }

        if (this.refreshBtn) {
            this.refreshBtn.addEventListener('click', () => this.listVisualDatas());
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

    async uploadPLY() {
        if (this.isUploading) {
            this.notificationSystem.show('Upload already in progress', 'info');
            return;
        }

        const title = this.titleInput.value;
        const file = this.fileInput.files[0];

        if (!title || !file) {
            this.notificationSystem.show('Please provide both title and file', 'error');
            return;
        }

        try {
            this.isUploading = true;
            this.uploadBtn.disabled = true;
            this.uploadBtn.textContent = 'Uploading...';

            DromoUtils.validateFileSize(file, 100); // 100MB max file size

            const formData = new FormData();
            formData.append('title', title);
            formData.append('file', file);

            await this.apiService.post('/upload', formData, {
                headers: { 'Content-Type': 'multipart/form-data' }
            });
            this.notificationSystem.show('PLY file uploaded successfully!', 'success');
            this.resetForm();
            this.listVisualDatas();
        } catch (error) {
            this.notificationSystem.show('Error uploading PLY file: ' + error, 'error');
        } finally {
            this.isUploading = false;
            this.uploadBtn.disabled = false;
            this.uploadBtn.textContent = 'Upload';
        }
    }

    resetForm() {
        this.fileInput.value = '';
        this.titleInput.value = '';
        this.fileNameElement.textContent = '';
        this.fileNameElement.style.display = 'none';
    }


    async listVisualDatas() {
        try {
            const visual_datas = await this.apiService.get('/visual_datas');
            this.visualDataList.innerHTML = '';
            visual_datas.forEach(visual_data => {
                const li = document.createElement('li');
                li.innerHTML = `
                    <span>${DromoUtils.truncateString(visual_data.title, 30)}</span>
                    <div>
                        <button onclick="window.visualDataManager.getVisualDataDetails('${visual_data.id}')">Details</button>
                        <button onclick="window.visualDataManager.preprocessVisualData('${visual_data.id}')">Preprocess</button>
                        <button class="delete" onclick="window.visualDataManager.deleteVisualData('${visual_data.id}')">Delete</button>
                    </div>
                `;
                this.visualDataList.appendChild(li);
            });
        } catch (error) {
            this.notificationSystem.show('Error listing visual_datas: ' + error.message, 'error');
        }
    }

    async getVisualDataDetails(id) {
        try {
            const visual_data = await this.apiService.get(`/visual_datas/${id}`);
            this.visualDataDetails.innerHTML = `
                <h3>${visual_data.title}</h3>
                <p>ID: ${visual_data.id}</p>
                <p>File Path: ${visual_data.file_path}</p>
                <p>Timestamp: ${DromoUtils.formatDate(visual_data.timestamp)}</p>
            `;
        } catch (error) {
            this.notificationSystem.show('Error getting visual_data details: ' + error.message, 'error');
        }
    }

    async preprocessVisualData(id) {
        try {
            const response = await this.apiService.post(`/preprocess/${id}`);
            if (response && response.status) {
                this.notificationSystem.show(`Preprocessing Completed. Status: ${response.status}`, 'success');
            } else {
                this.notificationSystem.show('Preprocessing Completed', 'success');
            }
        } catch (error) {
            this.notificationSystem.show('Error preprocessing visual_data: ' + error.message, 'error');
        }
    }

    async deleteVisualData(id) {
        if (confirm('Are you sure you want to delete this visual_data?')) {
            try {
                await this.apiService.delete(`/visual_datas/${id}`);
                this.notificationSystem.show('visual_data:' + id + ' deleted successfully', 'success');
                this.listVisualDatas();
            } catch (error) {
                this.notificationSystem.show('Error deleting visual_data: ' + error.message, 'error');
            }
        }
    }
}

export default VisualDataManager;