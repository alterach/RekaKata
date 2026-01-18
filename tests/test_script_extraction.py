"""Test script extraction with various AI output formats."""
import pytest
from src.core.prompt_engine import PromptEngine


class TestScriptExtractionPatterns:
    """Test various AI output formats for script extraction."""

    @pytest.fixture
    def engine(self):
        """Create PromptEngine instance for testing."""
        return PromptEngine()

    def test_standard_format(self, engine):
        """Test standard ## Hook format with newlines."""
        raw = """## Hook [0:00-0:03]
Test hook

## Body [0:03-0:45]
Test body

## CTA [0:45-0:60]
Test CTA"""

        script = engine._extract_script(raw)
        assert script["hook"] == "Test hook"
        assert script["body"] == "Test body"
        assert script["cta"] == "Test CTA"

    def test_bold_section_names(self, engine):
        """Test ## **Hook** format (AI common output)."""
        raw = """## **Hook** [0:00-0:03]
Test hook

## **Body** [0:03-0:45]
Test body

## **CTA** [0:45-0:60]
Test CTA"""

        script = engine._extract_script(raw)
        assert script["hook"] == "Test hook"
        assert script["body"] == "Test body"
        assert script["cta"] == "Test CTA"

    def test_inline_content(self, engine):
        """Test hook/body/cta content on same line as header."""
        raw = """## Hook: Test hook
## Body: Test body
## CTA: Test CTA"""

        script = engine._extract_script(raw)
        assert script["hook"] == "Test hook"
        assert script["body"] == "Test body"
        assert script["cta"] == "Test CTA"

    def test_numbered_list_format(self, engine):
        """Test numbered list format (1. Hook, 2. Body, etc.)."""
        raw = """1. Hook: Test hook
2. Body: Test body
3. CTA: Test CTA"""

        script = engine._extract_script(raw)
        assert script["hook"] == "Test hook"
        assert script["body"] == "Test body"
        assert script["cta"] == "Test CTA"

    def test_special_characters(self, engine):
        """Test script with Markdown special characters."""
        raw = """## Hook [0:00-0:03]
"Test hook with *special* chars!"

## Body [0:03-0:45]
Body with _underscore_ and (parens)

## CTA [0:45-0:60]
Call to action [with] brackets"""

        script = engine._extract_script(raw)
        assert script["hook"] != "N/A"
        assert script["body"] != "N/A"
        assert script["cta"] != "N/A"
        assert "*" in script["hook"]
        assert "_" in script["body"]
        assert "[" in script["cta"]

    def test_missing_sections(self, engine):
        """Test when some sections are missing."""
        raw = """## Hook [0:00-0:03]
Test hook

## Body [0:03-0:45]
Test body"""

        script = engine._extract_script(raw)
        assert script["hook"] == "Test hook"
        assert script["body"] == "Test body"
        assert script["cta"] == "N/A"

    def test_triple_bold_format(self, engine):
        """Test ***Hook*** format (AI sometimes uses 3 asterisks)."""
        raw = """## ***Hook*** [0:00-0:03]
Test hook

## ***Body*** [0:03-0:45]
Test body

## ***CTA*** [0:45-0:60]
Test CTA"""

        script = engine._extract_script(raw)
        assert script["hook"] == "Test hook"
        assert script["body"] == "Test body"
        assert script["cta"] == "Test CTA"

    def test_mixed_formatting(self, engine):
        """Test mix of different header formats in same response."""
        raw = """## **Hook** [0:00-0:03]
Test hook

### Body [0:03-0:45]
Test body

1. CTA: Test CTA"""

        script = engine._extract_script(raw)
        assert script["hook"] == "Test hook"
        assert script["body"] == "Test body"
        assert script["cta"] == "Test CTA"

    def test_empty_response(self, engine):
        """Test empty AI response."""
        raw = ""

        script = engine._extract_script(raw)
        assert script["hook"] == "N/A"
        assert script["body"] == "N/A"
        assert script["cta"] == "N/A"

    def test_content_with_quotes(self, engine):
        """Test content wrapped in quotes."""
        raw = """## Hook [0:00-0:03]
"Test hook in quotes"

## Body [0:03-0:45]
'Test body in single quotes'

## CTA [0:45-0:60]
Test CTA without quotes"""

        script = engine._extract_script(raw)
        assert script["hook"] == "Test hook in quotes"
        assert script["body"] == "Test body in single quotes"
        assert script["cta"] == "Test CTA without quotes"
