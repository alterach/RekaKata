"""Unit tests for Input Validator."""
import pytest
from src.core.input_validator import InputValidator


class TestInputValidator:
    """Test cases for InputValidator class."""

    @pytest.fixture
    def validator(self):
        """Create a validator instance for testing."""
        return InputValidator()

    def test_validate_success(self, validator):
        """Test successful validation with valid input."""
        result = validator.validate("Jualin skincare pagi hari yang bagus buat wajah berminyak")

        assert result["valid"] is True
        assert "sanitized" in result
        assert "language" in result
        assert "entities" in result
        assert result["length"] > 0

    def test_validate_short_input(self, validator):
        """Test validation with input that's too short."""
        result = validator.validate("tes")

        assert result["valid"] is False
        assert "error" in result
        assert "characters" in result["error"].lower()

    def test_validate_long_input(self, validator):
        """Test validation with input that's too long."""
        long_text = "a" * 3000
        result = validator.validate(long_text)

        assert result["valid"] is False
        assert "error" in result
        assert "characters" in result["error"].lower()

    def test_sanitize_html(self, validator):
        """Test HTML sanitization."""
        result = validator.validate("Test <script>alert('xss')</script> content")

        assert "<script>" not in result["sanitized"]
        assert "alert" not in result["sanitized"]

    def test_sanitize_extra_whitespace(self, validator):
        """Test whitespace sanitization."""
        result = validator.validate("Test    with    extra    spaces")

        assert result["sanitized"] == "Test with extra spaces"

    def test_detect_language_indonesian(self, validator):
        """Test Indonesian language detection."""
        result = validator.validate("Jualin skincare pagi hari yang bagus")

        assert result["language"] == "id"

    def test_detect_language_english(self, validator):
        """Test English language detection."""
        result = validator.validate("Sell morning skincare routine for oily skin")

        assert result["language"] == "en"

    def test_extract_entities_products(self, validator):
        """Test product entity extraction."""
        result = validator.validate("Review skincare and makeup products")

        entities = result["entities"]
        assert "products" in entities
        assert len(entities["products"]) > 0

    def test_extract_entities_topics(self, validator):
        """Test topic entity extraction."""
        result = validator.validate("Tutorial how to apply makeup")

        entities = result["entities"]
        assert "topics" in entities
        assert "tutorial" in entities["topics"]

    def test_extract_entities_empty(self, validator):
        """Test entity extraction with no matching entities."""
        result = validator.validate("Random text with no specific entities")

        entities = result["entities"]
        # Should return empty lists, not None
        assert isinstance(entities["products"], list)
        assert isinstance(entities["topics"], list)
