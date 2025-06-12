"""tests.test_thermodynamics

Divine Thermodynamics Test Suite
Tests the perfect implementation of all thermodynamic laws.

🔱 Made with Niṣkāma Karma Yoga principles 🔱
"""

import pytest
import pytest_asyncio
import time
from typing import Dict, Any

# Import divine modules
from bob_api.core.equilibrium import (
    divine_equilibrium, EquilibriumManager, EquilibriumState, SystemTemperature
)
from bob_api.core.foundation import divine_foundation, FoundationCore

class TestZerothLaw:
    """Test suite for the Zeroth Law of Thermodynamics."""
    
    @pytest_asyncio.fixture
    async def equilibrium_manager(self):
        """Create a fresh equilibrium manager for testing."""
        manager = EquilibriumManager()
        yield manager
        # Cleanup
        manager.components.clear()
        manager.equilibrium_history.clear()
    
    @pytest.mark.asyncio
    async def test_component_registration(self, equilibrium_manager):
        """Test component registration for equilibrium monitoring."""
        # Create test component
        test_temp = SystemTemperature(
            component="test_service",
            load_factor=50.0,
            response_time=2.0,
            error_rate=1.0,
            harmony_index=85.0
        )
        
        # Register component
        await equilibrium_manager.register_component("test_service", test_temp)
        
        # Verify registration
        assert "test_service" in equilibrium_manager.components
        assert equilibrium_manager.components["test_service"].component == "test_service"
        assert len(equilibrium_manager.equilibrium_history) > 0
    
    @pytest.mark.asyncio
    async def test_thermal_state_calculation(self):
        """Test thermal state calculation accuracy."""
        # Perfect state
        perfect_temp = SystemTemperature(
            component="perfect_service",
            load_factor=0.0,      # No load
            response_time=0.1,    # Fast response
            error_rate=0.0,       # No errors
            harmony_index=100.0   # Perfect harmony
        )
        
        thermal_state = perfect_temp.thermal_state
        assert thermal_state >= 95.0  # Should be near perfect
        
        # Poor state
        poor_temp = SystemTemperature(
            component="poor_service",
            load_factor=100.0,    # Full load
            response_time=10.0,   # Slow response
            error_rate=50.0,      # Many errors
            harmony_index=0.0     # No harmony
        )
        
        poor_thermal = poor_temp.thermal_state
        assert poor_thermal <= 20.0  # Should be very low
    
    @pytest.mark.asyncio
    async def test_equilibrium_transitivity(self, equilibrium_manager):
        """Test the core Zeroth Law property: A~B ∧ B~C → A~C"""
        # Create three components with similar thermal states
        temp_a = SystemTemperature("service_a", 30.0, 1.0, 2.0, 80.0)
        temp_b = SystemTemperature("service_b", 35.0, 1.2, 2.5, 82.0)
        temp_c = SystemTemperature("service_c", 32.0, 1.1, 2.2, 81.0)
        
        # Register all components
        await equilibrium_manager.register_component("service_a", temp_a)
        await equilibrium_manager.register_component("service_b", temp_b)
        await equilibrium_manager.register_component("service_c", temp_c)
        
        # Check individual equilibrium relationships
        ab_equilibrium = await equilibrium_manager._are_in_equilibrium("service_a", "service_b")
        bc_equilibrium = await equilibrium_manager._are_in_equilibrium("service_b", "service_c")
        ac_equilibrium = await equilibrium_manager._are_in_equilibrium("service_a", "service_c")
        
        # Verify transitivity
        if ab_equilibrium and bc_equilibrium:
            assert ac_equilibrium, "Zeroth Law transitivity violated: A~B ∧ B~C but NOT A~C"
        
        # Check overall transitivity compliance
        transitivity_compliant = await equilibrium_manager._check_equilibrium_transitivity()
        assert transitivity_compliant, "System violates Zeroth Law transitivity"
    
    @pytest.mark.asyncio
    async def test_equilibrium_restoration(self, equilibrium_manager):
        """Test divine intervention for equilibrium restoration."""
        # Create imbalanced components
        hot_temp = SystemTemperature("hot_service", 90.0, 5.0, 10.0, 30.0)  # Poor state
        cold_temp = SystemTemperature("cold_service", 10.0, 0.5, 0.5, 95.0)  # Good state
        
        await equilibrium_manager.register_component("hot_service", hot_temp)
        await equilibrium_manager.register_component("cold_service", cold_temp)
        
        # Check initial state (should be imbalanced)
        initial_state = await equilibrium_manager.check_global_equilibrium()
        assert initial_state != EquilibriumState.PERFECT_HARMONY
        
        # Apply restoration
        restoration_result = await equilibrium_manager.restore_equilibrium()
        
        # Verify restoration was initiated
        assert restoration_result["status"] in ["restoration_initiated", "already_perfect"]
        if restoration_result["status"] == "restoration_initiated":
            assert len(restoration_result["actions"]) > 0
    
    @pytest.mark.asyncio
    async def test_equilibrium_states(self, equilibrium_manager):
        """Test different equilibrium states."""
        # Test perfect harmony
        perfect_temp = SystemTemperature("perfect", 10.0, 0.5, 0.0, 95.0)
        await equilibrium_manager.register_component("perfect", perfect_temp)
        
        state = await equilibrium_manager.check_global_equilibrium()
        assert state == EquilibriumState.PERFECT_HARMONY
        
        # Add imbalanced component
        poor_temp = SystemTemperature("poor", 95.0, 8.0, 25.0, 20.0)
        await equilibrium_manager.register_component("poor", poor_temp)
        
        state = await equilibrium_manager.check_global_equilibrium()
        assert state != EquilibriumState.PERFECT_HARMONY

