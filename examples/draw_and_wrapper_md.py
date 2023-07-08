import openai


def draw(prompt: str) -> dict:
    """
    Draw a picture from a prompt using DALL-E.

    Args:
        prompt(str): The prompt to draw from.
    """
    return openai.Image.create(
        prompt=prompt,
    )

def output_img_as_md(img: str) -> str:
    """
    Output an image as Markdown.

    Args:
        img(str): The image to output.
    """
    return "![Generated Image]({})".format(img)

__functions__ = [
    draw,
    output_img_as_md
]
