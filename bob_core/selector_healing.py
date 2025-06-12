"""bob_core.selector_healing

Selector Healing system for dynamic CSS selector updates and adaptive web scraping.
Follows the principles of Niṣkāma Karma Yoga - selfless service with perfect execution.
"""
from __future__ import annotations

import time
import logging
import re
from typing import Any, Dict, List, Optional, Callable, Union, Tuple
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
import threading
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException, TimeoutException

__all__ = [
    "SelectorHealer", "SelectorStrategy", "SelectorCandidate", 
    "AdaptiveSelectorManager", "SelectorValidationResult",
    "CSSStrategy", "XPathStrategy", "TextStrategy", "AttributeStrategy"
]


@dataclass
class SelectorCandidate:
    """Represents a potential CSS/XPath selector."""
    selector: str
    selector_type: str  # 'css', 'xpath', 'text', 'attribute'
    confidence: float  # 0.0 to 1.0
    last_success_time: float
    success_count: int = 0
    failure_count: int = 0
    context: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def success_rate(self) -> float:
        """Calculate success rate."""
        total = self.success_count + self.failure_count
        return self.success_count / total if total > 0 else 0.0
    
    @property
    def is_reliable(self) -> bool:
        """Check if selector is reliable."""
        return self.success_rate >= 0.8 and self.success_count >= 3


@dataclass
class SelectorValidationResult:
    """Result of selector validation."""
    selector: str
    found: bool
    element_count: int
    execution_time: float
    error_message: Optional[str] = None
    element_text: Optional[str] = None
    element_attributes: Dict[str, str] = field(default_factory=dict)


class SelectorStrategy(ABC):
    """Abstract base class for selector generation strategies."""
    
    def __init__(self, name: str):
        self.name = name
        self._logger = logging.getLogger(f"bob_core.selector_healing.{name}")
    
    @abstractmethod
    def generate_candidates(self, 
                          element: WebElement,
                          driver: Any,
                          context: Dict[str, Any]) -> List[SelectorCandidate]:
        """Generate selector candidates for an element."""
        pass
    
    @abstractmethod
    def validate_selector(self, 
                         selector: str,
                         driver: Any,
                         expected_text: Optional[str] = None) -> SelectorValidationResult:
        """Validate if a selector works."""
        pass


