"""
Insurance Agent Tools - Provides tools for customer, policy, and claims management.
Uses LangGraph InMemoryStore for data persistence.
"""

import re
import uuid
from datetime import datetime
from typing import List, Optional, Dict, Any
from langchain_core.tools import tool
from langgraph.config import get_store
from langgraph.types import interrupt

try:
    from inmemory_store import user_namespace, claims_namespace, policies_namespace
    from utils import get_logger
except ImportError:
    # Fallback for direct imports
    user_namespace = ("users",)
    claims_namespace = ("claims",)
    policies_namespace = ("policies",)
    import logging
    def get_logger(name):
        logger = logging.getLogger(name)
        if not logger.hasHandlers():
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger

logger = get_logger(__name__)


def _unwrap_item(item):
    """Helper to unwrap InMemoryStore Item objects."""
    if item is None:
        return None
    if hasattr(item, 'value'):
        return item.value
    return item


# ===========================
# CUSTOMER INFORMATION TOOLS
# ===========================

@tool
def get_customer_information(customer_id: str) -> Dict[str, Any]:
    """
    Get customer information and contact details.
    
    Args:
        customer_id: The unique customer ID (e.g., "u1", "u2")
    
    Returns:
        Dictionary with customer details including name, age, and associated policy
    """
    try:
        store = get_store()
        user_data = _unwrap_item(store.get(namespace=user_namespace, key=customer_id))
        
        if not user_data:
            logger.warning(f"Customer {customer_id} not found")
            return {"error": f"Customer {customer_id} not found", "found": False}
        
        logger.info(f"Retrieved customer information for {customer_id}")
        return {
            "customer_id": customer_id,
            "name": user_data.get("name"),
            "email": user_data.get("email"),
            "phone": user_data.get("phone"),
            "address": user_data.get("address"),
            "date_of_birth": user_data.get("date_of_birth"),
            "join_date": user_data.get("join_date"),
            "found": True
        }
    except Exception as e:
        logger.error(f"Failed to retrieve customer information: {str(e)}")
        return {"error": f"Failed to retrieve customer information: {str(e)}"}

@tool
def get_customer_infoname(name: str) -> Dict[str, Any]:
    """
    Get customer information and contact details.
    
    Args:
        customer_name: The unique customer ID (e.g., "u1", "u2")
    
    Returns:
        Dictionary with customer details including name, age, and associated policy
    """
    try:
        store = get_store()
        user_data = _unwrap_item(store.get(namespace=user_namespace, key=name))
        
        if not user_data:
            logger.warning(f"Customer {name} not found")
            return {"error": f"Customer {name} not found", "found": False}
        
        logger.info(f"Retrieved customer information for {name}")
        return {
            "customer_id": user_data.get("customer_id"),
            "name": user_data.get("name"),
            "email": user_data.get("email"),
            "phone": user_data.get("phone"),
            "address": user_data.get("address"),
            "date_of_birth": user_data.get("date_of_birth"),
            "join_date": user_data.get("join_date"),
            "found": True
        }
    except Exception as e:
        logger.error(f"Failed to retrieve customer information: {str(e)}")
        return {"error": f"Failed to retrieve customer information: {str(e)}"}

@tool
def get_user_policy_info(user_id: str) -> Optional[Dict[str, Any]]:
    """Retrieve policy information for a given user ID."""
    store = get_store()
    user_data = _unwrap_item(store.get(namespace=user_namespace, key=user_id))
    if not user_data:
        logger.warning(f"User ID {user_id} not found.")
        return None
    policy_id = user_data.get("policy_id")
    policy_data = _unwrap_item(store.get(namespace=policies_namespace, key=policy_id))
    if not policy_data:
        logger.warning(f"Policy ID {policy_id} for User ID {user_id} not found.")
        return None
    result = {
        "user": user_data,
        "policy": policy_data
    }
    logger.info(f"Retrieved policy info for User ID {user_id}.")
    return result


# ===========================
# POLICY TOOLS
# ===========================

