import ApiService from './ApiService.js';
import NotificationSystem from './NotificationSystem.js';
import VisualDataManager from './VisualDataManager.js';
import PointCloudManager from './PointCloudManager.js';
import ModelManager from './ModelManager.js';
import ReconstructionProcess from './ReconstructionProcess.js';
import PointCloudProcessVisualization from './PointCloudProcessVisualization.js';
import ReconstructionProcessVisualization from './ReconstructionProcessVisualization.js';
import AboutUs from './AboutUs.js';

const API_URL = 'http://localhost:5000/api';

document.addEventListener('DOMContentLoaded', async () => {
    const apiService = new ApiService(API_URL);
    const notificationSystem = new NotificationSystem();
    const visualDataManager = new VisualDataManager(apiService, notificationSystem);
    const processVisualization = new PointCloudProcessVisualization('point-cloud-process-container', apiService);
    const pointCloudManager = new PointCloudManager(apiService, notificationSystem, processVisualization);
    // const reconstructionProcess = new ReconstructionProcess('reconstruction-process-container', apiService);
    const reconstructionProcess = new ReconstructionProcessVisualization('reconstruction-process-container', apiService);
    const modelManager = new ModelManager(apiService, notificationSystem, reconstructionProcess);
    const aboutUsRoot = document.getElementById('about-us-root');

    if (aboutUsRoot) {
        // const { createElement } =  await import('react');
        // const { createRoot } =  await import('react-dom/client');
        const { createElement } =  await import('react');
        const { createRoot } =  await import('react-dom/client');
        // const { createElement } = window.React;
        // const { createRoot } = window.ReactDOM;
        const root = createRoot(aboutUsRoot);
        root.render(createElement(AboutUs));
    }

    // Make manager instances globally accessible
    window.visualDataManager = visualDataManager;
    window.pointCloudManager = pointCloudManager;
    window.modelManager = modelManager;
    window.reconstructionProcess = reconstructionProcess;
    window.processVisualization = processVisualization;
    window.notificationSystem = notificationSystem;  // Make notificationSystem globally accessible

    // Initialize managers (if they have init methods)
    visualDataManager.init();
    pointCloudManager.init();
    // if (typeof visualDataManager.init === 'function') visualDataManager.init();
    // if (typeof pointCloudManager.init === 'function') pointCloudManager.init();
    if (typeof modelManager.init === 'function') modelManager.init();

    // Replace any remaining alert() calls with notificationSystem
    window.alert = (message) => {
        notificationSystem.show(message, 'info');
    };

    // Set up tab functionality
    const tabLinks = document.querySelectorAll('.tablinks');
    tabLinks.forEach(tabLink => {
        tabLink.addEventListener('click', (event) => openTab(event, event.target.dataset.tab));
    });

    // Open the first tab by default
    if (tabLinks.length > 0) {
        openTab({ currentTarget: tabLinks[0] }, tabLinks[0].dataset.tab);
    }
});

function openTab(evt, tabName) {
    const tabcontent = document.getElementsByClassName("tabcontent");
    for (let i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }

    const tablinks = document.getElementsByClassName("tablinks");
    for (let i = 0; i < tablinks.length; i++) {
        tablinks[i].classList.remove("active");
    }

    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.classList.add("active");

    // // Handle Tailwind CSS based on tab
    // if (tabName === 'AboutUsTab') {
    //     // manageTailwindCSS.load();
    //     scriptManager.switchToAboutUs();
    // } else {
    //     // manageTailwindCSS.unload();
    //     scriptManager.switchToOtherTabs();
    // }

    // If switching to the ModelTab and there's an active reconstruction, restore it
    if (tabName === 'ModelTab' && modelManager.hasActiveReconstruction()) {
        modelManager.restoreReconstructionProcess();
    }
    // If switching to the PointCloudTab and there's an active visualization, restore it
    if (tabName === 'PointCloudTab' && pointCloudManager.hasActiveVisualization()) {
        pointCloudManager.restoreProcessVisualization();
    }
}

// // Function to manage Tailwind CSS
// const manageTailwindCSS = {
//     styleId: 'tailwindcss',

//     load: () => {
//         if (!document.getElementById(manageTailwindCSS.styleId)) {
//             const script = document.createElement('script');
//             script.id = manageTailwindCSS.styleId;
//             script.src = 'https://cdn.tailwindcss.com';
//             script.async = true;
//             document.head.appendChild(script);
//         }
//     },

//     unload: () => {
//         const script = document.getElementById(manageTailwindCSS.styleId);
//         if (script) {
//             script.remove();
//         }
//     }
// };

// // Script management object
// const scriptManager = {
//     tailwindId: 'tailwindcss',
//     plotlyId: 'plotlyjs',

//     loadTailwind: () => {
//         if (!document.getElementById(scriptManager.tailwindId)) {
//             const script = document.createElement('script');
//             script.id = scriptManager.tailwindId;
//             script.src = 'https://cdn.tailwindcss.com';
//             document.head.appendChild(script);
//         }
//     },

//     loadPlotly: () => {
//         if (!document.getElementById(scriptManager.plotlyId)) {
//             const script = document.createElement('script');
//             script.id = scriptManager.plotlyId;
//             script.src = 'https://cdn.plot.ly/plotly-latest.min.js';
//             document.head.appendChild(script);
//         }
//     },

//     removeTailwind: () => {
//         const script = document.getElementById(scriptManager.tailwindId);
//         if (script) {
//             script.remove();
//         }
//     },

//     switchToAboutUs: () => {
//         scriptManager.removePlotly();
//         scriptManager.loadTailwind();
//     },

//     switchToOtherTabs: () => {
//         scriptManager.removeTailwind();
//         scriptManager.loadPlotly();
//     },

//     removePlotly: () => {
//         const script = document.getElementById(scriptManager.plotlyId);
//         if (script) {
//             script.remove();
//         }
//     }
// };