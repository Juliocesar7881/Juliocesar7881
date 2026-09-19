"""Gera os SVGs estaticos do README de perfil (banner, digitando, cards, linguagens, rodape).

Uso: python scripts/gerar_assets.py   (escreve em assets/)
linguagens.json: bytes por linguagem de cada repositorio, da API /repos/{repo}/languages.
"""
import json
import os
from html import escape

AQUI = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(AQUI, '..', 'assets')
os.makedirs(OUT, exist_ok=True)

SANS = "'Segoe UI',Inter,-apple-system,BlinkMacSystemFont,'Helvetica Neue',Helvetica,Arial,sans-serif"
MONO = "'JetBrains Mono','Cascadia Code','SF Mono',SFMono-Regular,Consolas,'Liberation Mono',Menlo,monospace"

BG = '#0B0D17'
CARD = '#10131F'
BORDER = '#262B40'
TEXT = '#E6EDF3'
MUTED = '#98A2B3'
VIOLET = '#8B5CF6'
LILAC = '#A78BFA'
CYAN = '#22D3EE'
PINK = '#F472B6'
GREEN = '#34D399'
AMBER = '#FBBF24'


def e(s):
    return escape(s, quote=True)


def salvar(nome, svg):
    with open(os.path.join(OUT, nome), 'w', encoding='utf-8', newline='\n') as f:
        f.write(svg.strip() + '\n')
    print(f'{nome}: {len(svg.encode()) / 1024:.1f} KB')


def mono_text(x, y, texto, fs, cor, extra='', cw=None):
    """Texto monoespacado com largura fixa (textLength), igual em qualquer fonte."""
    cw = cw or fs * 0.6
    return (f'<text x="{x}" y="{y}" font-family="{MONO}" font-size="{fs}" fill="{cor}" '
            f'textLength="{len(texto) * cw:.1f}" lengthAdjust="spacing" {extra}>{e(texto)}</text>')


