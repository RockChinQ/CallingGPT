import openai

def dalle_draw(prompt: str) -> dict:
    """
    Draw a picture from a prompt using DALL-E.

    Args:
        prompt(str): The prompt to draw from.
    """
    return openai.Image.create(
        prompt=prompt,
    )