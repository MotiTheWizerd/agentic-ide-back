"""
Seed script for agentic components and related tables.
Run from project root:  python -m scripts.seed_components
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sqlalchemy import select, delete
from app.core.db.base import async_session
from app.models.agentic_component import AgenticComponent, ComponentCategory, ProviderType
from app.models.component_field import ComponentField, FieldType
from app.models.component_port import ComponentPort, PortDirection, PortType
from app.models.component_api_config import ComponentApiConfig, ExecutorType
from app.models.component_output_schema import ComponentOutputSchema, OutputType

# ---------------------------------------------------------------------------
# 1. Components
# ---------------------------------------------------------------------------
COMPONENTS = [
    {
        "type": "initialPrompt",
        "name": "Initial Prompt",
        "description": "Starting point for text pipelines with optional persona injection",
        "category": ComponentCategory.input,
        "icon": "MessageSquareText",
        "color": "cyan",
        "uses_llm": True,
        "default_provider_id": "mistral",
        "default_model": "ministral-14b-2512",
        "provider_type": ProviderType.text,
        "is_active": True,
    },
    {
        "type": "promptEnhancer",
        "name": "Prompt Enhancer",
        "description": "Enhances upstream text with optional notes",
        "category": ComponentCategory.processing,
        "icon": "Sparkles",
        "color": "violet",
        "uses_llm": True,
        "default_provider_id": "mistral",
        "default_model": "ministral-14b-2512",
        "provider_type": ProviderType.text,
        "is_active": True,
    },
    {
        "type": "translator",
        "name": "Translator",
        "description": "Translates text to a selected target language",
        "category": ComponentCategory.processing,
        "icon": "Languages",
        "color": "orange",
        "uses_llm": True,
        "default_provider_id": "mistral",
        "default_model": "ministral-14b-2512",
        "provider_type": ProviderType.text,
        "is_active": True,
    },
    {
        "type": "storyTeller",
        "name": "Story Teller",
        "description": "Generates stories from ideas and tags",
        "category": ComponentCategory.processing,
        "icon": "BookOpen",
        "color": "amber",
        "uses_llm": True,
        "default_provider_id": "mistral",
        "default_model": "labs-mistral-small-creative",
        "provider_type": ProviderType.text,
        "is_active": True,
    },
    {
        "type": "grammarFix",
        "name": "Grammar Fix",
        "description": "Fixes grammar and adjusts writing style",
        "category": ComponentCategory.processing,
        "icon": "SpellCheck",
        "color": "green",
        "uses_llm": True,
        "default_provider_id": "mistral",
        "default_model": "ministral-14b-2512",
        "provider_type": ProviderType.text,
        "is_active": True,
    },
    {
        "type": "compressor",
        "name": "Compressor",
        "description": "Compresses long text while preserving meaning",
        "category": ComponentCategory.processing,
        "icon": "Shrink",
        "color": "teal",
        "uses_llm": True,
        "default_provider_id": "mistral",
        "default_model": "ministral-14b-2512",
        "provider_type": ProviderType.text,
        "is_active": True,
    },
    {
        "type": "imageDescriber",
        "name": "Image Describer",
        "description": "Describes an uploaded image using vision AI",
        "category": ComponentCategory.input,
        "icon": "ScanEye",
        "color": "pink",
        "uses_llm": True,
        "default_provider_id": "claude",
        "default_model": None,
        "provider_type": ProviderType.vision,
        "is_active": True,
    },
    {
        "type": "imageGenerator",
        "name": "Image Generator",
        "description": "Generates images from text prompts",
        "category": ComponentCategory.output,
        "icon": "ImageIcon",
        "color": "fuchsia",
        "uses_llm": True,
        "default_provider_id": "blackforestlabs",
        "default_model": "flux-kontext-pro",
        "provider_type": ProviderType.image,
        "is_active": True,
    },
    {
        "type": "personasReplacer",
        "name": "Personas Replacer",
        "description": "Replaces personas in a target image using vision AI",
        "category": ComponentCategory.processing,
        "icon": "UserRoundPen",
        "color": "rose",
        "uses_llm": True,
        "default_provider_id": "claude",
        "default_model": None,
        "provider_type": ProviderType.vision,
        "is_active": True,
    },
    {
        "type": "textOutput",
        "name": "Text Output",
        "description": "Displays the final text output",
        "category": ComponentCategory.output,
        "icon": "FileText",
        "color": "emerald",
        "uses_llm": False,
        "default_provider_id": None,
        "default_model": None,
        "provider_type": ProviderType.none,
        "is_active": True,
    },
    {
        "type": "consistentCharacter",
        "name": "Consistent Character",
        "description": "Provides character persona data for downstream nodes",
        "category": ComponentCategory.data_source,
        "icon": "UserRound",
        "color": "amber",
        "uses_llm": False,
        "default_provider_id": None,
        "default_model": None,
        "provider_type": ProviderType.none,
        "is_active": True,
    },
    {
        "type": "sceneBuilder",
        "name": "Scene Builder",
        "description": "Builds scene descriptions from visual parameters",
        "category": ComponentCategory.data_source,
        "icon": "CloudSun",
        "color": "sky",
        "uses_llm": False,
        "default_provider_id": None,
        "default_model": None,
        "provider_type": ProviderType.none,
        "is_active": True,
    },
    {
        "type": "group",
        "name": "Group",
        "description": "Visual grouping container for organizing nodes",
        "category": ComponentCategory.utility,
        "icon": "Group",
        "color": "blue",
        "uses_llm": False,
        "default_provider_id": None,
        "default_model": None,
        "provider_type": ProviderType.none,
        "is_active": True,
    },
]

# ---------------------------------------------------------------------------
# 2. Fields  (keyed by component type)
# ---------------------------------------------------------------------------
LANGUAGES = [
    {"value": "en", "label": "English"}, {"value": "es", "label": "Spanish"},
    {"value": "fr", "label": "French"}, {"value": "de", "label": "German"},
    {"value": "it", "label": "Italian"}, {"value": "pt", "label": "Portuguese"},
    {"value": "ru", "label": "Russian"}, {"value": "ja", "label": "Japanese"},
    {"value": "ko", "label": "Korean"}, {"value": "zh", "label": "Chinese"},
    {"value": "ar", "label": "Arabic"}, {"value": "hi", "label": "Hindi"},
    {"value": "tr", "label": "Turkish"}, {"value": "pl", "label": "Polish"},
    {"value": "nl", "label": "Dutch"}, {"value": "sv", "label": "Swedish"},
    {"value": "da", "label": "Danish"}, {"value": "fi", "label": "Finnish"},
    {"value": "no", "label": "Norwegian"}, {"value": "cs", "label": "Czech"},
    {"value": "el", "label": "Greek"}, {"value": "he", "label": "Hebrew"},
    {"value": "th", "label": "Thai"}, {"value": "vi", "label": "Vietnamese"},
    {"value": "id", "label": "Indonesian"}, {"value": "uk", "label": "Ukrainian"},
    {"value": "ro", "label": "Romanian"}, {"value": "hu", "label": "Hungarian"},
]

WRITING_STYLES = [
    {"value": "", "label": "Standard"}, {"value": "formal", "label": "Formal"},
    {"value": "casual", "label": "Casual"}, {"value": "creative", "label": "Creative"},
]

IMAGE_STYLES = [
    {"value": "realistic", "label": "Realistic"}, {"value": "artistic", "label": "Artistic"},
    {"value": "anime", "label": "Anime"}, {"value": "cinematic", "label": "Cinematic"},
    {"value": "watercolor", "label": "Watercolor"}, {"value": "oil painting", "label": "Oil Painting"},
    {"value": "3d render", "label": "3D Render"}, {"value": "pixel art", "label": "Pixel Art"},
]

LIGHTING = [
    {"value": "natural daylight", "label": "Natural Daylight"}, {"value": "golden hour", "label": "Golden Hour"},
    {"value": "night", "label": "Night"}, {"value": "neon", "label": "Neon"},
    {"value": "studio", "label": "Studio"}, {"value": "dramatic", "label": "Dramatic"},
    {"value": "soft diffused", "label": "Soft Diffused"}, {"value": "backlit", "label": "Backlit"},
]

TIME_OF_DAY = [
    {"value": "dawn", "label": "Dawn"}, {"value": "morning", "label": "Morning"},
    {"value": "noon", "label": "Noon"}, {"value": "afternoon", "label": "Afternoon"},
    {"value": "sunset", "label": "Sunset"}, {"value": "dusk", "label": "Dusk"},
    {"value": "night", "label": "Night"}, {"value": "midnight", "label": "Midnight"},
]

WEATHER = [
    {"value": "clear", "label": "Clear"}, {"value": "cloudy", "label": "Cloudy"},
    {"value": "rainy", "label": "Rainy"}, {"value": "foggy", "label": "Foggy"},
    {"value": "snowy", "label": "Snowy"}, {"value": "stormy", "label": "Stormy"},
    {"value": "windy", "label": "Windy"}, {"value": "hazy", "label": "Hazy"},
]

CAMERA_ANGLES = [
    {"value": "eye level", "label": "Eye Level"}, {"value": "low angle", "label": "Low Angle"},
    {"value": "high angle", "label": "High Angle"}, {"value": "bird's eye", "label": "Bird's Eye"},
    {"value": "worm's eye", "label": "Worm's Eye"}, {"value": "dutch angle", "label": "Dutch Angle"},
    {"value": "over the shoulder", "label": "Over the Shoulder"}, {"value": "close-up", "label": "Close-Up"},
]

CAMERA_LENSES = [
    {"value": "wide angle", "label": "Wide Angle"}, {"value": "standard", "label": "Standard"},
    {"value": "telephoto", "label": "Telephoto"}, {"value": "macro", "label": "Macro"},
    {"value": "fisheye", "label": "Fisheye"}, {"value": "tilt-shift", "label": "Tilt-Shift"},
]

MOODS = [
    {"value": "peaceful", "label": "Peaceful"}, {"value": "tense", "label": "Tense"},
    {"value": "mysterious", "label": "Mysterious"}, {"value": "joyful", "label": "Joyful"},
    {"value": "melancholic", "label": "Melancholic"}, {"value": "epic", "label": "Epic"},
    {"value": "romantic", "label": "Romantic"}, {"value": "eerie", "label": "Eerie"},
]

GROUP_COLORS = [
    {"value": "gray", "label": "Gray"}, {"value": "blue", "label": "Blue"},
    {"value": "purple", "label": "Purple"}, {"value": "green", "label": "Green"},
    {"value": "amber", "label": "Amber"}, {"value": "red", "label": "Red"},
    {"value": "cyan", "label": "Cyan"}, {"value": "pink", "label": "Pink"},
]

FIELDS: dict[str, list[dict]] = {
    "initialPrompt": [
        {"field_key": "text", "label": "Prompt", "field_type": FieldType.textarea,
         "placeholder": "Enter your prompt...", "default_value": "", "required": False,
         "options": None, "sort_order": 0},
    ],
    "promptEnhancer": [
        {"field_key": "notes", "label": "Enhancement Notes", "field_type": FieldType.textarea,
         "placeholder": "Add notes to guide enhancement...", "default_value": "", "required": False,
         "options": None, "sort_order": 0},
    ],
    "translator": [
        {"field_key": "language", "label": "Target Language", "field_type": FieldType.select,
         "placeholder": "Select language...", "default_value": "", "required": False,
         "options": LANGUAGES, "sort_order": 0},
    ],
    "storyTeller": [
        {"field_key": "idea", "label": "Story Idea", "field_type": FieldType.textarea,
         "placeholder": "Describe your story concept...", "default_value": "", "required": False,
         "options": None, "sort_order": 0},
        {"field_key": "tags", "label": "Tags", "field_type": FieldType.tags,
         "placeholder": "cinematic, moody, fantasy...", "default_value": "", "required": False,
         "options": None, "sort_order": 1},
    ],
    "grammarFix": [
        {"field_key": "style", "label": "Writing Style", "field_type": FieldType.select,
         "placeholder": None, "default_value": "", "required": False,
         "options": WRITING_STYLES, "sort_order": 0},
    ],
    # compressor: no fields
    "imageDescriber": [
        {"field_key": "image", "label": "Image", "field_type": FieldType.image,
         "placeholder": None, "default_value": None, "required": True,
         "options": None, "sort_order": 0},
    ],
    "imageGenerator": [
        {"field_key": "prompt", "label": "Prompt", "field_type": FieldType.textarea,
         "placeholder": "Direct prompt (optional if connected)...", "default_value": "", "required": False,
         "options": None, "sort_order": 0},
        {"field_key": "width", "label": "Width", "field_type": FieldType.number,
         "placeholder": None, "default_value": None, "required": False,
         "options": None, "sort_order": 1},
        {"field_key": "height", "label": "Height", "field_type": FieldType.number,
         "placeholder": None, "default_value": None, "required": False,
         "options": None, "sort_order": 2},
    ],
    "personasReplacer": [
        {"field_key": "image", "label": "Target Image", "field_type": FieldType.image,
         "placeholder": None, "default_value": None, "required": False,
         "options": None, "sort_order": 0},
    ],
    # textOutput: no fields
    "consistentCharacter": [
        {"field_key": "characterName", "label": "Character Name", "field_type": FieldType.text,
         "placeholder": None, "default_value": "", "required": True,
         "options": None, "sort_order": 0},
        {"field_key": "characterDescription", "label": "Description", "field_type": FieldType.textarea,
         "placeholder": None, "default_value": "", "required": True,
         "options": None, "sort_order": 1},
        {"field_key": "characterImagePath", "label": "Avatar", "field_type": FieldType.image,
         "placeholder": None, "default_value": None, "required": False,
         "options": None, "sort_order": 2},
    ],
    "sceneBuilder": [
        {"field_key": "imageStyle", "label": "Image Style", "field_type": FieldType.select,
         "placeholder": None, "default_value": "", "required": False,
         "options": IMAGE_STYLES, "sort_order": 0},
        {"field_key": "lighting", "label": "Lighting", "field_type": FieldType.select,
         "placeholder": None, "default_value": "", "required": False,
         "options": LIGHTING, "sort_order": 1},
        {"field_key": "timeOfDay", "label": "Time of Day", "field_type": FieldType.select,
         "placeholder": None, "default_value": "", "required": False,
         "options": TIME_OF_DAY, "sort_order": 2},
        {"field_key": "weather", "label": "Weather", "field_type": FieldType.select,
         "placeholder": None, "default_value": "", "required": False,
         "options": WEATHER, "sort_order": 3},
        {"field_key": "cameraAngle", "label": "Camera Angle", "field_type": FieldType.select,
         "placeholder": None, "default_value": "", "required": False,
         "options": CAMERA_ANGLES, "sort_order": 4},
        {"field_key": "cameraLens", "label": "Camera Lens", "field_type": FieldType.select,
         "placeholder": None, "default_value": "", "required": False,
         "options": CAMERA_LENSES, "sort_order": 5},
        {"field_key": "mood", "label": "Mood", "field_type": FieldType.select,
         "placeholder": None, "default_value": "", "required": False,
         "options": MOODS, "sort_order": 6},
    ],
    "group": [
        {"field_key": "label", "label": "Label", "field_type": FieldType.text,
         "placeholder": "Group name", "default_value": "", "required": False,
         "options": None, "sort_order": 0},
        {"field_key": "color", "label": "Color", "field_type": FieldType.select,
         "placeholder": None, "default_value": "gray", "required": False,
         "options": GROUP_COLORS, "sort_order": 1},
    ],
}

# ---------------------------------------------------------------------------
# 3. Ports  (keyed by component type)
# ---------------------------------------------------------------------------
PORTS: dict[str, list[dict]] = {
    "initialPrompt": [
        {"direction": PortDirection.out, "port_type": PortType.text, "handle_id": "text-out",
         "max_connections": None, "is_dynamic": False, "max_dynamic": 0, "sort_order": 0},
        {"direction": PortDirection.in_, "port_type": PortType.adapter, "handle_id": "adapter-in",
         "max_connections": None, "is_dynamic": True, "max_dynamic": 5, "sort_order": 1},
    ],
    "promptEnhancer": [
        {"direction": PortDirection.in_, "port_type": PortType.text, "handle_id": "text-in",
         "max_connections": None, "is_dynamic": False, "max_dynamic": 0, "sort_order": 0},
        {"direction": PortDirection.out, "port_type": PortType.text, "handle_id": "text-out",
         "max_connections": None, "is_dynamic": False, "max_dynamic": 0, "sort_order": 1},
        {"direction": PortDirection.in_, "port_type": PortType.adapter, "handle_id": "adapter-in",
         "max_connections": None, "is_dynamic": True, "max_dynamic": 5, "sort_order": 2},
    ],
    "translator": [
        {"direction": PortDirection.in_, "port_type": PortType.text, "handle_id": "text-in",
         "max_connections": None, "is_dynamic": False, "max_dynamic": 0, "sort_order": 0},
        {"direction": PortDirection.out, "port_type": PortType.text, "handle_id": "text-out",
         "max_connections": None, "is_dynamic": False, "max_dynamic": 0, "sort_order": 1},
    ],
    "storyTeller": [
        {"direction": PortDirection.in_, "port_type": PortType.text, "handle_id": "text-in",
         "max_connections": None, "is_dynamic": False, "max_dynamic": 0, "sort_order": 0},
        {"direction": PortDirection.out, "port_type": PortType.text, "handle_id": "text-out",
         "max_connections": None, "is_dynamic": False, "max_dynamic": 0, "sort_order": 1},
        {"direction": PortDirection.in_, "port_type": PortType.adapter, "handle_id": "adapter-in",
         "max_connections": None, "is_dynamic": True, "max_dynamic": 5, "sort_order": 2},
    ],
    "grammarFix": [
        {"direction": PortDirection.in_, "port_type": PortType.text, "handle_id": "text-in",
         "max_connections": None, "is_dynamic": False, "max_dynamic": 0, "sort_order": 0},
        {"direction": PortDirection.out, "port_type": PortType.text, "handle_id": "text-out",
         "max_connections": None, "is_dynamic": False, "max_dynamic": 0, "sort_order": 1},
    ],
    "compressor": [
        {"direction": PortDirection.in_, "port_type": PortType.text, "handle_id": "text-in",
         "max_connections": None, "is_dynamic": False, "max_dynamic": 0, "sort_order": 0},
        {"direction": PortDirection.out, "port_type": PortType.text, "handle_id": "text-out",
         "max_connections": None, "is_dynamic": False, "max_dynamic": 0, "sort_order": 1},
    ],
    "imageDescriber": [
        {"direction": PortDirection.out, "port_type": PortType.text, "handle_id": "text-out",
         "max_connections": None, "is_dynamic": False, "max_dynamic": 0, "sort_order": 0},
    ],
    "imageGenerator": [
        {"direction": PortDirection.in_, "port_type": PortType.text, "handle_id": "text-in",
         "max_connections": None, "is_dynamic": False, "max_dynamic": 0, "sort_order": 0},
        {"direction": PortDirection.out, "port_type": PortType.text, "handle_id": "text-out",
         "max_connections": None, "is_dynamic": False, "max_dynamic": 0, "sort_order": 1},
    ],
    "personasReplacer": [
        {"direction": PortDirection.in_, "port_type": PortType.text, "handle_id": "text-in",
         "max_connections": None, "is_dynamic": False, "max_dynamic": 0, "sort_order": 0},
        {"direction": PortDirection.out, "port_type": PortType.text, "handle_id": "text-out",
         "max_connections": None, "is_dynamic": False, "max_dynamic": 0, "sort_order": 1},
        {"direction": PortDirection.in_, "port_type": PortType.adapter, "handle_id": "adapter-in",
         "max_connections": None, "is_dynamic": True, "max_dynamic": 5, "sort_order": 2},
    ],
    "textOutput": [
        {"direction": PortDirection.in_, "port_type": PortType.text, "handle_id": "text-in",
         "max_connections": None, "is_dynamic": False, "max_dynamic": 0, "sort_order": 0},
    ],
    "consistentCharacter": [
        {"direction": PortDirection.out, "port_type": PortType.adapter, "handle_id": "adapter-out",
         "max_connections": None, "is_dynamic": False, "max_dynamic": 0, "sort_order": 0},
    ],
    "sceneBuilder": [
        {"direction": PortDirection.out, "port_type": PortType.text, "handle_id": "text-out",
         "max_connections": None, "is_dynamic": False, "max_dynamic": 0, "sort_order": 0},
    ],
    # group: no ports
}

# ---------------------------------------------------------------------------
# 4. API Configs  (keyed by component type)
# ---------------------------------------------------------------------------
API_CONFIGS: dict[str, dict] = {
    "initialPrompt": {
        "executor_type": ExecutorType.composite,
        "api_route": "/api/inject-persona",
        "request_mapping": {"personas": "$adapters", "promptText": "$field.text"},
        "response_mapping": {"text": "$.injected"},
        "pass_through_condition": None,
        "compression_threshold": None,
    },
    "promptEnhancer": {
        "executor_type": ExecutorType.api_call,
        "api_route": "/api/enhance",
        "request_mapping": {"text": "$input", "notes": "$field.notes"},
        "response_mapping": {"text": "$.enhanced"},
        "pass_through_condition": None,
        "compression_threshold": None,
    },
    "translator": {
        "executor_type": ExecutorType.api_call,
        "api_route": "/api/translate",
        "request_mapping": {"text": "$input", "language": "$field.language"},
        "response_mapping": {"text": "$.translation"},
        "pass_through_condition": {"field": "language", "when_empty": True},
        "compression_threshold": None,
    },
    "storyTeller": {
        "executor_type": ExecutorType.api_call,
        "api_route": "/api/storyteller",
        "request_mapping": {"text": "$input", "tags": "$field.tags"},
        "response_mapping": {"text": "$.story"},
        "pass_through_condition": None,
        "compression_threshold": None,
    },
    "grammarFix": {
        "executor_type": ExecutorType.api_call,
        "api_route": "/api/grammar-fix",
        "request_mapping": {"text": "$input", "style": "$field.style"},
        "response_mapping": {"text": "$.fixed"},
        "pass_through_condition": None,
        "compression_threshold": None,
    },
    "compressor": {
        "executor_type": ExecutorType.api_call,
        "api_route": "/api/compress",
        "request_mapping": {"text": "$input"},
        "response_mapping": {"text": "$.compressed"},
        "pass_through_condition": None,
        "compression_threshold": 2500,
    },
    "imageDescriber": {
        "executor_type": ExecutorType.api_call,
        "api_route": "/api/describe",
        "request_mapping": {"images": "$field.image"},
        "response_mapping": {"text": "$.description"},
        "pass_through_condition": None,
        "compression_threshold": None,
    },
    "imageGenerator": {
        "executor_type": ExecutorType.api_call,
        "api_route": "/api/generate-image",
        "request_mapping": {"prompt": "$input"},
        "response_mapping": {"image": "$.imageData"},
        "pass_through_condition": None,
        "compression_threshold": None,
    },
    "personasReplacer": {
        "executor_type": ExecutorType.api_call,
        "api_route": "/api/replace",
        "request_mapping": {"personas": "$adapters", "targetImage": "$field.image"},
        "response_mapping": {"text": "$.description"},
        "pass_through_condition": None,
        "compression_threshold": None,
    },
    "textOutput": {
        "executor_type": ExecutorType.pass_through,
        "api_route": None,
        "request_mapping": None,
        "response_mapping": None,
        "pass_through_condition": None,
        "compression_threshold": None,
    },
    "consistentCharacter": {
        "executor_type": ExecutorType.data_source,
        "api_route": None,
        "request_mapping": None,
        "response_mapping": None,
        "pass_through_condition": None,
        "compression_threshold": None,
    },
    "sceneBuilder": {
        "executor_type": ExecutorType.data_source,
        "api_route": None,
        "request_mapping": None,
        "response_mapping": None,
        "pass_through_condition": None,
        "compression_threshold": None,
    },
    "group": {
        "executor_type": ExecutorType.pass_through,
        "api_route": None,
        "request_mapping": None,
        "response_mapping": None,
        "pass_through_condition": None,
        "compression_threshold": None,
    },
}

# ---------------------------------------------------------------------------
# 5. Output Schemas  (keyed by component type)
# ---------------------------------------------------------------------------
OUTPUT_SCHEMAS: dict[str, list[dict]] = {
    "initialPrompt": [
        {"output_key": "text", "output_type": OutputType.text, "source": "$.injected or $field.text"},
        {"output_key": "personaName", "output_type": OutputType.persona_name, "source": "$adapters[0].name"},
        {"output_key": "personaDescription", "output_type": OutputType.persona_description, "source": "$adapters[0].description"},
    ],
    "promptEnhancer": [
        {"output_key": "text", "output_type": OutputType.text, "source": "$.enhanced"},
    ],
    "translator": [
        {"output_key": "text", "output_type": OutputType.text, "source": "$.translation"},
    ],
    "storyTeller": [
        {"output_key": "text", "output_type": OutputType.text, "source": "$.story"},
    ],
    "grammarFix": [
        {"output_key": "text", "output_type": OutputType.text, "source": "$.fixed"},
    ],
    "compressor": [
        {"output_key": "text", "output_type": OutputType.text, "source": "$.compressed"},
    ],
    "imageDescriber": [
        {"output_key": "text", "output_type": OutputType.text, "source": "$.description"},
        {"output_key": "image", "output_type": OutputType.image, "source": "$field.image"},
    ],
    "imageGenerator": [
        {"output_key": "image", "output_type": OutputType.image, "source": "$.imageData"},
        {"output_key": "text", "output_type": OutputType.text, "source": "$input"},
    ],
    "personasReplacer": [
        {"output_key": "text", "output_type": OutputType.text, "source": "$.description"},
    ],
    "textOutput": [
        {"output_key": "text", "output_type": OutputType.text, "source": "$input"},
    ],
    "consistentCharacter": [
        {"output_key": "personaName", "output_type": OutputType.persona_name, "source": "$field.characterName"},
        {"output_key": "personaDescription", "output_type": OutputType.persona_description, "source": "$field.characterDescription"},
        {"output_key": "text", "output_type": OutputType.text, "source": "$field.characterDescription"},
    ],
    "sceneBuilder": [
        {"output_key": "text", "output_type": OutputType.text, "source": "$composed"},
    ],
    # group: no outputs
}


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------
async def seed():
    async with async_session() as session:
        # Clear existing data (child tables first)
        await session.execute(delete(ComponentOutputSchema))
        await session.execute(delete(ComponentApiConfig))
        await session.execute(delete(ComponentPort))
        await session.execute(delete(ComponentField))
        await session.execute(delete(AgenticComponent))
        await session.flush()

        # Insert components
        comp_objects = []
        for data in COMPONENTS:
            comp = AgenticComponent(**data)
            session.add(comp)
            comp_objects.append(comp)
        await session.flush()

        # Build type → id lookup
        type_to_id: dict[str, str] = {}
        for comp in comp_objects:
            type_to_id[comp.type] = comp.id

        # Insert fields
        for comp_type, fields in FIELDS.items():
            cid = type_to_id[comp_type]
            for f in fields:
                session.add(ComponentField(component_id=cid, **f))

        # Insert ports
        for comp_type, ports in PORTS.items():
            cid = type_to_id[comp_type]
            for p in ports:
                session.add(ComponentPort(component_id=cid, **p))

        # Insert API configs
        for comp_type, cfg in API_CONFIGS.items():
            cid = type_to_id[comp_type]
            session.add(ComponentApiConfig(component_id=cid, **cfg))

        # Insert output schemas
        for comp_type, schemas in OUTPUT_SCHEMAS.items():
            cid = type_to_id[comp_type]
            for s in schemas:
                session.add(ComponentOutputSchema(component_id=cid, **s))

        await session.commit()

    print("Seed complete!")
    print(f"  Components:      {len(COMPONENTS)}")
    print(f"  Fields:          {sum(len(v) for v in FIELDS.values())}")
    print(f"  Ports:           {sum(len(v) for v in PORTS.values())}")
    print(f"  API Configs:     {len(API_CONFIGS)}")
    print(f"  Output Schemas:  {sum(len(v) for v in OUTPUT_SCHEMAS.values())}")


if __name__ == "__main__":
    asyncio.run(seed())
