# Prompt Template

Use this as a compact scaffold; replace bracketed fields with observations from the user's files.

```text
IDENTITY REFERENCES (the uploaded cat/dog photos) define one specific animal and are the only source of its identity. DESIGN REFERENCES define only the requested accessory and visual language; ignore any other animal shown in them.

Reconstruct the same animal in a new illustration, preserving these fixed traits: [species]; [head silhouette]; [ear size, angle, and inner-ear detail]; [eye shape, iris color/ring, and equal pupil diameter]; [exact eye spacing and height]; [nose size/color]; [wide/full muzzle and short mouth-to-chin distance]; [jaw/chin]; [coat colors, texture, and asymmetric marking boundaries]; [distinctive marks]. Do not average, symmetrize, beautify, age, or breed-shift the animal.

Add only this design: [accessory description, materials, colors, construction, attachment, and which facial areas it may cover]. Preserve distinctive irregular geometry and openings from the design reference. The accessory must not move, resize, or redraw the animal's eyes, pupils, nose, muzzle, jaw, or coat markings.

[Composition scope: head-only or body-inclusive], [front or requested angle], centered with stable margins, [background], [outline/shadow/style]. Default ordinary cat/dog heads to head-only: isolate the natural head and headwear silhouette and show nothing below the head. Select body-inclusive without asking only when paws, body, or pose are necessary for the visual concept; retain the complete required anatomy and no more. Never add a decorative body, neck stump, or fragmented torso. No extra animals, duplicate features, text, logo, watermark, or unrequested props. Generate one image.
```

For a wallpaper, use this template for each tile and request a tightly cropped transparent cutout with no outline, matte, shadow, or surrounding whitespace. Approve the intended subject silhouette, whether head-only or body-inclusive, then let the compositor add a gapless white outline from the alpha edge. Do not generate the finished collage in one model call.

## Review checklist

Compare each result against the identity photos at the same scale:

- silhouette and ear-to-head ratio
- eye shape, iris ring, pupil diameter, and eye spacing
- nose-to-muzzle distance and muzzle fullness
- jaw/chin width and coat patch boundaries
- accessory silhouette, material, openings, and attachment
- one animal only; no text, logos, or watermarks
