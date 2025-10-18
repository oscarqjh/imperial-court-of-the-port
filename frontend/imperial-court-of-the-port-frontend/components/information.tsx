"use client"

import { ChatHeader } from "./chat-header"

export default function Information() {
    return(<>
    <ChatHeader />
        <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4 sm:p-8">
                  
            <div className="w-full max-w-6xl">
                <div className="bg-white rounded-xl shadow-2xl p-6 md:p-10 lg:p-12 border border-gray-100">

                    <h1 className="text-3xl sm:text-4xl md:text-5xl font-extrabold text-gray-900 mb-6 sm:mb-8 text-center tracking-tight">
                        What Our Agents Are <span className="text-transparent bg-clip-text bg-gradient-to-r from-purple-600 to-purple-500">Orchestrating</span> Behind the Scenes
                    </h1>
                    
                    <p className="text-center text-gray-600 mb-10 text-lg max-w-3xl mx-auto">
                        The Imperial Court of the Port utilizes multiple specialized agents, each executing a crucial role in our 6-phase incident management protocol—achieving unprecedented speed and precision.
                    </p>

                    <div className="w-full flex justify-center">
                        <iframe src="https://drive.google.com/file/d/1OM2g1TBI4ZltZKz0G4gCGcGhwIPXvhom/preview" width="640" height="480" allow="autoplay"></iframe>
                    </div>
                </div>
            </div>
        </div>
        </>
    )
}