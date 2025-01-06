# auto-reel-edit

Enhance your 9:16 reels with Sieve! Replace backgrounds seamlessly and add captivating captions to make your reels stand out.

This Sieve pipeline transforms a 9:16 reel into an eye-catching, captioned video optimized for maximum engagement. It includes the following steps:

1. Replace the original background with a abstract video or image using [background-removal](https://www.sievedata.com/functions/sieve/background-removal) Sieve function.
2. Automatically generate transcript for the video using [transcribe](https://www.sievedata.com/functions/sieve/transcribe) Sieve function.
3. Utilize the transcript to caption the video using [remotion](https://www.remotion.dev) framework.

## Tutorial

A detailed explanation of the pipeline is provided in this [tutorial](https://www.sievedata.com).

## Options

* `file`: The 9:16 reel for editing.
* `subtitle_type`: The different types of styles available for captions.
* `background_media`: The image or video to be used as background.

## Deploying `auto-reel-edit` to your own Sieve account

First ensure you have the Sieve Python SDK installed: `pip install sievedata` and set `SIEVE_API_KEY` to your Sieve API key.
You can find your API key at [https://www.sievedata.com/dashboard/settings](https://www.sievedata.com/dashboard/settings).

Then deploy the function to your account:

```bash
git clone https://github.com/sieve-community/auto-reel-edit
cd auto-reel-edit
sieve deploy pipeline.py
```

You can now find the function in your Sieve account and call it via API or SDK.
