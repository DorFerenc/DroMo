import * as THREE from 'three';
import { MTLLoader } from 'three/addons/loaders/MTLLoader.js';
import { OBJLoader } from 'three/addons/loaders/OBJLoader.js';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

class ModelViewer {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.scene = new THREE.Scene();
        this.camera = new THREE.PerspectiveCamera(75, this.container.clientWidth / this.container.clientHeight, 0.1, 1000);
        this.renderer = new THREE.WebGLRenderer({ antialias: true });
        this.renderer.setSize(this.container.clientWidth, this.container.clientHeight);
        this.container.appendChild(this.renderer.domElement);

        this.camera.position.set(0, 0, 5);
        this.cameraTarget = new THREE.Vector3(0, 0, 0);
        this.camera.lookAt(this.cameraTarget);

        this.controls = new OrbitControls(this.camera, this.renderer.domElement);
        this.setupControls();

        this.addLights();
        this.addAxes();
        this.addGrid();

        this.animate = this.animate.bind(this);
        this.animationFrameId = null;
        this.isRotating = false;
        this.loadedObject = null;

        this.animate();

        this.setupEventListeners();

        console.log('ModelViewer initialized with camera controls');
    }

    setupControls() {
        this.controls.enableDamping = true;
        this.controls.dampingFactor = 0.25;
        this.controls.screenSpacePanning = true;
        this.controls.panSpeed = 0.8;
        this.controls.maxPolarAngle = Math.PI;
        this.controls.minDistance = 0.1;
        this.controls.maxDistance = 50;

        this.controls.mouseButtons = {
            LEFT: THREE.MOUSE.ROTATE,
            MIDDLE: THREE.MOUSE.DOLLY,
            RIGHT: THREE.MOUSE.PAN
        };

        this.controls.keys = {
            LEFT: 'ArrowLeft',
            UP: 'ArrowUp',
            RIGHT: 'ArrowRight',
            BOTTOM: 'ArrowDown'
        };
    }

    addLights() {
        const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
        this.scene.add(ambientLight);

        const directionalLight = new THREE.DirectionalLight(0xffffff, 0.5);
        directionalLight.position.set(0, 1, 0);
        this.scene.add(directionalLight);
    }

    addAxes() {
        this.axes = new THREE.AxesHelper(5);
        this.scene.add(this.axes);
    }

    addGrid() {
        this.grid = new THREE.GridHelper(10, 10);
        this.scene.add(this.grid);
    }

    async loadModel(modelId, objFile, mtlFile, textureFile) {
        console.log('Loading model:', { modelId, objFile, mtlFile, textureFile });
        const mtlLoader = new MTLLoader();
        const objLoader = new OBJLoader();
        const textureLoader = new THREE.TextureLoader();

        try {
            const materials = await mtlLoader.loadAsync(`/api/models/${modelId}/material`);
            materials.preload();

            const texture = await textureLoader.loadAsync(`/api/models/${modelId}/texture`);

            Object.values(materials.materials).forEach(material => {
                if (material.map) {
                    material.map = texture;
                    material.map.image.src = `/api/models/${modelId}/texture`;
                }
            });

            objLoader.setMaterials(materials);

            const object = await objLoader.loadAsync(`/api/models/${modelId}/obj`);

            object.traverse((child) => {
                if (child instanceof THREE.Mesh) {
                    child.material = materials.materials[child.material.name];
                }
            });

            if (this.loadedObject) {
                this.scene.remove(this.loadedObject);
            }
            this.loadedObject = object;

            this.centerModel();

            this.scene.add(object);
            console.log('Object added to scene');

            this.resetCamera();
            this.controls.update();
            console.log('Camera and controls updated');
        } catch (error) {
            console.error('Error loading 3D model:', error);
            throw error;
        }
    }

    centerModel() {
        if (this.loadedObject) {
            const box = new THREE.Box3().setFromObject(this.loadedObject);
            const center = box.getCenter(new THREE.Vector3());
            this.loadedObject.position.sub(center);

            this.cameraTarget.copy(center);
            this.camera.lookAt(this.cameraTarget);
            this.controls.target.copy(this.cameraTarget);

            const size = box.getSize(new THREE.Vector3());
            const maxDim = Math.max(size.x, size.y, size.z);
            const fov = this.camera.fov * (Math.PI / 180);
            let cameraZ = Math.abs(maxDim / 2 / Math.tan(fov / 2));
            this.camera.position.set(0, 0, cameraZ * 1.5);

            this.controls.minDistance = maxDim / 10;
            this.controls.maxDistance = cameraZ * 3;
        }
    }

    resetCamera() {
        if (this.loadedObject) {
            const box = new THREE.Box3().setFromObject(this.loadedObject);
            const size = box.getSize(new THREE.Vector3());
            const maxDim = Math.max(size.x, size.y, size.z);
            const fov = this.camera.fov * (Math.PI / 180);
            let cameraZ = Math.abs(maxDim / 2 / Math.tan(fov / 2));
            this.camera.position.set(0, 0, cameraZ * 1.5);
            this.camera.lookAt(this.cameraTarget);
            this.controls.target.copy(this.cameraTarget);
            this.controls.update();
        }
    }

    setView(view) {
        if (this.loadedObject) {
            const box = new THREE.Box3().setFromObject(this.loadedObject);
            const size = box.getSize(new THREE.Vector3());
            const maxDim = Math.max(size.x, size.y, size.z);
            const distance = maxDim * 1.5;

            switch (view) {
                case 'front':
                    this.camera.position.set(0, 0, distance);
                    break;
                case 'side':
                    this.camera.position.set(distance, 0, 0);
                    break;
                case 'top':
                    this.camera.position.set(0, distance, 0);
                    break;
            }

            this.camera.lookAt(this.cameraTarget);
            this.controls.target.copy(this.cameraTarget);
            this.controls.update();
        }
    }

    animate() {
        this.animationFrameId = requestAnimationFrame(this.animate);
        this.controls.update();

        if (this.isRotating && this.loadedObject) {
            this.loadedObject.rotation.y += 0.01;
        }

        this.renderer.render(this.scene, this.camera);
    }

    toggleBackground() {
        if (this.scene.background === null) {
            this.scene.background = new THREE.Color(0xffffff);
            this.renderer.setClearColor(0xffffff);
        } else {
            this.scene.background = null;
            this.renderer.setClearColor(0x000000);
        }
    }

    toggleAxes() {
        this.axes.visible = !this.axes.visible;
    }

    toggleGrid() {
        this.grid.visible = !this.grid.visible;
    }

    toggleWireframe() {
        if (this.loadedObject) {
            this.loadedObject.traverse((child) => {
                if (child instanceof THREE.Mesh) {
                    child.material.wireframe = !child.material.wireframe;
                }
            });
        }
    }

    toggleRotation() {
        this.isRotating = !this.isRotating;
    }

    setupEventListeners() {
        const container = this.container.parentElement;

        const createButton = (text, onClick) => {
            const button = document.createElement('button');
            button.textContent = text;
            button.addEventListener('click', onClick);
            container.appendChild(button);
        };

        createButton('Toggle Background', () => this.toggleBackground());
        createButton('Toggle Axes', () => this.toggleAxes());
        createButton('Toggle Grid', () => this.toggleGrid());
        createButton('Toggle Wireframe', () => this.toggleWireframe());
        createButton('Toggle Rotation', () => this.toggleRotation());
        createButton('Reset Camera', () => this.resetCamera());
        createButton('Front View', () => this.setView('front'));
        createButton('Side View', () => this.setView('side'));
        createButton('Top View', () => this.setView('top'));
        createButton('Center Model', () => this.centerModel());
    }

    dispose() {
        console.log('Disposing ModelViewer');
        if (this.animationFrameId) {
            cancelAnimationFrame(this.animationFrameId);
        }

        this.scene.traverse((object) => {
            if (object.geometry) {
                object.geometry.dispose();
            }
            if (object.material) {
                if (Array.isArray(object.material)) {
                    object.material.forEach(material => material.dispose());
                } else {
                    object.material.dispose();
                }
            }
        });

        this.renderer.dispose();

        if (this.renderer.domElement && this.renderer.domElement.parentNode) {
            this.renderer.domElement.parentNode.removeChild(this.renderer.domElement);
        }

        this.controls.dispose();

        // Remove added buttons
        const container = this.container.parentElement;
        while (container.lastChild !== this.container) {
            container.removeChild(container.lastChild);
        }

        console.log('ModelViewer disposed');
    }
}

export default ModelViewer;