class CSSStrategy(SelectorStrategy):
    """Strategy for generating CSS selectors."""
    
    def __init__(self):
        super().__init__("css")
    
    def generate_candidates(self, 
                          element: WebElement,
                          driver: Any,
                          context: Dict[str, Any]) -> List[SelectorCandidate]:
        """Generate CSS selector candidates."""
        candidates = []
        
        try:
            # Get element attributes
            tag_name = element.tag_name
            element_id = element.get_attribute("id")
            class_name = element.get_attribute("class")
            text_content = element.text.strip()
            
            # Strategy 1: ID selector (highest confidence)
            if element_id:
                candidates.append(SelectorCandidate(
                    selector=f"#{element_id}",
                    selector_type="css",
                    confidence=0.95,
                    last_success_time=time.time(),
                    context={"strategy": "id"}
                ))
            
            # Strategy 2: Class selector
            if class_name:
                classes = class_name.split()
                for cls in classes:
                    if cls and not cls.startswith("_"):  # Skip dynamic classes
                        candidates.append(SelectorCandidate(
                            selector=f".{cls}",
                            selector_type="css",
                            confidence=0.7,
                            last_success_time=time.time(),
                            context={"strategy": "class"}
                        ))
                
                # Combined class selector
                if len(classes) > 1:
                    stable_classes = [c for c in classes if not c.startswith("_")]
                    if stable_classes:
                        combined_selector = "." + ".".join(stable_classes)
                        candidates.append(SelectorCandidate(
                            selector=combined_selector,
                            selector_type="css",
                            confidence=0.8,
                            last_success_time=time.time(),
                            context={"strategy": "combined_class"}
                        ))
            
            # Strategy 3: Tag with attributes
            attributes = ["data-testid", "data-id", "name", "type", "role"]
            for attr in attributes:
                attr_value = element.get_attribute(attr)
                if attr_value:
                    candidates.append(SelectorCandidate(
                        selector=f"{tag_name}[{attr}='{attr_value}']",
                        selector_type="css",
                        confidence=0.85,
                        last_success_time=time.time(),
                        context={"strategy": "attribute", "attribute": attr}
                    ))
            
            # Strategy 4: Structural selectors
            parent = element.find_element(By.XPATH, "..")
            if parent:
                parent_tag = parent.tag_name
                siblings = parent.find_elements(By.TAG_NAME, tag_name)
                if len(siblings) > 1:
                    index = siblings.index(element) + 1
                    candidates.append(SelectorCandidate(
                        selector=f"{parent_tag} > {tag_name}:nth-child({index})",
                        selector_type="css",
                        confidence=0.6,
                        last_success_time=time.time(),
                        context={"strategy": "nth_child"}
                    ))
            
            # Strategy 5: Text-based selectors (for elements with unique text)
            if text_content and len(text_content) > 3:
                # Partial text match
                candidates.append(SelectorCandidate(
                    selector=f"{tag_name}:contains('{text_content[:20]}')",
                    selector_type="css",
                    confidence=0.75,
                    last_success_time=time.time(),
                    context={"strategy": "text_contains"}
                ))
            
        except Exception as e:
            self._logger.error(f"Error generating CSS candidates: {e}")
        
        return candidates
    
    def validate_selector(self, 
                         selector: str,
                         driver: Any,
                         expected_text: Optional[str] = None) -> SelectorValidationResult:
        """Validate CSS selector."""
        start_time = time.time()
        
        try:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            execution_time = time.time() - start_time
            
            if not elements:
                return SelectorValidationResult(
                    selector=selector,
                    found=False,
                    element_count=0,
                    execution_time=execution_time
                )
            
            element = elements[0]
            element_text = element.text.strip()
            
            # Check if text matches expected
            text_matches = True
            if expected_text:
                text_matches = expected_text.lower() in element_text.lower()
            
            # Get element attributes
            attributes = {}
            for attr in ["id", "class", "data-testid", "name", "type"]:
                value = element.get_attribute(attr)
                if value:
                    attributes[attr] = value
            
            return SelectorValidationResult(
                selector=selector,
                found=text_matches,
                element_count=len(elements),
                execution_time=execution_time,
                element_text=element_text,
                element_attributes=attributes
            )
            
        except Exception as e:
            execution_time = time.time() - start_time
            return SelectorValidationResult(
                selector=selector,
                found=False,
                element_count=0,
                execution_time=execution_time,
                error_message=str(e)
            )


