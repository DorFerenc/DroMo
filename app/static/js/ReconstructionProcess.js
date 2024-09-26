class ReconstructionProcess {
    constructor(containerId, apiService) {
        this.container = document.getElementById(containerId);
        this.apiService = apiService;
        this.currentStep = 0;
        this.modelId = null;
        this.steps = [
            {
                title: "Point Cloud Visualization",
                explanation: "We start with a cloud of points in 3D space. These points represent the surface of our object, captured by a special camera. <span class='technical'>[Technical: This point cloud data is preprocessed from a LiDAR camera scan. The DROMO system retrieves this preprocessed visual data, which is already in point cloud form.]</span>",
                dataUrl: '/reconstruction/point_cloud/'
            },
            {
                title: "Initial Mesh Generation",
                explanation: "Next, we connect the dots to create a rough 3D shape. Imagine drawing triangles between nearby points to create a surface. <span class='technical'>[Technical: This step utilizes the 3D Delaunay tetrahedralization algorithm to form a solid mesh representation. This algorithm connects neighboring points in the point cloud to create a network of triangles, effectively enclosing the space captured by the point cloud.]</span>",
                dataUrl: '/reconstruction/initial_mesh/'
            },
            {
                title: "Detailed Mesh Creation",
                explanation: "Now we refine our shape, making it smoother and more accurate. We fill in gaps and smooth out rough areas to better represent the real object. <span class='technical'>[Technical: The system applies algorithms such as Graph Cut Max-Flow to optimally cut the volume and extract the mesh surface. Laplacian filtering is then used to smoothen the mesh, removing local artifacts and imperfections.]</span>",
                dataUrl: '/reconstruction/refined_mesh/'
            },
            {
                title: "Textured Mesh",
                explanation: "Finally, we add color and surface details to make our 3D model look like the real object. It's like painting the model to match the original. <span class='technical'>[Technical: This involves texture mapping techniques. Automatic UV mapping approaches are implemented to minimize texture space usage, while multi-band blending algorithms are employed to blend pixel values from multiple views.]</span>",
                dataUrl: '/reconstruction/textured_mesh/'
            }
        ];

        this.cachedData = {};
        this.setupUI();
        this.setupEventListeners();
    }

    setupUI() {
        this.container.classList.add('reconstruction-process', 'tabcontent');
        this.container.innerHTML = `
            <div class="progress-bar">
                <span class="progress" style="width: 25%;"></span>
            </div>
            <div id="step-container"></div>
            <div class="navigation">
                <button id="prev-step-btn" class="button"><i class="fas fa-chevron-left"></i> Previous</button>
                <button id="next-step-btn" class="button">Next <i class="fas fa-chevron-right"></i></button>
            </div>
        `;
    }

    setupEventListeners() {
        this.prevButton = this.container.querySelector('#prev-step-btn');
        this.nextButton = this.container.querySelector('#next-step-btn');

        this.prevButton.addEventListener('click', () => this.prevStep());
        this.nextButton.addEventListener('click', () => this.nextStep());
    }

    // async showProcess(modelId) {
    //     this.modelId = modelId;
    //     this.container.style.display = 'block';
    //     this.currentStep = 0;
    //     this.updateNavigation();

    //     // Start loading all data asynchronously
    //     this.loadAllStepData();

    //     // Display the first step
    //     this.updateStep(this.currentStep);
    // }

    async showProcess(modelId) {
        if (this.modelId !== modelId) {
            // Only reset and reload if it's a different model
            this.modelId = modelId;
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
            if (!this.cachedData[step.dataUrl + this.modelId]) {
                this.apiService.get(step.dataUrl + this.modelId)
                    .then(data => {
                        this.cachedData[step.dataUrl + this.modelId] = data;
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

        const plotElement = this.container.querySelector(`#plot-${step}`);
        if (plotElement) {
            Plotly.purge(plotElement);
        }

        const data = this.cachedData[this.steps[step].dataUrl + this.modelId];
        if (data) {
            this.createPlot(`plot-${step}`, data);
        } else {
            this.showLoadingIndicator(`plot-${step}`);
        }
    }

    updateStepContent(step) {
        const container = this.container.querySelector('#step-container');
        container.innerHTML = `
            <div class="step">
                <div class="step-number">Step ${step + 1}/${this.steps.length}</div>
                <h2>${this.steps[step].title}</h2>
                <div id="plot-${step}" class="plot"></div>
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
        this.container.querySelector('#step-container').innerHTML = '';
        this.container.querySelector('.progress').style.width = '25%';
        this.currentStep = 0;
        this.updateNavigation();
        this.modelId = null;
        this.cachedData = {}; // Clear the cache when clearing visualization
    }

    hide() {
        this.container.style.display = 'none';
    }
}

export default ReconstructionProcess;