@tool
def get_customer_policies(customer_id: str) -> Dict[str, Any]:
    """
    Retrieve all policies for a customer.
    
    Args:
        customer_id: The unique customer ID
    
    Returns:
        List of policies associated with the customer
    """
    try:
        store = get_store()
        user_data = _unwrap_item(store.get(namespace=user_namespace, key=customer_id))
        
        if not user_data:
            logger.warning(f"Customer {customer_id} not found")
            return {"error": f"Customer {customer_id} not found"}
        
        policy_id = user_data.get("policy_id")
        if not policy_id:
            logger.info(f"No policies found for customer {customer_id}")
            return {"policies": [], "customer_id": customer_id}
        
        policy_data = _unwrap_item(store.get(namespace=policies_namespace, key=policy_id))
        
        if not policy_data:
            logger.warning(f"Policy {policy_id} not found")
            return {"policies": [], "customer_id": customer_id, "warning": f"Policy {policy_id} not found"}
        
        logger.info(f"Retrieved {1} policy for customer {customer_id}")
        return {
            "customer_id": customer_id,
            "policies": [policy_data],
            "count": 1
        }
    except Exception as e:
        logger.error(f"Failed to retrieve customer policies: {str(e)}")
        return {"error": f"Failed to retrieve customer policies: {str(e)}"}


@tool
def get_policy_details(policy_id: str) -> Dict[str, Any]:
    """
    Get detailed policy information including coverage amounts, deductibles, and premiums.
    
    Args:
        policy_id: The unique policy ID (e.g., "p1", "p2")
    
    Returns:
        Dictionary with detailed policy information
    """
    try:
        store = get_store()
        policy_data = _unwrap_item(store.get(namespace=policies_namespace, key=policy_id))
        
        if not policy_data:
            logger.warning(f"Policy {policy_id} not found")
            return {"error": f"Policy {policy_id} not found"}
        
        logger.info(f"Retrieved detailed information for policy {policy_id}")
        return {
            "policy_id": policy_id,
            "user_id": policy_data.get("user_id"),
            "policy_type": policy_data.get("policy_type"),
            "premium": policy_data.get("premium"),
            "deductible": policy_data.get("deductible"),
            "coverage_amount": policy_data.get("coverage_amount"),
            "start_date": policy_data.get("start_date"),
            "end_date": policy_data.get("end_date"),
            "status": policy_data.get("status", "Active")
        }
    except Exception as e:
        logger.error(f"Failed to retrieve policy details: {str(e)}")
        return {"error": f"Failed to retrieve policy details: {str(e)}"}


# ===========================
# CLAIMS TOOLS
# ===========================

@tool
def check_claims_exist(customer_id: str) -> Dict[str, Any]:
    """
    Check if claims exist in the system for a customer.
    
    Args:
        customer_id: The unique customer ID
    
    Returns:
        Boolean indicating if claims exist and basic claim info
    """
    try:
        store = get_store()
        
        # Get all claims and filter by customer_id
        all_claims = store.search(claims_namespace)
        customer_claims = [
            claim for claim in all_claims 
            if _unwrap_item(claim).get("user_id") == customer_id
        ]
        
        logger.info(f"Found {len(customer_claims)} claims for customer {customer_id}")
        return {
            "customer_id": customer_id,
            "has_claims": len(customer_claims) > 0,
            "claim_count": len(customer_claims)
        }
    except Exception as e:
        logger.error(f"Failed to check claims: {str(e)}")
        return {"error": f"Failed to check claims: {str(e)}"}


@tool
def get_customer_claims(customer_id: str) -> Dict[str, Any]:
    """
    View all claims for a specific customer.
    
    Args:
        customer_id: The unique customer ID
    
    Returns:
        List of all claims for the customer
    """
    try:
        store = get_store()
        
        # Get all claims and filter by customer_id
        all_claims = store.search(claims_namespace)
        customer_claims = [
            {
                "claim_id": claim.key,
                **_unwrap_item(claim)
            }
            for claim in all_claims 
            if _unwrap_item(claim).get("user_id") == customer_id
        ]
        
        logger.info(f"Retrieved {len(customer_claims)} claims for customer {customer_id}")
        return {
            "customer_id": customer_id,
            "claims": customer_claims,
            "total_claims": len(customer_claims)
        }
    except Exception as e:
        logger.error(f"Failed to retrieve customer claims: {str(e)}")
        return {"error": f"Failed to retrieve customer claims: {str(e)}"}


