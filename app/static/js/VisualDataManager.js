import DromoUtils from './DromoUtils.js';

class VisualDataManager {
    constructor(apiService, notificationSystem) {
        this.apiService = apiService;
        this.notificationSystem = notificationSystem;
        this.visualDataList = document.getElementById('visualDataList');
        this.visualDataDetails = document.getElementById('visualDataDetails');
    }

    init() {
        this.initEventListeners();
        this.listVisualDatas();
    }

    initEventListeners() {
        const uploadBtn = document.getElementById('uploadPLYBtn');
        const refreshBtn = document.getElementById('refreshVisualDataListBtn');

        if (uploadBtn) {
            uploadBtn.addEventListener('click', () => this.uploadPLY());
        }

        if (refreshBtn) {
            refreshBtn.addEventListener('click', () => this.listVisualDatas());
        }
    }

    async uploadPLY() {
        const title = document.getElementById('plyTitle').value;
        const file = document.getElementById('plyFile').files[0];

        if (!title || !file) {
            this.notificationSystem.show('Please provide both title and file', 'error');
            return;
        }

        try {
            DromoUtils.validateFileSize(file, 100); // 100MB max file size

            const formData = new FormData();
            formData.append('title', title);
            formData.append('file', file);

            await this.apiService.post('/upload', formData, {
                headers: { 'Content-Type': 'multipart/form-data' }
            });
            this.notificationSystem.show('PLY file uploaded successfully!', 'success');
            this.listVisualDatas();
        } catch (error) {
            this.notificationSystem.show('Error uploading PLY file: ' + error, 'error');
        }
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
                        <button onclick="visualDataManager.getVisualDataDetails('${visual_data.id}')">Details</button>
                        <button onclick="visualDataManager.preprocessVisualData('${visual_data.id}')">Preprocess</button>
                        <button class="delete" onclick="visualDataManager.deleteVisualData('${visual_data.id}')">Delete</button>
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
            this.notificationSystem.show(`Preprocessing started. Status: ${response.status}`, 'success');
        } catch (error) {
            this.notificationSystem.show('Error preprocessing visual_data: ' + error.message, 'error');
        }
    }

    async deleteVisualData(id) {
        if (confirm('Are you sure you want to delete this visual_data?')) {
            try {
                await this.apiService.delete(`/visual_datas/${id}`);
                this.notificationSystem.show('visual_data deleted successfully', 'success');
                this.listVisualDatas();
            } catch (error) {
                this.notificationSystem.show('Error deleting visual_data: ' + error.message, 'error');
            }
        }
    }
}

export default VisualDataManager;