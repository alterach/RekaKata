"""Groq API client for Llama 3.3 70B integration."""
from typing import Dict, List, Optional
from groq import Groq
from tenacity import retry, stop_after_attempt, wait_exponential
from config.settings import get_settings
from config.logging_config import log


class GroqClient:
    """Groq API client wrapper for Llama 3.3 70B."""

    def __init__(self):
        """Initialize Groq client."""
        settings = get_settings()
        self.client = Groq(api_key=settings.groq_api_key)
        self.model = settings.groq_model
        self.temperature = settings.groq_temperature
        self.max_tokens = settings.groq_max_tokens
        log.info(f"GroqClient initialized with model: {self.model}")

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
    )
    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> str:
        """
        Generate text using Groq API.

        Args:
            prompt: User prompt
            system_prompt: System prompt for context
            temperature: Temperature for generation (overrides default)
            max_tokens: Maximum tokens to generate (overrides default)

        Returns:
            Generated text as string

        Raises:
            Exception: If API call fails after retries
        """
        messages = []

        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        messages.append({"role": "user", "content": prompt})

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature or self.temperature,
                max_tokens=max_tokens or self.max_tokens,
            )

            result = response.choices[0].message.content
            log.info(f"Generated response ({len(result)} characters)")
            return result

        except Exception as e:
            log.error(f"Groq API error: {e}")
            raise

    def generate_prompt_from_input(
        self,
        user_input: str,
        entities: Dict,
        language: str,
        trending_elements: Dict,
        platform_specifics: Optional[Dict] = None,
    ) -> Dict:
        """
        Generate a complete prompt for text-to-video generation.

        Args:
            user_input: Original user input
            entities: Detected entities
            language: Input language
            trending_elements: Trending elements to inject
            platform_specifics: Platform-specific optimizations

        Returns:
            Dictionary containing all prompt components
        """
        system_prompt = self._get_system_prompt(language)

        user_prompt = self._build_user_prompt(
            user_input, entities, trending_elements, platform_specifics
        )

        generated_text = self.generate(
            prompt=user_prompt,
            system_prompt=system_prompt,
            temperature=0.7,
            max_tokens=2048,
        )

        # Parse the generated response into structured format
        result = self._parse_generated_response(generated_text, language)

        log.info("Prompt generation completed successfully")
        return result

    def _get_system_prompt(self, language: str) -> str:
        """
        Get system prompt for AI.

        Args:
            language: Output language

        Returns:
            System prompt string
        """
        if language == "id":
            return """Anda adalah asisten AI yang ahli dalam membuat prompt text-to-video berkualitas tinggi untuk konten UGC (User Generated Content).

Tugas Anda:
1. Analisis input pengguna dan buat prompt yang detail dan spesifik
2. Sertakan spesifikasi visual (style, camera, lighting, aspect ratio, mood)
3. Buat script yang terstruktur (Hook, Body, CTA)
4. Optimalkan untuk platform media sosial (TikTok/Instagram/YouTube)
5. Sertakan hashtag yang relevan

Format output yang diharapkan:
- MASTER PROMPT untuk AI video generator (RunwayML/Pika/Kling)
- VISUAL SPECIFICATIONS dalam format tabel
- SCRIPT dengan pembagian Hook [0:00-0:03], Body [0:03-0:45], CTA [0:45-0:60]
- PLATFORM OPTIMIZATION untuk TikTok, Instagram Reels, YouTube Shorts
- HASHTAGS yang relevan dan trending

Pastikan prompt:
- Spesifik dan detail
- Mudah dipahami oleh AI video generator
- Mengikuti tren terkini tahun 2025
- Sesuai dengan bahasa input pengguna"""
        else:
            return """You are an AI assistant expert in creating high-quality text-to-video prompts for UGC (User Generated Content).

Your tasks:
1. Analyze user input and create detailed, specific prompts
2. Include visual specifications (style, camera, lighting, aspect ratio, mood)
3. Create structured scripts (Hook, Body, CTA)
4. Optimize for social media platforms (TikTok/Instagram/YouTube)
5. Include relevant hashtags

Expected output format:
- MASTER PROMPT for AI video generator (RunwayML/Pika/Kling)
- VISUAL SPECIFICATIONS in table format
- SCRIPT with Hook [0:00-0:03], Body [0:03-0:45], CTA [0:45-0:60]
- PLATFORM OPTIMIZATION for TikTok, Instagram Reels, YouTube Shorts
- HASHTAGS that are relevant and trending

Ensure prompts are:
- Specific and detailed
- Easy for AI video generators to understand
- Following 2025 trends
- In the same language as user input"""

    def _build_user_prompt(
        self,
        user_input: str,
        entities: Dict,
        trending_elements: Dict,
        platform_specifics: Optional[Dict] = None,
    ) -> str:
        """
        Build user prompt from input and analysis.

        Args:
            user_input: Original user input
            entities: Detected entities
            trending_elements: Trending elements
            platform_specifics: Platform-specific info

        Returns:
            Formatted user prompt
        """
        prompt_parts = [
            f"# User Input:\n{user_input}\n",
        ]

        # Add entity information
        if entities:
            entities_text = "\n".join(
                [f"- {key}: {value}" for key, value in entities.items() if value]
            )
            prompt_parts.append(f"# Detected Entities:\n{entities_text}\n")

        # Add trending elements
        if trending_elements:
            trending_text = self._format_trending_elements(trending_elements)
            prompt_parts.append(f"# Trending Elements:\n{trending_text}\n")

        # Add platform specifics
        if platform_specifics:
            platform_text = self._format_platform_specifics(platform_specifics)
            prompt_parts.append(f"# Platform Specifics:\n{platform_text}\n")

        prompt_parts.append(
            "\nBased on the information above, generate a complete, detailed, and optimized prompt for text-to-video generation following the specified format."
        )

        return "\n".join(prompt_parts)

    def _format_trending_elements(self, trending_elements: Dict) -> str:
        """Format trending elements for prompt."""
        parts = []

        if trending_elements.get("format"):
            parts.append(f"- Format: {trending_elements['format']['name']}")

        if trending_elements.get("visual_style"):
            style = trending_elements["visual_style"]
            parts.append(f"- Visual Style: {style['name']} ({style['style']})")

        if trending_elements.get("hooks"):
            hooks_str = ", ".join(trending_elements["hooks"][:3])
            parts.append(f"- Example Hooks: {hooks_str}")

        if trending_elements.get("hashtags"):
            hashtags_str = ", ".join(trending_elements["hashtags"][:10])
            parts.append(f"- Hashtags: {hashtags_str}")

        return "\n".join(parts)

    def _format_platform_specifics(self, platform_specifics: Dict) -> str:
        """Format platform-specific information for prompt."""
        parts = []

        for platform, specs in platform_specifics.items():
            parts.append(f"\n## {platform.capitalize()}:")
            parts.append(f"- Aspect Ratio: {specs['aspect_ratio']}")
            parts.append(f"- Characteristics: {specs['characteristics']}")
            parts.append(f"- Optimal Length: {specs['optimal_length']}")

        return "\n".join(parts)

    def _parse_generated_response(self, response: str, language: str) -> Dict:
        """
        Parse generated AI response into structured format.

        Args:
            response: Raw AI response text
            language: Output language

        Returns:
            Structured dictionary with prompt components
        """
        # For now, return the raw response as-is
        # In production, we could parse this more carefully
        return {
            "raw_response": response,
            "language": language,
            "generated_at": None,  # Would be set to datetime.now()
        }