@tool
def get_claim_status(claim_id: str) -> Dict[str, Any]:
    """
    Get current status of any claim (Processing, Approved, Closed, Under Investigation, Denied).
    
    Args:
        claim_id: The unique claim ID (e.g., "c1", "c2")
    
    Returns:
        Current claim status and details
    """
    try:
        store = get_store()
        claim_data = _unwrap_item(store.get(namespace=claims_namespace, key=claim_id))
        
        if not claim_data:
            logger.warning(f"Claim {claim_id} not found")
            return {"error": f"Claim {claim_id} not found"}
        
        logger.info(f"Retrieved status for claim {claim_id}: {claim_data.get('status')}")
        return {
            "claim_id": claim_id,
            "customer_id": claim_data.get("user_id"),
            "status": claim_data.get("status", "Unknown"),
            "amount": claim_data.get("amount"),
            "last_updated": claim_data.get("last_updated", _get_current_system_date())
        }
    except Exception as e:
        logger.error(f"Failed to retrieve claim status: {str(e)}")
        return {"error": f"Failed to retrieve claim status: {str(e)}"}


@tool
def add_new_claim(customer_id: str, policy_id: str, amount: float, description: str = "") -> Dict[str, Any]:
    """
    Add new claims with validation that customer has active policy.
    
    Args:
        customer_id: The unique customer ID
        policy_id: The unique policy ID
        amount: Claim amount
        description: Optional claim description
    
    Returns:
        Newly created claim details or error
    """
    try:
        store = get_store()
        
        # Validate customer exists
        user_data = _unwrap_item(store.get(namespace=user_namespace, key=customer_id))
        if not user_data:
            logger.warning(f"Customer {customer_id} not found for claim creation")
            return {"error": f"Customer {customer_id} not found"}
        
        # Validate policy exists and is active
        policy_data = _unwrap_item(store.get(namespace=policies_namespace, key=policy_id))
        if not policy_data:
            logger.warning(f"Policy {policy_id} not found for claim creation")
            return {"error": f"Policy {policy_id} not found"}
        
        if policy_data.get("status") != "Active" and policy_data.get("status"):
            logger.warning(f"Policy {policy_id} is not active")
            return {"error": f"Policy {policy_id} is not active"}
        
        # Validate customer has this policy
        if user_data.get("policy_id") != policy_id:
            logger.warning(f"Customer {customer_id} does not have policy {policy_id}")
            return {"error": f"Customer {customer_id} does not have policy {policy_id}"}
        
        # Create new claim
        claim_id = f"c{uuid.uuid4().hex[:8]}"
        new_claim = {
            "claim_id": claim_id,
            "user_id": customer_id,
            "policy_id": policy_id,
            "amount": amount,
            "status": "Processing",
            "description": description,
            "created_date": _get_current_system_date(),
            "last_updated": _get_current_system_date()
        }
        
        store.put(namespace=claims_namespace, key=claim_id, value=new_claim)
        logger.info(f"New claim {claim_id} created for customer {customer_id}")
        
        return {
            "success": True,
            "claim_id": claim_id,
            "message": f"Claim {claim_id} created successfully",
            "claim": new_claim
        }
    except Exception as e:
        logger.error(f"Failed to add new claim: {str(e)}")
        return {"error": f"Failed to add new claim: {str(e)}"}


