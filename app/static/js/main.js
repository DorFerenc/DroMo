import ApiService from './ApiService.js';
import NotificationSystem from './NotificationSystem.js';
import VideoManager from './VideoManager.js';
import PointCloudManager from './PointCloudManager.js';
import ModelManager from './ModelManager.js';

const API_URL = 'http://localhost:5000/api';

document.addEventListener('DOMContentLoaded', () => {
    const apiService = new ApiService(API_URL);
    const notificationSystem = new NotificationSystem();
    const videoManager = new VideoManager(apiService, notificationSystem);
    const pointCloudManager = new PointCloudManager(apiService, notificationSystem);
    const modelManager = new ModelManager(apiService, notificationSystem);

    // Make manager instances globally accessible
    window.videoManager = videoManager;
    window.pointCloudManager = pointCloudManager;
    window.modelManager = modelManager;

    // Initialize managers (if they have init methods)
    if (typeof videoManager.init === 'function') videoManager.init();
    if (typeof pointCloudManager.init === 'function') pointCloudManager.init();
    if (typeof modelManager.init === 'function') modelManager.init();

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
}