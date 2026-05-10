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
