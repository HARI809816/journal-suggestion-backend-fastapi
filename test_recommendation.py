from fastapi.testclient import TestClient
from main import app
import json

client = TestClient(app)

def test_recommendation():
    # Data provided by user
    payload = [
        {
            "Journal_Name": "IEEE IoT Magazine",
            "Special_Issue_Name": "Deep Learning Assisted Visual IoT Technologies for Critical Infrastructure Protection",
            "Special_Issue_keywords": "Crowd intelligence and deep learning...",
            "Similarity_Score": 0.67402005,
            "Qdrant_id": "93774e59-5b0b-5336-90dc-217ef8d42856"
        },
        {
            "Journal_Name": "International Journal of Pervasive Computing and Communications",
            "Special_Issue_Name": "Scalable AI Techniques for Real-Time, Pervasive and Ubiquitous Computing Systems",
            "Similarity_Score": 0.62821984
        }
    ]

    response = client.post("/journals/recommendations", json=payload)
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Received {len(data)} results.")
        if data:
            print("First result sample:")
            print(json.dumps(data[0], indent=2, default=str))
            
            # Verify Similarity Score is present
            if 'Similarity_Score' in data[0]:
                print(f"Similarity Score Check: {data[0]['Similarity_Score']}")
            else:
                print("ERROR: Similarity_Score missing!")
        else:
            print("No matches found in DB (expected if DB is empty or names don't match exactly).")
    else:
        print(response.text)

if __name__ == "__main__":
    test_recommendation()
