"""Input Validator module for sanitizing and analyzing user input."""
import re
from typing import Dict, List, Optional
from langdetect import detect, LangDetectException
from config.logging_config import log


class InputValidator:
    """Validates and analyzes user input text."""

    def __init__(self):
        """Initialize input validator."""
        self.min_length = 5
        self.max_length = 2000

    def validate(self, text: str) -> Dict[str, any]:
        """
        Validate input text and return analysis results.

        Args:
            text: User input text

        Returns:
            Dictionary containing validation results and analysis
        """
        # Sanitize text
        sanitized = self._sanitize(text)

        # Validate length
        if not self._validate_length(sanitized):
            log.warning(f"Input length invalid: {len(sanitized)} characters")
            return {
                "valid": False,
                "error": f"Input must be between {self.min_length} and {self.max_length} characters",
                "sanitized": sanitized,
            }

        # Detect language
        language = self._detect_language(sanitized)

        # Extract entities
        entities = self._extract_entities(sanitized)

        log.info(f"Input validated successfully. Language: {language}, Entities: {len(entities)}")

        return {
            "valid": True,
            "sanitized": sanitized,
            "language": language,
            "entities": entities,
            "length": len(sanitized),
        }

    def _sanitize(self, text: str) -> str:
        """
        Sanitize input text by removing harmful content and extra whitespace.

        Args:
            text: Raw input text

        Returns:
            Sanitized text
        """
        # Remove extra whitespace
        sanitized = " ".join(text.split())

        # Remove special HTML/XML characters (basic)
        sanitized = re.sub(r"<[^>]+>", "", sanitized)

        # Remove potentially dangerous content
        dangerous_patterns = [
            r"javascript:",
            r"on\w+\s*=",
            r"data:text/html",
        ]
        for pattern in dangerous_patterns:
            sanitized = re.sub(pattern, "", sanitized, flags=re.IGNORECASE)

        return sanitized.strip()

    def _validate_length(self, text: str) -> bool:
        """
        Validate text length requirements.

        Args:
            text: Sanitized text

        Returns:
            True if length is valid, False otherwise
        """
        return self.min_length <= len(text) <= self.max_length

    def _detect_language(self, text: str) -> str:
        """
        Detect the language of the input text.

        Args:
            text: Sanitized text

        Returns:
            Language code (e.g., 'id', 'en', 'es')
        """
        try:
            lang = detect(text)
            log.debug(f"Detected language: {lang}")
            return lang
        except LangDetectException:
            log.warning("Language detection failed, defaulting to English")
            return "en"

    def _extract_entities(self, text: str) -> Dict[str, List[str]]:
        """
        Extract key entities from the input text.

        Args:
            text: Sanitized text

        Returns:
            Dictionary of entity categories and their values
        """
        entities = {
            "products": self._extract_products(text),
            "topics": self._extract_topics(text),
            "emotions": self._extract_emotions(text),
            "target_audience": self._extract_target_audience(text),
        }

        return entities

    def _extract_products(self, text: str) -> List[str]:
        """Extract product mentions from text."""
        # Common product categories and keywords
        product_keywords = [
            r"skincare",
            r"makeup",
            r"clothing|pakaian|baju",
            r"food|makanan",
            r"drink|minuman",
            r"gadget",
            r"phone|handphone|hp",
            r"shoes|sepatu",
            r"bag|tas",
            r"book|buku",
        ]

        products = []
        text_lower = text.lower()
        for keyword in product_keywords:
            matches = re.findall(keyword, text_lower)
            products.extend(matches)

        return list(set(products))

    def _extract_topics(self, text: str) -> List[str]:
        """Extract topic keywords from text."""
        # Common topic categories
        topic_keywords = [
            r"review",
            r"tutorial",
            r"tips",
            r"vlog",
            r"challenge",
            r"reaction",
            r"unboxing",
            r"testimoni|testimoni|review",
            r"promosi|promosi|promo",
        ]

        topics = []
        text_lower = text.lower()
        for keyword in topic_keywords:
            matches = re.findall(keyword, text_lower)
            topics.extend(matches)

        return list(set(topics))

    def _extract_emotions(self, text: str) -> List[str]:
        """Extract emotional keywords from text."""
        emotion_keywords = [
            r"excited|exciting|seru",
            r"happy|joyful|bahagia|senang",
            r"sad|sadness|sedih",
            r"angry|furious|marah",
            r"funny|humorous|lucu",
            r"inspiring|motivational|inspiratif|motivasi",
            r"calm|peaceful|tenang",
            r"energetic|energetic",
        ]

        emotions = []
        text_lower = text.lower()
        for keyword in emotion_keywords:
            matches = re.findall(keyword, text_lower)
            emotions.extend(matches)

        return list(set(emotions))

    def _extract_target_audience(self, text: str) -> List[str]:
        """Extract target audience mentions from text."""
        audience_keywords = [
            r"teen|teens|remaja",
            r"kids|children|anak-anak",
            r"adult|adults|dewasa",
            r"student|students|mahasiswa|pelajar",
            r"mom|mother|moms|ibu",
            r"professionals|profesional",
            r"gamer|gamers",
        ]

        audience = []
        text_lower = text.lower()
        for keyword in audience_keywords:
            matches = re.findall(keyword, text_lower)
            audience.extend(matches)

        return list(set(audience))
