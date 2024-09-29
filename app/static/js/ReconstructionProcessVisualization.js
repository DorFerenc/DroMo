class ReconstructionProcessVisualization {
    constructor(containerId, apiService) {
        this.container = document.getElementById(containerId);
        this.apiService = apiService;
        this.currentStep = 0;
        this.pointCloudId = null;
        this.steps = [
            {
                title: "Original Point Cloud",
                explanation: "This is the original point cloud data obtained from the 3D scan. <span class='technical'>[Technical: Raw point cloud data]</span>",
                dataKey: 'stage_0_points'
            },
            {
                title: "Generated Mesh",
                explanation: "In this step, we convert the point cloud into a mesh structure. <span class='technical'>[Technical: Point cloud to mesh conversion using triangulation algorithms]</span>",
                dataKey: 'stage_1_mesh'
            },
            {
                title: "Refined Mesh",
                explanation: "Here, we refine the generated mesh to improve its quality and accuracy. <span class='technical'>[Technical: Mesh refinement techniques such as smoothing and hole filling are applied]</span>",
                dataKey: 'stage_2_refined_mesh'
            },
            {
                title: "Textured Mesh",
                explanation: "In this step, we apply texture to the refined mesh to give it a more realistic appearance. <span class='technical'>[Technical: Texture mapping using UV coordinates and color information]</span>",
                dataKey: 'stage_3_textured_mesh'
            }
            // },
            // {
            //     title: "Final OBJ Model",
            //     explanation: "This is the final 3D model in OBJ format, ready for use in various 3D applications. <span class='technical'>[Technical: Conversion to OBJ format with associated material and texture files]</span>",
            //     dataKey: 'stage_4_obj_converter'
            // }
        ];

        this.cachedData = null;
        this.setupUI();
        this.setupEventListeners();
    }

    setupUI() {
        this.container.classList.add('reconstruction-process', 'tabcontent');
        this.container.innerHTML = `
            <div class="progress-bar">
                <span class="progress" style="width: 20%;"></span>
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

    async showProcess(pointCloudId) {
        if (!pointCloudId) {
            console.error('No point cloud ID provided');
            this.showErrorMessage('No point cloud ID provided');
            return;
        }

        try {
            if (this.pointCloudId !== pointCloudId) {
                this.pointCloudId = pointCloudId;
                this.currentStep = 0;
                this.cachedData = null;
                await this.loadReconstructionStages(pointCloudId);
            }

            this.container.style.display = 'block';
            this.updateNavigation();
            this.updateStep(this.currentStep);
        } catch (error) {
            console.error('Error in showProcess:', error);
            this.showErrorMessage(error.message);
        }
    }

    showErrorMessage(message) {
        const container = this.container.querySelector('#step-container');
        container.innerHTML = `
            <div class="error-message">
                <h2>Error</h2>
                <p>${message}</p>
            </div>
        `;
    }

    // async loadReconstructionStages(pointCloudId) {
    //     try {
    //         this.cachedData = await this.apiService.get(`/reconstruction_stages/${pointCloudId}`);
    //     } catch (error) {
    //         console.error('Error loading reconstruction stages:', error);
    //     }
    // }

    async loadReconstructionStages(pointCloudId) {
        try {
            this.cachedData = await this.apiService.get(`/reconstruction_stages/${pointCloudId}`);
        } catch (error) {
            console.error('Error loading reconstruction stages:', error);
            if (error.response && error.response.status === 404) {
                throw new Error(`Point cloud with ID ${pointCloudId} not found. Please check the model and try again.`);
            } else {
                throw new Error('Failed to load reconstruction stages. Please try again later.');
            }
        }
    }

    updateStep(step) {
        this.updateStepContent(step);
        this.container.querySelector('.progress').style.width = `${(step + 1) * (100 / this.steps.length)}%`;

        const plotElement = this.container.querySelector(`#plot-${step}`);
        if (plotElement) {
            Plotly.purge(plotElement);
        }

        if (this.cachedData) {
            const stageData = this.cachedData[this.steps[step].dataKey];
            if (stageData) {
                this.createPlot(`plot-${step}`, this.convertDataToPlotlyFormat(stageData, step));
            } else {
                this.showLoadingIndicator(`plot-${step}`);
            }
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

    convertDataToPlotlyFormat(data, step) {
        switch(step) {
            case 0: // Point Cloud
                return [{
                    type: 'scatter3d',
                    mode: 'markers',
                    x: data.points.map(p => p[0]),
                    y: data.points.map(p => p[1]),
                    z: data.points.map(p => p[2]),
                    marker: {
                        size: 1.5,
                        color: data.colors,
                        opacity: 1
                    }
                }];
            case 1: // Generated Mesh
                return this.createMeshData(data, 'rgb(255, 165, 0)', 'rgb(0, 0, 0)');
            case 2: // Refined Mesh
                return this.createMeshData(data, 'rgb(255, 140, 0)', 'rgb(0, 0, 0)');
            case 3: // Textured Mesh
                return [{
                    type: 'mesh3d',
                    x: data.points.map(v => v[0]),
                    y: data.points.map(v => v[1]),
                    z: data.points.map(v => v[2]),
                    i: data.faces.map(f => f[0]),
                    j: data.faces.map(f => f[1]),
                    k: data.faces.map(f => f[2]),
                    vertexcolor: data.vertex_colors || 'rgb(200, 200, 200)',
                    flatshading: false,
                    lighting: {
                        ambient: 0.8,
                        diffuse: 1,
                        fresnel: 1,
                        specular: 2,
                        roughness: 0.05,
                    },
                    lightposition: {x: 100, y: 200, z: 150},
                    opacity: 1.0
                }];
            default:
                return [];
        }
    }

    createMeshData(meshData, surfaceColor, wireframeColor) {
        const surface = {
            type: 'mesh3d',
            x: meshData.points.map(v => v[0]),
            y: meshData.points.map(v => v[1]),
            z: meshData.points.map(v => v[2]),
            i: meshData.faces.map(f => f[0]),
            j: meshData.faces.map(f => f[1]),
            k: meshData.faces.map(f => f[2]),
            color: surfaceColor,
            flatshading: true,
            lighting: {
                ambient: 0.8,
                diffuse: 0.9,
                fresnel: 0.5,
                specular: 0.5,
                roughness: 0.5,
            },
            lightposition: {x: 100, y: 200, z: 150},
            opacity: 0.7
        };

        const wireframe = {
            type: 'scatter3d',
            mode: 'lines',
            x: [],
            y: [],
            z: [],
            line: {
                color: wireframeColor,
                width: 1
            },
            opacity: 1.0
        };

        for (const face of meshData.faces) {
            for (let i = 0; i < 3; i++) {
                const p1 = meshData.points[face[i]];
                const p2 = meshData.points[face[(i + 1) % 3]];
                wireframe.x.push(p1[0], p2[0], null);
                wireframe.y.push(p1[1], p2[1], null);
                wireframe.z.push(p1[2], p2[2], null);
            }
        }

        return [surface, wireframe];
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
        this.container.querySelector('.progress').style.width = '20%';
        this.currentStep = 0;
        this.updateNavigation();
        this.pointCloudId = null;
        this.cachedData = null;
    }

    hide() {
        this.container.style.display = 'none';
    }
}

export default ReconstructionProcessVisualization;
