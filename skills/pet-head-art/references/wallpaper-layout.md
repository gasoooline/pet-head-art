# Default Wallpaper Layout

Apply these defaults only when the user requests a wallpaper without specifying style, layout, dimensions, or device.

- Use a vertical `9:16` canvas at `1440 x 2560`.
- Place all approved pet-head variants as flat sticker cutouts. Use each variant at least once, then repeat variants as needed to fill the canvas.
- Scatter portraits like loose stickers on a tabletop: use irregular positions and stacking order, broad but balanced scale variation, and uneven offsets instead of rows or columns.
- Mix near-upright portraits with rotations up to about 16 degrees in either direction. Overlap neighboring portraits by roughly 25% to 45% and crop some portraits at the canvas edges.
- Keep faces readable while allowing accessories and outer silhouettes to overlap. Avoid staggered grids, repeated diagonals, deep perspective, floating 3D layers, or large blank regions.
- Before composition, isolate each intended subject as a tight transparent cutout. Use a head/headwear silhouette with nothing below the head for ordinary cat/dog heads. Without asking, retain the smallest complete set of paws/body/pose only when it is necessary for the concept to read correctly. Never add a decorative body or use a partial-neck/fragmented-body crop. Remove the background, baked outline, matte, and shadow in either mode.
- Add one medium white sticker outline directly from the transparent silhouette so it touches the fur/accessory edge with no clear or colored gap. Add one soft low-opacity neutral-gray shadow behind the outline, with a broad blur and slight downward offset. The compositor defaults are an `8px` outline, `14px` blur, `8px` vertical offset, and `48/255` opacity; adjust proportionally for unusually large canvases. Do not create a hard dark rim, glow, double border, or shadow on internal details.
- Treat automatic white-background removal as a fallback only. Inspect its edge and re-cut semantically with an image-editing capability if neck/body remnants, baked borders, shadows, or gaps remain.
- Produce only the wallpaper artwork. Never add or reproduce a clock, date, carrier name, status icons, notifications, lock-screen controls, captions, logos, or watermarks from a reference screenshot.

Run `scripts/compose_wallpaper.py --layout stack --require-alpha`. Use `--seed` to reproduce a layout or try another arrangement without regenerating portraits.
