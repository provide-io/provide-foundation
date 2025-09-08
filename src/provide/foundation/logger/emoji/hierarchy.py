"""
Emoji Hierarchy Management for Logger Names
===========================================
Provides hierarchical emoji assignment based on logger module names.
"""

from typing import Any

# Global emoji hierarchy registry
_EMOJI_HIERARCHIES: dict[str, dict[str, str]] = {}
_SINGLE_EMOJI_MAPPINGS: dict[str, str] = {}


def register_emoji_hierarchy(base_module: str, hierarchy: dict[str, str]) -> None:
    """
    Register a hierarchical emoji mapping for a module tree.
    
    Args:
        base_module: The base module name (e.g., "wrknv", "myapp")
        hierarchy: Dict mapping module patterns to emojis
        
    Example:
        register_emoji_hierarchy("wrknv", {
            "wrknv": "🧰",
            "wrknv.cli": "⌨️", 
            "wrknv.wenv": "🌍",
            "wrknv.wenv.managers": "📦"
        })
    """
    _EMOJI_HIERARCHIES[base_module] = hierarchy.copy()


def register_single_emoji(module_pattern: str, emoji: str) -> None:
    """
    Register a single module pattern to emoji mapping.
    
    Args:
        module_pattern: Module name or pattern
        emoji: Emoji to use for this module
    """
    _SINGLE_EMOJI_MAPPINGS[module_pattern] = emoji


def get_emoji_for_logger(logger_name: str, override_emoji: str | None = None) -> str:
    """
    Get emoji for a logger name using hierarchy or single mappings.
    
    Args:
        logger_name: The logger name (e.g., "wrknv.wenv.version_resolver")
        override_emoji: Direct emoji override
        
    Returns:
        Emoji string for the logger
    """
    if override_emoji:
        return override_emoji
    
    # Check single mappings first (exact matches)
    if logger_name in _SINGLE_EMOJI_MAPPINGS:
        return _SINGLE_EMOJI_MAPPINGS[logger_name]
    
    # Check hierarchies (longest match first)
    best_match = ""
    best_emoji = ""
    
    for base_module, hierarchy in _EMOJI_HIERARCHIES.items():
        if logger_name.startswith(base_module):
            # Find the longest matching pattern in this hierarchy
            for pattern, emoji in hierarchy.items():
                if logger_name.startswith(pattern) and len(pattern) > len(best_match):
                    best_match = pattern
                    best_emoji = emoji
    
    # Fallback to default if no match found
    return best_emoji if best_emoji else "🔹"


def clear_emoji_registrations() -> None:
    """Clear all emoji registrations (useful for testing)."""
    _EMOJI_HIERARCHIES.clear()
    _SINGLE_EMOJI_MAPPINGS.clear()


def get_registered_hierarchies() -> dict[str, dict[str, str]]:
    """Get all registered emoji hierarchies (for debugging/inspection)."""
    return _EMOJI_HIERARCHIES.copy()


def get_registered_single_mappings() -> dict[str, str]:
    """Get all registered single emoji mappings (for debugging/inspection)."""
    return _SINGLE_EMOJI_MAPPINGS.copy()