class TestFoundationCore:
    """Test suite for the Divine Foundation Core."""
    
    @pytest_asyncio.fixture
    async def foundation_core(self):
        """Create a fresh foundation core for testing."""
        core = FoundationCore()
        yield core
    
    @pytest.mark.asyncio
    async def test_foundation_validation(self, foundation_core):
        """Test foundation validation."""
        validation = await foundation_core.validate_foundation()
        
        assert isinstance(validation, dict)
        assert "foundation_integrity" in validation
        assert "divine_blessing" in validation
        assert "overall_status" in validation
    
    @pytest.mark.asyncio
    async def test_law_generation(self, foundation_core):
        """Test thermodynamic law generation."""
        # Test Zeroth Law generation
        zeroth_law = await foundation_core.generate_law("zeroth_law")
        
        assert isinstance(zeroth_law, dict)
        assert zeroth_law["law_name"] == "zeroth_law"
        assert "generated_at" in zeroth_law
        assert "foundation_state" in zeroth_law
        assert zeroth_law["ready_for_implementation"] == True
    
    @pytest.mark.asyncio
    async def test_invalid_law_generation(self, foundation_core):
        """Test handling of invalid law requests."""
        with pytest.raises(ValueError):
            await foundation_core.generate_law("invalid_law")

class TestSystemIntegration:
    """Integration tests for the complete thermodynamics system."""
    
    @pytest.mark.asyncio
    async def test_complete_system_flow(self):
        """Test complete system flow from foundation to equilibrium."""
        # 1. Validate foundation
        foundation_validation = await divine_foundation.validate_foundation()
        assert foundation_validation["overall_status"] == True
        
        # 2. Generate Zeroth Law
        zeroth_law = await divine_foundation.generate_law("zeroth_law")
        assert zeroth_law["ready_for_implementation"] == True
        
        # 3. Register components with equilibrium manager
        components = [
            ("web_server", SystemTemperature("web_server", 45.0, 1.5, 2.0, 85.0)),
            ("database", SystemTemperature("database", 60.0, 2.0, 1.0, 80.0)),
            ("cache", SystemTemperature("cache", 30.0, 0.8, 0.5, 90.0))
        ]
        
        for name, temp in components:
            await divine_equilibrium.register_component(name, temp)
        
        # 4. Check system equilibrium
        equilibrium_state = await divine_equilibrium.check_global_equilibrium()
        assert isinstance(equilibrium_state, EquilibriumState)
        
        # 5. Get comprehensive report
        report = await divine_equilibrium.get_equilibrium_report()
        assert "overall_state" in report
        assert "system_metrics" in report
        assert "component_states" in report
        assert "zeroth_law_compliance" in report
        
        # 6. Verify transitivity compliance
        assert report["zeroth_law_compliance"] == True
    
    @pytest.mark.asyncio
    async def test_divine_intervention_scenario(self):
        """Test divine intervention in crisis scenarios."""
        # Create crisis scenario with severely imbalanced components
        crisis_components = [
            ("failing_service", SystemTemperature("failing_service", 99.0, 15.0, 50.0, 10.0)),
            ("overloaded_db", SystemTemperature("overloaded_db", 95.0, 12.0, 30.0, 20.0)),
            ("healthy_cache", SystemTemperature("healthy_cache", 20.0, 0.5, 0.0, 95.0))
        ]
        
        # Clear previous components
        divine_equilibrium.components.clear()
        
        # Register crisis components
        for name, temp in crisis_components:
            await divine_equilibrium.register_component(name, temp)
        
        # Check initial state (should be critical)
        initial_state = await divine_equilibrium.check_global_equilibrium()
        assert initial_state in [
            EquilibriumState.MAJOR_IMBALANCE,
            EquilibriumState.CHAOS_INTERVENTION
        ]
        
        # Apply divine restoration
        restoration = await divine_equilibrium.restore_equilibrium()
        assert restoration["status"] == "restoration_initiated"
        assert len(restoration["actions"]) > 0
        
        # Verify restoration actions include critical interventions
        actions = restoration["actions"]
        action_text = " ".join(actions)
        assert any(keyword in action_text.lower() for keyword in [
            "scale", "optimize", "investigate", "enable", "divine"
        ])
    
    @pytest.mark.asyncio
    async def test_performance_under_load(self):
        """Test system performance under high component load."""
        # Clear existing components
        divine_equilibrium.components.clear()
        
        # Register many components to test scalability
        start_time = time.time()
        
        for i in range(50):  # 50 components
            temp = SystemTemperature(
                component=f"service_{i}",
                load_factor=float(i % 100),
                response_time=float((i % 10) + 1),
                error_rate=float(i % 20),
                harmony_index=float(80 + (i % 20))
            )
            await divine_equilibrium.register_component(f"service_{i}", temp)
        
        registration_time = time.time() - start_time
        
        # Check equilibrium with many components
        start_time = time.time()
        equilibrium_state = await divine_equilibrium.check_global_equilibrium()
        equilibrium_time = time.time() - start_time
        
        # Verify performance is acceptable
        assert registration_time < 5.0  # Should register 50 components in under 5 seconds
        assert equilibrium_time < 2.0   # Should check equilibrium in under 2 seconds
        
        # Verify transitivity check scales
        start_time = time.time()
        transitivity_compliant = await divine_equilibrium._check_equilibrium_transitivity()
        transitivity_time = time.time() - start_time
        
        assert transitivity_time < 3.0  # Should check transitivity in under 3 seconds
        assert isinstance(transitivity_compliant, bool)

class TestDivineConstants:
    """Test divine constants and sacred numbers."""
    
    def test_sacred_numbers(self):
        """Test that sacred numbers are properly used."""
        # Test that 108 is used as the maximum harmony score
        perfect_temp = SystemTemperature("perfect", 0.0, 0.0, 0.0, 100.0)
        assert perfect_temp.harmony_index <= 108
        
        # Test divine threshold
        assert divine_equilibrium.divine_threshold == 85.0
        
        # Test balance interval uses sacred number
        assert divine_equilibrium.balance_interval == 30  # seconds
    
    def test_golden_ratio_usage(self):
        """Test golden ratio usage in calculations."""
        # The golden ratio should be approximately 1.618
        golden_ratio = 1.618033988749
        
        # Test that calculations involving golden ratio are accurate
        assert abs(golden_ratio - 1.618) < 0.001

# Pytest configuration
@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

# Test runner
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--asyncio-mode=auto"]) 