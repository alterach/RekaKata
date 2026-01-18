"""Trending Elements injector for 2025 content trends."""
import json
import random
from typing import Dict, List, Optional
from pathlib import Path
from config.logging_config import log


class TrendingInjector:
    """Injects trending elements into generated prompts."""

    def __init__(self, data_path: str = "data/trending_elements_2025.json"):
        """
        Initialize trending injector with cached data.

        Args:
            data_path: Path to trending elements JSON file
        """
        self.data_path = Path(data_path)
        self.data = self._load_data()
        log.info("TrendingInjector initialized")

    def _load_data(self) -> Dict:
        """
        Load trending data from JSON file.

        Returns:
            Dictionary containing trending elements
        """
        try:
            with open(self.data_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            log.info(f"Loaded trending data from {self.data_path}")
            return data
        except FileNotFoundError:
            log.error(f"Trending data file not found: {self.data_path}")
            return self._get_fallback_data()
        except json.JSONDecodeError as e:
            log.error(f"Error decoding trending data: {e}")
            return self._get_fallback_data()

    def _get_fallback_data(self) -> Dict:
        """
        Get fallback trending data if file load fails.

        Returns:
            Dictionary with basic trending data
        """
        return {
            "formats": [
                {"name": "POV", "platforms": ["tiktok", "instagram", "youtube"], "keywords": ["pov"]},
                {"name": "Tutorial", "platforms": ["tiktok", "instagram", "youtube"], "keywords": ["tutorial"]},
            ],
            "visual_styles": [
                {"name": "Clean", "keywords": ["clean"], "style": "minimalist", "camera": "close-up"},
                {"name": "Cinematic", "keywords": ["cinematic"], "style": "dramatic", "camera": "wide shots"},
            ],
            "hooks": [
                "Ini rahasianya!",
                "Coba deh ini!",
            ],
            "hashtags": {
                "general": ["#viral", "#fyp", "#trending"]
            },
            "cta": [
                "Follow untuk lebih lanjut ✨",
                "Save biar nggak lupa! 🔖",
            ],
        }

    def inject(self, entities: Dict[str, List[str]], language: str = "id") -> Dict[str, any]:
        """
        Inject trending elements based on detected entities.

        Args:
            entities: Dictionary of detected entities (products, topics, etc.)
            language: Output language ('id' or 'en')

        Returns:
            Dictionary containing trending elements to inject
        """
        trending_elements = {
            "format": self._get_matching_format(entities),
            "visual_style": self._get_visual_style(entities),
            "hooks": self._get_hooks(entities),
            "ctas": self._get_ctas(),
            "hashtags": self._get_hashtags(entities),
            "sound_suggestions": self._get_sound_suggestions(),
        }

        log.info(f"Injected trending elements: {trending_elements}")
        return trending_elements

    def _get_matching_format(self, entities: Dict[str, List[str]]) -> Optional[Dict]:
        """
        Get a matching format based on entities.

        Args:
            entities: Detected entities

        Returns:
            Format dictionary or None
        """
        formats = self.data.get("formats", [])

        # Try to match based on topics
        topics = entities.get("topics", [])
        for format_item in formats:
            for topic in topics:
                if any(keyword in format_item["keywords"] for keyword in format_item["keywords"]):
                    return format_item

        # Return random format if no match
        return random.choice(formats) if formats else None

    def _get_visual_style(self, entities: Dict[str, List[str]]) -> Optional[Dict]:
        """
        Get visual style based on entities.

        Args:
            entities: Detected entities

        Returns:
            Visual style dictionary or None
        """
        styles = self.data.get("visual_styles", [])

        # Match based on products and topics
        all_keywords = entities.get("products", []) + entities.get("topics", [])

        for style in styles:
            style_keywords = style.get("keywords", [])
            if any(keyword in " ".join(all_keywords) for keyword in style_keywords):
                return style

        # Return random style if no match
        return random.choice(styles) if styles else None

    def _get_hooks(self, entities: Dict[str, List[str]]) -> List[str]:
        """
        Get trending hooks.

        Args:
            entities: Detected entities

        Returns:
            List of hook strings
        """
        all_hooks = self.data.get("hooks", [])
        return random.sample(all_hooks, min(3, len(all_hooks)))

    def _get_ctas(self) -> List[str]:
        """
        Get trending call-to-actions.

        Returns:
            List of CTA strings
        """
        all_ctas = self.data.get("cta", [])
        return random.sample(all_ctas, min(2, len(all_ctas)))

    def _get_hashtags(self, entities: Dict[str, List[str]]) -> List[str]:
        """
        Get relevant hashtags based on entities.

        Args:
            entities: Detected entities

        Returns:
            List of hashtag strings
        """
        hashtags_data = self.data.get("hashtags", {})
        hashtags = []

        # Add category-specific hashtags
        for category, category_hashtags in hashtags_data.items():
            if category != "general":
                all_entities = " ".join(entities.get(category.replace("_", "").replace("s", ""), []))
                if category in all_entities.lower():
                    hashtags.extend(category_hashtags)

        # Add general hashtags
        hashtags.extend(hashtags_data.get("general", []))

        # Remove duplicates and limit to 15
        return list(dict.fromkeys(hashtags))[:15]

    def _get_sound_suggestions(self) -> List[Dict]:
        """
        Get sound suggestions for different platforms.

        Returns:
            List of sound suggestion dictionaries
        """
        sounds = self.data.get("sounds", [])
        return sounds[:3] if sounds else []

    def update_data(self, new_data: Dict) -> bool:
        """
        Update trending data with new information.

        Args:
            new_data: New trending data to merge

        Returns:
            True if successful, False otherwise
        """
        try:
            self.data.update(new_data)
            with open(self.data_path, "w", encoding="utf-8") as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
            log.info("Trending data updated successfully")
            return True
        except Exception as e:
            log.error(f"Error updating trending data: {e}")
            return False