# ---------------------------------------------------------------- banner
def banner():
    W, H = 1280, 400
    cores = {'kw': '#C084FC', 'var': '#7DD3FC', 'prop': '#F9A8D4', 'str': '#86EFAC', 'p': '#94A3B8', 'fn': '#FDE68A'}
    codigo = [
        [('const ', 'kw'), ('julio', 'var'), (' = {', 'p')],
        [('  stack', 'prop'), (': [', 'p'), ('"Next.js"', 'str'), (', ', 'p'), ('"Expo"', 'str'), (', ', 'p'), ('"Tauri"', 'str'), ('],', 'p')],
        [('  ia', 'prop'), (': ', 'p'), ('"visão computacional offline"', 'str'), (',', 'p')],
        [('  apps', 'prop'), (': [', 'p'), ('"web"', 'str'), (', ', 'p'), ('"android"', 'str'), (', ', 'p'), ('"desktop"', 'str'), ('],', 'p')],
        [('  extra', 'prop'), (': ', 'p'), ('"edição de vídeo e motion"', 'str'), (',', 'p')],
        [('};', 'p')],
        [('julio', 'var'), ('.', 'p'), ('build', 'fn'), ('(', 'p'), ('"o próximo projeto"', 'str'), (');', 'p')],
    ]
    wx, wy, ww, wh = 772, 64, 452, 272
    fs, cw, lh = 15, 9.0, 27
    linhas = []
    for i, partes in enumerate(codigo):
        y = wy + 78 + i * lh
        n = sum(len(t) for t, _ in partes)
        spans = ''.join(f'<tspan fill="{cores[c]}">{e(t)}</tspan>' for t, c in partes)
        atraso = 0.35 + i * 0.18
        linhas.append(
            f'<g class="ln" style="animation-delay:{atraso:.2f}s">'
            f'<text x="{wx + 36}" y="{y}" font-family="{MONO}" font-size="13" fill="#4B5270" text-anchor="end">{i + 1}</text>'
            f'<text x="{wx + 52}" y="{y}" font-family="{MONO}" font-size="{fs}" xml:space="preserve" '
            f'textLength="{n * cw:.1f}" lengthAdjust="spacing">{spans}</text></g>')
        if i == len(codigo) - 1:
            caret_x = wx + 52 + n * cw + 3
            caret_y = y - 15
    tags = ['Next.js', 'React Native', 'Tauri + Rust', 'PyTorch']
    chips, x = [], 72
    for t in tags:
        w = len(t) * 7.8 + 28
        chips.append(f'<rect x="{x}" y="296" width="{w:.1f}" height="34" rx="17" fill="#FFFFFF" fill-opacity="0.05" stroke="#FFFFFF" stroke-opacity="0.12"/>'
                     + mono_text(x + 14, 318, t, 13, '#C9D1D9'))
        x += w + 10
    svg = f'''
<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="titulo desc">
<title id="titulo">Júlio César Luchini</title>
<desc id="desc">Desenvolvedor full-stack e mobile. Web, Android, desktop e IA aplicada.</desc>
<defs>
  <linearGradient id="fundo" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{BG}"/><stop offset="1" stop-color="#12152A"/></linearGradient>
  <linearGradient id="grad" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{LILAC}"/><stop offset="0.55" stop-color="{CYAN}"/><stop offset="1" stop-color="{PINK}"/></linearGradient>
  <filter id="blur" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="64"/></filter>
  <pattern id="grade" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="#FFFFFF" stroke-opacity="0.05"/></pattern>
  <radialGradient id="foco" cx="0.35" cy="0.45" r="0.75"><stop offset="0" stop-color="#FFFFFF"/><stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/></radialGradient>
  <mask id="mascara"><rect width="{W}" height="{H}" fill="url(#foco)"/></mask>
  <clipPath id="canto"><rect width="{W}" height="{H}" rx="28"/></clipPath>
</defs>
<style>
  .blob{{animation:flutua 16s ease-in-out infinite alternate;transform-box:fill-box;transform-origin:center}}
  .b2{{animation-duration:21s;animation-delay:-7s}}
  .b3{{animation-duration:26s;animation-delay:-3s}}
  @keyframes flutua{{0%{{transform:translate(0,0) scale(1)}}50%{{transform:translate(70px,-30px) scale(1.18)}}100%{{transform:translate(-50px,28px) scale(.92)}}}}
  .ln{{opacity:0;animation:entra .5s ease-out forwards}}
  @keyframes entra{{from{{opacity:0;transform:translateX(-8px)}}to{{opacity:1;transform:none}}}}
  .cursor{{animation:pisca 1.1s steps(1) infinite}}
  @keyframes pisca{{50%{{opacity:0}}}}
  .sobe{{opacity:0;animation:sobe .8s cubic-bezier(.2,.7,.2,1) forwards}}
  @keyframes sobe{{from{{opacity:0;transform:translateY(14px)}}to{{opacity:1;transform:none}}}}
  @media (prefers-reduced-motion:reduce){{.blob,.cursor{{animation:none}}.ln,.sobe{{animation:none;opacity:1}}}}
</style>
<g clip-path="url(#canto)">
  <rect width="{W}" height="{H}" fill="url(#fundo)"/>
  <g filter="url(#blur)" opacity="0.6">
    <circle class="blob" cx="200" cy="70" r="170" fill="#7C3AED"/>
    <circle class="blob b2" cx="1120" cy="340" r="180" fill="#0891B2"/>
    <circle class="blob b3" cx="700" cy="30" r="120" fill="#DB2777" fill-opacity="0.55"/>
  </g>
  <rect width="{W}" height="{H}" fill="url(#grade)" mask="url(#mascara)"/>

  <g class="sobe">
    <rect x="72" y="72" width="268" height="34" rx="17" fill="#FFFFFF" fill-opacity="0.06" stroke="#FFFFFF" stroke-opacity="0.14"/>
    <circle cx="92" cy="89" r="5" fill="{GREEN}"/>
    <circle cx="92" cy="89" r="9" fill="none" stroke="{GREEN}" stroke-opacity="0.35"/>
    {mono_text(108, 94, 'full-stack · mobile · IA', 13.5, '#C9D1D9')}
  </g>
  <g class="sobe" style="animation-delay:.12s">
    <text x="70" y="178" font-family="{SANS}" font-size="58" font-weight="800" fill="{TEXT}" letter-spacing="-1">Júlio César</text>
    <text x="70" y="240" font-family="{SANS}" font-size="58" font-weight="800" fill="url(#grad)" letter-spacing="-1">Luchini</text>
  </g>
  <g class="sobe" style="animation-delay:.24s">
    <text x="72" y="276" font-family="{SANS}" font-size="19" fill="{MUTED}">Produtos digitais de ponta a ponta: do banco de dados à Play Store.</text>
  </g>
  <g class="sobe" style="animation-delay:.36s">{''.join(chips)}</g>

  <g class="sobe" style="animation-delay:.2s">
    <rect x="{wx}" y="{wy}" width="{ww}" height="{wh}" rx="16" fill="#0A0C18" fill-opacity="0.82" stroke="#FFFFFF" stroke-opacity="0.12"/>
    <path d="M{wx} {wy + 44}H{wx + ww}" stroke="#FFFFFF" stroke-opacity="0.08"/>
    <circle cx="{wx + 22}" cy="{wy + 22}" r="6" fill="#FF5F57"/>
    <circle cx="{wx + 42}" cy="{wy + 22}" r="6" fill="#FEBC2E"/>
    <circle cx="{wx + 62}" cy="{wy + 22}" r="6" fill="#28C840"/>
    {mono_text(wx + ww / 2 - 4 * 7.8, wy + 27, 'julio.ts', 13, '#6B7394')}
    {''.join(linhas)}
    <rect class="cursor" x="{caret_x:.1f}" y="{caret_y}" width="8" height="19" rx="1.5" fill="{LILAC}"/>
  </g>
</g>
<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="28" fill="none" stroke="#FFFFFF" stroke-opacity="0.08"/>
</svg>'''
    salvar('banner.svg', svg)


