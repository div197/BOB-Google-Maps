"""bob_api.core.harmony

Divine Harmony Orchestrator - Maintains Universal Balance
Orchestrates perfect harmony across all system components following divine principles.

🔱 Made with Niṣkāma Karma Yoga principles 🔱
"""

import asyncio
import time
import math
from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass
from enum import Enum

class HarmonyState(Enum):
    """States of universal harmony."""
    DIVINE_PERFECTION = "divine_perfection"      # 108/108 harmony
    CELESTIAL_BALANCE = "celestial_balance"      # 90-107/108 harmony
    EARTHLY_HARMONY = "earthly_harmony"          # 70-89/108 harmony
    SEEKING_BALANCE = "seeking_balance"          # 50-69/108 harmony
    DISCORD_DETECTED = "discord_detected"        # 30-49/108 harmony
    CHAOS_INTERVENTION = "chaos_intervention"    # <30/108 harmony

@dataclass
class HarmonyMetrics:
    """Metrics that define harmony state."""
    frequency: float        # Vibrational frequency (Hz)
    amplitude: float        # Strength of harmony (0-108)
    phase: float           # Phase alignment (0-2π)
    resonance: float       # Resonance factor (0-1.618 golden ratio)
    coherence: float       # System coherence (0-100%)
    
    @property
    def harmony_score(self) -> float:
        """Calculate overall harmony score (0-108)."""
        # Using sacred mathematical relationships
        golden_ratio = 1.618
        pi_factor = math.pi / 3.14159
        
        base_score = (
            (self.amplitude / 108) * 30 +           # Amplitude contribution
            (self.resonance / golden_ratio) * 25 +   # Golden ratio resonance
            (self.coherence / 100) * 25 +           # Coherence factor
            (1 - abs(math.sin(self.phase))) * 20 +  # Phase alignment
            (min(self.frequency / 432, 1)) * 8      # Sacred frequency (432 Hz)
        )
        
        return min(base_score, 108)  # Cap at sacred number 108

