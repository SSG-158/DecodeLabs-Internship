\# Intelligent Code Reviewer \& Explainer



\## Project Overview



The Intelligent Code Reviewer \& Explainer is a developer utility that analyzes source code, identifies potential bugs, explains the code in plain language, and provides improvement suggestions.



This project was developed as Project 4 of the DecodeLabs Generative AI Industrial Training Kit.



\## Features



\- Supports Python, JavaScript, and Java source files

\- Loads raw source code from a file

\- Identifies potential bugs and issues

\- Provides a plain-language explanation

\- Generates a structured Markdown review

\- Provides improvement suggestions

\- Supports Demo Mode without API credits

\- Supports OpenAI API Mode for AI-powered analysis



\## Supported File Types



\- `.py`

\- `.js`

\- `.java`



\## Modes



\### Demo Mode



Demo Mode uses local rule-based checks and does not require an OpenAI API key.



It is useful for testing the project without API credits.



\### OpenAI API Mode



OpenAI API Mode sends the supplied source code to an OpenAI model for code analysis.



A valid API key and available API quota are required.



\## How to Run



Activate the virtual environment and run:



```bash

python code\_reviewer.py

