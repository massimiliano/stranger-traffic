import uvicorn
import threading
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

class BackgroundServer:
    def __init__(self, port=8000):
        self.port = port
        self.app = FastAPI()
        
        self.app.mount("/", StaticFiles(directory=".", html=True), name="static")
        
        self.server_thread = threading.Thread(target=self._run_server)
        self.server_thread.daemon = True

    def _run_server(self):
        uvicorn.run(self.app, host="127.0.0.1", port=self.port, log_level="critical")

    def start(self):
        print(f"Server FastAPI listening on http://127.0.0.1:{self.port}")
        self.server_thread.start()

    def stop(self):
        pass