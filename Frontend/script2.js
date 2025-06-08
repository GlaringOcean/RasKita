// Pet Breed Backend Connection & CSV Description Handler (script2.js)
class PetBackendHandler {
    constructor() {
        // Configuration
        this.POSSIBLE_API_URLS = [
            'http://localhost:8000',
            'http://127.0.0.1:8000',
            'http://192.168.1.100:8000',
        ];
        
        this.workingApiUrl = null;
        
        // Initialize
        this.init();
    }
    
    init() {
        this.testApiConnectivity();
        console.log('Pet Backend Handler initialized');
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
    
    async predictBreed(selectedFile, frontendInstance) {
        if (!selectedFile) {
            frontendInstance.showError('Please select an image first.');
            return;
        }

        if (!this.workingApiUrl) {
            frontendInstance.showError('Unable to connect to the prediction service. Please check if the backend is running.');
            return;
        }

        frontendInstance.showLoading();
        frontendInstance.hideError();
        
        try {
            const formData = new FormData();
            formData.append('file', selectedFile);

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
                frontendInstance.displayResults(data);
            } else {
                frontendInstance.showError('No breed predictions could be made for this image.');
            }
            
        } catch (error) {
            console.error('Prediction error:', error);
            frontendInstance.showError(`Error during prediction: ${error.message}`);
        } finally {
            frontendInstance.hideLoading();
        }
    }
}

// Initialize backend handler when DOM is loaded
let petBackendInstance = null;

document.addEventListener('DOMContentLoaded', () => {
    petBackendInstance = new PetBackendHandler();
    window.petBackend = petBackendInstance;
});