# ---------------------------------------------------------------- frase digitando
def digitando():
    W, H, fs = 1280, 64, 26
    cw = fs * 0.6
    frases = [
        'Apps web completos com Next.js, React e Prisma',
        'Apps Android com React Native, Expo e Capacitor',
        'Visão computacional rodando offline no celular',
        'Apps desktop com Tauri e Rust',
        'IA generativa dentro de produtos reais',
        'Edição de vídeo e motion design',
    ]
    t_letra, t_apaga, t_fica, t_pausa = 0.05, 0.018, 2.2, 0.35
    maior = max(len(f) for f in frases) + 2
    x0 = (W - maior * cw) / 2
    xt = x0 + 2 * cw
    y = 42
    # linha do tempo
    eventos, t = [], 0.0
    for f in frases:
        n = len(f)
        ini = t
        fim_digita = ini + n * t_letra
        fim_fica = fim_digita + t_fica
        fim_apaga = fim_fica + n * t_apaga
        eventos.append((f, ini, fim_digita, fim_fica, fim_apaga))
        t = fim_apaga + t_pausa
    T = t

    def anim(attr, pontos):
        # pontos: [(tempo, valor)] em ordem; discreto
        limpo = []
        for tt, v in pontos:
            tt = round(tt / T, 5)
            if limpo and tt <= limpo[-1][0]:
                limpo[-1] = (limpo[-1][0], v)
                continue
            limpo.append((tt, v))
        if limpo[0][0] != 0:
            limpo.insert(0, (0, pontos[0][1] if pontos[0][0] == 0 else 0))
        kt = ';'.join(f'{a:g}' for a, _ in limpo)
        vs = ';'.join(f'{v:.1f}' for _, v in limpo)
        return (f'<animate attributeName="{attr}" dur="{T:.2f}s" repeatCount="indefinite" calcMode="discrete" '
                f'keyTimes="{kt}" values="{vs}"/>')

    defs, textos, cursor = [], [], [(0, xt)]
    for i, (f, ini, fd, ff, fa) in enumerate(eventos):
        n = len(f)
        pts = [(0, 0), (ini, 0)]
        for k in range(1, n + 1):
            pts.append((ini + k * t_letra, k * cw))
            cursor.append((ini + k * t_letra, xt + k * cw))
        for k in range(1, n + 1):
            pts.append((ff + k * t_apaga, (n - k) * cw))
            cursor.append((ff + k * t_apaga, xt + (n - k) * cw))
        defs.append(f'<clipPath id="c{i}"><rect x="{xt:.1f}" y="0" height="{H}" width="0">{anim("width", pts)}</rect></clipPath>')
        textos.append(f'<g clip-path="url(#c{i})">' + mono_text(round(xt, 1), y, f, fs, TEXT) + '</g>')
    svg = f'''
<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{e(' · '.join(frases))}">
<title>{e(' · '.join(frases))}</title>
<defs>{''.join(defs)}</defs>
<style>.cur{{animation:pisca 1s steps(1) infinite}}@keyframes pisca{{50%{{opacity:0}}}}@media (prefers-reduced-motion:reduce){{.cur{{animation:none}}}}</style>
<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="16" fill="{CARD}" stroke="{BORDER}"/>
{mono_text(round(x0, 1), y, '>', fs, LILAC, 'font-weight="700"')}
{''.join(textos)}
<rect class="cur" x="{xt:.1f}" y="{y - 22}" width="3" height="28" rx="1.5" fill="{CYAN}">{anim("x", cursor)}</rect>
</svg>'''
    salvar('digitando.svg', svg)