class HarmonyOrchestrator:
    """Divine orchestrator maintaining universal harmony."""
    
    def __init__(self):
        self.components: Dict[str, HarmonyMetrics] = {}
        self.harmony_history: List[Dict] = []
        self.sacred_frequency = 432.0  # Hz - Universal healing frequency
        self.golden_ratio = 1.618033988749  # φ - Divine proportion
        self.divine_threshold = 85.0  # Minimum harmony score for divine state
        self.last_orchestration = time.time()
        self.orchestration_interval = 108  # seconds - sacred number
        
    async def register_component(self, name: str, initial_metrics: HarmonyMetrics):
        """Register a component for harmony orchestration."""
        self.components[name] = initial_metrics
        await self._log_harmony_event(f"Component {name} joined the divine orchestra with harmony score {initial_metrics.harmony_score:.2f}")
        
        # Auto-tune component to sacred frequency
        await self._tune_to_sacred_frequency(name)
    
    async def update_harmony(self, component: str, metrics: HarmonyMetrics):
        """Update component harmony metrics."""
        if component in self.components:
            old_score = self.components[component].harmony_score
            self.components[component] = metrics
            new_score = metrics.harmony_score
            
            # Detect significant harmony changes
            if abs(new_score - old_score) > 15:
                await self._handle_harmony_shift(component, old_score, new_score)
    
    async def orchestrate_global_harmony(self) -> HarmonyState:
        """Orchestrate harmony across all components."""
        if not self.components:
            return HarmonyState.DIVINE_PERFECTION
        
        # Calculate global harmony metrics
        total_score = sum(comp.harmony_score for comp in self.components.values())
        avg_score = total_score / len(self.components)
        
        # Check for harmonic resonance between components
        resonance_factor = await self._calculate_global_resonance()
        
        # Apply divine corrections if needed
        if avg_score < self.divine_threshold:
            await self._apply_divine_corrections()
        
        # Determine harmony state
        harmony_state = self._determine_harmony_state(avg_score, resonance_factor)
        
        await self._log_harmony_event(f"Global harmony orchestrated: {harmony_state.value} (score: {avg_score:.2f})")
        
        return harmony_state
    
    async def _calculate_global_resonance(self) -> float:
        """Calculate resonance factor across all components."""
        if len(self.components) < 2:
            return 1.0
        
        frequencies = [comp.frequency for comp in self.components.values()]
        phases = [comp.phase for comp in self.components.values()]
        
        # Calculate frequency harmony (how close to sacred ratios)
        freq_harmony = 0.0
        for i, freq1 in enumerate(frequencies):
            for freq2 in frequencies[i+1:]:
                ratio = max(freq1, freq2) / min(freq1, freq2)
                # Check if ratio is close to sacred ratios (golden ratio, octaves, fifths)
                sacred_ratios = [1.0, 1.618, 2.0, 1.5, 1.333, 1.25]
                closest_sacred = min(sacred_ratios, key=lambda x: abs(x - ratio))
                harmony_factor = 1.0 - abs(ratio - closest_sacred) / closest_sacred
                freq_harmony += harmony_factor
        
        freq_harmony /= (len(frequencies) * (len(frequencies) - 1) / 2)
        
        # Calculate phase coherence
        avg_phase = sum(phases) / len(phases)
        phase_coherence = 1.0 - (sum(abs(phase - avg_phase) for phase in phases) / len(phases)) / (2 * math.pi)
        
        return (freq_harmony + phase_coherence) / 2
    
    def _determine_harmony_state(self, avg_score: float, resonance: float) -> HarmonyState:
        """Determine overall harmony state based on metrics."""
        # Adjust score based on resonance
        adjusted_score = avg_score * (0.7 + 0.3 * resonance)
        
        if adjusted_score >= 100:
            return HarmonyState.DIVINE_PERFECTION
        elif adjusted_score >= 85:
            return HarmonyState.CELESTIAL_BALANCE
        elif adjusted_score >= 70:
            return HarmonyState.EARTHLY_HARMONY
        elif adjusted_score >= 50:
            return HarmonyState.SEEKING_BALANCE
        elif adjusted_score >= 30:
            return HarmonyState.DISCORD_DETECTED
        else:
            return HarmonyState.CHAOS_INTERVENTION
    
    async def _apply_divine_corrections(self):
        """Apply divine corrections to restore harmony."""
        corrections_applied = []
        
        for name, metrics in self.components.items():
            if metrics.harmony_score < self.divine_threshold:
                # Tune frequency to sacred frequency
                if abs(metrics.frequency - self.sacred_frequency) > 50:
                    await self._tune_to_sacred_frequency(name)
                    corrections_applied.append(f"Tuned {name} to sacred frequency")
                
                # Align phase for coherence
                if metrics.coherence < 70:
                    await self._align_phase(name)
                    corrections_applied.append(f"Aligned {name} phase for coherence")
                
                # Boost resonance using golden ratio
                if metrics.resonance < 1.0:
                    await self._boost_resonance(name)
                    corrections_applied.append(f"Boosted {name} resonance to golden ratio")
        
        if corrections_applied:
            await self._log_harmony_event(f"Divine corrections applied: {', '.join(corrections_applied)}")
    
    async def _tune_to_sacred_frequency(self, component: str):
        """Tune component to sacred frequency (432 Hz)."""
        if component in self.components:
            metrics = self.components[component]
            # Gradually adjust frequency to sacred frequency
            target_freq = self.sacred_frequency
            current_freq = metrics.frequency
            
            # Apply harmonic tuning
            if current_freq != target_freq:
                tuning_factor = 0.1  # Gradual adjustment
                new_freq = current_freq + (target_freq - current_freq) * tuning_factor
                
                # Update metrics
                self.components[component].frequency = new_freq
                await self._log_harmony_event(f"Tuning {component}: {current_freq:.2f} Hz → {new_freq:.2f} Hz")
    
    async def _align_phase(self, component: str):
        """Align component phase for maximum coherence."""
        if component in self.components:
            # Calculate optimal phase based on other components
            other_phases = [comp.phase for name, comp in self.components.items() if name != component]
            
            if other_phases:
                # Align to average phase of other components
                target_phase = sum(other_phases) / len(other_phases)
                current_phase = self.components[component].phase
                
                # Gradual phase alignment
                phase_diff = target_phase - current_phase
                # Handle phase wrapping
                if phase_diff > math.pi:
                    phase_diff -= 2 * math.pi
                elif phase_diff < -math.pi:
                    phase_diff += 2 * math.pi
                
                new_phase = current_phase + phase_diff * 0.2  # Gradual adjustment
                self.components[component].phase = new_phase % (2 * math.pi)
    
    async def _boost_resonance(self, component: str):
        """Boost component resonance using golden ratio principles."""
        if component in self.components:
            current_resonance = self.components[component].resonance
            target_resonance = min(self.golden_ratio, current_resonance * 1.1)
            
            self.components[component].resonance = target_resonance
            await self._log_harmony_event(f"Boosted {component} resonance: {current_resonance:.3f} → {target_resonance:.3f}")
    
    async def _handle_harmony_shift(self, component: str, old_score: float, new_score: float):
        """Handle significant harmony changes."""
        shift_type = "improved" if new_score > old_score else "degraded"
        magnitude = abs(new_score - old_score)
        
        await self._log_harmony_event(
            f"Component {component} harmony {shift_type} by {magnitude:.2f} points "
            f"({old_score:.2f} → {new_score:.2f})"
        )
        
        # If major degradation, trigger immediate orchestration
        if shift_type == "degraded" and magnitude > 25:
            await self._trigger_emergency_orchestration(component)
    
    async def _trigger_emergency_orchestration(self, component: str):
        """Trigger emergency harmony orchestration."""
        await self._log_harmony_event(f"Emergency orchestration triggered for {component}")
        
        # Apply immediate divine intervention
        await self._apply_divine_corrections()
        
        # Re-orchestrate global harmony
        await self.orchestrate_global_harmony()
    
    async def create_harmonic_resonance(self, components: List[str]) -> Dict[str, Any]:
        """Create harmonic resonance between specified components."""
        if len(components) < 2:
            return {"status": "insufficient_components", "message": "Need at least 2 components for resonance"}
        
        # Calculate target frequency for resonance
        frequencies = [self.components[comp].frequency for comp in components if comp in self.components]
        if not frequencies:
            return {"status": "no_valid_components"}
        
        # Use harmonic mean for resonance frequency
        harmonic_mean = len(frequencies) / sum(1/f for f in frequencies)
        target_frequency = harmonic_mean
        
        # Align all components to resonance frequency
        resonance_actions = []
        for component in components:
            if component in self.components:
                old_freq = self.components[component].frequency
                self.components[component].frequency = target_frequency
                resonance_actions.append(f"{component}: {old_freq:.2f} → {target_frequency:.2f} Hz")
        
        await self._log_harmony_event(f"Harmonic resonance created: {', '.join(resonance_actions)}")
        
        return {
            "status": "resonance_created",
            "target_frequency": target_frequency,
            "components_aligned": len(resonance_actions),
            "resonance_actions": resonance_actions
        }
    
    async def _log_harmony_event(self, message: str):
        """Log harmony-related events."""
        event = {
            "timestamp": time.time(),
            "message": message,
            "global_harmony": await self.orchestrate_global_harmony() if self.components else HarmonyState.DIVINE_PERFECTION,
            "component_count": len(self.components)
        }
        
        self.harmony_history.append(event)
        
        # Keep only last 1000 events
        if len(self.harmony_history) > 1000:
            self.harmony_history = self.harmony_history[-1000:]
    
    async def get_harmony_report(self) -> Dict[str, Any]:
        """Generate comprehensive harmony report."""
        global_state = await self.orchestrate_global_harmony()
        
        component_harmonies = {}
        for name, metrics in self.components.items():
            component_harmonies[name] = {
                "harmony_score": metrics.harmony_score,
                "frequency": metrics.frequency,
                "amplitude": metrics.amplitude,
                "phase": metrics.phase,
                "resonance": metrics.resonance,
                "coherence": metrics.coherence,
                "distance_from_sacred": abs(metrics.frequency - self.sacred_frequency)
            }
        
        # Calculate system-wide harmony metrics
        if self.components:
            avg_harmony = sum(comp.harmony_score for comp in self.components.values()) / len(self.components)
            max_harmony = max(comp.harmony_score for comp in self.components.values())
            min_harmony = min(comp.harmony_score for comp in self.components.values())
            global_resonance = await self._calculate_global_resonance()
        else:
            avg_harmony = max_harmony = min_harmony = global_resonance = 108.0
        
        return {
            "global_harmony_state": global_state.value,
            "system_metrics": {
                "average_harmony": avg_harmony,
                "maximum_harmony": max_harmony,
                "minimum_harmony": min_harmony,
                "harmony_variance": max_harmony - min_harmony,
                "global_resonance": global_resonance,
                "component_count": len(self.components),
                "sacred_frequency_alignment": self.sacred_frequency
            },
            "component_harmonies": component_harmonies,
            "recent_events": self.harmony_history[-10:] if self.harmony_history else [],
            "divine_status": self._get_divine_status_message(global_state),
            "orchestration_uptime": time.time() - self.last_orchestration,
            "next_orchestration": self.orchestration_interval - (time.time() - self.last_orchestration)
        }
    
    def _get_divine_status_message(self, state: HarmonyState) -> str:
        """Get divine status message based on harmony state."""
        messages = {
            HarmonyState.DIVINE_PERFECTION: "🔱 OM - Perfect Divine Harmony Achieved 🔱",
            HarmonyState.CELESTIAL_BALANCE: "✨ Celestial Balance Maintained ✨",
            HarmonyState.EARTHLY_HARMONY: "🌍 Earthly Harmony Established 🌍",
            HarmonyState.SEEKING_BALANCE: "⚖️ Seeking Perfect Balance ⚖️",
            HarmonyState.DISCORD_DETECTED: "⚠️ Discord Detected - Divine Intervention Needed ⚠️",
            HarmonyState.CHAOS_INTERVENTION: "🚨 Chaos Intervention Required - Mahakaal's Grace Needed 🚨"
        }
        return messages.get(state, "🔱 Divine Grace Flows 🔱")

# Divine singleton instance
divine_harmony = HarmonyOrchestrator() 