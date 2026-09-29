import os
import base64
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI


# ---------------------------------------------------------
# SETUP
# ---------------------------------------------------------

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")

OUTPUT_DIR = Path("generated_images")
OUTPUT_DIR.mkdir(exist_ok=True)


# ---------------------------------------------------------
# DEMO MODE
# ---------------------------------------------------------

def generate_demo_image(prompt, size, count):
    """
    Creates simple local SVG preview files.
    This mode does NOT call an AI image-generation API.
    """

    width, height = map(int, size.split("x"))

    print("\nDemo Mode selected.")
    print("Creating local visual preview files...")

    for i in range(1, count + 1):

        safe_prompt = (
            prompt.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
        )

        svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg"
width="{width}" height="{height}" viewBox="0 0 {width} {height}">

<rect width="100%" height="100%" fill="#f4f4f4"/>

<rect x="5%" y="8%" width="90%" height="84%"
rx="30" fill="white" stroke="#333333" stroke-width="3"/>

<text x="50%" y="25%"
text-anchor="middle"
font-family="Arial"
font-size="32"
font-weight="bold">
Multimodal Image Generation Studio
</text>

<text x="50%" y="45%"
text-anchor="middle"
font-family="Arial"
font-size="24">
DEMO PREVIEW
</text>

<foreignObject x="10%" y="52%" width="80%" height="30%">
<div xmlns="http://www.w3.org/1999/xhtml"
style="font-family:Arial;font-size:20px;text-align:center;">
{safe_prompt}
</div>
</foreignObject>

<text x="50%" y="88%"
text-anchor="middle"
font-family="Arial"
font-size="16">
{size} | Demo Mode
</text>

</svg>
"""

        filename = OUTPUT_DIR / f"demo_image_{i}.svg"

        with open(filename, "w", encoding="utf-8") as file:
            file.write(svg_content)

        print(f"Saved: {filename}")


# ---------------------------------------------------------
# OPENAI API MODE
# ---------------------------------------------------------

def generate_openai_images(prompt, size, count, quality):
    """
    Generates real images using the OpenAI Images API.
    """

    if not API_KEY or API_KEY == "replace_with_your_api_key":
        print("\nNo valid OpenAI API key was found.")
        print("Please use Demo Mode or configure your API key.")
        return

    try:
        client = OpenAI(api_key=API_KEY)

        print("\nConnecting to OpenAI Image Generation API...")
        print("Please wait...")

        response = client.images.generate(
            model="gpt-image-2",
            prompt=prompt,
            size=size,
            quality=quality,
            n=count
        )

        for i, image_data in enumerate(response.data, start=1):

            if getattr(image_data, "b64_json", None):

                image_bytes = base64.b64decode(image_data.b64_json)

                filename = OUTPUT_DIR / f"generated_image_{i}.png"

                with open(filename, "wb") as file:
                    file.write(image_bytes)

                print(f"Saved: {filename}")

            elif getattr(image_data, "url", None):

                print(f"Generated image URL: {image_data.url}")

        print("\nImage generation completed successfully.")

    except Exception as error:

        print("\nImage generation failed.")
        print(f"Error: {error}")

        print("\nYou can still run the project using Demo Mode.")


# ---------------------------------------------------------
# INPUT VALIDATION
# ---------------------------------------------------------

def get_choice(message, choices):

    while True:

        print(message)

        for number, option in enumerate(choices, start=1):
            print(f"{number}. {option}")

        choice = input("Enter choice: ").strip()

        if choice.isdigit():

            number = int(choice)

            if 1 <= number <= len(choices):
                return choices[number - 1]

        print("Invalid choice. Please try again.\n")


def get_count():

    while True:

        value = input("Number of images (1-3): ").strip()

        if value.isdigit():

            count = int(value)

            if 1 <= count <= 3:
                return count

        print("Please enter a number between 1 and 3.")


# ---------------------------------------------------------
# MAIN APPLICATION
# ---------------------------------------------------------

def main():

    print("=" * 60)
    print("       MULTIMODAL IMAGE GENERATION STUDIO")
    print("=" * 60)

    print("\nThis application converts natural-language prompts")
    print("into image-generation requests.")

    # -----------------------------------------------------
    # MODE
    # -----------------------------------------------------

    mode = get_choice(
        "\nSelect Generation Mode:",
        [
            "Demo Mode - No API credits required",
            "OpenAI API Mode - Real AI image generation"
        ]
    )

    # -----------------------------------------------------
    # PROMPT
    # -----------------------------------------------------

    prompt = input(
        "\nEnter your image description:\n> "
    ).strip()

    while not prompt:

        print("Prompt cannot be empty.")

        prompt = input(
            "Enter your image description:\n> "
        ).strip()

    # -----------------------------------------------------
    # ASPECT RATIO
    # -----------------------------------------------------

    ratio = get_choice(
        "\nSelect Aspect Ratio:",
        [
            "Square (1:1)",
            "Landscape (3:2)",
            "Portrait (2:3)"
        ]
    )

    size_map = {
        "Square (1:1)": "1024x1024",
        "Landscape (3:2)": "1536x1024",
        "Portrait (2:3)": "1024x1536"
    }

    size = size_map[ratio]

    # -----------------------------------------------------
    # QUALITY
    # -----------------------------------------------------

    quality = get_choice(
        "\nSelect Image Quality:",
        [
            "low",
            "medium",
            "high"
        ]
    )

    # -----------------------------------------------------
    # GENERATION COUNT
    # -----------------------------------------------------

    count = get_count()

    # -----------------------------------------------------
    # SHOW SETTINGS
    # -----------------------------------------------------

    print("\n" + "=" * 60)
    print("GENERATION SETTINGS")
    print("=" * 60)

    print(f"Prompt       : {prompt}")
    print(f"Aspect Ratio : {ratio}")
    print(f"Resolution   : {size}")
    print(f"Quality      : {quality}")
    print(f"Image Count  : {count}")
    print(f"Mode         : {mode}")

    print("=" * 60)

    # -----------------------------------------------------
    # GENERATE
    # -----------------------------------------------------

    if mode.startswith("Demo"):

        generate_demo_image(
            prompt,
            size,
            count
        )

    else:

        generate_openai_images(
            prompt,
            size,
            count,
            quality
        )

    print("\n" + "=" * 60)
    print("PROJECT COMPLETE")
    print(f"Output folder: {OUTPUT_DIR.absolute()}")
    print("=" * 60)


# ---------------------------------------------------------
# PROGRAM ENTRY
# ---------------------------------------------------------

if __name__ == "__main__":
    main()