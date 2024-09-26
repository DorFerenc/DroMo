import DromoUtils from './DromoUtils.js';
import ModelViewer from './ModelViewer.js';

class ModelManager {
    constructor(apiService, notificationSystem, reconstructionProcess) {
        this.apiService = apiService;
        this.notificationSystem = notificationSystem;
        this.reconstructionProcess = reconstructionProcess;
        this.modelList = document.getElementById('modelList');
        this.modelDetails = document.getElementById('modelDetails');
        this.activeModelId = null;
        this.initEventListeners();
    }

    initEventListeners() {
        document.getElementById('refreshModelListBtn').addEventListener('click',
            DromoUtils.debounce(() => this.listModels(), 300));
    }

    async listModels() {
        try {
            const models = await this.apiService.get('/models');
            this.modelList.innerHTML = '';
            models.forEach(model => {
                const li = document.createElement('li');
                li.innerHTML = `
                    <span>Model ID: ${model.id}</span>
                    <div>
                        <button onclick="modelManager.getModelDetails('${model.id}')">Details</button>
                        <button onclick="modelManager.visualizeModel('${model.id}')">Visualize</button>
                        <button onclick="modelManager.downloadModel('${model.id}')">Download OBJ</button>
                        <button onclick="modelManager.downloadTexture('${model.id}')">Download Texture</button>
                        <button onclick="modelManager.downloadMaterial('${model.id}')">Download Material</button>
                        <button class="delete" onclick="modelManager.deleteModel('${model.id}')">Delete</button>
                    </div>
                `;
                this.modelList.appendChild(li);
            });
        } catch (error) {
            this.notificationSystem.show('Error listing 3D models: ' + error.message, 'error');
        }
    }

    async getModelDetails(id) {
        try {
            const model = await this.apiService.get(`/models/${id}`);
            this.modelDetails.innerHTML = `
                <h3>${model.name}</h3>
                <p>ID: ${model.id}</p>
                <p>Location: ${model.folder_path}</p>
                <p>Point Cloud ID: ${model.point_cloud_id}</p>
                <p>OBJ File: ${model.obj_file}</p>
                <p>MTL File: ${model.mtl_file}</p>
                <p>Texture File: ${model.texture_file}</p>
                <p>Created At: ${DromoUtils.formatDate(model.created_at)}</p>
            `;
        } catch (error) {
            this.notificationSystem.show('Error getting 3D model details: ' + error.message, 'error');
        }
    }

    async deleteModel(id) {
        if (confirm('Are you sure you want to delete this 3D model?')) {
            try {
                await this.apiService.delete(`/models/${id}`);
                this.notificationSystem.show('3D model deleted successfully', 'success');
                this.listModels();
            } catch (error) {
                this.notificationSystem.show('Error deleting 3D model: ' + error.message, 'error');
            }
        }
    }

    downloadModel(id) {
        window.location.href = `${this.apiService.baseUrl}/models/${id}/download`;
    }

    downloadTexture(id) {
        window.location.href = `${this.apiService.baseUrl}/models/${id}/texture`;
    }

    downloadMaterial(id) {
        window.location.href = `${this.apiService.baseUrl}/models/${id}/material`;
    }

    async visualizeModel(id) {
        try {

            const modelDetails = await this.apiService.get(`/models/${id}`);
            const { obj_file, mtl_file, texture_file } = modelDetails;

            const viewerContainer = document.getElementById('modelViewer');
            viewerContainer.innerHTML = '';

            if (window.currentModelViewer) {
                window.currentModelViewer.dispose();
            }

            // // Clear old visualization data in ReconstructionProcess
            // this.reconstructionProcess.clearVisualization();
            // Update the active model ID
            this.activeModelId = id;
            // Trigger the reconstruction process visualization
            this.reconstructionProcess.showProcess(id);

            window.currentModelViewer = new ModelViewer('modelViewer');
            await window.currentModelViewer.loadModel(id, obj_file, mtl_file, texture_file);

            // Switch to the ModelTab
            const modelTab = document.querySelector('[data-tab="ModelTab"]');
            if (modelTab) {
                modelTab.click();
            }
        } catch (error) {
            this.notificationSystem.show('Error visualizing 3D model: ' + error.message, 'error');
        }
    }

    // check if there's an active reconstruction
    hasActiveReconstruction() {
        return this.activeModelId !== null;
    }

    // restore the reconstruction process
    restoreReconstructionProcess() {
        if (this.hasActiveReconstruction()) {
            this.reconstructionProcess.showProcess(this.activeModelId);
        }
    }
}

export default ModelManager;