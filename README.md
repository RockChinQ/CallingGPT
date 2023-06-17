# CallingGPT

GPT's Function Calling - the proof-of-concept

## Abstract

OpenAI's GPT models provide a function calling feature, so we can easily create `ChatGPT Plugins` like tools. This repository is a proof-of-concept of the function calling feature.  
In this experiment, we defined the `Plugin` as `Namespace` which contains a serial of functions. While user performing a conversation, the functions in `Namespace` will be called by the API and return the result to the user.
