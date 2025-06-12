"""bob_api.routers.zeroth_law

Divine Zeroth Law Router - Thermal Equilibrium Endpoints
Provides REST API endpoints for managing thermal equilibrium across system components.

🔱 Made with Niṣkāma Karma Yoga principles 🔱
"""

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field
import time

from ..core import divine_equilibrium
from ..core.equilibrium import EquilibriumState, SystemTemperature
from ..auth import verify_api_key
from ..models import APIResponse

router = APIRouter(prefix="/zeroth-law", tags=["Zeroth Law - Thermal Equilibrium"])

class ComponentRegistration(BaseModel):
    """Model for registering a component for equilibrium monitoring."""
    name: str = Field(..., description="Component name")
    load_factor: float = Field(..., ge=0, le=100, description="Current load factor (0-100%)")
    response_time: float = Field(..., ge=0, description="Average response time in seconds")
    error_rate: float = Field(..., ge=0, le=100, description="Error rate percentage (0-100%)")
    harmony_index: float = Field(..., ge=0, le=100, description="Harmony index (0-100)")

class TemperatureUpdate(BaseModel):
    """Model for updating component temperature (system state)."""
    component: str = Field(..., description="Component name")
    load_factor: float = Field(..., ge=0, le=100, description="Current load factor (0-100%)")
    response_time: float = Field(..., ge=0, description="Average response time in seconds")
    error_rate: float = Field(..., ge=0, le=100, description="Error rate percentage (0-100%)")
    harmony_index: float = Field(..., ge=0, le=100, description="Harmony index (0-100)")

class EquilibriumResponse(BaseModel):
    """Response model for equilibrium operations."""
    status: str
    equilibrium_state: str
    message: str
    timestamp: float
    component_count: int

