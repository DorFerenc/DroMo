class ReconstructionProcess {
    constructor(containerId, apiService) {
        this.container = document.getElementById(containerId);
        this.apiService = apiService;
        this.currentStep = 0;
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
        this.loadingStates = this.steps.map(() => true);

        this.setupUI();
        this.setupEventListeners();
    }

    setupUI() {
        this.container.classList.add('reconstruction-process', 'section', 'collapsible');
        this.container.innerHTML = `
            <h2>3D Object Reconstruction Process <button class="collapse-btn"><i class="fas fa-chevron-up"></i></button></h2>
            <div class="content">
                <div class="progress-bar">
                    <span class="progress" style="width: 25%;"></span>
                </div>
                <div id="step-container"></div>
                <div id="loader" class="loader hidden"></div>
                <div class="navigation">
                    <button id="prev-step-btn" class="button"><i class="fas fa-chevron-left"></i> Previous</button>
                    <button id="clear-cache-btn" class="button"><i class="fas fa-sync"></i> Clear Cache</button>
                    <button id="next-step-btn" class="button">Next <i class="fas fa-chevron-right"></i></button>
                </div>
            </div>
        `;
    }

    setupEventListeners() {
        this.prevButton = this.container.querySelector('#prev-step-btn');
        this.nextButton = this.container.querySelector('#next-step-btn');
        this.clearCacheButton = this.container.querySelector('#clear-cache-btn');
        this.collapseButton = this.container.querySelector('.collapse-btn');

        this.prevButton.addEventListener('click', () => this.prevStep());
        this.nextButton.addEventListener('click', () => this.nextStep());
        this.clearCacheButton.addEventListener('click', () => this.clearCache());

        // Add collapsible functionality
        const content = this.container.querySelector('.content');
        this.collapseButton.addEventListener('click', (e) => {
            e.stopPropagation();
            this.container.classList.toggle('collapsed');
            this.collapseButton.querySelector('i').classList.toggle('fa-chevron-down');
            this.collapseButton.querySelector('i').classList.toggle('fa-chevron-up');
        });

        // Allow clicking on the entire header to collapse/expand
        this.container.querySelector('h2').addEventListener('click', (e) => {
            if (e.target !== this.collapseButton && e.target !== this.collapseButton.querySelector('i')) {
                this.collapseButton.click();
            }
        });
    }

    async showProcess(modelId) {
        this.modelId = modelId;
        this.container.style.display = 'block';
        this.currentStep = 0;
        this.updateNavigation();
        await this.updateStep(this.currentStep);
        // Ensure the section is expanded when showing the process
        this.container.classList.remove('collapsed');
        this.collapseButton.querySelector('i').classList.remove('fa-chevron-down');
        this.collapseButton.querySelector('i').classList.add('fa-chevron-up');
    }

    async updateStep(step) {
        this.updateStepContent(step);
        this.container.querySelector('.progress').style.width = `${(step + 1) * (100 / this.steps.length)}%`;

        if (this.cachedData[this.steps[step].dataUrl + this.modelId]) {
            this.createPlot(`plot-${step}`, this.cachedData[this.steps[step].dataUrl + this.modelId]);
        } else {
            await this.loadStepData(step);
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

    async loadStepData(step) {
        if (!this.loadingStates[step]) return; // Already loaded

        try {
            const data = await this.apiService.get(this.steps[step].dataUrl + this.modelId);
            this.cachedData[this.steps[step].dataUrl + this.modelId] = data;
            this.createPlot(`plot-${step}`, data);
        } catch (error) {
            console.error('Error loading step data:', error);
        }

        this.loadingStates[step] = false;
        this.updateLoaderVisibility();
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

    updateLoaderVisibility() {
        const isAnyStepLoading = this.loadingStates.some(state => state);
        this.container.querySelector('#loader').style.display = isAnyStepLoading ? 'block' : 'none';
    }

    async nextStep() {
        if (this.currentStep < this.steps.length - 1) {
            this.currentStep++;
            await this.updateStep(this.currentStep);
            this.updateNavigation();
        }
    }

    async prevStep() {
        if (this.currentStep > 0) {
            this.currentStep--;
            await this.updateStep(this.currentStep);
            this.updateNavigation();
        }
    }

    updateNavigation() {
        this.prevButton.disabled = this.currentStep === 0;
        this.nextButton.disabled = this.currentStep === this.steps.length - 1;
    }

    async clearCache() {
        try {
            const response = await this.apiService.post('/clear_cache');
            if (response.status === "success") {
                alert(response.message);
                this.cachedData = {};
                this.loadingStates = this.steps.map(() => true);
            } else {
                alert("Failed to clear cache.");
            }
        } catch (error) {
            console.error("Error clearing cache:", error);
            alert("Error clearing cache.");
        }
    }

    hide() {
        this.container.style.display = 'none';
    }
}

export default ReconstructionProcess;