import uvicorn
from .settings import settings


uvicorn.run("npv_app.app:app",
            reload=True,
            host=settings.host,
            port=settings.port)