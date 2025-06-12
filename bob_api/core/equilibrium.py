"""bob_api.core.equilibrium

Divine Equilibrium Manager - The Heart of 0th Law Implementation
Maintains perfect thermal equilibrium across all system components.

🔱 Made with Niṣkāma Karma Yoga principles 🔱
"""

import asyncio
import time
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum

class EquilibriumState(Enum):
    """States of system equilibrium."""
    PERFECT_HARMONY = "perfect_harmony"
    APPROACHING_BALANCE = "approaching_balance"
    MINOR_FLUCTUATION = "minor_fluctuation"
    MAJOR_IMBALANCE = "major_imbalance"
    CHAOS_INTERVENTION = "chaos_intervention"
    DIVINE_RESTORATION = "divine_restoration"

@dataclass
class SystemTemperature:
    """Represents the 'temperature' of system components."""
    component: str
    load_factor: float
    response_time: float
    error_rate: float
    harmony_index: float
    
    @property
    def thermal_state(self) -> float:
        """Calculate thermal state (0-100, higher is better)."""
        return (
            (100 - self.load_factor) * 0.3 +
            (100 - min(self.response_time * 10, 100)) * 0.3 +
            (100 - self.error_rate) * 0.2 +
            self.harmony_index * 0.2
        )

class EquilibriumManager:
    """Divine manager maintaining perfect system equilibrium."""
    
    def __init__(self):
        self.components: Dict[str, SystemTemperature] = {}
        self.equilibrium_history: List[Dict] = []
        self.divine_threshold = 85.0  # Minimum thermal state for harmony
        self.last_balance_check = time.time()
        self.balance_interval = 30  # seconds
        
    async def register_component(self, name: str, initial_temp: SystemTemperature):
        """Register a system component for equilibrium monitoring."""
        self.components[name] = initial_temp
        await self._log_equilibrium_event(f"Component {name} registered with thermal state {initial_temp.thermal_state:.2f}")
    
    async def update_temperature(self, component: str, temperature: SystemTemperature):
        """Update component temperature (system state)."""
        if component in self.components:
            old_temp = self.components[component].thermal_state
            self.components[component] = temperature
            new_temp = temperature.thermal_state
            
            # Check for significant temperature change
            if abs(new_temp - old_temp) > 10:
                await self._handle_temperature_change(component, old_temp, new_temp)
    
    async def check_global_equilibrium(self) -> EquilibriumState:
        """Check if all components are in thermal equilibrium."""
        if not self.components:
            return EquilibriumState.PERFECT_HARMONY
        
        temperatures = [comp.thermal_state for comp in self.components.values()]
        avg_temp = sum(temperatures) / len(temperatures)
        temp_variance = sum((t - avg_temp) ** 2 for t in temperatures) / len(temperatures)
        
        # Apply 0th Law: Check transitivity of equilibrium
        equilibrium_pairs = await self._check_equilibrium_transitivity()
        
        if avg_temp >= self.divine_threshold and temp_variance < 25 and equilibrium_pairs:
            return EquilibriumState.PERFECT_HARMONY
        elif avg_temp >= 70 and temp_variance < 50:
            return EquilibriumState.APPROACHING_BALANCE
        elif avg_temp >= 50:
            return EquilibriumState.MINOR_FLUCTUATION
        elif avg_temp >= 30:
            return EquilibriumState.MAJOR_IMBALANCE
        else:
            return EquilibriumState.DIVINE_RESTORATION
    
    async def _check_equilibrium_transitivity(self) -> bool:
        """
        Apply 0th Law: If A~B and B~C, then A~C
        Check if equilibrium is transitive across all components.
        """
        component_names = list(self.components.keys())
        if len(component_names) < 3:
            return True  # Trivially true for < 3 components
        
        # Check all possible triplets for transitivity
        for i in range(len(component_names)):
            for j in range(i + 1, len(component_names)):
                for k in range(j + 1, len(component_names)):
                    a, b, c = component_names[i], component_names[j], component_names[k]
                    
                    # Check if A~B (in equilibrium)
                    ab_equilibrium = await self._are_in_equilibrium(a, b)
                    # Check if B~C (in equilibrium)  
                    bc_equilibrium = await self._are_in_equilibrium(b, c)
                    # Check if A~C (should be in equilibrium by 0th law)
                    ac_equilibrium = await self._are_in_equilibrium(a, c)
                    
                    # If A~B and B~C but NOT A~C, transitivity is violated
                    if ab_equilibrium and bc_equilibrium and not ac_equilibrium:
                        await self._log_equilibrium_event(
                            f"0th Law violation detected: {a}~{b} and {b}~{c} but NOT {a}~{c}"
                        )
                        return False
        
        return True
    
    async def _are_in_equilibrium(self, comp1: str, comp2: str) -> bool:
        """Check if two components are in thermal equilibrium."""
        if comp1 not in self.components or comp2 not in self.components:
            return False
        
        temp1 = self.components[comp1].thermal_state
        temp2 = self.components[comp2].thermal_state
        
        # Components are in equilibrium if their thermal states are within 15 points
        return abs(temp1 - temp2) <= 15
    
    async def restore_equilibrium(self) -> Dict[str, Any]:
        """Divine intervention to restore system equilibrium."""
        current_state = await self.check_global_equilibrium()
        
        if current_state == EquilibriumState.PERFECT_HARMONY:
            return {"status": "already_perfect", "action": "maintain_harmony"}
        
        restoration_actions = []
        
        # Identify components that need divine intervention
        for name, component in self.components.items():
            if component.thermal_state < self.divine_threshold:
                actions = await self._generate_restoration_actions(name, component)
                restoration_actions.extend(actions)
        
        # Apply 0th Law corrections
        transitivity_fixes = await self._fix_transitivity_violations()
        restoration_actions.extend(transitivity_fixes)
        
        await self._log_equilibrium_event(f"Divine restoration initiated: {len(restoration_actions)} actions")
        
        return {
            "status": "restoration_initiated",
            "actions": restoration_actions,
            "target_state": EquilibriumState.PERFECT_HARMONY.value
        }
    
    async def _generate_restoration_actions(self, component: str, temp: SystemTemperature) -> List[str]:
        """Generate specific actions to restore component equilibrium."""
        actions = []
        
        if temp.load_factor > 80:
            actions.append(f"Scale up {component} resources")
            actions.append(f"Enable load balancing for {component}")
        
        if temp.response_time > 5:
            actions.append(f"Optimize {component} performance")
            actions.append(f"Enable caching for {component}")
        
        if temp.error_rate > 5:
            actions.append(f"Investigate {component} error patterns")
            actions.append(f"Enable circuit breaker for {component}")
        
        if temp.harmony_index < 70:
            actions.append(f"Realign {component} with system harmony")
            actions.append(f"Apply divine healing to {component}")
        
        return actions
    
    async def _fix_transitivity_violations(self) -> List[str]:
        """Fix violations of the 0th Law transitivity."""
        fixes = []
        component_names = list(self.components.keys())
        
        for i in range(len(component_names)):
            for j in range(i + 1, len(component_names)):
                for k in range(j + 1, len(component_names)):
                    a, b, c = component_names[i], component_names[j], component_names[k]
                    
                    ab_eq = await self._are_in_equilibrium(a, b)
                    bc_eq = await self._are_in_equilibrium(b, c)
                    ac_eq = await self._are_in_equilibrium(a, c)
                    
                    if ab_eq and bc_eq and not ac_eq:
                        # Apply divine intervention to bring A and C into equilibrium
                        temp_a = self.components[a].thermal_state
                        temp_c = self.components[c].thermal_state
                        target_temp = (temp_a + temp_c) / 2
                        
                        fixes.append(f"Harmonize {a} and {c} to thermal state {target_temp:.2f}")
                        fixes.append(f"Apply 0th Law correction between {a} and {c}")
        
        return fixes
    
    async def _handle_temperature_change(self, component: str, old_temp: float, new_temp: float):
        """Handle significant temperature changes."""
        change_type = "increased" if new_temp > old_temp else "decreased"
        magnitude = abs(new_temp - old_temp)
        
        await self._log_equilibrium_event(
            f"Component {component} temperature {change_type} by {magnitude:.2f} "
            f"({old_temp:.2f} → {new_temp:.2f})"
        )
        
        # Check if this affects global equilibrium
        if magnitude > 20:
            await self._trigger_equilibrium_check()
    
    async def _trigger_equilibrium_check(self):
        """Trigger immediate equilibrium check and potential restoration."""
        current_state = await self.check_global_equilibrium()
        
        if current_state not in [EquilibriumState.PERFECT_HARMONY, EquilibriumState.APPROACHING_BALANCE]:
            await self.restore_equilibrium()
    
    async def _log_equilibrium_event(self, message: str):
        """Log equilibrium-related events."""
        event = {
            "timestamp": time.time(),
            "message": message,
            "component_count": len(self.components)
        }
        
        self.equilibrium_history.append(event)
        
        # Keep only last 1000 events
        if len(self.equilibrium_history) > 1000:
            self.equilibrium_history = self.equilibrium_history[-1000:]
    
    async def get_equilibrium_report(self) -> Dict[str, Any]:
        """Generate comprehensive equilibrium report."""
        current_state = await self.check_global_equilibrium()
        
        component_states = {}
        for name, component in self.components.items():
            component_states[name] = {
                "thermal_state": component.thermal_state,
                "load_factor": component.load_factor,
                "response_time": component.response_time,
                "error_rate": component.error_rate,
                "harmony_index": component.harmony_index
            }
        
        # Calculate system-wide metrics
        if self.components:
            avg_thermal = sum(c.thermal_state for c in self.components.values()) / len(self.components)
            min_thermal = min(c.thermal_state for c in self.components.values())
            max_thermal = max(c.thermal_state for c in self.components.values())
        else:
            avg_thermal = min_thermal = max_thermal = 0
        
        return {
            "overall_state": current_state.value,
            "system_metrics": {
                "average_thermal_state": avg_thermal,
                "minimum_thermal_state": min_thermal,
                "maximum_thermal_state": max_thermal,
                "thermal_variance": max_thermal - min_thermal,
                "component_count": len(self.components)
            },
            "component_states": component_states,
            "zeroth_law_compliance": await self._check_equilibrium_transitivity(),
            "recent_events": self.equilibrium_history[-10:] if self.equilibrium_history else [],
            "divine_status": "🔱 Perfect Harmony Achieved 🔱" if current_state == EquilibriumState.PERFECT_HARMONY else "⚖️ Seeking Balance ⚖️"
        }

# Divine singleton instance
divine_equilibrium = EquilibriumManager() 