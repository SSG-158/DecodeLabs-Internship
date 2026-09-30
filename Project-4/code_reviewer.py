import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI


# Load environment variables
load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = os.getenv("OPENAI_MODEL", "gpt-5.6-luna")


# ---------------------------------------------------------
# DEMO MODE
# ---------------------------------------------------------

def demo_review(code, filename):

    bugs = []

    if "print(" in code:
        bugs.append(
            "Review point: print() statements are present. "
            "Consider using logging in production applications."
        )

    if "except:" in code:
        bugs.append(
            "Potential issue: a bare except statement can hide "
            "unexpected errors. Use specific exception types."
        )

    if "/ len(" in code:
        bugs.append(
            "Potential issue: dividing by len() may cause a "
            "ZeroDivisionError when the collection is empty."
        )

    if not bugs:
        bugs.append(
            "No obvious demonstration-level issues were detected."
        )

    bug_report = "\n".join(
        f"{index}. {bug}"
        for index, bug in enumerate(bugs, start=1)
    )

    language = Path(filename).suffix.lower().replace(".", "")

    result = (
        "# Intelligent Code Reviewer & Explainer\n\n"
        f"## File\n`{filename}`\n\n"
        "## Bug Report\n\n"
        f"{bug_report}\n\n"
        "## Plain-Language Explanation\n\n"
        "This program was reviewed using Demo Mode. "
        "The code is analyzed using local rule-based checks "
        "rather than an external AI model.\n\n"
        "## Optimized Code\n\n"
        f"```{language}\n"
        f"{code}\n"
        "```\n\n"
        "## Improvement Suggestions\n\n"
        "• Add input validation where required.\n"
        "• Handle possible runtime errors.\n"
        "• Use clear variable and function names.\n"
        "• Consider logging instead of print() for production code.\n\n"
        "## Review Status\n\n"
        "Demo review completed successfully.\n"
    )

    return result


# ---------------------------------------------------------
# OPENAI API MODE
# ---------------------------------------------------------

def ai_review(code, filename):

    if not API_KEY or API_KEY == "replace_with_your_api_key":
        return (
            "No valid OpenAI API key was found.\n"
            "Please use Demo Mode or configure your API key."
        )

    client = OpenAI(api_key=API_KEY)

    system_instruction = (
        "You are an expert software code reviewer.\n\n"
        "Analyze the supplied source code carefully.\n\n"
        "Return your response using exactly these Markdown sections:\n\n"
        "# Intelligent Code Reviewer & Explainer\n\n"
        "## Bug Report\n"
        "Identify bugs, errors, logical problems, and important risks. "
        "For each issue, explain why it is a problem.\n\n"
        "## Plain-Language Explanation\n"
        "Explain what the program does in simple language.\n\n"
        "## Optimized Code\n"
        "Provide a corrected and improved version of the code.\n\n"
        "## Improvement Suggestions\n"
        "Give practical suggestions for readability, maintainability, "
        "performance, and error handling.\n\n"
        "Use Markdown formatting. "
        "Put the optimized code inside a fenced code block. "
        "Do not invent bugs that are not supported by the supplied code."
    )

    user_prompt = (
        f"Filename: {filename}\n\n"
        "Source code:\n\n"
        f"{code}"
    )

    try:

        response = client.responses.create(
            model=MODEL,
            instructions=system_instruction,
            input=user_prompt
        )

        return response.output_text

    except Exception as error:

        return (
            "# API Error\n\n"
            "The OpenAI API request could not be completed.\n\n"
            f"Error: {error}\n\n"
            "You can continue testing the project using Demo Mode."
        )


# ---------------------------------------------------------
# FILE READING
# ---------------------------------------------------------

def read_code_file(filename):

    path = Path(filename)

    supported_extensions = {
        ".py",
        ".js",
        ".java"
    }

    if not path.exists():
        raise FileNotFoundError(
            f"File not found: {filename}"
        )

    if path.suffix.lower() not in supported_extensions:
        raise ValueError(
            "Unsupported file type. "
            "Please use a .py, .js, or .java file."
        )

    return path.read_text(encoding="utf-8")


# ---------------------------------------------------------
# MAIN PROGRAM
# ---------------------------------------------------------

def main():

    print("=" * 60)
    print("       INTELLIGENT CODE REVIEWER & EXPLAINER")
    print("=" * 60)

    print("\nGeneration Mode:")
    print("1. Demo Mode - No API credits required")
    print("2. OpenAI API Mode - AI-powered code review")

    mode = input("\nChoose mode (1 or 2): ").strip()

    if mode not in {"1", "2"}:
        print("Invalid choice.")
        return

    print("\nSupported files: .py, .js, .java")

    filename = input(
        "Enter the path of the code file: "
    ).strip()

    try:

        code = read_code_file(filename)

        print("\n" + "=" * 60)
        print("CODE LOADED SUCCESSFULLY")
        print("=" * 60)

        print(f"File: {filename}")
        print(f"Characters: {len(code)}")

        print("\nAnalyzing code...")

        if mode == "1":

            result = demo_review(
                code,
                Path(filename).name
            )

        else:

            result = ai_review(
                code,
                Path(filename).name
            )

        print("\n" + "=" * 60)
        print("REVIEW RESULT")
        print("=" * 60)

        print(result)

    except FileNotFoundError as error:

        print(f"\nError: {error}")

    except ValueError as error:

        print(f"\nError: {error}")

    except UnicodeDecodeError:

        print(
            "\nError: Could not read the file as UTF-8 text."
        )

    except Exception as error:

        print(
            f"\nUnexpected error: {error}"
        )


# ---------------------------------------------------------
# PROGRAM START
# ---------------------------------------------------------

if __name__ == "__main__":
    main()