class XPathStrategy(SelectorStrategy):
    """Strategy for generating XPath selectors."""
    
    def __init__(self):
        super().__init__("xpath")
    
    def generate_candidates(self, 
                          element: WebElement,
                          driver: Any,
                          context: Dict[str, Any]) -> List[SelectorCandidate]:
        """Generate XPath selector candidates."""
        candidates = []
        
        try:
            tag_name = element.tag_name
            text_content = element.text.strip()
            
            # Strategy 1: Text-based XPath
            if text_content:
                # Exact text match
                candidates.append(SelectorCandidate(
                    selector=f"//{tag_name}[text()='{text_content}']",
                    selector_type="xpath",
                    confidence=0.9,
                    last_success_time=time.time(),
                    context={"strategy": "exact_text"}
                ))
                
                # Contains text
                candidates.append(SelectorCandidate(
                    selector=f"//{tag_name}[contains(text(), '{text_content[:15]}')]",
                    selector_type="xpath",
                    confidence=0.8,
                    last_success_time=time.time(),
                    context={"strategy": "contains_text"}
                ))
            
            # Strategy 2: Attribute-based XPath
            attributes = ["id", "class", "data-testid", "name", "type", "role"]
            for attr in attributes:
                attr_value = element.get_attribute(attr)
                if attr_value:
                    candidates.append(SelectorCandidate(
                        selector=f"//{tag_name}[@{attr}='{attr_value}']",
                        selector_type="xpath",
                        confidence=0.85,
                        last_success_time=time.time(),
                        context={"strategy": "attribute", "attribute": attr}
                    ))
            
            # Strategy 3: Position-based XPath
            try:
                parent = element.find_element(By.XPATH, "..")
                siblings = parent.find_elements(By.TAG_NAME, tag_name)
                if len(siblings) > 1:
                    position = siblings.index(element) + 1
                    candidates.append(SelectorCandidate(
                        selector=f"({parent.tag_name}//{tag_name})[{position}]",
                        selector_type="xpath",
                        confidence=0.6,
                        last_success_time=time.time(),
                        context={"strategy": "position"}
                    ))
            except:
                pass
            
        except Exception as e:
            self._logger.error(f"Error generating XPath candidates: {e}")
        
        return candidates
    
    def validate_selector(self, 
                         selector: str,
                         driver: Any,
                         expected_text: Optional[str] = None) -> SelectorValidationResult:
        """Validate XPath selector."""
        start_time = time.time()
        
        try:
            elements = driver.find_elements(By.XPATH, selector)
            execution_time = time.time() - start_time
            
            if not elements:
                return SelectorValidationResult(
                    selector=selector,
                    found=False,
                    element_count=0,
                    execution_time=execution_time
                )
            
            element = elements[0]
            element_text = element.text.strip()
            
            # Check if text matches expected
            text_matches = True
            if expected_text:
                text_matches = expected_text.lower() in element_text.lower()
            
            return SelectorValidationResult(
                selector=selector,
                found=text_matches,
                element_count=len(elements),
                execution_time=execution_time,
                element_text=element_text
            )
            
        except Exception as e:
            execution_time = time.time() - start_time
            return SelectorValidationResult(
                selector=selector,
                found=False,
                element_count=0,
                execution_time=execution_time,
                error_message=str(e)
            )


class TextStrategy(SelectorStrategy):
    """Strategy for text-based element finding."""
    
    def __init__(self):
        super().__init__("text")
    
    def generate_candidates(self, 
                          element: WebElement,
                          driver: Any,
                          context: Dict[str, Any]) -> List[SelectorCandidate]:
        """Generate text-based selector candidates."""
        candidates = []
        
        try:
            text_content = element.text.strip()
            if not text_content:
                return candidates
            
            # Exact text match
            candidates.append(SelectorCandidate(
                selector=text_content,
                selector_type="text",
                confidence=0.95,
                last_success_time=time.time(),
                context={"strategy": "exact_text"}
            ))
            
            # Partial text match
            if len(text_content) > 10:
                candidates.append(SelectorCandidate(
                    selector=text_content[:20],
                    selector_type="text",
                    confidence=0.8,
                    last_success_time=time.time(),
                    context={"strategy": "partial_text"}
                ))
            
            # Normalized text (remove extra spaces, case insensitive)
            normalized_text = re.sub(r'\s+', ' ', text_content.lower())
            if normalized_text != text_content.lower():
                candidates.append(SelectorCandidate(
                    selector=normalized_text,
                    selector_type="text",
                    confidence=0.85,
                    last_success_time=time.time(),
                    context={"strategy": "normalized_text"}
                ))
            
        except Exception as e:
            self._logger.error(f"Error generating text candidates: {e}")
        
        return candidates
    
    def validate_selector(self, 
                         selector: str,
                         driver: Any,
                         expected_text: Optional[str] = None) -> SelectorValidationResult:
        """Validate text-based selector."""
        start_time = time.time()
        
        try:
            # Try to find element by link text
            try:
                elements = driver.find_elements(By.LINK_TEXT, selector)
            except:
                elements = []
            
            # Try partial link text if exact didn't work
            if not elements:
                try:
                    elements = driver.find_elements(By.PARTIAL_LINK_TEXT, selector)
                except:
                    elements = []
            
            # Try XPath with text content
            if not elements:
                try:
                    xpath = f"//*[contains(text(), '{selector}')]"
                    elements = driver.find_elements(By.XPATH, xpath)
                except:
                    elements = []
            
            execution_time = time.time() - start_time
            
            if not elements:
                return SelectorValidationResult(
                    selector=selector,
                    found=False,
                    element_count=0,
                    execution_time=execution_time
                )
            
            element = elements[0]
            element_text = element.text.strip()
            
            return SelectorValidationResult(
                selector=selector,
                found=True,
                element_count=len(elements),
                execution_time=execution_time,
                element_text=element_text
            )
            
        except Exception as e:
            execution_time = time.time() - start_time
            return SelectorValidationResult(
                selector=selector,
                found=False,
                element_count=0,
                execution_time=execution_time,
                error_message=str(e)
            )