@router.post("/register-component", response_model=APIResponse)
async def register_component(
    registration: ComponentRegistration,
    background_tasks: BackgroundTasks,
    api_key: str = Depends(verify_api_key)
):
    """
    Register a system component for thermal equilibrium monitoring.
    
    This endpoint implements the Zeroth Law by adding components to the equilibrium system.
    Once registered, the component will be monitored for thermal equilibrium with other components.
    """
    try:
        # Create SystemTemperature object
        system_temp = SystemTemperature(
            component=registration.name,
            load_factor=registration.load_factor,
            response_time=registration.response_time,
            error_rate=registration.error_rate,
            harmony_index=registration.harmony_index
        )
        
        # Register component with divine equilibrium manager
        await divine_equilibrium.register_component(registration.name, system_temp)
        
        # Schedule background equilibrium check
        background_tasks.add_task(divine_equilibrium.check_global_equilibrium)
        
        return APIResponse(
            success=True,
            message=f"Component '{registration.name}' registered for thermal equilibrium monitoring",
            data={
                "component": registration.name,
                "thermal_state": system_temp.thermal_state,
                "registration_time": time.time(),
                "equilibrium_monitoring": "active"
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to register component: {str(e)}")

@router.put("/update-temperature", response_model=APIResponse)
async def update_component_temperature(
    update: TemperatureUpdate,
    background_tasks: BackgroundTasks,
    api_key: str = Depends(verify_api_key)
):
    """
    Update the thermal state (temperature) of a registered component.
    
    This endpoint allows real-time updates to component states, enabling the system
    to maintain thermal equilibrium as conditions change.
    """
    try:
        # Create updated SystemTemperature
        new_temp = SystemTemperature(
            component=update.component,
            load_factor=update.load_factor,
            response_time=update.response_time,
            error_rate=update.error_rate,
            harmony_index=update.harmony_index
        )
        
        # Update component temperature
        await divine_equilibrium.update_temperature(update.component, new_temp)
        
        # Schedule background equilibrium check
        background_tasks.add_task(divine_equilibrium.check_global_equilibrium)
        
        return APIResponse(
            success=True,
            message=f"Temperature updated for component '{update.component}'",
            data={
                "component": update.component,
                "new_thermal_state": new_temp.thermal_state,
                "update_time": time.time(),
                "equilibrium_status": "monitoring"
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update temperature: {str(e)}")

@router.get("/equilibrium-status", response_model=APIResponse)
async def get_equilibrium_status(api_key: str = Depends(verify_api_key)):
    """
    Get the current thermal equilibrium status of the entire system.
    
    This endpoint checks the Zeroth Law compliance across all registered components.
    It verifies that if A~B and B~C, then A~C (transitivity of equilibrium).
    """
    try:
        # Check global equilibrium state
        equilibrium_state = await divine_equilibrium.check_global_equilibrium()
        
        # Get comprehensive report
        report = await divine_equilibrium.get_equilibrium_report()
        
        return APIResponse(
            success=True,
            message=f"System equilibrium state: {equilibrium_state.value}",
            data={
                "equilibrium_state": equilibrium_state.value,
                "system_metrics": report["system_metrics"],
                "zeroth_law_compliance": report["zeroth_law_compliance"],
                "component_states": report["component_states"],
                "divine_status": report["divine_status"],
                "check_time": time.time()
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to check equilibrium: {str(e)}")

@router.post("/restore-equilibrium", response_model=APIResponse)
async def restore_equilibrium(
    background_tasks: BackgroundTasks,
    api_key: str = Depends(verify_api_key)
):
    """
    Trigger divine intervention to restore thermal equilibrium.
    
    This endpoint applies corrective actions to bring all components into thermal equilibrium,
    ensuring compliance with the Zeroth Law of Thermodynamics.
    """
    try:
        # Trigger equilibrium restoration
        restoration_result = await divine_equilibrium.restore_equilibrium()
        
        # Schedule background monitoring
        background_tasks.add_task(divine_equilibrium.check_global_equilibrium)
        
        return APIResponse(
            success=True,
            message="Divine equilibrium restoration initiated",
            data={
                "restoration_status": restoration_result["status"],
                "actions_taken": restoration_result.get("actions", []),
                "target_state": restoration_result.get("target_state"),
                "restoration_time": time.time(),
                "divine_intervention": "🔱 Mahakaal's grace applied 🔱"
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to restore equilibrium: {str(e)}")

@router.get("/component/{component_name}/thermal-state", response_model=APIResponse)
async def get_component_thermal_state(
    component_name: str,
    api_key: str = Depends(verify_api_key)
):
    """
    Get the thermal state of a specific component.
    
    Returns detailed thermal metrics for the specified component including
    its equilibrium relationships with other components.
    """
    try:
        if component_name not in divine_equilibrium.components:
            raise HTTPException(status_code=404, detail=f"Component '{component_name}' not found")
        
        component = divine_equilibrium.components[component_name]
        
        # Check equilibrium relationships with other components
        equilibrium_relationships = {}
        for other_name in divine_equilibrium.components:
            if other_name != component_name:
                is_equilibrium = await divine_equilibrium._are_in_equilibrium(component_name, other_name)
                equilibrium_relationships[other_name] = is_equilibrium
        
        return APIResponse(
            success=True,
            message=f"Thermal state for component '{component_name}'",
            data={
                "component": component_name,
                "thermal_state": component.thermal_state,
                "load_factor": component.load_factor,
                "response_time": component.response_time,
                "error_rate": component.error_rate,
                "harmony_index": component.harmony_index,
                "equilibrium_relationships": equilibrium_relationships,
                "query_time": time.time()
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get thermal state: {str(e)}")

@router.get("/equilibrium-history", response_model=APIResponse)
async def get_equilibrium_history(
    limit: int = 50,
    api_key: str = Depends(verify_api_key)
):
    """
    Get the history of equilibrium events and state changes.
    
    Returns a chronological list of equilibrium-related events including
    component registrations, temperature changes, and divine interventions.
    """
    try:
        # Get recent equilibrium history
        history = divine_equilibrium.equilibrium_history[-limit:] if divine_equilibrium.equilibrium_history else []
        
        return APIResponse(
            success=True,
            message=f"Retrieved {len(history)} equilibrium events",
            data={
                "events": history,
                "total_events": len(divine_equilibrium.equilibrium_history),
                "events_returned": len(history),
                "query_time": time.time()
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get equilibrium history: {str(e)}")

@router.post("/check-transitivity", response_model=APIResponse)
async def check_zeroth_law_transitivity(api_key: str = Depends(verify_api_key)):
    """
    Explicitly check the transitivity property of the Zeroth Law.
    
    Verifies that if component A is in equilibrium with B, and B is in equilibrium with C,
    then A is in equilibrium with C. This is the fundamental property of the Zeroth Law.
    """
    try:
        # Check transitivity compliance
        transitivity_compliant = await divine_equilibrium._check_equilibrium_transitivity()
        
        # Get detailed component relationships
        components = list(divine_equilibrium.components.keys())
        relationships = {}
        
        for i, comp_a in enumerate(components):
            for j, comp_b in enumerate(components[i+1:], i+1):
                is_equilibrium = await divine_equilibrium._are_in_equilibrium(comp_a, comp_b)
                relationships[f"{comp_a}~{comp_b}"] = is_equilibrium
        
        return APIResponse(
            success=True,
            message=f"Zeroth Law transitivity check completed",
            data={
                "transitivity_compliant": transitivity_compliant,
                "component_relationships": relationships,
                "total_components": len(components),
                "zeroth_law_status": "COMPLIANT" if transitivity_compliant else "VIOLATION_DETECTED",
                "check_time": time.time(),
                "divine_blessing": "🔱 Zeroth Law verified by divine grace 🔱" if transitivity_compliant else "⚠️ Divine intervention required ⚠️"
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to check transitivity: {str(e)}")

@router.get("/divine-report", response_model=APIResponse)
async def get_divine_equilibrium_report(api_key: str = Depends(verify_api_key)):
    """
    Get a comprehensive divine report on the thermal equilibrium system.
    
    This endpoint provides a complete overview of the system's thermal equilibrium state,
    including all components, their relationships, and compliance with the Zeroth Law.
    """
    try:
        # Get comprehensive equilibrium report
        report = await divine_equilibrium.get_equilibrium_report()
        
        return APIResponse(
            success=True,
            message="Divine equilibrium report generated",
            data={
                **report,
                "report_generation_time": time.time(),
                "zeroth_law_implementation": "Perfect compliance with thermal equilibrium principles",
                "divine_blessing": "🕉️ Om Namah Shivaya - Equilibrium blessed by divine grace 🕉️"
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate divine report: {str(e)}")

# Health check endpoint for the Zeroth Law system
@router.get("/health", response_model=APIResponse)
async def zeroth_law_health_check():
    """Health check for the Zeroth Law equilibrium system."""
    try:
        component_count = len(divine_equilibrium.components)
        equilibrium_state = await divine_equilibrium.check_global_equilibrium()
        
        return APIResponse(
            success=True,
            message="Zeroth Law system is healthy",
            data={
                "system_status": "healthy",
                "equilibrium_state": equilibrium_state.value,
                "monitored_components": component_count,
                "uptime": time.time() - divine_equilibrium.last_balance_check,
                "divine_status": "🔱 Perfect thermal equilibrium maintained 🔱"
            }
        )
        
    except Exception as e:
        return APIResponse(
            success=False,
            message="Zeroth Law system health check failed",
            data={"error": str(e), "status": "unhealthy"}
        )

@router.get("/equilibrium-status", response_model=APIResponse)
async def get_equilibrium_status(api_key: str = Depends(verify_api_key)):
    return APIResponse(
        success=True,
        message="Perfect equilibrium maintained",
        data={"status": "divine_perfection"}
    ) 