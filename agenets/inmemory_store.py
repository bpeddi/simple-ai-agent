from langgraph.store.memory import InMemoryStore
from langgraph.config import get_store
from typing import Dict, List

user_namespace = ("users",)
claims_namespace = ("claims",)
policies_namespace = ("policies",)

user_info = [
    {
        "user_id": "u1",
        "name": "Alice Johnson",
        "email": "alice.johnson@email.com",
        "phone": "+1-555-0101",
        "address": "123 Main St, New York, NY 10001",
        "date_of_birth": "1994-03-15",
        "join_date": "2020-06-15",
    },
    {
        "user_id": "u2",
        "name": "Bob Smith",
        "email": "bob.smith@email.com",
        "phone": "+1-555-0102",
        "address": "456 Oak Ave, Los Angeles, CA 90001",
        "date_of_birth": "1979-07-22",
        "join_date": "2018-03-10",
    },
    {
        "user_id": "u3",
        "name": "Charlie Davis",
        "email": "charlie.davis@email.com",
        "phone": "+1-555-0103",
        "address": "789 Pine Ln, Chicago, IL 60601",
        "date_of_birth": "1996-11-08",
        "join_date": "2021-01-20",
    },
    {
        "user_id": "u4",
        "name": "Diana Wilson",
        "email": "diana.wilson@email.com",
        "phone": "+1-555-0104",
        "address": "321 Elm St, Houston, TX 77001",
        "date_of_birth": "1988-05-30",
        "join_date": "2019-09-12",
    },
    {
        "user_id": "u5",
        "name": "Edward Martinez",
        "email": "edward.martinez@email.com",
        "phone": "+1-555-0105",
        "address": "654 Birch Rd, Phoenix, AZ 85001",
        "date_of_birth": "1985-12-10",
        "join_date": "2017-02-28",
    },
    {
        "user_id": "u6",
        "name": "Fiona Brown",
        "email": "fiona.brown@email.com",
        "phone": "+1-555-0106",
        "address": "987 Cedar Way, Philadelphia, PA 19103",
        "date_of_birth": "1991-09-25",
        "join_date": "2022-04-05",
    },
    {
        "user_id": "u7",
        "name": "George Taylor",
        "email": "george.taylor@email.com",
        "phone": "+1-555-0107",
        "address": "147 Maple Dr, San Antonio, TX 78201",
        "date_of_birth": "1983-01-18",
        "join_date": "2020-11-14",
    },
    {
        "user_id": "u8",
        "name": "Hannah Anderson",
        "email": "hannah.anderson@email.com",
        "phone": "+1-555-0108",
        "address": "258 Spruce Ave, San Diego, CA 92101",
        "date_of_birth": "1993-08-07",
        "join_date": "2021-07-22",
    },
]

policy_info = [
    {
        "policy_id": "p1",
        "user_id": "u1",
        "policy_type": "Health",
        "premium": 350.00,
        "deductible": 1000.00,
        "coverage_amount": 500000,
        "start_date": "2023-06-15",
        "end_date": "2025-06-15",
        "status": "Active"
    },
    {
        "policy_id": "p2",
        "user_id": "u2",
        "policy_type": "Auto",
        "premium": 120.00,
        "deductible": 500.00,
        "coverage_amount": 250000,
        "start_date": "2022-03-10",
        "end_date": "2026-03-10",
        "status": "Active"
    },
    {
        "policy_id": "p3",
        "user_id": "u3",
        "policy_type": "Home",
        "premium": 850.00,
        "deductible": 2000.00,
        "coverage_amount": 750000,
        "start_date": "2021-01-20",
        "end_date": "2026-01-20",
        "status": "Active"
    },
    {
        "policy_id": "p4",
        "user_id": "u4",
        "policy_type": "Life",
        "premium": 45.00,
        "deductible": 0.00,
        "coverage_amount": 1000000,
        "start_date": "2019-09-12",
        "end_date": "2029-09-12",
        "status": "Active"
    },
    {
        "policy_id": "p5",
        "user_id": "u1",
        "policy_type": "Auto",
        "premium": 95.00,
        "deductible": 250.00,
        "coverage_amount": 300000,
        "start_date": "2023-01-01",
        "end_date": "2026-01-01",
        "status": "Active"
    },
    {
        "policy_id": "p6",
        "user_id": "u5",
        "policy_type": "Health",
        "premium": 275.00,
        "deductible": 1500.00,
        "coverage_amount": 400000,
        "start_date": "2023-02-14",
        "end_date": "2025-02-14",
        "status": "Active"
    },
    {
        "policy_id": "p7",
        "user_id": "u6",
        "policy_type": "Travel",
        "premium": 85.00,
        "deductible": 100.00,
        "coverage_amount": 50000,
        "start_date": "2024-01-01",
        "end_date": "2027-01-01",
        "status": "Active"
    },
    {
        "policy_id": "p8",
        "user_id": "u2",
        "policy_type": "Home",
        "premium": 920.00,
        "deductible": 1500.00,
        "coverage_amount": 600000,
        "start_date": "2022-05-20",
        "end_date": "2026-05-20",
        "status": "Active"
    },
    {
        "policy_id": "p9",
        "user_id": "u7",
        "policy_type": "Life",
        "premium": 60.00,
        "deductible": 0.00,
        "coverage_amount": 750000,
        "start_date": "2020-11-14",
        "end_date": "2030-11-14",
        "status": "Active"
    },
    {
        "policy_id": "p10",
        "user_id": "u8",
        "policy_type": "Auto",
        "premium": 130.00,
        "deductible": 750.00,
        "coverage_amount": 350000,
        "start_date": "2021-07-22",
        "end_date": "2025-07-22",
        "status": "Active"
    },
    {
        "policy_id": "p11",
        "user_id": "u3",
        "policy_type": "Life",
        "premium": 55.00,
        "deductible": 0.00,
        "coverage_amount": 500000,
        "start_date": "2021-01-20",
        "end_date": "2031-01-20",
        "status": "Active"
    },
    {
        "policy_id": "p12",
        "user_id": "u5",
        "policy_type": "Auto",
        "premium": 105.00,
        "deductible": 500.00,
        "coverage_amount": 200000,
        "start_date": "2023-03-15",
        "end_date": "2026-03-15",
        "status": "Inactive"
    },
]

