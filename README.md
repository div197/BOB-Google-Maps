# BOB Google Maps

*Build Online Business – Made in 🇮🇳, Made for the World*

BOB Google Maps is an open-source (MIT) toolkit that turns raw location data into actionable business intelligence. Powered by principles of **Niṣkāma Karma Yoga** (self-less, excellence-first action), BOB combines the entrepreneurial spirit of Bill Gates, Steve Jobs and Jeff Bezos (our Trimūrti) into a single developer-friendly package.

## Key Goals

1. **Fast, Accurate Scraping** – Selenium-based crawler extracts business profiles & reviews at scale.
2. **AI-Driven Insights** – Sentiment, competitive landscape & opportunity scoring out-of-the-box.
3. **Plug-and-Play API** – Use BOB as a CLI, Python library or REST micro-service.
4. **Community-Centric** – 100 % open source, transparent roadmap and welcoming contributor guide.

## Repository Structure (v0.1)

```text
bob_core/         # Fresh, fully-typed MIT codebase (WIP)
legacy/           # Original GPL code (reference only, do not distribute)
docs/             # Vision, design docs & architecture diagrams
.github/          # CI / CD workflows
CHANGELOG.md      # Version history
LICENSE           # MIT license
```

## Getting Started

```bash
# Clone
$ git clone https://github.com/div197/BOB-Google-Maps.git
$ cd BOB-Google-Maps

# (Soon) install
$ pip install -e .

# (Soon) run a quick scrape
$ bob gmaps "https://maps.google.com/...&hl=en"

# Scrape a single place (headless)
bob gmaps "https://maps.google.com/?q=Eiffel+Tower&hl=en"

# Batch scrape from file (4 workers)
bob batch urls.txt --workers 4

# Analyze scraped data for business insights
bob analyze results.json

# Use Playwright backend (faster)
bob gmaps "https://maps.google.com/?q=restaurant&hl=en" --backend playwright
```

> **Status – Beta (0.3.0)**
> Full-featured scraper with Playwright backend, analytics, and business intelligence. Ready for production use. See `CHANGELOG.md` for details.

## Contributing

We welcome pull requests, issues and ideas – all in the spirit of service (seva) and excellence. Please read `docs/vision.md` to understand the project philosophy.

## License

MIT © 2025 Divyanshu Singh Chouhan (<divyanshu@abcsteps.com>) 