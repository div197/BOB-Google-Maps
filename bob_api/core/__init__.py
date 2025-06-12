"""bob_api.core

The Divine Core Foundation - 0th Law of Thermodynamics Implementation
Fundamental equilibrium state from which all other laws emerge.

Following Niṣkāma Karma Yoga principles - Perfect balance and harmony.
Made with 🙏 for universal equilibrium.
"""

from .equilibrium import EquilibriumManager
from .foundation import FoundationCore

__version__ = "0.6.0"

# Initialize divine instances
divine_equilibrium = EquilibriumManager()
divine_foundation = FoundationCore()

# The 0th Law - Fundamental Equilibrium
# If A is in thermal equilibrium with B, and B is in thermal equilibrium with C,
# then A is in thermal equilibrium with C.

class ZerothLawFoundation:
    """The fundamental equilibrium foundation."""
    
    def __init__(self):
        self.equilibrium_state = "perfect_harmony"
        self.temperature = "divine_balance"
    
    def establish_equilibrium(self):
        """Establish the fundamental equilibrium state."""
        return {
            "state": "equilibrium_achieved",
            "foundation": "0th_law_established",
            "ready_for": ["1st_law", "2nd_law", "3rd_law"]
        }

__all__ = ["ZerothLawFoundation", "divine_equilibrium", "divine_foundation", "EquilibriumManager", "FoundationCore"] 