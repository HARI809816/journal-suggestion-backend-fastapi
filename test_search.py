from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_search():
    # Test 1: Search by query (assuming some data exists, or just checking 200 OK and empty list if no data)
    response = client.get("/journals/search?query=test")
    print(f"Test 1 (Query): Status {response.status_code}")
    if response.status_code == 200:
        print(f"Response: {response.json()[:2]}") # Show first 2 results

    # Test 2: Search by publisher
    response = client.get("/journals/search?publisher=Elsevier")
    print(f"Test 2 (Publisher): Status {response.status_code}")
    
    # Test 3: No params (should return all or many)
    response = client.get("/journals/search")
    print(f"Test 3 (No params): Status {response.status_code}")
    print(f"Count: {len(response.json())}")

if __name__ == "__main__":
    test_search()
