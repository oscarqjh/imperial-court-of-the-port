// src/utils/httpUtils.js (This function makes the POST request)

import axios from 'axios';

// IMPORTANT: Ensure this function is exported as 'export const'
export const postFilesData = async (endpoint, data) => {
    const formData = new FormData();
    // Assuming data.files is an array of UploadedFile objects (which have a 'data' field)
    const uploadedFiles = data.files || []; 

    // 1. Separate the IncidentRequest JSON fields
    const incidentRequestData = {
        incident_type: data.incident_type,
        severity: data.severity || 'Medium',
        payload: data.payload || {} 
    };

    // 2. Append the IncidentRequest JSON as a string
    formData.append('request_data', JSON.stringify(incidentRequestData)); 

    // 3. Append the files
    if (uploadedFiles.length > 0) {
        uploadedFiles.forEach(uploadedFile => {
            const nativeFile = uploadedFile.data; // ⬅️ EXTRACT THE NATIVE FILE OBJECT
            
            // CRITICAL: Check the extracted object's type
            if (!(nativeFile instanceof File) && !(nativeFile instanceof Blob)) {
                 throw new TypeError(`File object for ${uploadedFile.name} is not a Blob or File instance. Serialization error.`);
            }
            
            // Append the native File/Blob object
            formData.append('files', nativeFile, uploadedFile.name); 
        });
    }

    // 4. Make the Axios Request
    try {
        const response = await axios.post(endpoint, formData);
        return response.data;
    } catch (error) {
        // ... (Error handling remains the same as before) ...
        console.error(`POST request failed for endpoint: ${endpoint}`);
        if (error.response) {
            throw new Error(`Server error (${error.response.status}): ${JSON.stringify(error.response.data)}`);
        } else {
            throw new Error(`Request error: ${error.message}`);
        }
    }
};