class AttributeStrategy(SelectorStrategy):
    """Strategy for attribute-based element finding."""
    
    def __init__(self):
        super().__init__("attribute")
    
    def generate_candidates(self, 
                          element: WebElement,
                          driver: Any,
                          context: Dict[str, Any]) -> List[SelectorCandidate]:
        """Generate attribute-based selector candidates."""
        candidates = []
        
        try:
            # Priority attributes for different element types
            priority_attrs = {
                "input": ["name", "id", "type", "placeholder"],
                "button": ["id", "name", "type", "data-testid"],
                "a": ["href", "id", "class", "data-testid"],
                "img": ["src", "alt", "id", "class"],
                "div": ["id", "class", "data-testid", "role"],
                "span": ["id", "class", "data-testid"],
            }
            
            tag_name = element.tag_name
            attrs_to_check = priority_attrs.get(tag_name, ["id", "class", "data-testid", "name"])
            
            for attr in attrs_to_check:
                attr_value = element.get_attribute(attr)
                if attr_value:
                    confidence = 0.9 if attr in ["id", "data-testid"] else 0.7
                    candidates.append(SelectorCandidate(
                        selector=f"{attr}={attr_value}",
                        selector_type="attribute",
                        confidence=confidence,
                        last_success_time=time.time(),
                        context={"strategy": "attribute", "attribute": attr}
                    ))
            
        except Exception as e:
            self._logger.error(f"Error generating attribute candidates: {e}")
        
        return candidates
    
    def validate_selector(self, 
                         selector: str,
                         driver: Any,
                         expected_text: Optional[str] = None) -> SelectorValidationResult:
        """Validate attribute-based selector."""
        start_time = time.time()
        
        try:
            # Parse attribute selector
            if "=" not in selector:
                raise ValueError("Invalid attribute selector format")
            
            attr_name, attr_value = selector.split("=", 1)
            xpath = f"//*[@{attr_name}='{attr_value}']"
            
            elements = driver.find_elements(By.XPATH, xpath)
            execution_time = time.time() - start_time
            
            if not elements:
                return SelectorValidationResult(
                    selector=selector,
                    found=False,
                    element_count=0,
                    execution_time=execution_time
                )
            
            element = elements[0]
            element_text = element.text.strip()
            
            # Check if text matches expected
            text_matches = True
            if expected_text:
                text_matches = expected_text.lower() in element_text.lower()
            
            return SelectorValidationResult(
                selector=selector,
                found=text_matches,
                element_count=len(elements),
                execution_time=execution_time,
                element_text=element_text
            )
            
        except Exception as e:
            execution_time = time.time() - start_time
            return SelectorValidationResult(
                selector=selector,
                found=False,
                element_count=0,
                execution_time=execution_time,
                error_message=str(e)
            )


