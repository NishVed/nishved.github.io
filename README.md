# nishved.github.io

Personal site of Nishanth Veduruvada — AI, Security & Systems Architect.
Built with [Hugo](https://gohugo.io/) and the
[PaperMod](https://github.com/adityatelange/hugo-PaperMod/) theme, deployed to
GitHub Pages by `.github/workflows/hugo.yaml`.

## Local development

```sh
git submodule update --init --recursive   # PaperMod lives in themes/
hugo server
```

## Site icons

The favicon and apple-touch icon are generated from `assets/img/portrait.jpg`:

```sh
python3 tools/make-favicon.py
```

Icons need a much harder levels curve than the on-page portrait — a dim
photograph of a face is unreadable at 16px without it — so the two are
produced separately from the same source. Bump `VERSION` in that script when
the image changes: Chrome caches favicons by URL and will not re-fetch an
unchanged path.

## Theme overrides

`layouts/_partials/footer.html` is a fork of the PaperMod partial. Only the
visible `<footer>` element differs; the scripts below it are the theme's own.
Re-check it when bumping the theme.
