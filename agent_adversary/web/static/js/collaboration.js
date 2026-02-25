class CollaborationManager {
    constructor(ws) {
        this.ws = ws;
        this.activeSession = null;
        this.callbacks = new Map();
    }

    subscribe(sessionId, callback) {
        if (this.activeSession === sessionId) return;
        
        this.activeSession = sessionId;
        this.callbacks.set(sessionId, callback);
        
        if (this.ws && this.ws.readyState === WebSocket.OPEN) {
            this.ws.send(JSON.stringify({
                type: 'subscribe',
                session_id: sessionId
            }));
            console.log(`[Collaboration] Subscribed to Watch Party: ${sessionId}`);
        }
    }

    handleMessage(data) {
        if (data.session_id && this.callbacks.has(data.session_id)) {
            const cb = this.callbacks.get(data.session_id);
            cb(data);
        }
    }
}

window.CollaborationManager = CollaborationManager;
