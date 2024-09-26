import DromoUtils from './DromoUtils.js';

class VideoManager {
    constructor(apiService, notificationSystem) {
        this.apiService = apiService;
        this.notificationSystem = notificationSystem;
        this.videoList = document.getElementById('videoList');
        this.videoDetails = document.getElementById('videoDetails');
    }

    init() {
        this.initEventListeners();
        this.listVideos();
    }

    initEventListeners() {
        const uploadBtn = document.getElementById('uploadPLYBtn');
        const refreshBtn = document.getElementById('refreshVideoListBtn');

        if (uploadBtn) {
            uploadBtn.addEventListener('click', () => this.uploadPLY());
        }

        if (refreshBtn) {
            refreshBtn.addEventListener('click', () => this.listVideos());
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
            this.listVideos();
        } catch (error) {
            this.notificationSystem.show('Error uploading PLY file: ' + error, 'error');
        }
    }

    async listVideos() {
        try {
            const videos = await this.apiService.get('/videos');
            this.videoList.innerHTML = '';
            videos.forEach(video => {
                const li = document.createElement('li');
                li.innerHTML = `
                    <span>${DromoUtils.truncateString(video.title, 30)}</span>
                    <div>
                        <button onclick="videoManager.getVideoDetails('${video.id}')">Details</button>
                        <button onclick="videoManager.preprocessVideo('${video.id}')">Preprocess</button>
                        <button class="delete" onclick="videoManager.deleteVideo('${video.id}')">Delete</button>
                    </div>
                `;
                this.videoList.appendChild(li);
            });
        } catch (error) {
            this.notificationSystem.show('Error listing videos: ' + error.message, 'error');
        }
    }

    async getVideoDetails(id) {
        try {
            const video = await this.apiService.get(`/videos/${id}`);
            this.videoDetails.innerHTML = `
                <h3>${video.title}</h3>
                <p>ID: ${video.id}</p>
                <p>File Path: ${video.file_path}</p>
                <p>Timestamp: ${DromoUtils.formatDate(video.timestamp)}</p>
            `;
        } catch (error) {
            this.notificationSystem.show('Error getting video details: ' + error.message, 'error');
        }
    }

    async preprocessVideo(id) {
        try {
            const response = await this.apiService.post(`/preprocess/${id}`);
            this.notificationSystem.show(`Preprocessing started. Status: ${response.status}`, 'success');
        } catch (error) {
            this.notificationSystem.show('Error preprocessing video: ' + error.message, 'error');
        }
    }

    async deleteVideo(id) {
        if (confirm('Are you sure you want to delete this video?')) {
            try {
                await this.apiService.delete(`/videos/${id}`);
                this.notificationSystem.show('Video deleted successfully', 'success');
                this.listVideos();
            } catch (error) {
                this.notificationSystem.show('Error deleting video: ' + error.message, 'error');
            }
        }
    }
}

export default VideoManager;