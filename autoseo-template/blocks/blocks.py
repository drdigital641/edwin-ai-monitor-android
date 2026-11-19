"""AutoSEO shared blocks (look v2, from the JT Autoworks review, Edwin 20 Nov 2026).
Soft, premium blocks every new AutoSEO site starts from instead of plain boxes:
  photo_hero()   full-bleed real photo behind a transparent header, white headline + WhatsApp on the photo, fades into the next band
  video_tile()   9:16 video tile that always shows its real poster frame + play icon; <video poster> when the MP4 is self-hosted,
                 otherwise an <img> facade that swaps to the official Facebook embed on tap. No poster frame = no tile.
  reel_strip()   one horizontal swipe strip of video tiles (~64vw on phones, 4 across on desktop)
  soft_card()    rounded card with a contained poster, big price, list and a WhatsApp button (package strip)
  lap_block()    overlapping photo-and-text block
CSS: blocks.css (tokens + all blocks). JS: blocks.js (header glass, facade swap, floating bar, hero video).
Pure functions: pass in already-escaped strings / CTA HTML from the site's own wa()/call() helpers so data-cta stays per site.
Rules kept here: real photos use cover; designed posters always contain; never an empty or black video box."""
import html
import urllib.parse

E = html.escape
PLAY = '<span class="vf-play" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M8 5.2v13.6L19 12z"/></svg></span>'


def img_tag(url, w, h, alt, eager=False, cls=None):
    c = f' class="{cls}"' if cls else ''
    load = ' fetchpriority="high"' if eager == 'high' else ('' if eager else ' loading="lazy"')
    return f'<img{c} src="{E(url)}" width="{w}" height="{h}" alt="{E(alt)}"{load} decoding="async">'


def photo_hero(tall, wide, alt, kicker, h1, line, cta_html):
    """tall/wide = (url, w, h) or None. tall is the phone crop (4:5 or taller), wide the desktop photo. Real photos only."""
    pic = ''
    if tall:
        src = f'<source media="(min-width: 760px)" srcset="{E(wide[0])}" width="{wide[1]}" height="{wide[2]}">' if wide else ''
        pic = f'<picture class="hero-bg">{src}{img_tag(tall[0], tall[1], tall[2], alt, eager="high")}</picture>'
    k = f'<p class="kicker">{E(kicker)}</p>' if kicker else ''
    return (f'<section class="hero on-navy">{pic}<div class="wrap hero-in">{k}<h1>{E(h1)}</h1>'
            f'<p class="hero-line">{E(line)}</p><div class="hero-cta">{cta_html}</div></div></section>')


def fb_embed_src(reel_id):
    href = f'https://www.facebook.com/reel/{reel_id}/'
    return 'https://www.facebook.com/plugins/video.php?href=' + urllib.parse.quote(href, safe='') + '&show_text=false&width=360&height=640'


def video_tile(caption, play_label, poster=None, length=None, fb_reel_id=None, mp4=None, sound_label='Tap for sound', extra_html='', eager=False):
    """poster = (url, w, h) of the real 9:16 frame. mp4 = (url, w, h) when self-hosted. Returns '' without a poster frame or MP4."""
    if not poster and not mp4:
        return ''
    if mp4:
        p = f' poster="{E(poster[0])}"' if poster else ''
        box = (f'<div class="vf vf-own"><video muted playsinline loop preload="none"{p} width="{mp4[1]}" height="{mp4[2]}" aria-label="{E(caption)}">'
               f'<source src="{E(mp4[0])}" type="video/mp4"></video><button class="vf-snd" type="button" aria-pressed="false">{E(sound_label)}</button></div>')
    else:
        ln = f'<span class="vf-len num">{E(length)}</span>' if length else ''
        box = (f'<div class="vf"><button class="vf-b" type="button" data-src="{E(fb_embed_src(fb_reel_id))}" aria-label="{E(play_label + ": " + caption)}">'
               f'{img_tag(poster[0], poster[1], poster[2], "", eager=eager)}{PLAY}{ln}</button></div>')
    return f'<figure class="reel">{box}<figcaption><span>{E(caption)}</span>{extra_html}</figcaption></figure>'


def reel_strip(tiles):
    items = ''.join(f'<li>{t}</li>' for t in tiles if t)
    return f'<ul class="reels">{items}</ul>' if items else ''


def soft_card(tag_letter, tag, title, price, price_note, sub, items, cta_html, poster=None, poster_alt=''):
    """Package / offer card. poster = (url, w, h) of a designed poster: shown contained, never cropped."""
    fig = f'<div class="pk-img">{img_tag(poster[0], poster[1], poster[2], poster_alt)}</div>' if poster else ''
    lis = ''.join(f'<li>{E(x)}</li>' for x in items)
    b = f'<b>{E(tag_letter)}</b>' if tag_letter else ''
    return (f'<li class="pk-c">{fig}<div class="pk-b"><p class="pk-tag">{b}{E(tag)}</p><h3 class="pk-oil">{E(title)}</h3>'
            f'<p class="pk-p num">{E(price)}<small>{E(price_note)}</small></p><p class="pk-x num">{E(sub)}</p><ul>{lis}</ul>{cta_html}</div></li>')


def soft_cards(cards):
    return f'<ul class="pk">{"".join(cards)}</ul>'


def lap_block(photo, alt, h2, paras, link_html='', band='white', flip=False):
    """photo = (url, w, h) real photo (cover). Falls back to plain prose when there is no photo."""
    body = ''.join(f'<p>{E(p)}</p>' for p in paras)
    if not photo:
        return f'<section class="sec {band}"><div class="wrap prose"><h2>{E(h2)}</h2>{body}{link_html}</div></section>'
    return (f'<section class="sec {band}"><div class="wrap lap{" flip" if flip else ""}"><figure class="lap-img">{img_tag(photo[0], photo[1], photo[2], alt)}</figure>'
            f'<div class="lap-card"><h2>{E(h2)}</h2>{body}{link_html}</div></div></section>')
