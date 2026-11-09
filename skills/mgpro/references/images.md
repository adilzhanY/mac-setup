# Images: one hero across many frames, and where generated images can come from

mgpro draws everything in code by default (`rights.md`; the Bauwerk lesson: "use only drawn elements"). Generated or edited images enter a film only when the brief needs them (a character, an illustrated hero, a painted world) and the user allows it, and only through a route whose terms fit where the film goes: a published commercial needs a licence that covers commercial use. Merged from vizavi-motion (image continuity and image providers).

## Keep one hero the same

- Use one reference and editing process for one character, object or scene. Keep identity, proportions, construction, style, lighting and the key details; change only what was asked: the pose, the position, the angle or the part of the action.
- For every new pose feed **the same canonical set of references**, not just the latest regeneration with its accumulated drift. Never generate each frame as an independent look-alike with no tie to the source.
- Before generating, fix: the constant traits, the camera and shot size, the anchors, the scale, the light source, the background or alpha, and what changes in each phase.
- After generating: align anchor points, silhouette and contact; check the face and anatomy, the hands, the object's details, the perspective and the direction of light.
- Write down the real intervals in which each state appears in the film. The task sets the number of poses; an old rule of three or five poses is not a norm.
- For smooth motion it is often better to animate one consistent cutout or rig than to generate every frame independently.

## Honest about motion

- Three poses swapped are a discrete series, not a smooth rotation.
- A crop, a zoom, interpolation or a 2.5D parallax of one image is not a new pose and not a free 3D camera.
- A smooth change needs enough consistent in between states, or real geometry. Choose the method for the task and name the result honestly. Never pass off a morph through wrong anatomy as smoothness.

## Real transparency

- Make a real PNG with alpha. A painted checkerboard or a flat background is not transparency.
- Check the alpha channel (`magick hero.png -format "%[channels] %[opaque]\n" info:` must print `srgba False`), the edge on a dark and on a light backing (`magick hero.png -background black -flatten b.png`, then white), colour halos and premultiplied alpha.
- Export and scaling must not bring back a baked background or a ragged edge.

## Give the image a role

- In motion, an image is the hero, an object something touches, a layer of the space, a material, or a participant in a transformation. Tie its motion to the storyboard (`storyboard.md`). A camera gliding over a passive picture does not replace the action the storyboard promised.
- Layers and painted in hidden areas must hold up under the chosen camera. Never promise a believable new angle from data the source does not contain.

## Providers (research handed to vizavi-motion, dated 16.10.2026)

Only the documentation was checked, not whether a character really stays the same. None of this installs an integration or means there is account access. Use a tool that is already available and allowed; a new sign up, MCP server, API key or local backend is never turned on by itself. If one route is unavailable, take another, keeping the staging and stating the limits honestly.

### Krea: a ready MCP candidate

