async def test_health(test_client):
    heal = await test_client.get("/health")
    assert heal.json() == {"status": "alive"}

async def test_ready(test_client):
    ready = await test_client.get("/ready")
    assert ready.json() == {"status": "ready", "database": "connected"}

