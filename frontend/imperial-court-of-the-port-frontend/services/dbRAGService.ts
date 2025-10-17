// src/services/dbRAGService.ts (This function maps the Message to the payload)

import { postFilesData } from '@/utils/httpUtils'; // Import the corrected utility
import type { Message } from '@/types/chat-interface'; // Import your Message type

/**
 * Service function to send the user's message (query and files) 
 * to the RAG endpoint, formatted as the IncidentRequest payload.
 */
export default async function dbRAGService(userMessage: Message) {
    const endpoint = 'http://0.0.0.0:8000/run';

    // Map the Message object data to the expected callPayload structure.
    const callPayload = {
        // IncidentRequest Pydantic Fields
        incident_type: userMessage.files?.length ? 'RAG_QUERY_WITH_FILES' : 'RAG_QUERY_TEXT_ONLY',
        severity: 'Medium',
        payload: {
            query_text: userMessage.content,
            message_id: userMessage.id, 
        },
        
        // Pass the array of custom UploadedFile objects directly
        // postFilesData will handle extracting the native File from the 'data' field
        files: userMessage.files || [] 
    };

    try {
        const response = await postFilesData(endpoint, callPayload); 
        return response;
        
    } catch (error) {
        console.error('Error in dbRAGService:', error);
        throw error;
    }
}