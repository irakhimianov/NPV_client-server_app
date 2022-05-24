import uvicorn
from config import config


uvicorn.run("server.app:app",
            reload=True,
            host=config.host,
            port=config.port)