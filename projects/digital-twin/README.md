---
title: digital_twin
app_file: app.py
sdk: gradio
sdk_version: 6.19.0
---

# Mancy's Digital Twin

An AI chatbot that acts as a digital twin of Mancy Ko, designed to answer questions about her career, background, skills, and projects. Built to be embedded in a personal portfolio website.

## Features

- Answers questions about education, experience, skills, and projects
- Automatically scrapes the live portfolio website on startup — no manual updates needed when new projects are added
- Captures visitor contact intent, notifies the owner, and sends the visitor a confirmation email
- Dark/light mode support via Gradio's built-in theme toggle

## Tech Stack

- **LLM:** DeepSeek (`deepseek-chat`) via OpenAI-compatible API
- **UI:** Gradio `ChatInterface`
- **Email:** EmailJS (owner notification + visitor acknowledgment templates)
- **Context:** Resume PDF (`pypdf`) + `summary.txt` + live portfolio scrape (`beautifulsoup4`)

## Project Structure

```
digital_twin/
├── app.py          # Gradio app and chat loop
├── context.py      # System prompt — loads resume, summary, and scrapes portfolio
├── tools.py        # Tool definitions and handlers (record email, record unknown questions)
├── styles.py       # Custom CSS, JS, and example prompts
├── summary.txt     # Short bio used in the system prompt
├── KoManSze_resume.pdf
└── requirements.txt
```

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure environment variables

Create a `.env` file in the project root:

```env
DEEPSEEK_API_KEY=your_deepseek_api_key
OWNER_EMAIL=your_notification_email
EMAILJS_SERVICE_ID=your_emailjs_service_id
EMAILJS_TEMPLATE_NOTIFY_ID=your_owner_notification_template_id
EMAILJS_TEMPLATE_ACK_ID=your_visitor_acknowledgment_template_id
EMAILJS_PUBLIC_KEY=your_emailjs_public_key
EMAILJS_PRIVATE_KEY=your_emailjs_private_key
```

> Requires an [EmailJS](https://www.emailjs.com/) account with a service and two templates: one that notifies the owner (`EMAILJS_TEMPLATE_NOTIFY_ID`) and one that acknowledges the visitor (`EMAILJS_TEMPLATE_ACK_ID`).

### 3. Run locally

```bash
python app.py
```

The app will be available at `http://127.0.0.1:7860`.

## Deployment

Deployed on [Hugging Face Spaces](https://huggingface.co/spaces/mancykokms/digital_twin) and embedded into the portfolio site via `<iframe>`. Add the environment variables as **Secrets** in the Space settings.

```html
<iframe
  src="https://mancykokms-digital-twin.hf.space"
  frameborder="0"
  width="100%"
  height="700">
</iframe>
```

### Syncing this folder to the Space

This folder lives inside the `mancykokms.github.io` repo, not as its own git repo, so it doesn't push to the Space directly. To sync:

```bash
git subtree split --prefix=projects/digital-twin -b hf-split
git lfs migrate import --include="*.pdf" -- hf-split   # PDF must be an LFS pointer, HF rejects raw binaries
git push --force https://<user>:<HF_TOKEN>@huggingface.co/spaces/mancykokms/digital_twin hf-split:main
git branch -D hf-split
```

The Space's git history is unrelated to this repo's, so pushes must be forced.
