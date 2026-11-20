Fonts (self-hosted, latin subsets from Google Fonts, 20 Nov 2026):
- assets/fonts/bodonimoda.woff2  Bodoni Moda variable (opsz 6-96, wght 400-700), latin
- assets/fonts/albertsans.woff2  Albert Sans variable (wght 400-600), latin
- assets/fonts/notoserifsc-sub.woff2  Noto Serif SC 500, only the glyphs in assets/fonts-src/zh-chars.txt
Re-subset after changing Chinese copy: rebuild, collect CJK glyphs from dist/ into zh-chars.txt, then request
https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@500&text=<urlencoded chars> and download the woff2 it names.
check.py fails if a built page uses a CJK glyph that is not in zh-chars.txt.
