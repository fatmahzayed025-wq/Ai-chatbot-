# Saudi E-commerce Chatbot (Gemini Edition)

This is a standalone Python script designed for e-commerce platforms targeting Saudi customers. It features a Gemini-powered chatbot configured with a persona that uses a casual Saudi Arabic dialect. The chatbot is designed to assist with tracking orders, answering product inquiries, and providing product recommendations, while gracefully transferring unanswerable queries to a human support agent on WhatsApp.

## Features
- **Persona:** Casual Saudi Arabic dialect.
- **Roles:** Track orders, answer product inquiries, provide recommendations.
- **Fallback:** Provides a configurable WhatsApp number for human support when it doesn't know the answer.
- **Concurrent User Limit:** Automatically limits active connections to a configurable maximum (default: 15). If the limit is exceeded, it responds with a polite Saudi Arabic wait message: *"المعذرة، فريقنا مشغول حالياً، ثواني وبنكون معاك، شكراً لانتظارك."*
- **Standalone:** Includes an interactive Command Line Interface (CLI) for immediate testing.
- **Integration-Ready:** Provides a clean `SaudiEcommerceChatbot` class that you can easily integrate into any Python application (Flask, FastAPI, Django, etc.).

## Prerequisites

- Python 3.7+
- A Google Gemini API Key

## Installation

1. Clone or download this repository.
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set your Gemini API key:
   ```bash
   export GEMINI_API_KEY='your-api-key'
   ```
4. Run the web server:
   ```bash
   gunicorn app:app
   ```

## Deployment on Render

To host this chatbot for free using a public URL on Render, follow these steps:

1. **Push to GitHub**: Make sure your code is pushed to a GitHub repository.
2. **Create a Render Account**: Go to [render.com](https://render.com) and sign up/log in.
3. **New Web Service**: Click on "New" -> "Web Service".
4. **Connect GitHub**: Select "Build and deploy from a Git repository" and connect your GitHub account. Select the repository containing this chatbot.
5. **Configure the Service**:
   - **Name**: Choose a name for your service (e.g., `saudi-ecommerce-bot`).
   - **Environment**: Select `Python 3`.
   - **Region**: Choose a region closest to your users.
   - **Branch**: Typically `main` or `master`.
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
6. **Set Environment Variables**:
   - Scroll down to the "Environment Variables" section.
   - Click "Add Environment Variable".
   - Key: `GEMINI_API_KEY`
   - Value: Paste your actual Gemini API Key here.
7. **Deploy**: Click "Create Web Service". Render will automatically build and deploy your app.
8. **Auto-Updates**: Because you connected your GitHub repository, any future `git push` to the selected branch will automatically trigger a new deployment.