- [Official instructions](https://www.krea.ai/docs/developers/mcp), endpoint `https://api.krea.ai/mcp`.
- MCP through OAuth spends the workspace's compute units; an API token spends a **separate, paid API balance**. Do not mix the two ways of paying.
- [Pricing](https://www.krea.ai/pricing): Free gives 100 units a day without a card. The page's guide is about 25 Klein or 5 Krea 3 Beta images a day; that is **not a guaranteed number of reference edits**. Do not promise free Nano Banana or GPT Image.
- The MCP describes discovery and schemas, references by URL, base64 or upload, jobs and fetching results. Read the actual schema of the chosen tool before calling it.
- [Krea 3](https://www.krea.ai/blog/introducing-krea-3) claims up to 6 references; character stability was not tested in the research.
- A commercial licence is stated for paid plans. Treat Free as a route for personal tests and never promise it is fit for a monetised final film.
- Native alpha is not confirmed: download the result and remove the background locally if needed, checking the edge.

### Cloudflare Workers AI: a REST candidate, not a ready universal MCP

- [Pricing](https://developers.cloudflare.com/workers-ai/platform/pricing/): Free 10,000 neurons a day, reset at 00:00 UTC, no paid overage on Free; the [product page](https://www.cloudflare.com/products/workers-ai/) says no card is needed. Neurons are compute units, **not a number of finished pictures**.
- [FLUX.2 Klein 4B](https://developers.cloudflare.com/workers-ai/models/flux-2-klein-4b/), per the [schema announcement](https://developers.cloudflare.com/changelog/post/2026-01-15-flux-2-klein-4b-workers-ai/): multipart input, up to 4 binary fields `input_image_0` to `input_image_3`, each reference **smaller than 512x512**; output sizes 256 to 1920; the result comes as base64. Do not substitute another schema or another model's limits.
- The [REST API](https://developers.cloudflare.com/workers-ai/get-started/rest-api/) needs a small adapter script in a suitable client, if that is separately allowed. The general `https://mcp.cloudflare.com/mcp` was not checked for this flow; do not promise a turnkey MCP. Native alpha is not confirmed.

### Web interfaces as a fallback

- [Gemini on the web](https://support.google.com/gemini/answer/14286560?hl=en) describes reference editing and downloading; [its limits float](https://support.google.com/gemini/answer/16275805?hl=en). It is **not a free image API**; [API pricing](https://ai.google.dev/gemini-api/docs/pricing) is a separate matter. Automating it is only possible with a browser tool that is really available (in this setup browser automation is off, so the user would do it by hand); an ordinary chat does not mean a browser exists.
- [Images in ChatGPT](https://help.openai.com/en/articles/11084440-images-in-chatgpt) is a similar web fallback, including asking for transparency. ChatGPT Free does not mean a free API, and asking for transparency does not replace checking the result's alpha.

### Other options and the limits of "free"

| Option | What the docs confirm, and what not to promise |
|---|---|
| [Leonardo pricing](https://leonardo.ai/pricing) | 150 tokens a day, free work is public, the API is separate. [Image guidance](https://intercom.help/leonardo-ai/en/articles/8497988-image-guidance) is Limited. [Transparency](https://intercom.help/leonardo-ai/en/articles/9075772-transparency) is described for suitable SD1.5 and SDXL models; reference plus alpha on Free needs a real test. |
| [Ideogram plans](https://docs.ideogram.ai/plans-and-billing/available-plans.md) | 30 credits a week with a Google, Apple or Microsoft login; free work is public. Do not promise a free API. |
| [Hugging Face Inference](https://huggingface.co/docs/inference-providers/main/pricing) and [ZeroGPU Spaces](https://huggingface.co/docs/hub/main/spaces-zerogpu) | $0.10 a month in Inference; queues and quotas in Spaces. Not a reliable production backend by default. |
| [Pollinations Pollen FAQ](https://raw.githubusercontent.com/pollinations/pollinations/main/enter.pollinations.ai/POLLEN_FAQ.md) | Pollen is bought or earned. Not unlimited, not a free daily image API. |
| [Recraft Free](https://www.recraft.ai/docs/plans-and-billing/free-plan) | A limited free plan with no commercial licence; never promise a free commercial final. |
| Replicate, fal | Trials are not recurring free use. Do not list them as permanent free routes without checking the specific offer again. |

### An optional local route

[ComfyUI MCP](https://docs.comfy.org/agent-tools/mcp), a small SD1.5 with IPAdapter, and [rembg](https://github.com/danielgatis/rembg) for background removal are a separate option when a suitable environment already exists or setting one up is explicitly allowed. Never install them automatically. The research measured the standard Klein 4B at 8.4 GB of VRAM, which rules out a 6 GB card such as an RTX 3050; this machine has an RTX 5070 with 12 GB (about 11 GB usable), so it would fit, but it is still not installed without the user's go ahead.

## Say what was used

In the final reply name the provider and model actually used, the route, the date the limits were checked, and the source and its terms. These notes were written from documentation; no images were generated while preparing them.
