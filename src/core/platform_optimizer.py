"""Platform Optimizer for TikTok, Instagram Reels, and YouTube Shorts."""
from typing import Dict, List, Optional
from config.logging_config import log


class PlatformOptimizer:
    """Optimizes prompts for different social media platforms."""

    PLATFORM_SPECS = {
        "tiktok": {
            "aspect_ratio": "9:16",
            "max_duration": "60s",
            "resolution": "1080x1920",
            "characteristics": "fast-paced, energetic, trending sounds, hook in first 3 seconds",
            "optimal_length": "15-30s",
        },
        "instagram": {
            "aspect_ratio": "9:16",
            "max_duration": "90s",
            "resolution": "1080x1920",
            "characteristics": "high production quality, aesthetic, saveable content, carousel ready",
            "optimal_length": "15-60s",
        },
        "youtube": {
            "aspect_ratio": "9:16",
            "max_duration": "60s",
            "resolution": "1080x1920",
            "characteristics": "engaging, teaser for longer content, subscribe CTA",
            "optimal_length": "30-60s",
        },
    }

    def __init__(self, platforms: Optional[List[str]] = None):
        """
        Initialize platform optimizer.

        Args:
            platforms: List of target platforms (default: all platforms)
        """
        self.platforms = platforms or list(self.PLATFORM_SPECS.keys())
        log.info(f"PlatformOptimizer initialized for: {self.platforms}")

    def optimize_for_platform(self, platform: str, content: Dict) -> Dict:
        """
        Optimize content for a specific platform.

        Args:
            platform: Platform name (tiktok, instagram, youtube)
            content: Dictionary containing content elements

        Returns:
            Platform-specific optimized content
        """
        if platform not in self.PLATFORM_SPECS:
            log.warning(f"Unknown platform: {platform}, using default")
            platform = "tiktok"

        specs = self.PLATFORM_SPECS[platform]

        optimized = {
            "platform": platform,
            "aspect_ratio": specs["aspect_ratio"],
            "max_duration": specs["max_duration"],
            "resolution": specs["resolution"],
            "characteristics": specs["characteristics"],
            "optimal_length": specs["optimal_length"],
        }

        # Platform-specific customizations
        if platform == "tiktok":
            optimized.update(
                {
                    "caption_style": "catchy, short, include trending hashtags",
                    "music_suggestion": "Use trending sounds from TikTok library",
                    "editing_tips": "Quick cuts, text overlays, green screen effects",
                    "posting_time": "Peak hours: 7-9 AM, 12-3 PM, 7-11 PM",
                }
            )
        elif platform == "instagram":
            optimized.update(
                {
                    "caption_style": "engaging, include questions for engagement",
                    "music_suggestion": "Use trending Instagram Reels audio",
                    "editing_tips": "High quality, smooth transitions, aesthetic",
                    "posting_time": "Peak hours: 11 AM, 7 PM, 9 PM",
                }
            )
        elif platform == "youtube":
            optimized.update(
                {
                    "caption_style": "informative, include subscribe reminder",
                    "music_suggestion": "Use royalty-free or trending Shorts audio",
                    "editing_tips": "Engaging hook, subscribe CTA at end",
                    "posting_time": "Peak hours: 2-4 PM, 7-10 PM",
                }
            )

        log.info(f"Optimized content for {platform}")
        return optimized

    def optimize_for_all_platforms(self, content: Dict) -> Dict[str, Dict]:
        """
        Optimize content for all configured platforms.

        Args:
            content: Dictionary containing content elements

        Returns:
            Dictionary of platform-specific optimized content
        """
        all_optimized = {}

        for platform in self.platforms:
            all_optimized[platform] = self.optimize_for_platform(platform, content)

        log.info(f"Optimized content for {len(all_optimized)} platforms")
        return all_optimized

    def get_best_platform_for_content(self, content_type: str, entities: Dict) -> str:
        """
        Recommend the best platform for given content type.

        Args:
            content_type: Type of content (e.g., tutorial, review, vlog)
            entities: Detected entities from input

        Returns:
            Recommended platform name
        """
        # Content type preferences
        content_preferences = {
            "tutorial": ["instagram", "youtube"],
            "review": ["youtube", "tiktok"],
            "challenge": ["tiktok"],
            "vlog": ["youtube", "instagram"],
            "transformation": ["tiktok", "instagram"],
            "asmr": ["tiktok", "instagram"],
        }

        # Get platforms for content type
        preferred = content_preferences.get(content_type.lower(), self.platforms)

        # Filter by available platforms
        available = [p for p in preferred if p in self.platforms]

        # Return first available or default to TikTok
        recommendation = available[0] if available else "tiktok"

        log.info(f"Recommended platform for {content_type}: {recommendation}")
        return recommendation

    def get_caption_suggestions(self, platform: str, entities: Dict, language: str = "id") -> List[str]:
        """
        Generate caption suggestions for a platform.

        Args:
            platform: Platform name
            entities: Detected entities
            language: Output language

        Returns:
            List of caption suggestions
        """
        if language == "id":
            captions = {
                "tiktok": [
                    "Gak nyangka bisa se-viral ini! 🤯",
                    "Wajib coba sebelum nyesel!",
                    "Share ke temen kamu yang butuh ini! 👯",
                    "Ini dia rahasianya! ✨",
                ],
                "instagram": [
                    "Simpan biar nggak lupa! 🔖",
                    "Kamu pernah coba ini? Drop di komen! 💬",
                    "Tag temen yang wajib tau ini! 👇",
                    "Double tap kalau suka! ❤️",
                ],
                "youtube": [
                    "Subscribe buat konten seru lainnya! 🔔",
                    "Nyesel baru tau sekarang! 😅",
                    "Yang masih belum tau, angkat tangan! 🙋",
                    "Share ke yang belum tahu! 📢",
                ],
            }
        else:
            captions = {
                "tiktok": [
                    "Can't believe how viral this got! 🤯",
                    "Must try before you regret it!",
                    "Share with a friend who needs this! 👯",
                    "Here's the secret! ✨",
                ],
                "instagram": [
                    "Save this for later! 🔖",
                    "Have you tried this? Drop a comment! 💬",
                    "Tag a friend who needs to know this! 👇",
                    "Double tap if you like it! ❤️",
                ],
                "youtube": [
                    "Subscribe for more content like this! 🔔",
                    "Can't believe I just found out! 😅",
                    "Raise your hand if you didn't know! 🙋",
                    "Share with someone who doesn't know yet! 📢",
                ],
            }

        return captions.get(platform, captions["tiktok"])

    def get_posting_schedule(self, platform: str) -> List[str]:
        """
        Get recommended posting schedule for a platform.

        Args:
            platform: Platform name

        Returns:
            List of optimal posting times
        """
        schedules = {
            "tiktok": [
                "7:00 AM - 9:00 AM",
                "12:00 PM - 3:00 PM",
                "7:00 PM - 11:00 PM",
            ],
            "instagram": [
                "11:00 AM",
                "7:00 PM",
                "9:00 PM",
            ],
            "youtube": [
                "2:00 PM - 4:00 PM",
                "7:00 PM - 10:00 PM",
            ],
        }

        return schedules.get(platform, schedules["tiktok"])
