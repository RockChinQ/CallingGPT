# CallingGPT

[![PyPi](https://img.shields.io/pypi/v/CallingGPT.svg)](https://pypi.python.org/pypi/CallingGPT)

GPT's Function Calling Demo, a experiment of self-hosted ChatGPT-Plugins-like platform.

> Recommend reading: [function-calling](https://platform.openai.com/docs/guides/gpt/function-calling)

## Abstract

OpenAI's GPT models provide a function calling feature, so we can easily create `ChatGPT-Plugins-like` tools. This repository is a proof-of-concept of the function calling feature.  
In this experiment, we defined the `Plugin` as `Namespace` which contains a serial of functions. While user performing a conversation, the functions in `Namespace` will be called by the API and return the result to the user.

## Usage

1. Clone this repository and install the dependencies.

    ```bash
    git clone https://github.com/RockChinQ/CallingGPT
    cd CallingGPT
    pip install -r requirements.txt
    ```

2. Run the `main.py` to generate `config.yaml`

    ```bash
    python main.py
    ```

3. Edit the `config.yaml` to set your API key and other settings.
4. Run the `main.py` and pass your modules.

    ```bash
    python main.py <module0> <module1> ...
    ```

## Example

Use the `example/greet.py`, provides a `greet` function called when user ask GPT to greet someone.

```bash
python main.py example/greet.py
```

Then you can talk to the bot.

```
$ python main.py examples/greet.py 
Using module: examples.greet
>>> hello and who are you?              
<<< Hello! I am an AI assistant here to help you. How may I assist you today?
>>> say hello to Rock
func<examples.greet.greet>: Hello, Rock!
>>> and to Alice
func<examples.greet.greet>: Hello, Alice!
>>> 
```

Type `help` to get help.

### Other Examples

<details>
<summary>examples/draw.py</summary>

Provides a `dalle_draw` function to use DALL·E model when user ask GPT to draw something.

```bash
python main.py examples/draw.py
```

```
$ python main.py examples/draw.py 
Using module: examples.draw
>>> draw cars heading home under the sunset
func<examples.draw.dalle_draw>: {
  "created": 1687098971,
  "data": [
    {
      "url": "https://oaidalleapiprodscus.blob.core.windows.net/private/org-VS9HEpJba78GXVfOcmVo7qaM/user-OHa7Jo3kL4XJDg9lo7AzdWNT/img-eAwt4YgHn6ed1cr96MoRWs0d.png?st=2023-06-18T13%3A36%3A11Z&se=2023-06-18T15%3A36%3A11Z&sp=r&sv=2021-08-06&sr=b&rscd=inline&rsct=image/png&skoid=6aaadede-4fb3-4698-a8f6-684d7786b067&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2023-06-17T20%3A54%3A10Z&ske=2023-06-18T20%3A54%3A10Z&sks=b&skv=2021-08-06&sig=ZY4DTE1fYPyT7/jYBLJLuAgxpNuPsOhjbid1CWTyfKo%3D"
    }
  ]
}
>>>
```

</details>

## For Code

1. Install the package

    ```bash
    pip install --upgrade CallingGPT
    ```

2. Create your own functions in modules(these modules can also be used in the CLI mode)

    ```python
    # your_module_a.py
    def func_a(prompt: str) -> str:  # Type hint of EACH argument and return value is REQUIRED.
        """
        The description of this func a, will be provided to the api.

        Args:
            prompt(str): The prompt of the function.

        Returns:
            The result of the function.
        """
        # Google style docstring is REQUIRED, it will be split into
        # `description` and `params`(required if there are args) and 
        # `returns`(optional), `\n\n` between each part.
        return "func_a: " + prompt
    ```

    ```python
    # your_module_b.py
    def adder(a: int, b: int) -> int:
        """
        Add two numbers.

        Args:
            a: The first number.
            b: The second number.

        Returns:
            The sum of a and b.
        """
        # Type hints of args in docstring is optional.
        return a + b
    ```

3. Call the wrapper

    ```python
    from CallingGPT.session.session import Session
    import your_module_a, your_module_b
    import openai

    openai.api_key = 'your_openai_api_key'

    session = Session([your_module_a, your_module_b])

    session.ask("your prompt")
    ```

    `Session` will automatically manage context for you.
