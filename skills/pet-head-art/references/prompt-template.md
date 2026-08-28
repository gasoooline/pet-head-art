# Prompt Template

Use this as a compact scaffold; replace bracketed fields with observations from the user's files.

```text
IDENTITY REFERENCES (the uploaded cat/dog photos) define one specific animal and are the only source of its identity. DESIGN REFERENCES define only the requested accessory and visual language; ignore any other animal shown in them.

Reconstruct the same animal in a new illustration, preserving these fixed traits: [species]; [head silhouette]; [ear size, angle, and inner-ear detail]; [eye shape, iris color/ring, and equal pupil diameter]; [exact eye spacing and height]; [nose size/color]; [wide/full muzzle and short mouth-to-chin distance]; [jaw/chin]; [coat colors, texture, and asymmetric marking boundaries]; [distinctive marks]. Do not average, symmetrize, beautify, age, or breed-shift the animal.

Add only this design: [accessory description, materials, colors, construction, attachment, and which facial areas it may cover]. Preserve distinctive irregular geometry and openings from the design reference. The accessory must not move, resize, or redraw the animal's eyes, pupils, nose, muzzle, jaw, or coat markings.

[Composition scope: head-only or body-inclusive], [front or requested angle], centered with stable margins, [background], [style]. Default ordinary cat/dog heads to head-only: isolate the natural head and headwear silhouette and show nothing below the head. Select body-inclusive without asking only when paws, body, or pose are necessary for the visual concept; retain the complete required anatomy and no more. Never add a decorative body, neck stump, or fragmented torso.

Unless another finish is requested, render the finished avatar on solid white as one naturally edged sticker portrait. Generate the white sticker edge together with the pet rather than treating it as a uniform post-process stroke. At the final delivered size, make the edge read as approximately 6px overall. Keep close to that full weight on smooth accessory contours, taper subtly around delicate hairs, and allow a few fine hairs to cross into or through the white edge. Scale the edge proportionally if the working image will be resized before delivery. Behind the finished silhouette, generate one soft neutral-gray ambient contact shadow: low opacity, broad feathering, close to and slightly stronger below the lower silhouette, with only a faint presence at the sides and almost none above. Keep the full shadow inside the canvas. Do not create an equal-width expanded mask, vector-smooth border, mechanical cutout, omnidirectional glow, double border, hard dark rim, transparent or colored gap, or outlines on facial features, fur patches, eyes, muzzle, or accessory openings. No extra animals, duplicate features, text, logo, watermark, or unrequested props. Generate one image.
```

For a wallpaper, keep the same naturally generated white edge and contact shadow, but request a transparent background instead of solid white. Preserve transparent pixels through the full soft shadow falloff, with no rectangular matte or clipped blur. Approve each finished sticker silhouette, whether head-only or body-inclusive, before arranging it. The compositor must only place the approved pixels; do not ask it to synthesize the edge or shadow and do not generate the finished collage in one model call.

## Review checklist

Compare each result against the identity photos at the same scale:

- silhouette and ear-to-head ratio
- eye shape, iris ring, pupil diameter, and eye spacing
- nose-to-muzzle distance and muzzle fullness
- jaw/chin width and coat patch boundaries
- accessory silhouette, material, openings, and attachment
- a natural white outer edge that follows fur/material detail rather than a mathematically equal-width stroke
- a soft contact shadow concentrated below the silhouette, with no clipped falloff
- no mask-expansion artifacts, gaps, double borders, hard dark rims, uniform glow, or internal outlines
- one animal only; no text, logos, or watermarks