class SelectorHealer:
    """
    Main class for healing broken selectors and maintaining selector health.
    
    Features:
    - Automatic selector generation and validation
    - Adaptive selector learning
    - Fallback selector strategies
    - Performance monitoring
    
    Example:
        ```python
        healer = SelectorHealer()
        
        # Register strategies
        healer.add_strategy(CSSStrategy())
        healer.add_strategy(XPathStrategy())
        
        # Heal a broken selector
        new_selector = healer.heal_selector(
            driver, 
            broken_selector="button.old-class",
            expected_text="Submit",
            element_type="button"
        )
        ```
    """
    
    def __init__(self):
        self.strategies: List[SelectorStrategy] = []
        self.selector_cache: Dict[str, List[SelectorCandidate]] = {}
        self._lock = threading.RLock()
        self._logger = logging.getLogger("bob_core.selector_healer")
        
        # Add default strategies
        self.add_strategy(CSSStrategy())
        self.add_strategy(XPathStrategy())
        self.add_strategy(TextStrategy())
        self.add_strategy(AttributeStrategy())
    
    def add_strategy(self, strategy: SelectorStrategy) -> None:
        """Add a selector generation strategy."""
        self.strategies.append(strategy)
        self._logger.info(f"Added selector strategy: {strategy.name}")
    
    def heal_selector(self, 
                     driver: Any,
                     broken_selector: str,
                     expected_text: Optional[str] = None,
                     element_type: Optional[str] = None,
                     context: Dict[str, Any] = None) -> Optional[str]:
        """
        Heal a broken selector by finding alternative selectors.
        
        Parameters
        ----------
        driver : WebDriver
            Selenium WebDriver instance
        broken_selector : str
            The selector that is no longer working
        expected_text : str, optional
            Expected text content of the element
        element_type : str, optional
            Type of element (button, input, etc.)
        context : dict, optional
            Additional context for healing
            
        Returns
        -------
        str or None
            New working selector, or None if healing failed
        """
        with self._lock:
            context = context or {}
            cache_key = f"{broken_selector}:{expected_text}:{element_type}"
            
            # Check cache first
            if cache_key in self.selector_cache:
                cached_candidates = self.selector_cache[cache_key]
                for candidate in sorted(cached_candidates, key=lambda x: x.confidence, reverse=True):
                    if self._validate_candidate(driver, candidate, expected_text):
                        self._logger.info(f"Using cached selector: {candidate.selector}")
                        return candidate.selector
            
            # Try to find element using various strategies
            self._logger.info(f"Healing broken selector: {broken_selector}")
            
            # Strategy 1: Try variations of the broken selector
            healed_selector = self._try_selector_variations(driver, broken_selector, expected_text)
            if healed_selector:
                return healed_selector
            
            # Strategy 2: Search by expected text
            if expected_text:
                healed_selector = self._find_by_text(driver, expected_text, element_type)
                if healed_selector:
                    return healed_selector
            
            # Strategy 3: Generate new candidates using all strategies
            all_candidates = []
            
            # Try to find any element that might match
            potential_elements = self._find_potential_elements(driver, expected_text, element_type)
            
            for element in potential_elements:
                for strategy in self.strategies:
                    try:
                        candidates = strategy.generate_candidates(element, driver, context)
                        all_candidates.extend(candidates)
                    except Exception as e:
                        self._logger.warning(f"Strategy {strategy.name} failed: {e}")
            
            # Validate and rank candidates
            valid_candidates = []
            for candidate in all_candidates:
                if self._validate_candidate(driver, candidate, expected_text):
                    valid_candidates.append(candidate)
            
            if valid_candidates:
                # Sort by confidence and success rate
                valid_candidates.sort(key=lambda x: (x.confidence, x.success_rate), reverse=True)
                best_candidate = valid_candidates[0]
                
                # Cache the results
                self.selector_cache[cache_key] = valid_candidates[:5]  # Keep top 5
                
                self._logger.info(f"Found healed selector: {best_candidate.selector}")
                return best_candidate.selector
            
            self._logger.error(f"Failed to heal selector: {broken_selector}")
            return None
    
    def _try_selector_variations(self, 
                                driver: Any,
                                selector: str,
                                expected_text: Optional[str]) -> Optional[str]:
        """Try variations of the broken selector."""
        variations = []
        
        # CSS selector variations
        if selector.startswith("."):
            # Try without specific classes
            class_parts = selector[1:].split(".")
            for i in range(len(class_parts)):
                variation = "." + ".".join(class_parts[:i+1])
                variations.append(variation)
        
        elif selector.startswith("#"):
            # Try as class selector
            variations.append(f".{selector[1:]}")
        
        elif "[" in selector:
            # Try without attribute constraints
            base_selector = selector.split("[")[0]
            variations.append(base_selector)
        
        # XPath variations
        if selector.startswith("//"):
            # Try more generic XPath
            if "[" in selector:
                base_xpath = selector.split("[")[0]
                variations.append(base_xpath)
        
        # Test variations
        for variation in variations:
            try:
                if self._test_selector(driver, variation, expected_text):
                    self._logger.info(f"Selector variation worked: {variation}")
                    return variation
            except:
                continue
        
        return None
    
    def _find_by_text(self, 
                     driver: Any,
                     text: str,
                     element_type: Optional[str]) -> Optional[str]:
        """Find element by text content."""
        text_strategies = [
            f"//*[text()='{text}']",
            f"//*[contains(text(), '{text}')]",
            f"//button[contains(text(), '{text}')]" if element_type == "button" else None,
            f"//a[contains(text(), '{text}')]" if element_type == "link" else None,
            f"//input[@value='{text}']" if element_type == "input" else None,
        ]
        
        for strategy in text_strategies:
            if strategy is None:
                continue
            
            try:
                if self._test_selector(driver, strategy, text, selector_type="xpath"):
                    return strategy
            except:
                continue
        
        return None
    
    def _find_potential_elements(self, 
                               driver: Any,
                               expected_text: Optional[str],
                               element_type: Optional[str]) -> List[WebElement]:
        """Find potential elements that might be the target."""
        elements = []
        
        try:
            # Search by element type
            if element_type:
                type_elements = driver.find_elements(By.TAG_NAME, element_type)
                elements.extend(type_elements)
            
            # Search by text content
            if expected_text:
                text_elements = driver.find_elements(By.XPATH, f"//*[contains(text(), '{expected_text[:10]}')]")
                elements.extend(text_elements)
            
            # Search common interactive elements
            interactive_tags = ["button", "a", "input", "select", "textarea"]
            for tag in interactive_tags:
                tag_elements = driver.find_elements(By.TAG_NAME, tag)
                elements.extend(tag_elements)
            
            # Remove duplicates
            unique_elements = []
            seen_elements = set()
            
            for element in elements:
                try:
                    element_id = element.id
                    if element_id not in seen_elements:
                        unique_elements.append(element)
                        seen_elements.add(element_id)
                except:
                    continue
            
            return unique_elements[:20]  # Limit to prevent performance issues
            
        except Exception as e:
            self._logger.error(f"Error finding potential elements: {e}")
            return []
    
    def _validate_candidate(self, 
                          driver: Any,
                          candidate: SelectorCandidate,
                          expected_text: Optional[str]) -> bool:
        """Validate a selector candidate."""
        try:
            # Find strategy for this candidate type
            strategy = None
            for s in self.strategies:
                if s.name == candidate.selector_type:
                    strategy = s
                    break
            
            if not strategy:
                return False
            
            result = strategy.validate_selector(candidate.selector, driver, expected_text)
            
            if result.found:
                candidate.success_count += 1
                candidate.last_success_time = time.time()
                return True
            else:
                candidate.failure_count += 1
                return False
                
        except Exception as e:
            candidate.failure_count += 1
            return False
    
    def _test_selector(self, 
                      driver: Any,
                      selector: str,
                      expected_text: Optional[str] = None,
                      selector_type: str = "css") -> bool:
        """Test if a selector works."""
        try:
            if selector_type == "css":
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
            elif selector_type == "xpath":
                elements = driver.find_elements(By.XPATH, selector)
            else:
                return False
            
            if not elements:
                return False
            
            # Check text content if provided
            if expected_text:
                element_text = elements[0].text.strip()
                return expected_text.lower() in element_text.lower()
            
            return True
            
        except Exception:
            return False
    
    def get_selector_statistics(self) -> Dict[str, Any]:
        """Get statistics about selector healing."""
        with self._lock:
            total_cached = len(self.selector_cache)
            total_candidates = sum(len(candidates) for candidates in self.selector_cache.values())
            
            strategy_stats = {}
            for strategy in self.strategies:
                strategy_stats[strategy.name] = {
                    "name": strategy.name,
                    "active": True
                }
            
            return {
                "cached_selectors": total_cached,
                "total_candidates": total_candidates,
                "strategies": strategy_stats,
                "cache_keys": list(self.selector_cache.keys())
            }
    
    def clear_cache(self) -> None:
        """Clear the selector cache."""
        with self._lock:
            self.selector_cache.clear()
            self._logger.info("Cleared selector cache")


