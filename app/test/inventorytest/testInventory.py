import pytest
from datetime import date

def testAddInventory(client):
    response = client.post(
        "/inventory/",
        json={
        "techname": "Tech1",
        "chemname": "ChemicalA",
        "usageLt" : 5.0,
        "recDate": str(date.today())
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["techName"] == "Tech1"
    assert data["chemName"] == "ChemicalA"
    assert data["usageLt"] == 5.0
    
def testUpdateInventory(client):
    addResp = client.post(
        "/inventory/",
        json={
        "techname": "Tech2",
        "chemname": "ChemicalB",
        "usageLt" : 3.0,
        "recDate": str(date.today())
        }
    )
    
    recordId = addResp.json()["id"]
    
    updateResp = client.put(f"/inventory/{recordId}?usageLt=7.5")
    assert updateResp.status_code == 200
    assert updateResp.json()["usageLt"] == 7.5
    
def testDeleteInventory(client):
    addResp = client.post(
        "/inventory/",
        json={
        "techname": "Tech1",
        "chemname": "ChemicalA",
        "usageLt" : 5.0,
        "recDate": str(date.today())
        }
    )
    recordId = addResp.json()["id"]
    
    delResp = client.get(f"/inventory/{recordId}")
    assert delResp.status_code == 200
    assert delResp.json()["message"] == "Record deleted successfully"