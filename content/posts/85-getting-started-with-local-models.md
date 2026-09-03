---
title: "Getting started with local LLMs"
date: 2026-09-03T23:32:31+02:00
tags: [ai, tutorials, local models, llm]
categories: ["Blog"]
draft: true
---

I was discussing options to run LLMs locally, also on low-resources systems, with a colleague today. He was looking into installing OpenClaw or something similar, making me jump on my chair to warn him.

It made me think that it could be a good time to revise the topic here, also because at this point we have very small local models whose quality is comparable or surpassing GPT-4o or Claude 3.5, and smallish one that definitely surpass them!

## Beware of the Claws

While famous for the marketing noise that it made at its release and for being acquired by OpenAI, I would strongly recommend to stay away from [OpenClaw](https://openclaw.ai/) or similar "Claws" like [NanoClaw](https://nanoclaw.dev/), [PicoClaw](https://picoclaw.io/), [Hermes Agent](https://hermes-agent.nousresearch.com/), etc.

These AI agents are meant to take control of your computer and independently perform tasks that you assign to them remotely via Telegram, Discord, Slack or some other asynchronous messenger.

Unless you know what you are doing, properly sandboxing the thing and keeping it away from machines or data you care about, this is a [recipe for disaster](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/). Below I will give you an alternative small harness that works well enough with local models, with a way to partially sandbox it, but before that let's see what is the lightest way to run local models (and still have a web interface).

## Running local models

If you look back at my post history, you see that I started with "visual" ways, ending up using AI Studio for a little bit. While it provides a simple way to run LLMs, on my constrained systems it ended up not being flexible enough and needlessly wasting resources. It is quite a while at this point that I stopped all of this and ended up using directly the engine at the core of all those products: [LLama.cpp](https://llama.app/)

I am stubborn enough to compile it from sources with my custom flags, but you can now use the installer on the page above (which also bundles a new handy single `llama` command) or you can manually download and run the executables of the latest release from <https://github.com/ggml-org/llama.cpp/releases>.

For this tutorial I am assuming some familiarity with the command line, so I'll leave it at that with the installation instruction. What matters is that once installed you can run an LLM with e.g.

```bash
llama-server --hf-repo unsloth/gemma-4-E2B-it-qat-GGUF:UD-Q4_K_XL --spec-type draft-mtp --top-k 64 --temp 1.0 --ctx-size 32768 -ngl 0 --no-mmproj
```
or
```bash
llama-cli --hf-repo LiquidAI/LFM2.5-2.6B-GGUF:Q6_K --temp 0.1 --top-k 50 --repeat-penalty 1.1 --ctx-size 32768 -ngl 99
```

Let's examine the commands above in details, starting from the command:

- `llama-server` starts an OpenAI compatible server on your computer, exposing a nice html interface for you to use as a local ChatGPT-like chate, accessible at <http://localhost:8080> by default (in the recent future this will change to <http://localhost:9931>). This is what you need if you want to use some coding agent or if you are writing your llm-aware scripts (the API is reachable at <http://localhost:8080/v1>)

- `llama-cli` is a chat-like command line interface, use it only if you are in a terminal, need to make simple experiments, and want to avoid opening a browser.

Both commands share a number of options:

- `--hf-repo` points to the GGUF file containing the model hosted on huggingface. For instance, `unsloth/gemma-4-E2B-it-qat-GGUF:UD-Q4_K_XL` refers to the model file on <https://huggingface.co/unsloth/gemma-4-E2B-it-qat-GGUF> with [quantization](https://developer.nvidia.com/blog/model-quantization-concepts-methods-and-why-it-matters/) `UD-Q4_K_XL`, and similarly for `LiquidAI/LFM2.5-2.6B-GGUF:Q6_K`. Llama.cpp will automatically download the model for you, after which you are good to go.

  I am not going to explain anything about the quantization, you are curious [A visual guide to quantization is an excellent resource to get started](https://www.maartengrootendorst.com/blog/quantization/). What matters is that a model with 2.6B parameter like LFM2.5-2.6B above requires 5.6 or even 11.2 Gb of RAM to be able to run, because each of its 2.6B parameter uses 16 or 32 bits to be stored. There are techniques to reduce the precision to approximately 8 (Q8), 6 (Q6) or 4 (Q4) bits, at the price of some quality loss but potentially huge gain in speed and memory for low resources hardware. The LFM2.5 from the example only needs 2.86Gb at Q8, 2.22Gb at Q6 and 1.67Gb at Q4. The other letters appearing in the quantization identify the type of algorithm used and which weights are shrunk.

- `--temp` (temperature), `--top-k`, `--top-p`, `--repeat-penalty` (or repetition penalty), are all parameters for the inference

- `--spec-type draft-mtp` some models, like Qwen or Gemma, have speculative decoders that help speed them up. If you want to know more look up ngram, MTP or DSpark, otherwise just try the line above, see if it works and if the speed improves (you only see improvements with good enough GPUs though)

- `--ctx-size 32768`: this is the model context, in some sense it indicates how much it remembers of the chat. The default is 4096. If you don't need long chat, keep the default since the longer the context the more additional memory you will need. While the context uses generally 32 bits for its storage, you can reduce this playing it with the `-ctv` and `-ctk` parameters. In many cases setting them both to `q8_0` reduces by 4 the amount of memory required for the context at a negligible cost, but small models can be a bit sensitive to this. You'll need some trial and error.

- `--no-mmproj`: Gemma4 E2B can also read images and audio (up to 30s), this is done using an additional small "model" saved in a mmproj file. This flag says: save the memory, I only need to operate on text. Drop it if you want to pass images or sounds to the model (provided that the model supports it of course).

- `-ngl 99`: how many layers of the model need to be offloaded on the GPU. With 0 the model runs fully on CPU, with 99 or 999 any small model will be fully loaded on GPU. It is not necessarily faster, for instance using my laptop's GPU slows the inference a lot, while on my mac mini it improves substantially.

That's it... you are good to go. There is a lot more you can experiment with to optimize the inferece or run larger models that don't fit in memory, but I think the best way to get it right, is to look at the help (which is not as helpful as it sound!) and play around with the flags.

## Which model to run?

As a rule of thumbs, you need a model that is a lot smaller than your RAM since it needs to be able to store simultaneously the (active part of the) model, its context (yes, all your messages and responses are going to take lots of space) and the rest of your running software.

I already gave away two remarkable small models above. Gemma4 E2B is very good with text (translation, summarization, manipulation of sentences, etc.) and LFM2.5 is very good with tool use and information retrieval. Both are very small and can run on a laptop with 8Gb of RAM, being fast even without a GPU.
If you have 16Gb of RAM you could try also Gemma4 E4B, with a noticeable quality improvement. For coding tasks, on a resource constrained environment, try `unsloth/Qwen3.5-4B-MTP-GGUF:Q4_K_XL`.

There are a lot of models out there, each with their strengths and weaknesses. Depending on what you need, different more specialized models may be better choices. The only way to find out is to look around in <https://huggingface.co> and try them out.

## A note about audio
speech to text

## Coding agents
nono with pi

## Largish models on low resources systems
zunzuncito for constrained systems