# ---------------------------------------------------------------- icones dos cards
def icone(tipo):
    s = 'fill="none" stroke="#FFFFFF" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"'
    if tipo == 'pegadas':
        return ('<g fill="#FFFFFF">'
                '<ellipse cx="19" cy="33" rx="5.6" ry="8" transform="rotate(-12 19 33)"/>'
                '<circle cx="14.2" cy="22.2" r="1.9"/><circle cx="17.8" cy="20.6" r="1.9"/><circle cx="21.6" cy="21.2" r="1.8"/><circle cx="24.4" cy="23.4" r="1.6"/>'
                '<ellipse cx="33.5" cy="26" rx="5.2" ry="7.6" transform="rotate(12 33.5 26)"/>'
                '<circle cx="28.8" cy="15.6" r="1.8"/><circle cx="32.4" cy="13.8" r="1.8"/><circle cx="36.1" cy="14.6" r="1.7"/><circle cx="38.8" cy="17" r="1.5"/>'
                '</g>')
    if tipo == 'mira':
        return (f'<path d="M13 20v-7h7M32 13h7v7M39 32v7h-7M20 39h-7v-7" {s}/>'
                '<circle cx="21" cy="23" r="3.2" fill="#FFFFFF"/><circle cx="31" cy="21" r="3.2" fill="#FFFFFF"/>'
                '<circle cx="26" cy="31" r="3.2" fill="#FFFFFF" fill-opacity="0.55"/>')
    if tipo == 'velas':
        return (f'<path d="M16 12v28M26 10v30M36 16v22" {s}/>'
                '<rect x="12" y="18" width="8" height="13" rx="2" fill="#FFFFFF"/>'
                '<rect x="22" y="14" width="8" height="17" rx="2" fill="#FFFFFF" fill-opacity="0.55"/>'
                '<rect x="32" y="21" width="8" height="11" rx="2" fill="#FFFFFF"/>')
    if tipo == 'orbita':
        return (f'<ellipse cx="26" cy="26" rx="18" ry="8.5" transform="rotate(-28 26 26)" {s}/>'
                '<path d="M22.5 19.5v13l10.5-6.5z" fill="#FFFFFF"/>'
                '<circle cx="40.5" cy="16.5" r="2.6" fill="#FFFFFF"/>')
    raise ValueError(tipo)


