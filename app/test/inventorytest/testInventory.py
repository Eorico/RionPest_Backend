import pytest
from datetime import date, time

def test_add_inventory(client):
    # Updated JSON to match the new nested schema
    payload = {
        "Date": 6,
        "month": 4,
        "year": 2026,
        "category": "treatment",
        "client_name": "Client A",
        "start_time": "09:00:00",
        "end_time": "10:00:00",
        "meridiem": "PM",
        "chemicals_use": [
            {"chemical_name": "Chemical A", "quantity": 15.0}
        ],
        "actual_chemicals_used": [
            {"actual_chemical_name": "Actual Chem A", "quantity": 5.0}
        ]
    }
    
    response = client.post("/inventory/", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    
    # Assertions for the main record
    assert data["category"] == "treatment"
    assert data["client_name"] == "Client A"
    assert data["Date"] == int
    assert data["month"] == int
    assert data["year"] == int
    
    # Assertions for the nested lists
    assert len(data["chemicals_used"]) == 1
    assert data["chemicals_used"][0]["chemical_name"] == "Chemical A"
    assert data["chemicals_used"][0]["quantity"] == 15.0
    
    assert data["actual_chemicals_used"][0]["actual_chemical_name"] == "Actual Chem A"

def test_update_inventory(client):
    # 1. Create a record first
    add_resp = client.post(
        "/inventory/",
        json={
            "Date": 6,
            "month": 4,
            "year": 2026,
            "category": "inspection",
            "client_name": "Client B",
            "start_time": "09:00:00",
            "end_time": "10:00:00",
            "meridiem": "PM",
            "chemicals_use": [{"chemical_name": "Chemical B", "quantity": 20.0}],
            "actual_chemicals_used": []
        }
    )
    
    rec_id = add_resp.json()["id"]
    
    # 2. Update a field (Ensure your backend logic for PUT handles these params)
    # If you changed your schema, you might need to update the whole object instead of query params
    update_resp = client.put(f"/inventory/{rec_id}?client_name=Updated Client B")
    
    assert update_resp.status_code == 200
    assert update_resp.json()["client_name"] == "Updated Client B"

def test_delete_inventory(client):
    # 1. Create a record to delete
    add_resp = client.post(
        "/inventory/",
        json={
            "Date": 8,
            "month": 4,
            "year": 2026,
            "category": "treatment",
            "client_name": "Client C",
            "start_time": "09:00:00",
            "end_time": "10:00:00",
            "meridiem": "PM",
            "chemicals_use": [{"chemical_name": "Chemical C", "quantity": 10.0}],
            "actual_chemicals_used": []
        }
    )
    rec_id = add_resp.json()["id"]
    
    # 2. Delete it (Using DELETE method usually, but following your code's logic)
    # If your backend uses GET for deletion, keep this, but DELETE is standard REST
    del_resp = client.delete(f"/inventory/{rec_id}") 
    
    assert del_resp.status_code == 200
    assert del_resp.json()["message"] == "Record deleted successfully"