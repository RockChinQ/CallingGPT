# CallingGPT

[English](README.md) | 简体中文

[![PyPi](https://img.shields.io/pypi/v/CallingGPT.svg)](https://pypi.python.org/pypi/CallingGPT)

OpenAI GPT接口的函数调用功能演示，一个自托管的类ChatGPT Plugin平台的实验。

> 建议您先阅读: [function-calling](https://platform.openai.com/docs/guides/gpt/function-calling)

## 摘要

OpenAI的GPT模型提供了函数调用功能，因此我们可以轻松地创建`类ChatGPT Plugin`的工具。本存储库是函数调用功能的概念验证以及基本封装。

在这个实验中，我们将`Plugin`定义为包含一系列函数的`Namespace`。当用户进行对话时，API将调用`Namespace`中的函数，并将结果返回给用户。

## 用法

1. 克隆此存储库并安装依赖项。

    ```bash
    git clone https://github.com/RockChinQ/CallingGPT
    cd CallingGPT
    pip install -r requirements.txt
    ```

2. 运行`main.py`以生成`config.yaml`

    ```bash
    python main.py
    ```

3. 编辑`config.yaml`以设置您的`api_key`和其他设置。
4. 运行`main.py`并传递您的模块。

    ```bash
    python main.py <module0> <module1> ...
    ```

## 示例

使用`example/greet.py`，提供一个`greet`函数，当用户要求GPT向某人打招呼时调用。

```bash
python main.py example/greet.py
```

然后您可以与机器人交谈。

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

输入`help`以获取帮助。  
有关函数格式，请参见[wiki](https://github.com/RockChinQ/CallingGPT/wiki/1.-Function-Format)

### 更多示例

<details>
<summary>examples/draw_and_wrapper_md.py </summary>

提供一个`dalle_draw`函数，当用户要求GPT画画时，使用DALL·E模型。

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

## 代码调用

1. 安装包

    ```bash
    pip install --upgrade CallingGPT
    ```

2. 编写模块（亦可用于CLI模式）

    ```python
    # your_module_a.py
    def func_a(prompt: str) -> str:  # 每个参数和函数返回值的类型提示是必需的
        """
        The description of this func a, will be provided to the api.

        Args:
            prompt(str): The prompt of the function.

        Returns:
            The result of the function.
        """
        # 必须使用Google风格的docstring，它将被分割为`description`和`params`(如果有参数则必需)和`returns`(可选)，每个部分之间用`\n\n`分隔。
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
        # docstring中的参数类型提示是可选的
        return a + b
    ```

3. 调用

    ```python
    from CallingGPT.session.session import Session
    import your_module_a, your_module_b
    import openai

    openai.api_key = 'your_openai_api_key'

    session = Session([your_module_a, your_module_b])

    for reply in session.ask("your prompt"):
        # session.ask将在api返回结果时每次产生一个返回值
        # 在调用函数之前，它将打印函数名和参数。
        # 例如，这是一个函数调用：
        # {
        #   "role": "assistant",
        #   "content": null,
        #   "function_call": {
        #     "name": "examples-draw_and_wrapper_md-draw",
        #     "arguments": "{\n  \"prompt\": \"cat\"\n}"
        #   }
        # }
        #
        # 而这是一个普通的回复：
        # {
        #   "role": "assistant",
        #   "content": "Hello, I am an AI assistant. How can I assist you today?"
        # }
        print(reply)
    ```

    `Session`将自动为您管理上下文。

查看[wiki](https://github.com/RockChinQ/CallingGPT/wiki/1.-Function-Format)以获取更多信息。