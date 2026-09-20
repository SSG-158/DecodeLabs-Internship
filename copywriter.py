import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
model = os.getenv("OPENAI_MODEL")

if not api_key:
    raise RuntimeError("OPENAI_API_KEY is missing from .env")

if not model:
    raise RuntimeError("OPENAI_MODEL is missing from .env")

client = OpenAI(api_key=api_key)


def generate_demo_copy(product_name, description, platform, tone):
    """Generate sample marketing copy locally without using the API."""

    if platform.lower() == "linkedin":
        return f"""
{product_name} — Smarter Learning Starts Here

{description}

Designed for students who want a more organized and personalized
learning experience.

Tone: {tone}
Platform: LinkedIn
"""

    elif platform.lower() == "instagram":
        return f"""
🚀 Meet {product_name}!

{description}

Make learning more organized, personalized, and easier to manage.

Tone: {tone}
#Education #AI #Students #Learning
"""

    elif platform.lower() == "email":
        return f"""
Subject: Discover {product_name}

Hello,

{description}

Discover a smarter way to organize your learning experience.

Best regards,
{product_name} Team
"""

    else:
        return f"""
{product_name}

{description}

Tone: {tone}
Platform: {platform}
"""


def generate_ai_copy(
    product_name,
    description,
    platform,
    tone,
    temperature,
    top_p
):
    """Generate marketing copy using the OpenAI API."""

    prompt = f"""
You are a professional marketing copywriter.

Create marketing copy for the following product.

Product Name: {product_name}
Product Description: {description}
Platform: {platform}
Tone: {tone}

Requirements:
- Adapt the writing style specifically for the selected platform.
- Match the requested tone.
- Make the copy clear, professional, and engaging.
- Do not invent technical specifications.
"""

    response = client.responses.create(
        model=model,
        input=prompt,
        temperature=temperature,
        top_p=top_p
    )

    return response.output_text


print("=" * 60)
print("       AUTOMATED COPYWRITING & TONE TRANSFORMER")
print("=" * 60)

product_name = input("Product Name: ").strip()
description = input("Product Description: ").strip()
platform = input("Platform (LinkedIn/Instagram/Email): ").strip()
tone = input("Tone (Professional/Friendly/Persuasive): ").strip()

temperature_input = input(
    "Temperature (0.0 - 2.0, default 0.7): "
).strip()

top_p_input = input(
    "Top_P (0.0 - 1.0, default 0.9): "
).strip()

temperature = float(temperature_input) if temperature_input else 0.7
top_p = float(top_p_input) if top_p_input else 0.9

if not product_name or not description or not platform or not tone:
    print("\nError: All fields are required.")

elif not 0.0 <= temperature <= 2.0:
    print("\nError: Temperature must be between 0.0 and 2.0.")

elif not 0.0 <= top_p <= 1.0:
    print("\nError: Top_P must be between 0.0 and 1.0.")

else:
    print("\nChoose generation mode:")
    print("1. Demo Mode (no API credits required)")
    print("2. OpenAI API Mode")

    mode = input("Enter choice (1/2): ").strip()

    if mode == "1":
        print("\nGenerating demo marketing copy...\n")

        result = generate_demo_copy(
            product_name,
            description,
            platform,
            tone
        )

        print("-" * 60)
        print(result)
        print("-" * 60)

    elif mode == "2":
        try:
            print("\nGenerating AI marketing copy...\n")

            result = generate_ai_copy(
                product_name,
                description,
                platform,
                tone,
                temperature,
                top_p
            )

            print("-" * 60)
            print(result)
            print("-" * 60)

        except Exception as e:
            print("\nAPI Error:", e)

    else:
        print("\nError: Please choose 1 or 2.")