def card(nome, titulo, subtitulo, linhas, chips, status, cor_status, tipo_icone, c1, c2, rodape):
    W, H = 460, 272
    fs_s, cw_s = 11, 6.6
    w_status = 34 + len(status) * cw_s
    xs = W - 26 - w_status
    ch, x = [], 26
    for c in chips:
        w = len(c) * 7.2 + 20
        ch.append(f'<rect x="{x:.1f}" y="200" width="{w:.1f}" height="25" rx="12.5" fill="#FFFFFF" fill-opacity="0.05" stroke="#FFFFFF" stroke-opacity="0.1"/>'
                  + mono_text(round(x + 10, 1), 217, c, 12, '#C9D1D9'))
        x += w + 7
    if x > W - 20:
        raise SystemExit(f'{nome}: chips estouram a largura ({x:.0f}px)')
    desc = ''.join(f'<text x="26" y="{122 + i * 24}" font-family="{SANS}" font-size="16" fill="{TEXT}" fill-opacity="0.88">{e(l)}</text>'
                   for i, l in enumerate(linhas))
    cadeado = ''
    if status == 'PRIVADO':
        cadeado = (f'<g transform="translate({xs + 12} 33)" fill="none" stroke="{cor_status}" stroke-width="1.6">'
                   f'<rect x="0" y="4.5" width="9" height="7" rx="1.5" fill="{cor_status}" stroke="none"/><path d="M2 4.5V3a2.5 2.5 0 0 1 5 0v1.5"/></g>')
        ponto = ''
    else:
        ponto = f'<circle cx="{xs + 16}" cy="41" r="4" fill="{cor_status}"><animate attributeName="opacity" values="1;.35;1" dur="2.4s" repeatCount="indefinite"/></circle>'
    svg = f'''
<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t d">
<title id="t">{e(titulo)}</title><desc id="d">{e(subtitulo + '. ' + ' '.join(linhas))}</desc>
<defs>
  <linearGradient id="ic" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient>
  <linearGradient id="topo" x1="0" x2="1"><stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}" stop-opacity="0"/></linearGradient>
  <radialGradient id="brilho" cx="1" cy="0" r="0.9"><stop offset="0" stop-color="{c2}" stop-opacity="0.22"/><stop offset="1" stop-color="{c2}" stop-opacity="0"/></radialGradient>
  <clipPath id="k"><rect width="{W}" height="{H}" rx="18"/></clipPath>
</defs>
<g clip-path="url(#k)">
  <rect width="{W}" height="{H}" fill="{CARD}"/>
  <rect width="{W}" height="{H}" fill="url(#brilho)"/>
  <rect width="{W}" height="3" fill="url(#topo)"/>
</g>
<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="18" fill="none" stroke="{BORDER}"/>
<rect x="26" y="26" width="52" height="52" rx="14" fill="url(#ic)"/>
<g transform="translate(26 26)">{icone(tipo_icone)}</g>
<text x="92" y="50" font-family="{SANS}" font-size="21" font-weight="700" fill="{TEXT}">{e(titulo)}</text>
<text x="92" y="72" font-family="{SANS}" font-size="13.5" fill="{MUTED}">{e(subtitulo)}</text>
<rect x="{xs:.1f}" y="30" width="{w_status:.1f}" height="22" rx="11" fill="{cor_status}" fill-opacity="0.12" stroke="{cor_status}" stroke-opacity="0.45"/>
{ponto}{cadeado}
{mono_text(round(xs + 26, 1), 45, status, fs_s, cor_status, 'font-weight="700"', cw_s)}
{desc}
{''.join(ch)}
{mono_text(26, 252, rodape, 12, c2 if c2 != '#FFFFFF' else LILAC)}
</svg>'''
    salvar(nome, svg)


# ---------------------------------------------------------------- linguagens
def linguagens():
    with open(os.path.join(AQUI, 'linguagens.json'), encoding='utf-8') as f:
        dados = json.load(f)
    total = {}
    for repo in dados.values():
        for k, v in repo.items():
            total[k] = total.get(k, 0) + v
    soma = sum(total.values())
    cores = {'TypeScript': '#3178C6', 'JavaScript': '#F1E05A', 'Dart': '#00B4AB', 'HTML': '#E34C26', 'CSS': '#8E5CD9',
             'Python': '#3572A5', 'Kotlin': '#A97BFF', 'PLpgSQL': '#336790', 'Java': '#B07219', 'Rust': '#DEA584'}
    nomes = {'PLpgSQL': 'SQL'}
    principais = [k for k, _ in sorted(total.items(), key=lambda x: -x[1]) if k in cores][:8]
    itens = [(nomes.get(k, k), total[k] / soma, cores[k]) for k in principais]
    resto = 1 - sum(p for _, p, _ in itens)
    outras = sorted((k for k in total if k not in principais and total[k] / soma >= 0.001), key=lambda k: -total[k])
    itens.append(('Outras', resto, '#6E7681'))
    W, H = 900, 234
    x, barra = 32, []
    larg = W - 64
    for i, (n, p, c) in enumerate(itens):
        w = larg * p
        barra.append(f'<rect x="{x:.2f}" y="92" width="{max(w, 0.5):.2f}" height="14" fill="{c}"/>')
        x += w
    leg = []
    for i, (n, p, c) in enumerate(itens):
        col, lin = i % 3, i // 3
        lx, ly = 32 + col * 290, 146 + lin * 30
        leg.append(f'<circle cx="{lx + 6}" cy="{ly - 5}" r="6" fill="{c}"/>'
                   f'<text x="{lx + 22}" y="{ly}" font-family="{SANS}" font-size="15" fill="{TEXT}">{e(n)}</text>'
                   + mono_text(lx + 150, ly, f'{p * 100:5.1f}%'.strip(), 14, MUTED))
    svg = f'''
<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t d">
<title id="t">Linguagens mais usadas</title>
<desc id="d">{e(', '.join(f'{n} {p * 100:.1f}%' for n, p, _ in itens))}</desc>
<defs><clipPath id="b"><rect x="32" y="92" width="{larg}" height="14" rx="7"/></clipPath>
<radialGradient id="brilho" cx="0" cy="0" r="1"><stop offset="0" stop-color="{VIOLET}" stop-opacity="0.16"/><stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/></radialGradient>
<clipPath id="k"><rect width="{W}" height="{H}" rx="18"/></clipPath></defs>
<g clip-path="url(#k)"><rect width="{W}" height="{H}" fill="{CARD}"/><rect width="{W}" height="{H}" fill="url(#brilho)"/></g>
<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="18" fill="none" stroke="{BORDER}"/>
<text x="32" y="50" font-family="{SANS}" font-size="20" font-weight="700" fill="{TEXT}">Linguagens mais usadas</text>
<text x="32" y="73" font-family="{SANS}" font-size="13.5" fill="{MUTED}">Somando todos os meus repositórios, inclusive os privados · setembro de 2026</text>
<g clip-path="url(#b)">{''.join(barra)}</g>
{''.join(leg)}
</svg>'''
    salvar('linguagens.svg', svg)
    print('   outras:', ', '.join(outras))


