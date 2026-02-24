import pytest
from datetime import date, time

def test_add_inventory(client):
    response = client.post(
        "/inventory/",
        json={
        "treatmentDate": str(date.today()),
        "clientName":  "Client A",
        "startTime": str(time(9,0)),
        "endTime" : str(time(10,0)),
        "chemicalName": "Chemical A",
        "actualChemicalOnHand": 15.0
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["clientName"] == "Client A"
    assert data["chemicalName"] == "Chemical A"
    assert data["actualChemicalOnHand"] == 15.0
    assert data["treatmentDate"] == str(date.today())
    assert data["startTime"] == "09:00:00"
    assert data["endTime"] == "10:00:00"
    
def test_update_inventory(client):
    addResp = client.post(
        "/inventory/",
        json={
        "treatmentDate": str(date.today()),
        "clientName":  "Client B",
        "startTime": str(time(9,0)),
        "endTime" : str(time(10,0)),
        "chemicalName": "Chemical B",
        "actualChemicalOnHand": 20.0
        }
    )
    
    recordId = addResp.json()["id"]
    
    updateResp = client.put(f"/inventory/{recordId}?actualChemcialOnHand=12.5")
    assert updateResp.status_code == 200
    assert updateResp.json()["actualChemcialOnHand"] == 12.5
    
def test_delete_inventory(client):
    addResp = client.post(
        "/inventory/",
        json={
        "treatmentDate": str(date.today()),
        "clientName":  "Client C",
        "startTime": str(time(9,0)),
        "endTime" : str(time(10,0)),
        "chemicalName": "Chemical C",
        "actualChemicalOnHand": 10.0
        }
    )
    recordId = addResp.json()["id"]
    
    delResp = client.get(f"/inventory/{recordId}")
    assert delResp.status_code == 200
    assert delResp.json()["message"] == "Record deleted successfully"