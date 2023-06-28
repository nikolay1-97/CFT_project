from fastapi.testclient import TestClient
from app.main import application


client = TestClient(application)

