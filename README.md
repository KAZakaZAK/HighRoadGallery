# High Road Gallery & Studios: redesign proof of concept

Static, framework-free PoC. Mobile first at 360px, dark mode, 8px grid, WCAG AA or better.

## Deploy to GitHub Pages
1. Create a repo and push the contents of this folder to the root of `main`.
2. Settings > Pages > Source: Deploy from a branch > `main` / root.
3. Open `https://<user>.github.io/<repo>/` on a phone. All paths are relative, so project sites work.

## Structure
- `index.html` homepage
- `assets/css/tokens.css` design tokens (mirror these as Figma Variables)
- `assets/css/styles.css` layout and components
- `assets/js/main.js` menu drawer and service worker registration
- `sw.js`, `manifest.webmanifest`, `assets/icons/` PWA files
- `docs/design-tokens.json` token export for Figma variable import plugins

## Notes
- Logo and hero photo are hotlinked from the client's Squarespace CDN. Swap in a transparent SVG logo at `assets/img/` when available.
- Fonts (Cormorant Garamond, Work Sans) are both in the Squarespace font library.
- All page links point to the live site so the PoC can be tapped through.
- After editing cached files, bump `CACHE` in `sw.js`.
