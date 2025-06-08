// Pet Breed Classifier - JavaScript Implementation with SQL Database Support
class PetBreedClassifier {
    constructor() {
        // Configuration
        this.POSSIBLE_API_URLS = [
            'http://localhost:8000',
            'http://127.0.0.1:8000',
            'http://192.168.1.100:8000',
        ];
        
        // State
        this.selectedFile = null;
        this.previewUrl = null;
        this.isLoading = false;
        this.workingApiUrl = null;
        this.currentStream = null;
        this.facingMode = 'environment';
        this.cameraSupported = false;
        
        // Initialize
        this.init();
    }
    
    init() {
        this.bindElements();
        this.bindEvents();
        this.testApiConnectivity();
        this.checkCameraSupport();
    }
    
    bindElements() {
        // UI Elements
        this.loadingOverlay = document.getElementById('loadingOverlay');
        this.uploadBtn = document.getElementById('uploadBtn');
        this.cameraBtn = document.getElementById('cameraBtn');
        this.fileInput = document.getElementById('fileInput');
        this.uploadArea = document.getElementById('uploadArea');
        this.imagePreview = document.getElementById('imagePreview');
        this.previewImg = document.getElementById('previewImg');
        this.removeImageBtn = document.getElementById('removeImage');
        this.predictBtn = document.getElementById('predictBtn');
        this.errorMessage = document.getElementById('errorMessage');
        
        // Camera elements
        this.cameraSection = document.getElementById('cameraSection');
        this.video = document.getElementById('video');
        this.canvas = document.getElementById('canvas');
        this.captureBtn = document.getElementById('captureBtn');
        this.switchCameraBtn = document.getElementById('switchCameraBtn');
        this.closeCameraBtn = document.getElementById('closeCameraBtn');
        
        // Results elements
        this.resultsSection = document.getElementById('resultsSection');
        this.confidenceMessage = document.getElementById('confidenceMessage');
        this.resultsGrid = document.getElementById('resultsGrid');
    }
    
    bindEvents() {
        // Upload events
        this.uploadBtn.addEventListener('click', () => this.fileInput.click());
        this.fileInput.addEventListener('change', (e) => this.handleFileSelect(e));
        this.uploadArea.addEventListener('click', () => this.fileInput.click());
        this.uploadArea.addEventListener('drop', (e) => this.handleDrop(e));
        this.uploadArea.addEventListener('dragover', (e) => this.handleDragOver(e));
        this.uploadArea.addEventListener('dragenter', (e) => this.handleDragEnter(e));
        this.uploadArea.addEventListener('dragleave', (e) => this.handleDragLeave(e));
        this.removeImageBtn.addEventListener('click', (e) => this.removeImage(e));
        
        // Camera events
        this.cameraBtn.addEventListener('click', () => this.startCamera());
        this.captureBtn.addEventListener('click', () => this.capturePhoto());
        this.switchCameraBtn.addEventListener('click', () => this.switchCamera());
        this.closeCameraBtn.addEventListener('click', () => this.closeCamera());
        
        // Predict button
        this.predictBtn.addEventListener('click', () => this.predictBreed());
        
        // Navigation
        this.bindNavigation();
    }
    
