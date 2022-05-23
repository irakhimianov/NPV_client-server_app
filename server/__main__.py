import uvicorn
from .settings import settings


uvicorn.run("server.app:app",
            reload=True,
            host=settings.host,
            port=settings.port)