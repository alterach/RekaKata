# RekaKata - UGC Prompt Generator

AI-powered prompt generator for text-to-video content creation. Generate optimized prompts for RunwayML, Pika Labs, and Kling AI video generators.

## Features

- **CLI Interface**: Generate prompts directly from your terminal
- **Telegram Bot**: Create prompts via Telegram with simple commands
- **AI-Powered**: Uses Groq API with Llama 3.3 70B for intelligent prompt generation
- **Platform Optimization**: Optimized for TikTok, Instagram Reels, and YouTube Shorts
- **Multi-Language**: Supports input in various languages with matching output
- **Visual Specs**: Includes style, camera, lighting, and mood specifications
- **Script Generation**: Generates hooks, body content, and CTAs
- **Hashtag Suggestions**: Provides relevant hashtags for each platform

## Quick Start

### Prerequisites

- Python 3.11 or higher
- Groq API key (Get free at https://console.groq.com/)
- Telegram Bot token (Create bot via @BotFather)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd SaaS-Ideas/RekaKata
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
```bash
cp .env.example .env
# Edit .env and add your API keys
```

### Usage

#### CLI

Generate a prompt:
```bash
python -m src.cli generate "Jualin skincare pagi hari yang bagus buat wajah berminyak"
```

#### Telegram Bot

1. Start the bot:
```bash
python -m src.bot.main
```

2. In Telegram:
   - `/start` - Initialize the bot
   - `/generate <your idea>` - Generate a prompt
   - `/export` - Export the last generated prompt as .md file

## Project Structure

```
RekaKata/
├── src/
│   ├── core/           # Core functionality
│   ├── bot/            # Telegram bot
│   └── cli/            # CLI interface
├── tests/              # Test files
├── data/               # Data files and templates
├── config/             # Configuration files
├── output/             # Generated prompts (markdown files)
└── logs/               # Application logs
```

## Development

### Running Tests

```bash
pytest
```

### Code Coverage

```bash
pytest --cov=src --cov-report=html
```

## Deployment

### Railway

1. Connect repository to Railway
2. Add environment variables
3. Deploy

### Render

1. Create new Web Service
2. Connect repository
3. Add build command: `pip install -r requirements.txt`
4. Add start command: `python -m src.bot.main`

## Cost

- **Groq API**: FREE (14,400 requests/day)
- **Telegram Bot**: FREE
- **Hosting**: FREE (Railway/Render free tiers)

## License

MIT License

## Support

For issues and questions, please open an issue on GitHub.
