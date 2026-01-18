# RekaKata - UGC Prompt Generator

## Apa Itu RekaKata?

**RekaKata** adalah aplikasi AI yang secara otomatis menghasilkan prompt text-to-video berkualitas tinggi untuk konten UGC (User Generated Content). Cukup masukkan deskripsi produk atau ide konten, dan RekaKata akan menghasilkan prompt lengkap yang siap digunakan di platform AI video generation seperti RunwayML, Pika Labs, atau Kling.

## Masalah yang Diselesaikan

Bagi content creator, marketer, dan bisnis kecil:
- ** Kesulitan membuat prompt** yang efektif untuk AI video generator
- ** Tidak tahu trending format** yang sedang viral
- ** Butuh waktu lama** untuk riset format per platform
- **Hasil tidak konsisten** karena prompt kurang detail

## Solusi RekaKata

Dengan satu input teks sederhana, RekaKata akan:
1. Menganalisis konteks dan tujuan konten
2. Menginjeksi elemen trending terkini
3. Mengoptimasi untuk platform target (TikTok/IG/YT)
4. Menghasilkan prompt lengkap dengan spesifikasi visual, script, dan hashtag

## Target Pengguna

| Segment | Use Case |
|---------|----------|
| **Content Creator** | Bikin video viral dengan AI |
| **Digital Marketer** | Produksi konten ads lebih cepat |
| **Small Business** | Konten marketing tanpa tim produksi |
| **Agency** | Skala produksi konten UGC |
| **Influencer** | Konten konsisten dengan AI assistance |

## Value Proposition

| Sebelum RekaKata | Setelah RekaKata |
|------------------|------------------|
| Buat prompt manual 15-30 menit | Prompt siap dalam 30 detik |
| Hasil tidak terprediksi | Prompt terstruktur & optimized |
| Tidak tahu trending | Selalu update dengan trend |
| Platform-specific | Satu input, semua platform |

## Arsitektur Sistem

```
User Input (Teks)
     │
     ▼
┌───────────────────┐
│  Input Validator  │
│  - Sanitize       │
│  - Detect Lang    │
│  - Extract Entity │
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│  Prompt Engine    │
│  ┌─────────────┐  │
│  │Context Anal │  │
│  │Trend Inject │  │
│  │Platform Opt │  │
│  │Prompt Gen   │  │
│  └─────────────┘  │
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│  Groq API         │
│  Llama 3.3 70B    │
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│ Output Formatter  │
│  - Markdown       │
│  - Platform Var   │
│  - Hashtags       │
└────────┬──────────┘
         │
         ▼
Output: .md file + Preview
```

## Tech Stack

| Layer | Technology |
|-------|------------|
| **Language** | Python 3.11+ |
| **AI Provider** | Groq (Llama 3.3 70B) - FREE |
| **Bot Platform** | Telegram Bot API |
| **Hosting** | Railway / Render (FREE) |
| **Format Output** | Markdown |

## Fitur Utama MVP

### ✅ MVP Features
- [ ] CLI Interface
- [ ] Telegram Bot Integration
- [ ] Single AI Provider (Groq)
- [ ] Auto-analyze input text
- [ ] Generate Master Prompt (Text-to-Video)
- [ ] Visual Specs (Style, Camera, Lighting, AR)
- [ ] Script Generation (Hook, Body, CTA)
- [ ] Platform Optimization (TikTok/IG/YT)
- [ ] Hashtag Suggestions
- [ ] Output Language Matching
- [ ] Local .md File Storage
- [ ] Trending Elements 2025 Integration

### 📈 Future Features
- [ ] Discord Bot Integration
- [ ] Multiple AI Providers (OpenRouter, etc.)
- [ ] Web Dashboard
- [ ] Template Management
- [ ] Team Collaboration
- [ ] API Access
- [ ] Export to Notion/JSON
- [ ] Analytics Dashboard
- [ ] Mobile App
- [ ] AI Trend Auto-Update

## Timeline Pengembangan

| Phase | Durasi | Deliverables |
|-------|--------|--------------|
| **Phase 1: Setup** | 1-2 jam | Folder structure, requirements, config |
| **Phase 2: Core** | 2-3 jam | Prompt Engine, Groq API, Formatters |
| **Phase 3: Bot** | 1-2 jam | Telegram Bot integration |
| **Phase 4: Data** | 30 min | Trending cache, templates |
| **Phase 5: Testing** | 1 jam | Unit tests, integration test |
| **Phase 6: Deploy** | 30 min | Railway/Render deployment |

## Biaya Operasional

| Item | Biaya |
|------|-------|
| **Groq API** | FREE (14.400 req/day) |
| **Telegram Bot** | FREE |
| **Hosting Railway** | FREE (500 jam/bulan) |
| **Hosting Render** | FREE (750 jam/bulan) |
| **Total/Month** | **Rp 0** |

## Cara Kerja

### Input Contoh
```
User: "Jualin skincare pagi hari yang bagus buat wajah berminyak"
```

### Output (Markdown)
```markdown
# MASTER PROMPT (Text-to-Video)

**Prompt untuk RunwayML/Pika/Kling:**
"A cinematic morning skincare routine for oily skin, soft natural lighting, close-up shots of product application, ASMR sound, 9:16 vertical format"

---

# VISUAL SPECIFICATIONS

| Element | Value |
|---------|-------|
| Style | Cinematic / Clean Beauty |
| Camera | Close-up, POV, Slow motion |
| Lighting | Soft natural, rim light |
| Aspect Ratio | 9:16 |
| Mood | Fresh, Clean, Trustworthy |

---

# SCRIPT

## Hook [0:00-0:03]
*"Pagi-pagi udah bangun, wajah mengkilap kayak chef masak?"*

## Body [0:03-0:45]
[Show product application process with ASMR sounds]
[Before/after skin comparison]
[Quick tips for oily skin]

## CTA [0:45-0:60]
*"Follow untuk skincare yang actually kerja ✨"*

---

# PLATFORM OPTIMIZATION

**TikTok:**
- Use trending "skincare routine" sound
- Green screen ready for reaction
- Caption: "belum mandi dulu nonton ini"

**Instagram Reels:**
- Higher production quality
- Carousel slides for product details
- Save-able content

**YouTube Shorts:**
- Teaser untuk video longer
- Subscribe CTA di end screen

---

# HASHTAGS
#skincare #skincareroutine #oilyskin #acne #facecare #beautytips #indonesianbeauty # skincareviral #morningroutine #cewekbanget
```

## Metric Keberhasilan MVP

| Metric | Target |
|--------|--------|
| **Response Time** | < 5 detik |
| **User Satisfaction** | > 4/5 rating |
| **Uptime** | > 99% |
| **Daily Active Users** | 50+ dalam 30 hari |
| **Prompt Quality** | User tidak perlu edit manual |

## Risiko dan Mitigasi

| Risiko | Mitigasi |
|--------|----------|
| Groq API limit | Implementasi caching, multiple providers |
| Trending outdated | Auto-update mechanism, manual review |
| User feedback negatif | Rapid iteration, A/B testing |
| Hosting downtime | Multi-region deployment |

## Langkah Selanjutnya

1. **Review** dokumen ini dan give feedback
2. **Set up** development environment
3. **Start coding** sesuai `app_development.md`
4. **Test** dengan use cases nyata
5. **Deploy** ke Railway/Render
6. **Launch** ke audience pertama

---

*Document Version: 1.0*
*Last Updated: January 2026*
*Project: RekaKata - UGC Prompt Generator*