# ---------------------------------------------------------------- rodape
def rodape():
    W, H = 1280, 150
    svg = f'''
<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Obrigado pela visita!">
<title>Obrigado pela visita!</title>
<defs><linearGradient id="g" x1="0" x2="1"><stop offset="0" stop-color="{VIOLET}"/><stop offset="0.5" stop-color="{CYAN}"/><stop offset="1" stop-color="{PINK}"/></linearGradient></defs>
<style>.o{{animation:onda 9s ease-in-out infinite alternate}}.o2{{animation-duration:12s;animation-delay:-4s}}
@keyframes onda{{from{{transform:translateX(0)}}to{{transform:translateX(-160px)}}}}
@media (prefers-reduced-motion:reduce){{.o{{animation:none}}}}</style>
<g opacity="0.9">
<path class="o" d="M0 110 C160 70 320 150 480 110 S800 70 960 110 S1280 150 1440 110 V150 H0Z" fill="url(#g)" fill-opacity="0.35"/>
<path class="o o2" d="M0 125 C160 95 320 155 480 125 S800 95 960 125 S1280 155 1440 125 V150 H0Z" fill="url(#g)" fill-opacity="0.6"/>
</g>
<text x="{W / 2}" y="62" text-anchor="middle" font-family="{SANS}" font-size="22" font-weight="600" fill="url(#g)">Obrigado pela visita!</text>
</svg>'''
    salvar('rodape.svg', svg)


banner()
digitando()
card('projeto-pequenos-passos.svg', 'Pequenos Passos', 'Plataforma pedagógica para a educação infantil',
     ['Planejamento, registros com foto e voz, avaliações', 'com IA e uma biblioteca de 1.500+ projetos.',
      'Site + app Android com sincronização offline.'],
     ['Next.js', 'React 19', 'Prisma', 'Postgres', 'Expo'], 'NO AR', GREEN, 'pegadas', '#8B5CF6', '#EC4899',
     'pequenospassos.space ↗')
card('projeto-visor-crypto.svg', 'Visor Crypto', 'Criptomoedas em tempo real · open source',
     ['Gráficos de velas, índice de medo e ganância,', 'dados macro, notícias e um conselheiro de', 'mercado com IA. Publicado na Google Play.'],
     ['JavaScript', 'Capacitor', 'Android', 'CF Workers'], 'GOOGLE PLAY', GREEN, 'velas', '#0EA5E9', '#22D3EE',
     'play.google.com ↗')
card('projeto-contador-pupunhas.svg', 'Contador de Pupunhas', 'Visão computacional 100% offline no celular',
     ['Conta cabeças de pupunha em fotos de paletes', 'com dois modelos RF-DETR que eu treinei,', 'rodando no aparelho, sem internet nem nuvem.'],
     ['Expo', 'Kotlin', 'PyTorch', 'RF-DETR', 'LiteRT'], 'PRIVADO', AMBER, 'mira', '#F59E0B', '#EF4444',
     'app Android · distribuído em APK')
card('projeto-orbit-studio.svg', 'Orbit Studio', 'Estúdio de publicação para o YouTube',
     ['Solte um vídeo e a IA escreve título, descrição', 'e tags, cria a thumbnail, escolhe o horário de', 'pico e publica em vários canais.'],
     ['Tauri', 'Rust', 'TypeScript', 'Vite', 'Workers'], 'EM BREVE', LILAC, 'orbita', '#6366F1', '#A855F7',
     'app desktop para Windows')
linguagens()
rodape()
