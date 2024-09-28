class PointCloudProcessVisualization {
    constructor(containerId, apiService) {
        this.container = document.getElementById(containerId);
        this.apiService = apiService;
        this.currentStep = 0;
        this.pointCloudId = null;
        this.steps = [
            {
                title: "Filtered and Normalized",
                explanation: "In this initial step, we clean and standardize the raw point cloud data. We remove statistical outliers (points that are far from their neighbors), perform voxel downsampling (reducing the number of points while maintaining the overall shape), and estimate surface normals (directions perpendicular to the surface at each point). This prepares the data for further processing. <span class='technical'>[Technical: Statistical outlier removal, voxel grid filtering, and normal estimation using PCA are applied.]</span>",
                dataUrl: '/preprocess/filtered_ply/'
            },
            {
                title: "Remove Background",
                explanation: "Here, we separate the main object from its background. We use a plane segmentation algorithm to identify and remove the largest flat surface (usually the ground or table). Then, we cluster the remaining points to isolate the main object. <span class='technical'>[Technical: RANSAC plane segmentation is used with adaptive thresholding based on object height. DBSCAN clustering is then applied to identify the main object cluster.]</span>",
                dataUrl: '/preprocess/removed_background_ply/'
            },
            {
                title: "Bottom Surface",
                explanation: "Often, 3D scans miss the bottom of objects where they contact the surface they're sitting on. In this step, we artificially create this missing bottom surface. We compute a convex hull of the object, sample its surface, and then extract and add a flat bottom. <span class='technical'>[Technical: Convex hull computation, surface sampling, and planar surface generation are used to create a realistic object bottom.]</span>",
                dataUrl: '/preprocess/bottom_surface_ply/'
            },
            {
                title: "Complete Object",
                explanation: "This final step shows the fully preprocessed object, combining all previous steps. The point cloud now represents a complete 3D model of the scanned object, with background removed and bottom surface added. This preprocessed point cloud is ready for further 3D modeling or analysis tasks. <span class='technical'>[Technical: This is the result of all previous preprocessing steps combined, providing a clean, complete point cloud representation of the object.]</span>",
                dataUrl: '/preprocess/complete_object_ply/'
            }
        ];

        this.cachedData = {};
        this.setupUI();
        this.setupEventListeners();
    }

    setupUI() {
        this.container.classList.add('point-cloud-process', 'tabcontent');
        this.container.innerHTML = `
            <div class="progress-bar">
                <span class="progress" style="width: 25%;"></span>
            </div>
            <div id="pc-step-container"></div>
            <div class="navigation">
                <button id="pc-prev-step-btn" class="button"><i class="fas fa-chevron-left"></i> Previous</button>
                <button id="pc-next-step-btn" class="button">Next <i class="fas fa-chevron-right"></i></button>
            </div>
        `;
    }

    setupEventListeners() {
        this.prevButton = this.container.querySelector('#pc-prev-step-btn');
        this.nextButton = this.container.querySelector('#pc-next-step-btn');

        this.prevButton.addEventListener('click', () => this.prevStep());
        this.nextButton.addEventListener('click', () => this.nextStep());
    }


    async showProcess(pointCloudId) {
        if (this.pointCloudId !== pointCloudId) {
            // Only reset and reload if it's a different model
            this.pointCloudId = pointCloudId;
            this.currentStep = 0;
            this.cachedData = {};
            // Start loading all data asynchronously
            this.loadAllStepData();
        }

        this.container.style.display = 'block';
        this.updateNavigation();
        // Display the first step
        this.updateStep(this.currentStep);
    }

    loadAllStepData() {
        this.steps.forEach((step, index) => {
            if (!this.cachedData[step.dataUrl + this.pointCloudId]) {
                this.apiService.get(step.dataUrl + this.pointCloudId)
                    .then(data => {
                        this.cachedData[step.dataUrl + this.pointCloudId] = data;
                        if (index === this.currentStep) {
                            this.updateStep(this.currentStep);
                        }
                    })
                    .catch(error => {
                        console.error(`Error loading data for step ${index + 1}:`, error);
                    });
            }
        });
    }

    updateStep(step) {
        this.updateStepContent(step);
        this.container.querySelector('.progress').style.width = `${(step + 1) * (100 / this.steps.length)}%`;

        const plotElement = this.container.querySelector(`#pc-plot-${step}`);
        if (plotElement) {
            Plotly.purge(plotElement);
        }

        const data = this.cachedData[this.steps[step].dataUrl + this.pointCloudId];
        if (data) {
            this.createPlot(`pc-plot-${step}`, data);
        } else {
            this.showLoadingIndicator(`pc-plot-${step}`);
        }
    }

    updateStepContent(step) {
        const container = this.container.querySelector('#pc-step-container');
        container.innerHTML = `
            <div class="step">
                <div class="step-number">Step ${step + 1}/${this.steps.length}</div>
                <h2>${this.steps[step].title}</h2>
                <div id="pc-plot-${step}" class="plot"></div>
                <div class="explanation">${this.steps[step].explanation}</div>
            </div>
        `;
    }

    createPlot(elementId, data) {
        const layout = {
            scene: {
                aspectmode: 'data',
                xaxis: {title: 'X'},
                yaxis: {title: 'Y'},
                zaxis: {title: 'Z'},
                camera: {
                    eye: {x: 1.5, y: 1.5, z: 1.5}
                }
            },
            margin: {l: 0, r: 0, t: 0, b: 0}
        };
        Plotly.newPlot(elementId, data, layout);
    }

    showLoadingIndicator(elementId) {
        const element = document.getElementById(elementId);
        element.innerHTML = `
            <div class="loading-indicator">
                <div class="spinner"></div>
                <p>Loading data...</p>
            </div>
        `;
    }

    nextStep() {
        if (this.currentStep < this.steps.length - 1) {
            this.currentStep++;
            this.updateStep(this.currentStep);
            this.updateNavigation();
        }
    }

    prevStep() {
        if (this.currentStep > 0) {
            this.currentStep--;
            this.updateStep(this.currentStep);
            this.updateNavigation();
        }
    }

    updateNavigation() {
        this.prevButton.disabled = this.currentStep === 0;
        this.nextButton.disabled = this.currentStep === this.steps.length - 1;
    }

    clearVisualization() {
        this.container.querySelector('#pc-step-container').innerHTML = '';
        this.container.querySelector('.progress').style.width = '25%';
        this.currentStep = 0;
        this.updateNavigation();
        this.pointCloudId = null;
        this.cachedData = {};
    }

    hide() {
        this.container.style.display = 'none';
    }

}

export default PointCloudProcessVisualization;