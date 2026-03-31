"""
Preset configurations for quick cartoon effects.
"""

CLASSIC_PRESETS = {
    "Bold Cartoon": {
        "edge_threshold": 120,
        "bilateral_d": 9,
        "num_colors": 6,
        "description": "Strong edges, bold colors"
    },
    "Soft Cartoon": {
        "edge_threshold": 80,
        "bilateral_d": 11,
        "num_colors": 10,
        "description": "Gentle edges, more colors"
    },
    "Minimal": {
        "edge_threshold": 100,
        "bilateral_d": 9,
        "num_colors": 4,
        "description": "Very simple, few colors"
    },
    "Detailed": {
        "edge_threshold": 90,
        "bilateral_d": 7,
        "num_colors": 12,
        "description": "More detail preserved"
    }
}

AI_STYLE_PRESETS = {
    "Light": 0.5,
    "Medium": 0.8,
    "Strong": 1.0
}
