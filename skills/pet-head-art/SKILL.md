---
name: pet-head-art
description: Generate a pet-head avatar or wallpaper from user-provided cat or dog photos while preserving the same animal's face, coat pattern, eyes, pupils, muzzle, ears, and proportions. Use with any agent's available reference-image-capable generator; no specific model or provider is required. Trigger for pet avatars, animal stickers, accessory-wearing portraits, themed cat/dog heads, or wallpapers assembled from such portraits.
---

# Pet Head Art

Apply this provider-neutral identity-locking workflow with the best image-generation or image-editing capability already available to the current agent.

## Select a generation capability

1. Prefer the host's native image generation/editing capability when it accepts reference images.
2. Otherwise use an already connected image tool that supports image-to-image or multiple reference images.
3. Use a provider-specific skill, API, or credential only when the user explicitly selects that provider. Do not install a provider, request an API key, reuse a generic credential, or redirect credentials to another service merely to run this skill.
4. If no tool accepts reference images, explain that identity consistency will be weaker, build the identity lock from the photos, and generate only one pilot before proceeding.

Do not hard-code a model name, endpoint, SDK, or credential convention. Translate the provider-neutral prompt in [references/prompt-template.md](references/prompt-template.md) into the selected tool's normal reference-image interface.

## Input and output

- Accept one or more clear photos of the same cat or dog as **identity references**. Ask for another photo only when the face is substantially occluded, tiny, or inconsistent across uploads.
- Accept optional accessory/style images or a text description. Treat these as **design references only**; never use another animal's face, markings, or body as identity.
- Default output: one centered 1:1 head avatar on a clean white background, high resolution, no text/logo/watermark. Generate the pet, accessory, natural white sticker edge, and soft contact shadow together as one finished image. Target an optical white-edge width of about `6px` at the final delivered size. Keep that weight clear along smooth accessory contours, but allow subtle tapering and a few fine hairs to cross into or through the edge so it never reads as a geometrically uniform stroke. Scale the target proportionally when generating above or below the final delivery resolution. Use one low-opacity neutral-gray contact shadow that is diffuse, close to the lower silhouette, and slightly downward biased; keep it faint or absent along the top edge. Never simulate this finish with an equal-width expanded mask, vector stroke, hard cutout, uniform halo, or post-processing script. In head-only mode, isolate the natural head and headwear silhouette without leaving an exposed neck or partial torso. Change background color, aspect ratio, transparency, or the default sticker finish only when requested.
- For an ordinary cat-head or dog-head image, show nothing below the head. Independently allow the smallest coherent amount of paws or body only when the visual concept needs them to read correctly, such as holding an object, sitting in a container, or performing an action. Do not require an explicit user request for this exception, but do not add a body decoratively. Never leave only a neck stump or fragmented torso.
- For a wallpaper, generate each approved subject as an individually finished transparent sticker cutout that already includes the natural white edge and soft contact shadow. The cutout may be head-only or intentionally body-inclusive. Keep transparent pixels beyond the complete shadow falloff, with no opaque canvas, rectangular matte, or clipped blur. The compositor must preserve these pixels and only arrange the stickers; it must not create or replace the edge or shadow.

## Workflow

