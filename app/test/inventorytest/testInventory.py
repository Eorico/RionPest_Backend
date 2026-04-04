import pytest
from datetime import date, time

def test_add_inventory(client):
    response = client.post(
        "/inventory/",
        json={
        "Date": str(date.today()),
        "category": str("treatment"),
        "client_name":  "Client A",
        "start_time": str(time(9,0)),
        "end_time" : str(time(10,0)),
        "chemical_name": "Chemical A",
        "actual_chemica_on_hand": 15.0
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["category"] == "treatment"
    assert data["client_name"] == "Client A"
    assert data["chemical_name"] == "Chemical A"
    assert data["actual_chemica_on_hand"] == 15.0
    assert data["Date"] == str(date.today())
    assert data["start_time"] == "09:00:00"
    assert data["end_time"] == "10:00:00"
    
def test_update_inventory(client):
    add_resp = client.post(
        "/inventory/",
        json={
        "Date": str(date.today()),
        "category": str("inspection"),
        "client_name":  "Client B",
        "start_time": str(time(9,0)),
        "end_time" : str(time(10,0)),
        "chemical_name": "Chemical B",
        "actual_chemica_on_hand": 20.0
        }
    )
    
    rec_id = add_resp.json()["id"]
    
    update_resp = client.put(f"/inventory/{rec_id}?actual_chemica_on_hand=12.5")
    assert update_resp.status_code == 200
    assert update_resp.json()["actual_chemica_on_hand"] == 12.5
    
def test_delete_inventory(client):
    add_resp = client.post(
        "/inventory/",
        json={
        "Date": str(date.today()),
        "category": str("treatment"),
        "client_name":  "Client C",
        "start_time": str(time(9,0)),
        "end_time" : str(time(10,0)),
        "chemical_name": "Chemical C",
        "actual_chemica_on_hand": 10.0
        }
    )
    rec_id = add_resp.json()["id"]
    
    del_resp = client.get(f"/inventory/{rec_id}")
    assert del_resp.status_code == 200
    assert del_resp.json()["message"] == "Record deleted successfully"