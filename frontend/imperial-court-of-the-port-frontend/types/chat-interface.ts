// src/types/chat-interface.ts

/**
 * Interface for the file object stored in state after upload.
 * The 'data' field is CRITICAL for file uploads via FormData.
 */
export interface UploadedFile {
    id: string;
    name: string;
    size: number;
    type: string;
    // CRITICAL: Stores the native browser File object
    data: File; 
}

/**
 * Interface for the message object, which may include files.
 */
export interface Message {
    id: string;
    role: "user" | "assistant";
    content: string; // The user's query text
    files?: UploadedFile[]; // Array of custom file objects
    timestamp: Date;
}