1. **Separate the references.** Label pet photos `IDENTITY` and accessory/style images `DESIGN`. If a prior generated image is supplied, use it only as a style/acceptance reference unless the user explicitly says it is the canonical pet photo.
2. **Build an identity lock.** Inspect all identity photos and write a compact, concrete descriptor: species, head silhouette, ear size/angle, eye shape and iris/pupil proportions, eye spacing, nose and muzzle width, jaw/chin, coat colors and asymmetric boundaries, fur length/texture, and distinctive marks. Resolve conflicts by trusting repeated traits in unobstructed photos; do not average away asymmetry.
3. **Define the design and scope.** Describe the requested accessory, material, attachment/occlusion, palette, and line/outline language. Choose `head-only` for ordinary pet-head images. Choose `body-inclusive` without asking only when paws, body, or pose are necessary to communicate the concept; include the complete required anatomy and no more. Preserve recognizable construction details (for example, irregular torn openings or a tied top) instead of replacing them with generic masks. Unless the user requests another finish, generate the natural white sticker edge and soft contact shadow as part of the image around the complete outer silhouette only. See [references/prompt-template.md](references/prompt-template.md).
4. **Calibrate before batching.** Generate one 1:1 pilot with the identity lock and design reference. Check eye size and equal pupils, eye distance, muzzle fullness, nose size, ear silhouette, coat boundaries, and accessory geometry. If any fail, revise the prompt/references and regenerate the pilot.
5. **Generate variants separately.** For each accessory, send the same identity photos and identity lock again; send only the relevant design references. Request one image per call. Never use a different generated variant as the pet's identity source.
6. **Quality gate.** Reject any result with a pointed/narrow muzzle, changed eye or pupil proportions, shifted coat patches, extra animals/limbs, missing accessory-defining features, or text/logos. In head-only mode, reject exposed necks and partial torsos; in body-inclusive mode, require a coherent pose and complete intended anatomy. Inspect the finish at final display size and zoomed in: the white edge should read as approximately `6px` overall while responding naturally to fur and material contours, with occasional fine hairs crossing it, and the soft shadow should concentrate below the silhouette. Reject borders that read materially thinner or thicker than the target, perfectly equal-width or vector-smooth borders, jagged mask expansion, gray/color gaps, double borders, omnidirectional glow, hard dark shadows, internal facial outlines, or clipped effects. For wallpaper assets, also reject opaque or rectangular backgrounds and require transparent pixels through the full shadow falloff. Regenerate only the failed item.
7. **Deliver.** Return the approved avatar(s). For a wallpaper, use the compositor below, preserving each approved portrait as pixels; report the final dimensions and file path.

## Privacy and credentials

- Treat pet photos as user content. Use only the files the user supplied for this task.
- Before sending images to a non-native external service that the user did not already select, identify the destination and obtain confirmation.
- Never place API keys in prompts, Skill files, output metadata, logs, or command arguments. Never treat a general-purpose credential as valid for a different provider.
- Keep temporary references and generated artifacts within the task's approved workspace or output location.

## Prompt rules

- State that identity photos define the animal and design images define only the accessory/style.
- Say “reconstruct the same animal” rather than “copy/paste/cut out the face”; avoid face-swapping language.
- Lock geometry, not just breed or color: explicitly mention equal pupil diameter, fixed eye spacing, muzzle width, jaw length, ear proportions, and asymmetric markings.
- Keep ordinary pet-head compositions constrained to one head with nothing below it. Add paws/body only when they are functionally necessary to the concept, and keep the resulting pose coherent.
- Generate the white edge and contact shadow once around the combined pet/accessory silhouette, never around eyes, muzzle, individual fur patches, or accessory openings. Describe this as part of the intended image, not as a later filter or scripted effect, and keep enough canvas margin that the shadow is not clipped.
- Ask for an identity-preserving redraw for each item, but use deterministic compositing for the final wallpaper.

## Wallpaper assembly

When the user specifies a wallpaper style, follow it. When the user gives no style or layout direction, use the dense flat-stack default in [references/wallpaper-layout.md](references/wallpaper-layout.md): vertical 9:16, overlapping sticker portraits, minimal empty space, and no clock, date, status bar, controls, text, logo, or watermark.

After every tile passes the quality gate, run the default stack layout:

```bash
python <skill-directory>/scripts/compose_wallpaper.py \
  --input approved/a.png approved/b.png approved/c.png \
  --output wallpaper.png --layout stack --require-alpha \
  --width 1440 --height 2560
```

Use `--layout grid` only when the user requests an orderly grid. Provide only approved transparent sticker cutouts whose natural edges and shadows are already complete. The compositor repeats inputs as needed for dense coverage, preserves each tile as pixels, and never redraws the pet or adds a procedural border.
