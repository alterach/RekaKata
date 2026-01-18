"""Prompt Engine - Main orchestrator for prompt generation."""
from typing import Dict, Optional
from src.core.input_validator import InputValidator
from src.core.trending_injector import TrendingInjector
from src.core.groq_client import GroqClient
from src.core.platform_optimizer import PlatformOptimizer
from src.core.output_formatter import OutputFormatter
from config.logging_config import log


class PromptEngine:
    """Main engine for generating optimized UGC prompts."""

    def __init__(self, platforms: Optional[list] = None):
        """
        Initialize prompt engine with all components.

        Args:
            platforms: List of target platforms (default: all platforms)
        """
        self.validator = InputValidator()
        self.trending_injector = TrendingInjector()
        self.groq_client = GroqClient()
        self.platform_optimizer = PlatformOptimizer(platforms)
        self.formatter = OutputFormatter()

        self.last_generated = None
        log.info("PromptEngine initialized with all components")

    def generate_prompt(self, user_input: str, platforms: Optional[list] = None) -> Dict:
        """
        Generate a complete prompt for text-to-video generation.

        Args:
            user_input: User's content idea or description
            platforms: List of target platforms (optional)

        Returns:
            Dictionary containing all prompt components and outputs
        """
        try:
            log.info(f"Starting prompt generation for: '{user_input[:50]}...'")

            # Step 1: Validate and analyze input
            validation_result = self.validator.validate(user_input)
            if not validation_result["valid"]:
                log.error(f"Validation failed: {validation_result['error']}")
                return {
                    "success": False,
                    "error": validation_result["error"],
                    "user_input": user_input,
                }

            log.info("Input validation successful")

            # Extract relevant data
            sanitized_input = validation_result["sanitized"]
            language = validation_result["language"]
            entities = validation_result["entities"]

            # Step 2: Inject trending elements
            trending_elements = self.trending_injector.inject(entities, language)
            log.info("Trending elements injected")

            # Step 3: Optimize for platforms
            if platforms:
                optimizer = PlatformOptimizer(platforms)
            else:
                optimizer = self.platform_optimizer

            platform_specifics = optimizer.optimize_for_all_platforms(
                {"entities": entities, "language": language}
            )
            log.info("Platform optimization completed")

            # Step 4: Generate AI prompt
            ai_result = self.groq_client.generate_prompt_from_input(
                user_input=sanitized_input,
                entities=entities,
                language=language,
                trending_elements=trending_elements,
                platform_specifics=platform_specifics,
            )
            log.info("AI generation completed")

            # Step 5: Parse and structure the result
            # For now, we'll use a simple structure based on the AI response
            # In production, we would parse this more carefully
            structured_result = self._structure_result(
                ai_result, trending_elements, platform_specifics, language
            )

            # Step 6: Format outputs
            markdown_output = self.formatter.format_markdown(
                structured_result, platform_specifics
            )
            telegram_output = self.formatter.format_telegram_message(
                structured_result, platform_specifics
            )

            # Store last generated for export functionality
            self.last_generated = {
                "structured": structured_result,
                "markdown": markdown_output,
                "telegram": telegram_output,
                "platform_specifics": platform_specifics,
            }

            log.info("Prompt generation completed successfully")

            return {
                "success": True,
                "user_input": user_input,
                "sanitized_input": sanitized_input,
                "language": language,
                "entities": entities,
                "structured_result": structured_result,
                "markdown_output": markdown_output,
                "telegram_output": telegram_output,
                "platform_specifics": platform_specifics,
            }

        except Exception as e:
            log.error(f"Error in prompt generation: {e}", exc_info=True)
            return {
                "success": False,
                "error": str(e),
                "user_input": user_input,
            }

    def _structure_result(
        self,
        ai_result: Dict,
        trending_elements: Dict,
        platform_specifics: Dict,
        language: str,
    ) -> Dict:
        """
        Structure the AI result into a standardized format.

        Args:
            ai_result: Raw result from Groq client
            trending_elements: Trending elements injected
            platform_specifics: Platform optimizations
            language: Output language

        Returns:
            Structured result dictionary
        """
        # Extract raw response
        raw_response = ai_result.get("raw_response", "")

        # Parse the AI response to extract structured data
        # This is a simplified parser - in production, we would use more robust parsing
        master_prompt = self._extract_master_prompt(raw_response)
        visual_specs = self._extract_visual_specs(raw_response)
        script = self._extract_script(raw_response)
        hashtags = self._extract_hashtags(raw_response, trending_elements)

        return {
            "master_prompt": master_prompt,
            "visual_specifications": visual_specs,
            "script": script,
            "hashtags": hashtags,
            "language": language,
            "raw_response": raw_response,
        }

    def _extract_master_prompt(self, raw_response: str) -> str:
        """Extract master prompt from AI response."""
        # Look for the section after "MASTER PROMPT" or similar
        if "MASTER PROMPT" in raw_response:
            lines = raw_response.split("\n")
            in_section = False
            prompt_lines = []

            for line in lines:
                if "MASTER PROMPT" in line:
                    in_section = True
                    continue
                if in_section:
                    if line.strip().startswith("#") or "---" in line:
                        break
                    if line.strip():
                        # Remove quote marks if present
                        clean_line = line.strip().strip('"')
                        prompt_lines.append(clean_line)

            return " ".join(prompt_lines)

        return raw_response.split("\n")[0] if raw_response else "N/A"

    def _extract_visual_specs(self, raw_response: str) -> Dict:
        """Extract visual specifications from AI response."""
        specs = {
            "Style": "N/A",
            "Camera": "N/A",
            "Lighting": "N/A",
            "Aspect Ratio": "9:16",
            "Mood": "N/A",
        }

        if "VISUAL SPECIFICATIONS" in raw_response or "Visual Specifications" in raw_response:
            # Try to parse table format
            lines = raw_response.split("\n")
            in_section = False

            for i, line in enumerate(lines):
                if "VISUAL" in line or "Visual" in line:
                    in_section = True
                    continue

                if in_section and "---" in line:
                    continue

                if in_section and "|" in line and "---" not in line:
                    # This is a table row
                    parts = [p.strip() for p in line.split("|") if p.strip()]
                    if len(parts) >= 2:
                        key = parts[0]
                        value = parts[1]
                        if key in specs:
                            specs[key] = value

                if in_section and "#" in line and "VISUAL" not in line:
                    break

        return specs

    def _extract_script(self, raw_response: str) -> Dict:
        """Extract script sections from AI response with robust regex."""
        import re
        script = {"hook": "N/A", "body": "N/A", "cta": "N/A"}

        # Try to find script section
        if "SCRIPT" not in raw_response.upper():
            log.warning("SCRIPT section not found in AI response")
            return script

        # Normalize line endings
        text = raw_response.replace("\r\n", "\n")
        
        # Regex patterns for sections
        # Matches: ## Hook, **Hook**, Hook:, etc.
        patterns = {
            "hook": r"(?:^|\n)(?:##|\*\*|###)?\s*(?:Hook|HOOK).*?(?:\n|$)(.*?)(?=\n(?:##|\*\*|###)?\s*(?:Body|BODY|CTA|Cta)|$)",
            "body": r"(?:^|\n)(?:##|\*\*|###)?\s*(?:Body|BODY).*?(?:\n|$)(.*?)(?=\n(?:##|\*\*|###)?\s*(?:CTA|Cta|Hook|HOOK)|$)",
            "cta": r"(?:^|\n)(?:##|\*\*|###)?\s*(?:CTA|Cta|Call to Action).*?(?:\n|$)(.*?)(?=\n(?:##|\*\*|###)?\s*(?:#|---)|$)"
        }

        for section, pattern in patterns.items():
            match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
            if match:
                content = match.group(1).strip()
                # Clean up quotes if present
                content = content.strip('"').strip("'").strip("*")
                if content:
                    script[section] = content
                    log.info(f"Extracted {section}: {content[:30]}...")

        return script

    def _extract_hashtags(self, raw_response: str, trending_elements: Dict) -> list:
        """Extract hashtags from AI response or trending elements."""
        # First try to extract from response
        if "HASHTAGS" in raw_response or "Hashtags" in raw_response:
            lines = raw_response.split("\n")
            in_section = False
            hashtag_lines = []

            for line in lines:
                if "HASHTAGS" in line or "Hashtags" in line:
                    in_section = True
                    continue

                if in_section:
                    # Check for next section header (must be # HEADER format)
                    if (line.strip().startswith("#") and 
                        not line.strip().startswith("# ") and 
                        "#" not in line.strip()[1:]): # Simple heuristic: headers usually don't have multiple # inside
                        break
                    
                    # Also check for --- separator
                    if "---" in line:
                        break

                    if line.strip():
                        hashtag_lines.append(line.strip())

            if hashtag_lines:
                # Parse hashtags from the collected lines
                hashtags = []
                for line in hashtag_lines:
                    # Extract words starting with #
                    words = line.split()
                    hashtags.extend([w.replace("#", "") for w in words if w.startswith("#")])

                if hashtags:
                    return hashtags

        # Fallback to trending elements
        return trending_elements.get("hashtags", [])[:15]

    def export_last_generated(self, format: str = "md") -> Optional[str]:
        """
        Export the last generated prompt to file.

        Args:
            format: Output format ('md' or 'json')

        Returns:
            Path to saved file or None
        """
        if not self.last_generated:
            log.warning("No previously generated prompt to export")
            return None

        try:
            if format == "md":
                filepath = self.formatter.save_markdown(self.last_generated["markdown"])
            elif format == "json":
                filepath = self.formatter.save_json(self.last_generated["structured"])
            else:
                log.error(f"Unsupported format: {format}")
                return None

            return filepath

        except Exception as e:
            log.error(f"Error exporting prompt: {e}")
            return None