class AdaptiveSelectorManager:
    """
    Manager for adaptive selector healing across multiple pages/sites.
    
    Learns from successful healings and applies patterns to new situations.
    """
    
    def __init__(self):
        self.healers: Dict[str, SelectorHealer] = {}
        self.global_patterns: Dict[str, List[str]] = {}
        self._lock = threading.RLock()
        self._logger = logging.getLogger("bob_core.adaptive_selector_manager")
    
    def get_healer(self, domain: str) -> SelectorHealer:
        """Get or create a selector healer for a specific domain."""
        with self._lock:
            if domain not in self.healers:
                self.healers[domain] = SelectorHealer()
                self._logger.info(f"Created selector healer for domain: {domain}")
            
            return self.healers[domain]
    
    def heal_selector_adaptive(self, 
                             driver: Any,
                             domain: str,
                             broken_selector: str,
                             expected_text: Optional[str] = None,
                             element_type: Optional[str] = None) -> Optional[str]:
        """Heal selector with adaptive learning."""
        healer = self.get_healer(domain)
        
        # Try domain-specific healing first
        result = healer.heal_selector(driver, broken_selector, expected_text, element_type)
        
        if result:
            # Learn from successful healing
            self._learn_pattern(domain, broken_selector, result, element_type)
            return result
        
        # Try patterns from other domains
        return self._try_global_patterns(driver, broken_selector, expected_text, element_type)
    
    def _learn_pattern(self, 
                      domain: str,
                      old_selector: str,
                      new_selector: str,
                      element_type: Optional[str]) -> None:
        """Learn a healing pattern."""
        with self._lock:
            pattern_key = f"{element_type}:{old_selector[:20]}"
            
            if pattern_key not in self.global_patterns:
                self.global_patterns[pattern_key] = []
            
            if new_selector not in self.global_patterns[pattern_key]:
                self.global_patterns[pattern_key].append(new_selector)
                self._logger.info(f"Learned new pattern: {pattern_key} -> {new_selector}")
    
    def _try_global_patterns(self, 
                           driver: Any,
                           broken_selector: str,
                           expected_text: Optional[str],
                           element_type: Optional[str]) -> Optional[str]:
        """Try patterns learned from other domains."""
        pattern_key = f"{element_type}:{broken_selector[:20]}"
        
        if pattern_key in self.global_patterns:
            for pattern_selector in self.global_patterns[pattern_key]:
                try:
                    if self._test_selector_simple(driver, pattern_selector, expected_text):
                        self._logger.info(f"Global pattern worked: {pattern_selector}")
                        return pattern_selector
                except:
                    continue
        
        return None
    
    def _test_selector_simple(self, 
                            driver: Any,
                            selector: str,
                            expected_text: Optional[str]) -> bool:
        """Simple selector test."""
        try:
            # Try as CSS first
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
            except:
                # Try as XPath
                elements = driver.find_elements(By.XPATH, selector)
            
            if not elements:
                return False
            
            if expected_text:
                element_text = elements[0].text.strip()
                return expected_text.lower() in element_text.lower()
            
            return True
            
        except:
            return False
    
    def get_global_statistics(self) -> Dict[str, Any]:
        """Get global statistics about adaptive healing."""
        with self._lock:
            return {
                "domains": len(self.healers),
                "global_patterns": len(self.global_patterns),
                "pattern_details": {
                    key: len(patterns) for key, patterns in self.global_patterns.items()
                }
            }


# Global adaptive selector manager
_global_selector_manager: Optional[AdaptiveSelectorManager] = None
_global_selector_healer: Optional[SelectorHealer] = None


def get_global_selector_manager() -> AdaptiveSelectorManager:
    """Get or create global adaptive selector manager."""
    global _global_selector_manager
    if _global_selector_manager is None:
        _global_selector_manager = AdaptiveSelectorManager()
    return _global_selector_manager


def get_global_selector_healer() -> SelectorHealer:
    """Get or create global selector healer."""
    global _global_selector_healer
    if _global_selector_healer is None:
        _global_selector_healer = SelectorHealer()
    return _global_selector_healer 