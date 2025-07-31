# 🤝 Contributing to OmniAI-Dashboard

Thank you for considering contributing to **OmniAI Dashboard** — a groundbreaking AI-powered simulation platform that represents the future of autonomous businesses.

We welcome all kinds of contributions, including:
- 🚀 New features and enhancements
- 🐛 Bug fixes and testing
- 📝 Documentation improvements
- 🌐 Translations
- 💡 Ideas and suggestions

---

## 🧰 Project Setup

1. **Fork this repository**
2. Clone your fork:
   ```bash
   git clone https://github.com/OtiEdema/OmniAI-Dashboard.git
   cd OmniAI-Dashboard
   ```
3. Create a new branch for your work:
   ```bash
   git checkout -b feature/your-feature-name
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Add your OpenAI API key to `.streamlit/secrets.toml`:
   ```toml
   OPENAI_API_KEY = "your-api-key-here"
   ```

6. Run the app:
   ```bash
   streamlit run main.py
   ```

---

## 📦 Guidelines

### ✅ Pull Requests

- Explain what your PR does
- Link any related issues
- Keep commits clean and focused
- Always test before pushing!

### 🧪 Testing

Please test all changes locally before submitting. If you're adding new features, consider adding sample voice/text input and agent interactions.

---

## 🌐 Language Contributions

To contribute a new language:
- Add the language code to the `language_map` in `main.py`
- Test it with Whisper and translation
- Submit a PR with the updates

---

## 🛡️ Code of Conduct

Please review our [Code of Conduct](CODE_OF_CONDUCT.md) (coming soon). Be respectful, kind, and inclusive.

---

## 🙌 Acknowledgements

Built with 💙 by [@OtiEdema](https://github.com/OtiEdema) and the open-source community.

---

Ready to contribute? Open a PR or [create an issue](https://github.com/OtiEdema/OmniAI-Dashboard/issues).