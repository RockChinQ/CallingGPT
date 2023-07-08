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
>>> Hello and who are you?
<<< Hello! I am an AI assistant. How can I assist you today?
>>> say hello to Rock
call<examples-greet-greet>: {
  "user": "Rock"
}
<<< Hello, Rock! How can I assist you today?
>>> and to Alice
call<examples-greet-greet>: {
  "user": "Alice"
}
<<< Hello, Alice! How can I assist you today?
>>>
```

Type `help` to get help.  
See [wiki](https://github.com/RockChinQ/CallingGPT/wiki/1.-Function-Format) for the function format.

### Other Examples

<details>
<summary>examples/draw_and_wrapper_md.py </summary>

Provides a `dalle_draw` function to use DALL·E model when user ask GPT to draw something.

```bash
python main.py examples/draw_and_wrapper_md.py 
```

```
$ python main.py examples/draw_and_wrapper_md.py 
Using module: examples.draw_and_wrapper_md
>>> hello!
<<< Hi there! How can I assist you today?
>>> draw a sunset for me please
call<examples-draw_and_wrapper_md-draw>: {
  "prompt": "sunset"
}
<<< Sure! Here's a beautiful sunset for you:

![Sunset](https://oaidalleapiprodscus.blob.core.windows.net/private/org-VS9HEpJba78GXVfOcmVo7qaM/user-OHa7Jo3kL4XJDg9lo7AzdWNT/img-QmDUiwp1IGFcu8pDGZh0i7r8.png)

I hope you like it! Let me know if there's anything else I can help you with.
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

    for reply in session.ask("your prompt"):
        # session.ask will yield each time the api returns a result,
        # before calling function, it will print the function name and args.
        # e.g. here's a function call:
        # {
        #   "role": "assistant",
        #   "content": null,
        #   "function_call": {
        #     "name": "examples-draw_and_wrapper_md-draw",
        #     "arguments": "{\n  \"prompt\": \"cat\"\n}"
        #   }
        # }
        # 
        # while here's a normal reply:
        # {
        #   "role": "assistant",
        #   "content": "Hello, I am an AI assistant. How can I assist you today?"
        # }
        print(reply)
    ```

    `Session` will automatically manage context for you.
  
See [wiki](https://github.com/RockChinQ/CallingGPT/wiki/1.-Function-Format) for the function format.
