class PointCloudProcessVisualization {
    constructor(containerId, apiService) {
        this.container = document.getElementById(containerId);
        this.apiService = apiService;
        this.currentStep = 0;
        this.pointCloudId = null;
        this.steps = [
            {
                title: "Original pointCloud",
                explanation: "test </span>",
                dataUrl: '/preprocess/original_ply/'
            },
            {
                title: "Filtered and Normalized",
                explanation: "test </span>",
                dataUrl: '/preprocess/filtered_ply/'
            },
            {
                title: "Remove Background",
                explanation: "test </span>",
                dataUrl: '/preprocess/removed_background_ply/'
            },
            {
                title: "Bottom Surface ",
                explanation: "test </span>",
                dataUrl: '/preprocess/bottom_surface_ply/'
            },
            {
                title: "Complete object",
                explanation: "test </span>",
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