---
title: "Running LLMs locally"
date: 2024-07-24T18:37:42+02:00
tags: ["tutorial", "llms"]
categories: ["Blog"]
---

Large Language Models, like the ones you chat with when you use [ChatGPT](https://chat.openai.com/), [Anthropic Claude](https://claude.ai/), [Google Gemini](https://gemini.google.com/), and [Perplexity AI](https://www.perplexity.ai/), are powerful tools for generating human-like text responses.
Nowadays people are using them for editing purposes, writing, brainstorming, and even for generating code snippets.
When used **responsibly and critically** as a tool to assist human creativity, they can be very helpful.

Recently I spent some time playing with these models and I found them fascinating. However, mainly because of privacy concerns and their high environmental costs, I don't feel comfortable using them on the cloud.
This post is an account of my experience with running LLMs locally on my machines. It turns out that this can be rather trivial to do, and if you have 8-16Gb of RAM and a decent GPU, you can run these models on your machine without any issues.

All my experiments were made using my M1 iMac and Mac Mini, and I found the experience to be quite smooth.

I am going to describe two ways to run LLMs locally: using pre-made graphical applications and using the command line.
Needless to say, I find more comfortable the latter, although it requires a bit more setup.

Before we move on, let me clarify that I am not going to cover the ethical implications of using these models. I am not an expert on the subject, and I am not going to pretend to be one.

Moreover, don't expect answers as good as the ones you get from the famous cloud-based services that I listed above. The models that you can run on average (or even good) consumer hardware need to be greatly compressed at the expense of the quality of the response, but they are good enough for many use cases.

## The easiest way: GUIs

There are a few applications that allow you to run LLMs locally with a graphical interface. In my opinion the nicest and easiest to use is the open source project [GPT4All](https://www.nomic.ai/gpt4all).

{{< rawhtml >}}
<p><video src="https://github.com/nomic-ai/gpt4all/assets/70534565/513a0f15-4964-4109-89e4-4f9a9011f311" controls="controls" muted="muted" style="max-height:640px; min-height: 100px; width: 100%;">
</video></p>
{{< /rawhtml >}}

Just download the installer, run it, and you are kind of ready to go.

The project itself is [well documented](https://docs.gpt4all.io/gpt4all_desktop/quickstart.html) but it can be confusing if you try to follow the steps in the video above: the first time you run the software, there is not yet any model downloaded, so you will need to download one first. To do this, click on the `Download` button in the `Models` tab, and then select the model you want to download. This will take some time, so be patient.

Depending on the RAM and GPU you have, you can choose between different models. This is rather confusing, and very poorly explained in my opinion. It took some trial and error to find the right models for my system and one that was producing good enough answers for my use cases.

So far, I had the best experiences with the models called `Nous Hermes 2 Mistral DPO` and `Llama 3 Instruct`. They both worked fine on the iMac with 16Gb of RAM but struggled on the Mac Mini with 8Gb of RAM. There I had to use `Phi-3 Mini Instruct` to get decent results at decent performances.

A benchmark and comparison of the main language models in the wild can be found on the [LMSYS Chatbot Arena Leaderboard](https://chat.lmsys.org/?leaderboard), this will give you an idea of the quality of the models you can run locally.

Once the model is downloaded and installed you can head to the `Chat` tab and start chatting with the model. At some point you may notice that responses are cut out before they are finished. This is because the tool has a limit on the length of the response it can generate. You can change this limit in the `Settings` tab, by increasing the number of tokens in the `Maximum Response Length` option.

If for some reasons you are not happy with `GPT4All`, you can try [Jan](https://jan.ai/). It is also open source and, from what I understand, more performant than `GPT4All` with practically the same functionalities.

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

The model will be downloaded in the background the first time you try using it. For example, to chat with `Phi-3 Mini` model you can run:

```bash
llm chat -m Phi-3-mini-4k-instruct
```

Also in this case, if you notice that the responses are cut too short, try extending the maximum number of tokens. You can do this by running:

```bash
llm chat -m Phi-3-mini-4k-instruct -p max_length 4096
```

Have fun!

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

## The harder way: coding your own interaction

If you are like me and you prefer to use the command line, you can use the [Hugging Face Transformers](https://huggingface.co/transformers/) library to run LLMs locally.

I have played a bit with this library and I found it to be very powerful and easy to use, but so far I never needed the extra flexibility it provides. It is so easy to use the `llm` command above that I don't see any reason to use this method unless you want to code your own interaction with the model.