@tool
def update_claim_status(claim_id: str, new_status: str) -> Dict[str, Any]:
    """
    Update claim status (Processing, Approved, Closed, Under Investigation, Denied).
    
    Args:
        claim_id: The unique claim ID
        new_status: New status for the claim
    
    Returns:
        Updated claim details
    """
    try:
        store = get_store()
        claim_data = _unwrap_item(store.get(namespace=claims_namespace, key=claim_id))
        
        if not claim_data:
            logger.warning(f"Claim {claim_id} not found for status update")
            return {"error": f"Claim {claim_id} not found"}
        
        # Validate status
        valid_statuses = ["Processing", "Approved", "Closed", "Under Investigation", "Denied"]
        if new_status not in valid_statuses:
            logger.warning(f"Invalid status {new_status} for claim {claim_id}")
            return {"error": f"Invalid status. Valid options: {', '.join(valid_statuses)}"}
        
        # Update claim
        claim_data["status"] = new_status
        claim_data["last_updated"] = _get_current_system_date()
        
        store.put(namespace=claims_namespace, key=claim_id, value=claim_data)
        logger.info(f"Claim {claim_id} status updated to {new_status}")
        
        return {
            "success": True,
            "claim_id": claim_id,
            "new_status": new_status,
            "message": f"Claim {claim_id} status updated to {new_status}",
            "claim": claim_data
        }
    except Exception as e:
        logger.error(f"Failed to update claim status: {str(e)}")
        return {"error": f"Failed to update claim status: {str(e)}"}


# ===========================
# COVERAGE & PREMIUM TOOLS
# ===========================

@tool
def calculate_remaining_coverage(customer_id: str) -> Dict[str, Any]:
    """
    Calculate coverage remaining after potential claims.
    
    Args:
        customer_id: The unique customer ID
    
    Returns:
        Remaining coverage amount and claims deducted
    """
    try:
        store = get_store()
        
        # Get customer and policy
        user_data = _unwrap_item(store.get(namespace=user_namespace, key=customer_id))
        if not user_data:
            logger.warning(f"Customer {customer_id} not found for coverage calculation")
            return {"error": f"Customer {customer_id} not found"}
        
        policy_id = user_data.get("policy_id")
        policy_data = _unwrap_item(store.get(namespace=policies_namespace, key=policy_id))
        
        if not policy_data:
            logger.warning(f"Policy {policy_id} not found for coverage calculation")
            return {"error": f"Policy {policy_id} not found"}
        
        total_coverage = policy_data.get("coverage_amount", 0)
        
        # Get all approved/closed claims for this customer
        all_claims = store.search(claims_namespace)
        approved_claims = [
            claim for claim in all_claims
            if _unwrap_item(claim).get("user_id") == customer_id 
            and _unwrap_item(claim).get("status") in ["Approved", "Closed"]
        ]
        
        total_claimed = sum(_unwrap_item(claim).get("amount", 0) for claim in approved_claims)
        remaining_coverage = total_coverage - total_claimed
        
        logger.info(f"Calculated remaining coverage for customer {customer_id}: {remaining_coverage}")
        return {
            "customer_id": customer_id,
            "policy_id": policy_id,
            "total_coverage": total_coverage,
            "amount_claimed": total_claimed,
            "remaining_coverage": max(0, remaining_coverage),
            "utilization_percent": round((total_claimed / total_coverage * 100) if total_coverage > 0 else 0, 2)
        }
    except Exception as e:
        logger.error(f"Failed to calculate remaining coverage: {str(e)}")
        return {"error": f"Failed to calculate remaining coverage: {str(e)}"}


