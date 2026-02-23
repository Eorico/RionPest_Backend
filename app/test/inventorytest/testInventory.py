import pytest
from datetime import date, time

def testAddInventory(client):
    response = client.post(
        "/inventory/",
        json={
        "treatmentDate": str(date.today()),
        "clientName":  "Client A",
        "startTime": time,
        "endTime" : time,
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
    assert data["startTime"] == time
    assert data["endTime"] == time
    
def testUpdateInventory(client):
    addResp = client.post(
        "/inventory/",
        json={
        "treatmentDate": str(date.today()),
        "clientName":  "Client B",
        "startTime": time,
        "endTime" : time,
        "chemicalName": "Chemical B",
        "actualChemicalOnHand": 20.0
        }
    )
    
    recordId = addResp.json()["id"]
    
    updateResp = client.put(f"/inventory/{recordId}?actualChemcialOnHand=12.5")
    assert updateResp.status_code == 200
    assert updateResp.json()["actualChemcialOnHand"] == 12.5
    
def testDeleteInventory(client):
    addResp = client.post(
        "/inventory/",
        json={
        "treatmentDate": str(date.today()),
        "clientName":  "Client C",
        "startTime": time,
        "endTime" : time,
        "chemicalName": "Chemical C",
        "actualChemicalOnHand": 10.0
        }
    )
    recordId = addResp.json()["id"]
    
    delResp = client.get(f"/inventory/{recordId}")
    assert delResp.status_code == 200
    assert delResp.json()["message"] == "Record deleted successfully"