IronLayer: The DLP Layer for Generative AI
IronLayer is a high-performance security proxy that sanitizes sensitive data (PII, PHI, IP) before it reaches external LLMs like OpenAI or Anthropic.

Why IronLayer?
Zero Data Leakage: Automatically redacts Credit Cards, Emails, and Custom Secrets.
Bi-Directional Restoration: Users see the clean, real output; the AI sees only placeholders.
Model Agnostic: Works with OpenAI, Anthropic, Groq, and local LLMs.
Audit Ready: Generates real-time logs of every intercepted risk.
Quick Start (Docker)
Pull the container:
docker pull ironlayer/gateway:latest
Run the container:
bash

docker run -p 8000:8000 -e API_KEY=your_openai_key ironlayer/gateway:latest
Send traffic:
Point your OpenAI client to http://localhost:8000/v1 instead of the OpenAI URL.
Configuration
Set these environment variables to customize behavior:

API_KEY: Your LLM provider API key.
PROVIDER: Choose openai, groq, or openrouter.
CUSTOM_SECRET_WORDS: Comma-separated list of project names to scrub (e.g., ProjectStarlight,SecretFormula).
License
MIT License.