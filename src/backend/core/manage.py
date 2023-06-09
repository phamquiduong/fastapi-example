import uvicorn


class Manage:
    def __init__(self, app: str, host: str, port: str | int):
        self.app = app
        self.host = host
        self.port = int(port)

    def __str__(self):
        return self.app.split(':')[0]

    def check_db_connection(self):
        return True
    
    def load_config(self):
        pass

    def run(self, reload: bool = False):
        uvicorn.run(
            app=self.app,
            host=self.host,
            port=self.port,
            reload=reload,
        )