    bindNavigation() {
        const navLinks = document.querySelectorAll('.nav-link');
        navLinks.forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const target = link.getAttribute('href');
                const element = document.querySelector(target);
                if (element) {
                    element.scrollIntoView({ behavior: 'smooth' });
                }
                
                // Update active nav
                navLinks.forEach(nl => nl.classList.remove('active'));
                link.classList.add('active');
            });
        });
    }
    
    async checkCameraSupport() {
        try {
            // Check if getUserMedia is supported
            if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
                this.cameraSupported = false;
                this.showError('Camera is not supported on this device or browser.');
                this.disableCameraButton();
                return;
            }
            
            // Check if we're on HTTPS or localhost (required for camera access)
            const isSecure = location.protocol === 'https:' || 
                           location.hostname === 'localhost' || 
                           location.hostname === '127.0.0.1';
            
            if (!isSecure) {
                this.cameraSupported = false;
                this.showError('Camera access requires HTTPS or localhost. Please use a secure connection.');
                this.disableCameraButton();
                return;
            }
            
            // Try to enumerate devices to check camera availability
            const devices = await navigator.mediaDevices.enumerateDevices();
            const hasCamera = devices.some(device => device.kind === 'videoinput');
            
            if (!hasCamera) {
                this.cameraSupported = false;
                this.showError('No camera detected on this device.');
                this.disableCameraButton();
                return;
            }
            
            this.cameraSupported = true;
            console.log('Camera support detected and available');
            
        } catch (error) {
            console.error('Error checking camera support:', error);
            this.cameraSupported = false;
            this.showError('Unable to check camera availability.');
            this.disableCameraButton();
        }
    }
    
    disableCameraButton() {
        if (this.cameraBtn) {
            this.cameraBtn.disabled = true;
            this.cameraBtn.style.opacity = '0.5';
            this.cameraBtn.style.cursor = 'not-allowed';
            this.cameraBtn.title = 'Camera not available';
        }
    }
    
    showError(message) {
        if (this.errorMessage) {
            this.errorMessage.textContent = message;
            this.errorMessage.style.display = 'block';
            this.errorMessage.style.background = '#ef4444';
            this.errorMessage.style.color = 'white';
            this.errorMessage.style.padding = '1rem';
            this.errorMessage.style.borderRadius = '8px';
            this.errorMessage.style.marginBottom = '1rem';
            
            // Auto-hide after 5 seconds
            setTimeout(() => {
                this.hideError();
            }, 5000);
        }
    }
    
    hideError() {
        if (this.errorMessage) {
            this.errorMessage.style.display = 'none';
            this.errorMessage.textContent = '';
        }
    }
    
    async testApiConnectivity() {
        for (const url of this.POSSIBLE_API_URLS) {
            try {
                const response = await fetch(`${url}/health`, { 
                    method: 'GET',
                    mode: 'cors',
                    headers: {
                        'Accept': 'application/json',
                    }
                });
                if (response.ok) {
                    this.workingApiUrl = url;
                    console.log(`Connected to API at: ${url}`);
                    break;
                }
            } catch (error) {
                console.log(`Failed to connect to ${url}`);
            }
        }
    }
    
    handleFileSelect(event) {
        const file = event.target.files[0];
        if (file && file.type.startsWith('image/')) {
            this.setSelectedFile(file);
            this.hideError();
        } else if (file) {
            this.showError('Please select a valid image file.');
        }
    }
    
    handleDrop(event) {
        event.preventDefault();
        this.uploadArea.classList.remove('dragover');
        
        const file = event.dataTransfer.files[0];
        if (file && file.type.startsWith('image/')) {
            this.setSelectedFile(file);
            this.hideError();
        } else if (file) {
            this.showError('Please drop a valid image file.');
        }
    }
    
    handleDragOver(event) {
        event.preventDefault();
    }
    
    handleDragEnter(event) {
        event.preventDefault();
        this.uploadArea.classList.add('dragover');
    }
    
    handleDragLeave(event) {
        event.preventDefault();
        if (!this.uploadArea.contains(event.relatedTarget)) {
            this.uploadArea.classList.remove('dragover');
        }
    }
    
    setSelectedFile(file) {
        this.selectedFile = file;
        this.previewUrl = URL.createObjectURL(file);
        this.previewImg.src = this.previewUrl;
        this.imagePreview.classList.add('active');
        this.predictBtn.disabled = false;
        this.clearResults();
    }
    
    removeImage(event) {
        event.stopPropagation();
        this.selectedFile = null;
        if (this.previewUrl) {
            URL.revokeObjectURL(this.previewUrl);
            this.previewUrl = null;
        }
        this.imagePreview.classList.remove('active');
        this.predictBtn.disabled = true;
        this.fileInput.value = '';
        this.clearResults();
    }
    
    async startCamera() {
        if (!this.cameraSupported) {
            this.showError('Camera is not supported or available on this device.');
            return;
        }
        
        try {
            // Request camera permission with explicit constraints
            const constraints = {
                video: {
                    facingMode: this.facingMode,
                    width: { ideal: 640 },
                    height: { ideal: 480 }
                },
                audio: false
            };
            
            const stream = await navigator.mediaDevices.getUserMedia(constraints);
            
            this.video.srcObject = stream;
            this.currentStream = stream;
            this.cameraSection.classList.add('active');
            this.hideError();
            
            // Wait for video to be ready
            this.video.addEventListener('loadedmetadata', () => {
                this.video.play();
            });
            
        } catch (error) {
            console.error('Error accessing camera:', error);
            
            let errorMessage = 'Unable to access camera. ';
            
            if (error.name === 'NotAllowedError') {
                errorMessage += 'Camera permission was denied. Please allow camera access and try again.';
            } else if (error.name === 'NotFoundError') {
                errorMessage += 'No camera found on this device.';
            } else if (error.name === 'NotReadableError') {
                errorMessage += 'Camera is already in use by another application.';
            } else if (error.name === 'OverconstrainedError') {
                errorMessage += 'Camera does not support the requested settings.';
            } else if (error.name === 'SecurityError') {
                errorMessage += 'Camera access blocked for security reasons. Please use HTTPS.';
            } else {
                errorMessage += `Error: ${error.message}`;
            }
            
            this.showError(errorMessage);
        }
    }
    
    async switchCamera() {
        if (!this.currentStream) {
            this.showError('No active camera stream to switch.');
            return;
        }
        
        // Stop current stream
        this.currentStream.getTracks().forEach(track => track.stop());
        
        // Switch facing mode
        this.facingMode = this.facingMode === 'user' ? 'environment' : 'user';
        
        try {
            const constraints = {
                video: {
                    facingMode: this.facingMode,
                    width: { ideal: 640 },
                    height: { ideal: 480 }
                },
                audio: false
            };
            
            const stream = await navigator.mediaDevices.getUserMedia(constraints);
            
            this.video.srcObject = stream;
            this.currentStream = stream;
            this.hideError();
            
        } catch (error) {
            console.error('Error switching camera:', error);
            this.showError('Unable to switch camera. Only one camera may be available.');
            
            // Try to restart with original facing mode
            this.facingMode = this.facingMode === 'user' ? 'environment' : 'user';
            this.startCamera();
        }
    }
    
    capturePhoto() {
        if (!this.video || !this.canvas || !this.currentStream) {
            this.showError('Camera not ready for capture.');
            return;
        }
        
        try {
            const ctx = this.canvas.getContext('2d');
            
            // Set canvas dimensions to match video
            this.canvas.width = this.video.videoWidth || 640;
            this.canvas.height = this.video.videoHeight || 480;
            
            // Draw current video frame to canvas
            ctx.drawImage(this.video, 0, 0, this.canvas.width, this.canvas.height);
            
            // Convert canvas to blob and create file
            this.canvas.toBlob((blob) => {
                if (blob) {
                    const timestamp = new Date().getTime();
                    const file = new File([blob], `camera-photo-${timestamp}.jpg`, { 
                        type: 'image/jpeg' 
                    });
                    this.setSelectedFile(file);
                    this.closeCamera();
                    this.hideError();
                } else {
                    this.showError('Failed to capture photo. Please try again.');
                }
            }, 'image/jpeg', 0.8);
            
        } catch (error) {
            console.error('Error capturing photo:', error);
            this.showError('Failed to capture photo. Please try again.');
        }
    }
    
    closeCamera() {
        if (this.currentStream) {
            this.currentStream.getTracks().forEach(track => track.stop());
            this.currentStream = null;
        }
        
        if (this.video) {
            this.video.srcObject = null;
        }
        
        this.cameraSection.classList.remove('active');
    }
    
    showLoading() {
        this.isLoading = true;
        this.loadingOverlay.classList.add('active');
    }
    
    hideLoading() {
        this.isLoading = false;
        this.loadingOverlay.classList.remove('active');
    }
    
    clearResults() {
        this.resultsSection.classList.remove('active');
        this.confidenceMessage.classList.remove('active');
        this.resultsGrid.innerHTML = '';
    }
    
    // NEW: Updated method to handle SQL database format
    formatBreedInfo(data) {
        // Define the exact order and mapping of fields for SQL database structure
        const fieldOrder = [
            { key: 'height', label: 'Height', icon: 'fas fa-ruler-vertical', type: 'gender_range' },
            { key: 'weight', label: 'Weight', icon: 'fas fa-weight', type: 'gender_range' },
            { key: 'lifespan', label: 'Life Expectancy', icon: 'fas fa-heart', type: 'range' },
            { key: 'characteristics', label: 'Characteristic', icon: 'fas fa-smile', type: 'text' },
            { key: 'exercise_needs', label: 'Exercise Needs', icon: 'fas fa-running', type: 'text' },
            { key: 'grooming_requirements', label: 'Grooming Requirements', icon: 'fas fa-cut', type: 'text' },
            { key: 'health_considerations', label: 'Health Considerations', icon: 'fas fa-stethoscope', type: 'text' },
            { key: 'diet_nutrition', label: 'Diet and Nutrition', icon: 'fas fa-utensils', type: 'text' }
        ];

        // Extract data from the SQL database response
        const extractedData = {};
        
        // Process SQL database format
        if (typeof data === 'object' && data !== null) {
            // Height formatting (Male/Female ranges)
            if (data.height_male_min !== undefined && data.height_male_max !== undefined &&
                data.height_female_min !== undefined && data.height_female_max !== undefined) {
                extractedData.height = {
                    male: this.formatRange(data.height_male_min, data.height_male_max),
                    female: this.formatRange(data.height_female_min, data.height_female_max)
                };
            }
            
            // Weight formatting (Male/Female ranges)
            if (data.weight_male_min !== undefined && data.weight_male_max !== undefined &&
                data.weight_female_min !== undefined && data.weight_female_max !== undefined) {
                extractedData.weight = {
                    male: this.formatRange(data.weight_male_min, data.weight_male_max),
                    female: this.formatRange(data.weight_female_min, data.weight_female_max)
                };
            }
            
            // Life Expectancy formatting (single range)
            if (data.life_expectancy_min !== undefined && data.life_expectancy_max !== undefined) {
                extractedData.lifespan = this.formatRange(data.life_expectancy_min, data.life_expectancy_max);
            }
            
            // Direct text mappings
            extractedData.characteristics = data.characteristics || 'Information not available';
            extractedData.exercise_needs = data.exercise_needs || 'Information not available';
            extractedData.grooming_requirements = data.grooming_requirements || 'Information not available';
            extractedData.health_considerations = data.health_considerations || 'Information not available';
            extractedData.diet_nutrition = data.diet_nutrition || 'Information not available';
        }

        return { extractedData, fieldOrder };
    }
    
    // NEW: Helper method to format numeric ranges
    formatRange(min, max) {
        if (min === null || min === undefined || max === null || max === undefined) {
            return 'Information not available';
        }
        
        if (min === max) {
            return `${min}`;
        }
        
        return `${min} - ${max}`;
    }
    
    // NEW: Helper method to format gender-specific ranges
    formatGenderRange(data) {
        if (!data || (!data.male && !data.female)) {
            return 'Information not available';
        }
        
        const maleRange = data.male || 'Information not available';
        const femaleRange = data.female || 'Information not available';
        
        return `
            <div class="gender-range">
                <div class="gender-item">
                    <span class="gender-label">Male:</span>
                    <span class="gender-value">${maleRange}</span>
                </div>
                <div class="gender-item">
                    <span class="gender-label">Female:</span>
                    <span class="gender-value">${femaleRange}</span>
                </div>
            </div>
        `;
    }
    
    // UPDATED: Display results with new SQL format
    displayResults(data) {
        this.resultsSection.classList.add('active');
        
        // Show confidence message if available
        if (data.confidence_message) {
            this.confidenceMessage.textContent = data.confidence_message;
            this.confidenceMessage.classList.add('active');
        }
        
        // Clear previous results
        this.resultsGrid.innerHTML = '';
        
        // Display each prediction
        data.predictions.forEach((result, index) => {
            const { extractedData, fieldOrder } = this.formatBreedInfo(result);
            
            const resultCard = document.createElement('div');
            resultCard.className = 'result-card';
            resultCard.style.animationDelay = `${index * 0.1}s`;
            
            // Build details HTML in consistent order
            let detailsHTML = '';
            
            fieldOrder.forEach(field => {
                const value = extractedData[field.key];
                let displayValue = 'Information not available';
                
                if (field.type === 'gender_range' && value) {
                    displayValue = this.formatGenderRange(value);
                } else if (field.type === 'range' && value) {
                    displayValue = value;
                } else if (field.type === 'text' && value) {
                    displayValue = value;
                }
                
                detailsHTML += `
                    <div class="breed-detail-item">
                        <i class="${field.icon}"></i>
                        <span class="breed-detail-label">${field.label}:</span>
                        <div class="breed-detail-value">${displayValue}</div>
                    </div>
                `;
            });
            
            resultCard.innerHTML = `
                <div class="result-header">
                    <h3 class="breed-name">Breed: ${result.breed_name || result.breed || 'Unknown'}</h3>
                    <span class="confidence">${result.confidence || '0%'}</span>
                </div>
                <div class="breed-details">${detailsHTML}</div>
                <style>
                    .gender-range {
                        margin-left: 1rem;
                    }
                    .gender-item {
                        display: flex;
                        margin: 0.25rem 0;
                    }
                    .gender-label {
                        font-weight: 500;
                        margin-right: 0.5rem;
                        min-width: 4rem;
                    }
                    .gender-value {
                        color: #6b7280;
                    }
                    .breed-detail-value {
                        flex: 1;
                    }
                </style>
            `;
            
            this.resultsGrid.appendChild(resultCard);
        });
        
        // Scroll to results
        setTimeout(() => {
            this.resultsSection.scrollIntoView({ behavior: 'smooth' });
        }, 100);
    }
    
    async predictBreed() {
        if (!this.selectedFile) {
            this.showError('Please select an image first.');
            return;
        }

        if (!this.workingApiUrl) {
            this.showError('Unable to connect to the prediction service. Please check if the backend is running.');
            return;
        }

        this.showLoading();
        this.hideError();
        
        try {
            const formData = new FormData();
            formData.append('file', this.selectedFile);

            const response = await fetch(`${this.workingApiUrl}/predict`, {
                method: 'POST',
                body: formData,
                mode: 'cors'
            });

            if (!response.ok) {
                const errorData = await response.text();
                throw new Error(`Prediction failed: ${response.status} - ${errorData}`);
            }

            const data = await response.json();
            
            if (data.predictions && data.predictions.length > 0) {
                this.displayResults(data);
            } else {
                this.showError('No breed predictions could be made for this image.');
            }
            
        } catch (error) {
            console.error('Prediction error:', error);
            this.showError(`Error during prediction: ${error.message}`);
        } finally {
            this.hideLoading();
        }
    }
}

// Store instance globally for cleanup
let petClassifierInstance = null;

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    petClassifierInstance = new PetBreedClassifier();
    window.petClassifier = petClassifierInstance;
});

// Cleanup on page unload
window.addEventListener('beforeunload', () => {
    if (petClassifierInstance && petClassifierInstance.currentStream) {
        petClassifierInstance.currentStream.getTracks().forEach(track => track.stop());
    }
    
    // Clean up any object URLs
    if (petClassifierInstance && petClassifierInstance.previewUrl) {
        URL.revokeObjectURL(petClassifierInstance.previewUrl);
    }
});

// Handle page visibility changes (mobile browsers)
document.addEventListener('visibilitychange', () => {
    if (document.hidden && petClassifierInstance && petClassifierInstance.currentStream) {
        // Pause camera when page is hidden
        petClassifierInstance.closeCamera();
    }
});