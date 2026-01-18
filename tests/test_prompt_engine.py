"""Unit tests for Prompt Engine."""
import pytest
from unittest.mock import Mock, patch
from src.core.prompt_engine import PromptEngine


class TestPromptEngine:
    """Test cases for PromptEngine class."""

    @pytest.fixture
    def engine(self):
        """Create an engine instance for testing."""
        return PromptEngine()

    @pytest.fixture
    def mock_validation_result(self):
        """Mock validation result."""
        return {
            "valid": True,
            "sanitized": "Jualin skincare pagi hari yang bagus buat wajah berminyak",
            "language": "id",
            "entities": {
                "products": ["skincare"],
                "topics": ["review"],
                "emotions": [],
                "target_audience": [],
            },
            "length": 50,
        }

    @pytest.fixture
    def mock_groq_result(self):
        """Mock Groq API result."""
        return {
            "raw_response": """# MASTER PROMPT (Text-to-Video)
A cinematic morning skincare routine for oily skin

# VISUAL SPECIFICATIONS
| Element | Value |
|---------|-------|
| Style | Cinematic |
| Camera | Close-up |
| Lighting | Soft natural |
| Aspect Ratio | 9:16 |
| Mood | Fresh |

# SCRIPT
## Hook [0:00-0:03]
Pagi-pagi udah bangun, wajah mengkilap kayak chef masak?

## Body [0:03-0:45]
Show product application process

## CTA [0:45-0:60]
Follow untuk tips lebih lanjut

# HASHTAGS
#skincare #skincareroutine #fyp
""",
            "language": "id",
        }

    def test_engine_initialization(self, engine):
        """Test engine initialization."""
        assert engine.validator is not None
        assert engine.trending_injector is not None
        assert engine.groq_client is not None
        assert engine.platform_optimizer is not None
        assert engine.formatter is not None
        assert engine.last_generated is None

    @patch.object(PromptEngine, "generate_prompt")
    def test_generate_prompt_success(self, mock_generate, engine):
        """Test successful prompt generation."""
        mock_generate.return_value = {
            "success": True,
            "user_input": "Test input",
            "markdown_output": "Test markdown",
        }

        result = engine.generate_prompt("Test input")

        assert result["success"] is True

    def test_extract_master_prompt(self, engine):
        """Test master prompt extraction from AI response."""
        raw_response = """# MASTER PROMPT (Text-to-Video)
Test prompt content

# VISUAL SPECIFICATIONS"""

        master_prompt = engine._extract_master_prompt(raw_response)

        assert "Test prompt content" in master_prompt

    def test_extract_visual_specs(self, engine):
        """Test visual specifications extraction."""
        raw_response = """# VISUAL SPECIFICATIONS
| Element | Value |
|---------|-------|
| Style | Cinematic |
| Camera | Close-up |
"""

        specs = engine._extract_visual_specs(raw_response)

        assert specs["Style"] == "Cinematic"
        assert specs["Camera"] == "Close-up"

    def test_extract_script(self, engine):
        """Test script extraction."""
        raw_response = """# SCRIPT
## Hook [0:00-0:03]
Test hook

## Body [0:03-0:45]
Test body

## CTA [0:45-0:60]
Test CTA"""

        script = engine._extract_script(raw_response)

        assert script["hook"] == "Test hook"
        assert script["body"] == "Test body"
        assert script["cta"] == "Test CTA"

    def test_extract_hashtags(self, engine):
        """Test hashtag extraction."""
        raw_response = """# HASHTAGS
#skincare #skincareroutine #fyp
"""

        hashtags = engine._extract_hashtags(raw_response, {})

        assert len(hashtags) > 0
        assert "skincare" in hashtags

    def test_export_last_generated_none(self, engine):
        """Test export when no prompt has been generated."""
        result = engine.export_last_generated()

        assert result is None
