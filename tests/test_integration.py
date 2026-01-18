"""Integration tests for end-to-end flow."""
import pytest
from unittest.mock import Mock, patch
from src.core.prompt_engine import PromptEngine
from src.core.output_formatter import OutputFormatter
from src.core.platform_optimizer import PlatformOptimizer
from src.core.input_validator import InputValidator


class TestIntegration:
    """Integration tests for the entire flow."""

    def test_input_validator_to_optimizer_flow(self):
        """Test flow from input validation to platform optimization."""
        validator = InputValidator()
        optimizer = PlatformOptimizer()

        # Validate input
        validation_result = validator.validate(
            "Jualin skincare pagi hari yang bagus buat wajah berminyak"
        )

        assert validation_result["valid"] is True

        # Optimize for platforms
        platform_specifics = optimizer.optimize_for_all_platforms(
            {"entities": validation_result["entities"], "language": validation_result["language"]}
        )

        assert "tiktok" in platform_specifics
        assert "instagram" in platform_specifics
        assert "youtube" in platform_specifics

    @patch("src.core.groq_client.GroqClient.generate")
    def test_formatter_to_output_flow(self, mock_generate):
        """Test flow from formatter to output."""
        # Mock Groq response
        mock_generate.return_value = """A cinematic morning skincare routine"""

        formatter = OutputFormatter()

        # Create test data
        prompt_data = {
            "master_prompt": "Test prompt",
            "visual_specifications": {
                "Style": "Cinematic",
                "Camera": "Close-up",
            },
            "script": {
                "hook": "Test hook",
                "body": "Test body",
                "cta": "Test CTA",
            },
            "hashtags": ["skincare", "fyp"],
        }

        # Format as markdown
        markdown = formatter.format_markdown(prompt_data)

        assert "MASTER PROMPT" in markdown
        assert "VISUAL SPECIFICATIONS" in markdown
        assert "SCRIPT" in markdown

    def test_platform_optimizer_caption_generation(self):
        """Test platform optimizer generates captions correctly."""
        optimizer = PlatformOptimizer()

        # Test Indonesian captions
        captions_id = optimizer.get_caption_suggestions(
            "tiktok", {}, language="id"
        )

        assert len(captions_id) > 0
        assert all(isinstance(c, str) for c in captions_id)

        # Test English captions
        captions_en = optimizer.get_caption_suggestions(
            "instagram", {}, language="en"
        )

        assert len(captions_en) > 0
        assert all(isinstance(c, str) for c in captions_en)

    def test_platform_optimizer_schedule_generation(self):
        """Test platform optimizer generates posting schedules."""
        optimizer = PlatformOptimizer()

        # Test each platform
        for platform in ["tiktok", "instagram", "youtube"]:
            schedule = optimizer.get_posting_schedule(platform)

            assert len(schedule) > 0
            assert all(isinstance(s, str) for s in schedule)

    @patch("src.core.groq_client.GroqClient.generate")
    def test_end_to_end_mock_flow(self, mock_generate):
        """Test complete end-to-end flow with mocked Groq."""
        # Mock Groq response
        mock_generate.return_value = """# MASTER PROMPT (Text-to-Video)
Test prompt for skincare routine

# VISUAL SPECIFICATIONS
| Element | Value |
|---------|-------|
| Style | Cinematic |
| Camera | Close-up |

# SCRIPT
## Hook [0:00-0:03]
Test hook

## Body [0:03-0:45]
Test body

## CTA [0:45-0:60]
Test CTA

# HASHTAGS
#skincare #fyp
"""

        # Create engine
        engine = PromptEngine()

        # Generate prompt
        result = engine.generate_prompt(
            "Jualin skincare pagi hari yang bagus buat wajah berminyak"
        )

        # Verify result
        assert result["success"] is True
        assert "structured_result" in result
        assert "markdown_output" in result
        assert "telegram_output" in result

        # Verify structured result
        structured = result["structured_result"]
        assert structured["master_prompt"] is not None
        assert len(structured["hashtags"]) > 0

    def test_formatter_telegram_message_generation(self):
        """Test Telegram message formatting."""
        formatter = OutputFormatter()

        prompt_data = {
            "master_prompt": "Test prompt",
            "visual_specifications": {
                "Style": "Cinematic",
                "Camera": "Close-up",
            },
            "script": {
                "hook": "Test hook",
                "cta": "Test CTA",
            },
            "hashtags": ["skincare", "fyp"],
        }

        telegram_msg = formatter.format_telegram_message(prompt_data)

        assert "MASTER PROMPT" in telegram_msg
        assert "VISUAL SPECIFICATIONS" in telegram_msg
        assert len(telegram_msg) > 0
