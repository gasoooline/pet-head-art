# Default Wallpaper Layout

Apply these defaults only when the user requests a wallpaper without specifying style, layout, dimensions, or device.

- Use a vertical `9:16` canvas at `1440 x 2560`.
- Place all approved pet-head variants as flat sticker cutouts. Use each variant at least once, then repeat variants as needed to fill the canvas.
- Scatter portraits like loose stickers on a tabletop: use irregular positions and stacking order, broad but balanced scale variation, and uneven offsets instead of rows or columns.
- Mix near-upright portraits with rotations up to about 16 degrees in either direction. Overlap neighboring portraits by roughly 25% to 45% and crop some portraits at the canvas edges.
- Keep faces readable while allowing accessories and outer silhouettes to overlap. Avoid staggered grids, repeated diagonals, deep perspective, floating 3D layers, or large blank regions.
- Before composition, generate each intended subject as a finished transparent sticker cutout. Use a head/headwear silhouette with nothing below the head for ordinary cat/dog heads. Without asking, retain the smallest complete set of paws/body/pose only when it is necessary for the concept to read correctly. Never add a decorative body or use a partial-neck/fragmented-body crop.
- Generate the natural white sticker edge and soft contact shadow with each portrait before composition. At each portrait's intended final display scale, target an optical edge width of about `6px`; keep that weight on smooth accessory contours while allowing natural tapering around fine fur. Never use an equal-width expanded mask. Keep the shadow low-opacity, broadly feathered, slightly downward biased, and fully preserved in transparent pixels. The compositor must add neither effect.
- Require true transparency for wallpaper assets. If semantic background removal is necessary, preserve the generated white edge, fine hairs, and complete shadow falloff; reject rectangular mattes, clipped blur, neck/body remnants, gaps, or mask-expansion artifacts.
- Produce only the wallpaper artwork. Never add or reproduce a clock, date, carrier name, status icons, notifications, lock-screen controls, captions, logos, or watermarks from a reference screenshot.

Run `scripts/compose_wallpaper.py --layout stack --require-alpha`. Use `--seed` to reproduce a layout or try another arrangement without regenerating portraits. The script only arranges approved sticker pixels.