@tool
def get_premium_breakdown(policy_id: str) -> Dict[str, Any]:
    """
    Get premium breakdown (annual, monthly, quarterly payments).
    
    Args:
        policy_id: The unique policy ID
    
    Returns:
        Detailed premium breakdown
    """
    try:
        store = get_store()
        policy_data = _unwrap_item(store.get(namespace=policies_namespace, key=policy_id))
        
        if not policy_data:
            logger.warning(f"Policy {policy_id} not found for premium breakdown")
            return {"error": f"Policy {policy_id} not found"}
        
        annual_premium = policy_data.get("premium", 0)
        monthly_premium = annual_premium / 12
        quarterly_premium = annual_premium / 4
        
        logger.info(f"Retrieved premium breakdown for policy {policy_id}")
        return {
            "policy_id": policy_id,
            "policy_type": policy_data.get("policy_type"),
            "coverage": policy_data.get("coverage_amount", 0),
            "annual_premium": round(annual_premium, 2),
            "monthly_premium": round(monthly_premium, 2),
            "quarterly_premium": round(quarterly_premium, 2),
            "payment_schedule": {
                "annual": round(annual_premium, 2),
                "semi_annual": round(annual_premium / 2, 2),
                "quarterly": round(quarterly_premium, 2),
                "monthly": round(monthly_premium, 2)
            }
        }
    except Exception as e:
        logger.error(f"Failed to retrieve premium breakdown: {str(e)}")
        return {"error": f"Failed to retrieve premium breakdown: {str(e)}"}


# ===========================
# SYSTEM & FILTER TOOLS
# ===========================

@tool
def filter_claims_by_status(status: str) -> Dict[str, Any]:
    """
    Filter claims by status across all customers.
    
    Args:
        status: Claim status to filter by (Processing, Approved, Closed, Under Investigation, Denied)
    
    Returns:
        List of all claims with specified status
    """
    try:
        store = get_store()
        
        # Get all claims and filter by status
        all_claims = store.search(claims_namespace)
        filtered_claims = [
            {
                "claim_id": claim.key,
                **_unwrap_item(claim)
            }
            for claim in all_claims
            if _unwrap_item(claim).get("status") == status
        ]
        
        logger.info(f"Found {len(filtered_claims)} claims with status {status}")
        return {
            "status": status,
            "claims": filtered_claims,
            "count": len(filtered_claims)
        }
    except Exception as e:
        logger.error(f"Failed to filter claims by status: {str(e)}")
        return {"error": f"Failed to filter claims by status: {str(e)}"}


def _get_current_system_date() -> str:
    """
    Internal helper to get current system date and time.
    
    Returns:
        Current system date and time as ISO format string
    """
    return datetime.now().isoformat()


@tool
def get_current_system_date() -> str:
    """
    Get current system date and time.
    
    Returns:
        Current system date and time as ISO format string
    """
    current_date = _get_current_system_date()
    logger.info(f"Retrieved current system date: {current_date}")
    return current_date


# ===========================
# HELPER FUNCTIONS
# ===========================

def _calculate_annual_premium(policy: Dict[str, Any]) -> float:
    """
    Calculate annual premium based on policy type and coverage.
    Premium calculation: coverage * rate based on type.
    """
    coverage = policy.get("coverage", 0)
    policy_type = policy.get("type", "Standard")
    
    # Premium rates per $1000 of coverage
    rates = {
        "Health": 0.008,      # $8 per $1000
        "Auto": 0.012,        # $12 per $1000
        "Home": 0.006,        # $6 per $1000
        "Standard": 0.010     # $10 per $1000
    }
    
    rate = rates.get(policy_type, 0.010)
    return coverage * rate


def _calculate_deductible(policy: Dict[str, Any]) -> float:
    """
    Calculate deductible based on policy type.
    Standard deductibles by type.
    """
    policy_type = policy.get("type", "Standard")
    
    deductibles = {
        "Health": 1000,
        "Auto": 500,
        "Home": 2000,
        "Standard": 750
    }
    
    return deductibles.get(policy_type, 750)


# ===========================
# TOOL REGISTRY
# ===========================

def get_all_insurance_tools():
    """Returns a list of all available insurance tools for the agent."""
    return [
        get_customer_information,
        get_customer_infoname,
        get_customer_policies,
        get_policy_details,
        check_claims_exist,
        get_customer_claims,
        get_claim_status,
        add_new_claim,
        update_claim_status,
        calculate_remaining_coverage,
        get_premium_breakdown,
        filter_claims_by_status,
        get_current_system_date,
    ]


# Export TOOLS for compatibility
TOOLS = get_all_insurance_tools()
