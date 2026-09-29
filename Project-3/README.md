\# Multimodal Image Generation Studio



\## Project 3 - DecodeLabs Generative AI Internship



\### Description



Multimodal Image Generation Studio is a Python application designed to

translate natural-language image descriptions into image-generation requests.



The application provides configurable generation settings including:



\- Natural-language image prompts

\- Aspect ratio

\- Image resolution

\- Image quality

\- Number of generated images

\- Demo Mode

\- OpenAI API Mode



\### Features



\- Interactive command-line interface

\- Prompt-based image generation workflow

\- Square, landscape, and portrait formats

\- Resolution selection

\- Quality selection

\- Multiple image generation

\- Local Demo Mode without API credits

\- OpenAI API integration

\- Automatic output directory creation

\- Generated image file handling

\- Basic input validation

\- API error handling



\### Generation Modes



\#### Demo Mode



Demo Mode does not use an external AI API or require API credits.



It creates local SVG preview files based on the user's prompt and

selected resolution.



\#### OpenAI API Mode



OpenAI API Mode is designed to generate real images through the

OpenAI Images API.



A valid OpenAI API key and available API access are required.



The API key is stored locally in `.env` and is excluded from GitHub

using `.gitignore`.



\### Project Structure



```text

Generative-AI-Project-3/

│

├── image\_studio.py

├── README.md

├── .env

├── .env.example

├── .gitignore

├── requirements.txt

│

└── generated\_images/

