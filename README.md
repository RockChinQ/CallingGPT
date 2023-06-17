# CallingGPT

GPT's Function Calling - the proof-of-concept.  

> Read this guide before you start: [function-calling](https://platform.openai.com/docs/guides/gpt/function-calling)

## Abstract

OpenAI's GPT models provide a function calling feature, so we can easily create `ChatGPT Plugins` like tools. This repository is a proof-of-concept of the function calling feature.  
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

Use the `example/greet.py`

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