claim_info = [
    {
        "claim_id": "c1",
        "policy_id": "p1",
        "user_id": "u1",
        "claim_type": "Medical Treatment",
        "claim_date": "2024-05-10",
        "amount": 5000.00,
        "status": "Approved",
        "description": "Emergency room visit and hospital stay for appendicitis"
    },
    {
        "claim_id": "c2",
        "policy_id": "p2",
        "user_id": "u2",
        "claim_type": "Vehicle Damage",
        "claim_date": "2024-06-20",
        "amount": 15000.00,
        "status": "Processing",
        "description": "Collision damage to vehicle - hit and run incident"
    },
    {
        "claim_id": "c3",
        "policy_id": "p3",
        "user_id": "u3",
        "claim_type": "Property Damage",
        "claim_date": "2024-04-05",
        "amount": 7000.00,
        "status": "Denied",
        "description": "Water damage from burst pipe - claimed wear and tear"
    },
    {
        "claim_id": "c4",
        "policy_id": "p1",
        "user_id": "u1",
        "claim_type": "Prescription Coverage",
        "claim_date": "2024-07-15",
        "amount": 2500.00,
        "status": "Approved",
        "description": "Monthly prescription medications for chronic condition management"
    },
    {
        "claim_id": "c5",
        "policy_id": "p3",
        "user_id": "u3",
        "claim_type": "Home Maintenance",
        "claim_date": "2024-08-01",
        "amount": 12000.00,
        "status": "Under Investigation",
        "description": "Roof replacement due to storm damage"
    },
    {
        "claim_id": "c6",
        "policy_id": "p2",
        "user_id": "u2",
        "claim_type": "Liability Claim",
        "claim_date": "2024-03-12",
        "amount": 8500.00,
        "status": "Closed",
        "description": "Third-party liability claim - settlement reached"
    },
    {
        "claim_id": "c7",
        "policy_id": "p6",
        "user_id": "u5",
        "claim_type": "Medical Treatment",
        "claim_date": "2024-09-05",
        "amount": 3500.00,
        "status": "Approved",
        "description": "Routine surgery and post-operative care"
    },
    {
        "claim_id": "c8",
        "policy_id": "p8",
        "user_id": "u2",
        "claim_type": "Fire Damage",
        "claim_date": "2024-10-15",
        "amount": 45000.00,
        "status": "Under Investigation",
        "description": "Kitchen fire damage - structural repairs needed"
    },
    {
        "claim_id": "c9",
        "policy_id": "p10",
        "user_id": "u8",
        "claim_type": "Windshield Replacement",
        "claim_date": "2024-11-01",
        "amount": 600.00,
        "status": "Approved",
        "description": "Rock damage to windshield while driving on highway"
    },
    {
        "claim_id": "c10",
        "policy_id": "p7",
        "user_id": "u6",
        "claim_type": "Trip Cancellation",
        "claim_date": "2024-08-20",
        "amount": 2000.00,
        "status": "Closed",
        "description": "Travel insurance claim for cancelled international trip due to illness"
    },
]

def bootstrap_memory_store(store: InMemoryStore) -> InMemoryStore:
    """Populate the InMemoryStore with initial data for users, policies, and claims."""
    if not store: 
        store = get_store()
        
    for user in user_info:
        store.put(user_namespace, user["user_id"],
                  {
                      "name": user["name"],
                      "email": user["email"],
                      "phone": user["phone"],
                      "address": user["address"],
                      "date_of_birth": user["date_of_birth"],
                      "join_date": user["join_date"]
                      
                  } 
                  )
    
    for policy in policy_info:
        store.put(policies_namespace, policy["policy_id"], 
                  
                  {
                      "user_id": policy["user_id"],
                      "policy_type": policy["policy_type"],
                      "premium": policy["premium"],
                      "deductible": policy["deductible"],
                      "coverage_amount": policy["coverage_amount"],
                      "start_date": policy["start_date"],
                      "end_date": policy["end_date"],
                      "status": policy["status"]
                  }
                  
                  )
    
    for claim in claim_info:
        store.put(claims_namespace, claim["claim_id"], 
                  {
                        "policy_id": claim["policy_id"],
                        "user_id": claim["user_id"],
                        "claim_type": claim["claim_type"],
                        "claim_date": claim["claim_date"],
                        "amount": claim["amount"],
                        "status": claim["status"],
                        "description": claim["description"]
                  })
    
    return store