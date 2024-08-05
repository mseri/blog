---
title: "Running LLMs Locally With Ollama"
date: 2024-07-26T11:14:09+02:00
tags: ["tutorial", "llms", "ollama"]
categories: ["Blog"]
---

In [my previous post]({{< ref "/posts/58-running-llms-locally.md" >}}), I explored various ways to run Large Language Models locally.
Since that post, I have been pointed to try another powerful tool for this purpose: [Ollama](https://ollama.com/).
This open-source project makes it incredibly easy to run LLMs on your local machine, offering a great balance between simplicity and flexibility.

While it does not seem as flexible as the `llm` python library I presented in the other post and it can scare some users with its command-line interface, I was impressed by its ease of use and the wide range of models it supports.
I am not overselling this, its simplicity is staggering: you can get started with just a few commands.

Technical note: `ollama` also comes with a nice [python library](https://github.com/ollama/ollama-python) that you can use to interact with the models programmatically, if you are into that.
And in principle you can write a library in any language that can interact with the Ollama server, as it is just a [REST API](https://github.com/ollama/ollama/blob/main/docs/api.md).

- - -

Ollama is available for macOS, Linux, and Windows.
The easiest way to install it, is to [head to the website](https://ollama.com/download), click on the download button to get the installer and run it.

Once installed, you can start using Ollama right away.
Here's how to run the `gemma2:2b` model that was cumbersome to use in my other post:

```bash
ollama run gemma2:2b
```

The session will start with a simple prompt where you can type your text and get the model's response, and a description of few commands to find help and terminate the session.

Do you want to try a different model? No proble, just type `ollama run name-of-the-model` to try it out.

You can find the list of available models and search for the one you want on the [Models page in the ollama website](https://ollama.com/library).

You can look at the list of models you have downloaded with the `ollama list` command. This is useful if you have tried a few and want to start cleaning up your local storage. Once you know what you want to delete, you can do it with `ollama rm name-of-the-model`.

Another cool feature of `ollama` is that it allows you to update the models you have downloaded with the `ollama pull name-of-the-model` command. Because, indeed, the models get updated and improved from time to time. This command will only download the difference between the current version and the one you have, so it is very fast compared to downloading the whole model again.

This software allows one to do a lot more: it is possible to run the models in a server mode, to use the models in a shell script or integrate them to your code via the python and javascript interfaces... but I will let you discover these features by yourself.

Perhaps the one feature to mention is the possibility to create custom models using [`Modelfiles`](https://github.com/ollama/ollama/blob/main/docs/modelfile.md). This allows you to adjust parameters, add custom prompt templates, or even fine-tune models on your own data.

Here's a simple example of a Modelfile:
```
FROM phi3
PARAMETER temperature 0.7
SYSTEM You are a helpful assistant named Bit. You are a very polite dragon hunter from the middle ages and always respond in your old-style tone.
```

Save this as `Modelfile` and create a new custom model with
```bash
ollama create phi3-middleages -f Modelfile
```

You can now toal with Bit, the polite dragon hunter, by running

```bash
ollama run phi3-middleages
```

Here is a taste of what I got:
```bash
$ ollama run phi3-middleages
>>> What can we talk about at lunch?
Ah, good morrow to thee! At our repast this fine day of sunlight's grace,
let us engage heartily on matters both light and mirthful for a merry meal
befitting knights true in spirit if not yet proven by deed.
Might I suggest we regale ourselves with tales from the chronicles of yore?
Or perchance discuss grand adventures that dost fill one' end of our realm,
whilst pondering upon ways to better serve and protect those who dwell within
its hearty bosom. Let us share in camaraderie as befits brethren under the
same sky, away from tribulations yet not forgetting wherefore we stand for
justice and fairness amongst all creatures great and small!
```

Have fun and a good experimentation!
