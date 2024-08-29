---
title: "Running LLMs locally"
date: 2024-07-24T18:37:42+02:00
tags: ["tutorial", "llms"]
categories: ["Blog"]
---

Large Language Models (LLMs) are powerful tools for generating human-like text responses. You might be familiar with them through services like [ChatGPT](https://chat.openai.com/), [Anthropic Claude](https://claude.ai/), [Google Gemini](https://gemini.google.com/), and [Perplexity AI](https://www.perplexity.ai/),
Nowadays people are using them for editing purposes, writing, brainstorming, and even for generating code snippets.
When used **responsibly and critically** as a tool to assist human creativity, they can be very helpful.

Recently, I spent some time playing with these models and I found them fascinating. However, due to privacy concerns and their high environmental costs, I don't feel comfortable using cloud-based services.
This post is an account of my experience with running LLMs locally on my machines.
This can be quite straightforward, and if you have 8-16GB of RAM and a decent GPU, you can run these models on your own computer without significant issues.

All my experiments were conducted on my M1 iMac and Mac Mini, and I found the experience to be quite smooth.

I am going to describe two ways to run LLMs locally: using pre-made graphical applications and using the command line interface (CLI).
While I find more comfortable the latter, it requires a bit more setup and it can be more error-prone at first.

Before we dive in, let me clarify that I am not going to cover the ethical implications of using these models. I am not an expert on the subject, and I am not going to pretend to be one.

Moreover, be aware that you shouldn't expect answers as sophisticated as those from famous cloud-based services. The models that run on average (or even good) consumer hardware need to be greatly compressed at the expense of the quality of the response, but they are good enough for many use cases.

## The easiest way: GUIs

There are a few applications that allow you to run LLMs locally with a graphical interface. In my opinion, the nicest and easiest to use is the open source project [GPT4All](https://www.nomic.ai/gpt4all).

{{< rawhtml >}}
<p><video src="https://github.com/nomic-ai/gpt4all/assets/70534565/513a0f15-4964-4109-89e4-4f9a9011f311" controls="controls" muted="muted" style="max-height:640px; min-height: 100px; width: 100%;">
</video></p>
{{< /rawhtml >}}

Just download the installer, run it, and you are kind of ready to go.

The project itself is [well documented](https://docs.gpt4all.io/gpt4all_desktop/quickstart.html) but it can be confusing if you try to follow the steps in the video above: the first time you run the software, there is not yet any model downloaded, so you will need to download one first.
To do this, click on the `Download` button in the `Models` tab, and then select the model you want to download. This will take some time, so be patient.

Depending on the RAM and GPU you have, you can choose between different models. This is rather confusing, and very poorly explained in my opinion. It took some trial and error to find the right models for my system and one that was producing good enough answers for my use cases.

Selecting an appropriate model can be confusing due to limited documentation.
Through trial and error, I found the following models worked well:

- For systems with 16GB RAM (e.g., my iMac):
  - `Nous Hermes 2 Mistral DPO`
  - `Llama 3 Instruct`
- For systems with 8GB RAM (e.g., my Mac Mini):
  - `Gemma2`, `2b` version
  - `Phi-3 Mini Instruct`

A benchmark and comparison of the main language models in the wild can be found on the [LMSYS Chatbot Arena Leaderboard](https://chat.lmsys.org/?leaderboard), this will give you an idea of the quality of the models you can run locally.

Once the model is downloaded and installed you can head to the `Chat` tab and start chatting with the model.
At some point you may notice that responses are cut out before they are finished. This is because the tool has a limit on the length of the response it can generate.
You can change this limit in the `Settings` tab, by increasing the number of tokens in the `Maximum Response Length` option.

If for some reasons you are not happy with `GPT4All`, you can try [Msty](https://msty.app/), [Jan](https://jan.ai/) or [LMStudio](https://lmstudio.ai/).
`Jan` and `LMStudio` are also open source and some people claim also more performant than `GPT4All` with practically the same functionalities.
`Msty` is closed source but seems to be rather well designed and easy to use.
What I find nicer of the these three alternatives is that they allow to use a wider range of models, including `gemma2`, that seems to be the best performing small model for me.

## The geeky way: command line interface

This is the way I prefer to run LLMs locally.
It is more flexible and, in my opinion, more powerful than using a GUI.
And in my experiment turned out also to be more performant, about twice as fast as the GUI.

The best experience I had so far, was with the `llm` command from the [python llm library](https://github.com/simonw/llm).

Don't worry, you don't need to know how to use python to use it.
You just need to have python installed on your machine and a few steps to install the library.

To avoid messing up your system, I recommend to first install [a tool called `pipx`](https://pipx.pypa.io/stable/) that allows you to install python packages in isolated environments. You can follow the instructions of the link above or your favourite package manager to install it.

Once you have `pipx` installed, you can install the `llm` command by running the following command in your terminal:

```bash
pipx install llm
```

Before being able to chat with a model, you need to download one.
The easiest thing to do, is to install a plugin that enables support for all the `GPT4All` mofels.

You can do this by running the following command:

```bash
llm install llm-gpt4all
```

Then you can check the available models by running:

```bash
llm models
```

The model will be downloaded in the background the first time you try using it. For example, to chat with `Mini Orca` model, a rather small model from microsoft, you can run:

```bash
llm chat -m orca-mini-3b-gguf2-q4_0
```

Also in this case, if you notice that the responses are cut too short, try extending the maximum number of tokens. You can do this by running:

```bash
llm chat -m orca-mini-3b-gguf2-q4_0 -p max_length 2048
```

Have fun!

Note: the `Phi3 mini` [does not yet quite work with `llm`](https://github.com/simonw/llm-gpt4all/issues/30), although the output is often usable.
You can still try it [following the instructions here](https://huggingface.co/microsoft/Phi-3-mini-4k-instruct-gguf#how-to-use-with-llamafile), at least, that is what I have done while waiting for the fix to land :)

The `llm` library is really flexible, have a look at its documentation to get an idea of the many ways you can interact with it.

The author of this tool has a nice blog full of examples of use, and is always on top of the novelties. For example you can already use it to try [the new Llama 3.1 model](https://simonwillison.net/2024/Jul/23/llm-gguf/).
Quoting its blog post, you can install the model by running:

```bash
llm install llm-gguf
llm gguf download-model \
  https://huggingface.co/lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF/resolve/main/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf \
  --alias llama-3.1-8b-instruct --alias l31i
```

and then chat with it as we did above, runinng:

```bash
llm chat -m l31i
```

If you have few resources, you can try the very small yet very performant `gemma2` model, by running:

```bash
llm gguf download-model \
  https://huggingface.co/lmstudio-community/gemma-2-2b-it-GGUF/blob/main/gemma-2-2b-it-Q4_K_M.gguf \
  --alias gemma-2-2b-instruct --alias g2i
llm chat -m g2i
```

## The harder way: coding your own interaction

Of course you can go further in the deep hole and start coding your own ways to interact. There are a lot of ways to this, a rather immediate one (if you allow me to use this term) it to use the [Hugging Face Transformers](https://huggingface.co/transformers/) library to run LLMs locally.
While powerful, this approach requires more coding knowledge and may be overkill unless you need very specific functionality.
For complex applications you probably also want to look at the [`langchain`](https://www.langchain.com/langchain) library.

I have played a bit with this library and I found it to be very powerful and relatively easy to use, but so far I never needed the extra flexibility it provides.
It is so easy to use the `llm` command above that I don't see any reason to use this method unless you want to code your own interaction with the model.

On Apple hardware, you can squeeze a bit more power out of your system by using the [`mlx`](https://github.com/ml-explore/mlx/) library.
You can find plenty of example of use in the [`mlx-examples`](https://github.com/ml-explore/mlx-examples/) repository.
