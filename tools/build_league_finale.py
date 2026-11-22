#!/usr/bin/env python3
"""Finale Rivella League (29.11.2026): Programm + Preise auf rivella-league.html (EN/FR/DE).

Setzt den Block zwischen <!-- finale:start --> und <!-- finale:end --> direkt vor das Live-Widget.
Erneut laufen lassen ersetzt den Block. Aufruf im Repo-Root: python3 tools/build_league_finale.py
"""
import re, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent

# Programm: (Zeit, [(Plätze, Art)]) Art: '' normal, 'f' Final 17/18, 'gf' grosser Final
SCHEDULE = [
    ('08:45', [('31/32', '')]),
    ('10:00', [('29/30', ''), ('27/28', ''), ('25/26', '')]),
    ('11:15', [('23/24', ''), ('21/22', ''), ('19/20', '')]),
    ('12:30', [('17/18', 'f'), ('15/16', ''), ('13/14', '')]),
    ('13:45', [('7/8', ''), ('5/6', ''), ('3/4', '')]),
    ('15:00', [('1/2', 'gf'), ('9/10', ''), ('11/12', '')]),
]
# Preise pro Spieler (wie Instagram-Carousel 22.11.2026)
PLAYTOMIC = {r: 60 - 2 * i for i, r in enumerate(range(3, 17))}   # 60 .. 34
TRAINING = {r: 33 - i for i, r in enumerate(range(17, 26))}        # 33 .. 25
SPA = range(26, 33)

T = {
 'en': dict(
   h2='Grand final · Sunday 29 November',
   lede='Salgesch · from 08:45 · every position is played out on court. Spectators welcome!',
   perks=['Free for players', '1 bifana + 1 Rivella on us', 'A prize + a surprise for every player', 'Prize ceremony + apéro at 16:15'],
   sched='Schedule', rules='3 full sets · be there 20 min before your match · 15 min late = walkover',
   place='Place', final='Final', gfinal='Grand final', ceremony='Prize ceremony + apéro',
   prizes='Prizes (per player)', every='At every place: + a surprise + a Rivella',
   p1='Babolat Viper racket', p2='Babolat Veron racket',
   pt='Playtomic credit', tr='Training voucher', spa='Spa entry',
   r3='3rd–16th', r17='17th–25th', r26='26th–32nd', from_to='CHF {a} to {b}', spa_txt='Spa entry',
   all='See the prize for every place', ord=lambda r: f'{r}{"st" if r==1 else "nd" if r==2 else "rd" if r==3 else "th"}'),
 'fr': dict(
   h2='Grande finale · dimanche 29 novembre',
   lede='Salgesch · dès 08:45 · chaque place se joue sur le terrain. Public bienvenu !',
   perks=['Gratuit pour les joueurs', '1 bifana + 1 Rivella offerts', 'Un prix + une surprise pour chaque joueur', 'Remise des prix + apéro à 16h15'],
   sched='Programme', rules='3 sets complets · sois là 20 min avant ton match · 15 min de retard = WO',
   place='Place', final='Finale', gfinal='Grande finale', ceremony='Remise des prix + apéro',
   prizes='Les prix (par joueur)', every='À chaque place : + une surprise + un Rivella',
   p1='Raquette Babolat Viper', p2='Raquette Babolat Veron',
   pt='Crédit Playtomic', tr='Bon entraînement', spa='Entrée spa',
   r3='3e–16e', r17='17e–25e', r26='26e–32e', from_to='CHF {a} à {b}', spa_txt='Entrée spa',
   all='Voir le prix de chaque place', ord=lambda r: f'{r}{"er" if r==1 else "e"}'),
 'de': dict(
   h2='Grosser Final · Sonntag, 29. November',
   lede='Salgesch · ab 08:45 · jeder Platz wird auf dem Court ausgespielt. Zuschauer willkommen!',
   perks=['Gratis für Spieler', '1 Bifana + 1 Rivella offeriert', 'Ein Preis + eine Überraschung für jeden Spieler', 'Siegerehrung + Apéro um 16:15'],
   sched='Programm', rules='3 volle Sätze · 20 Min vor deinem Spiel da sein · 15 Min zu spät = WO',
   place='Platz', final='Final', gfinal='Grosser Final', ceremony='Siegerehrung + Apéro',
   prizes='Preise (pro Spieler)', every='Auf jedem Platz: + eine Überraschung + ein Rivella',
   p1='Schläger Babolat Viper', p2='Schläger Babolat Veron',
   pt='Playtomic-Guthaben', tr='Trainingsgutschein', spa='Spa-Eintritt',
   r3='3.–16.', r17='17.–25.', r26='26.–32.', from_to='CHF {a} bis {b}', spa_txt='Spa-Eintritt',
   all='Preis für jeden Platz anzeigen', ord=lambda r: f'{r}.'),
}

def block(lang):
    t = T[lang]
    rows = []
    for time, games in SCHEDULE:
        cells = []
        for pl, kind in games:
            lab = {'': t['place'], 'f': t['final'], 'gf': '🏆 ' + t['gfinal']}[kind]
            cells.append(f'<div class="fn-g {kind}"><small>{lab}</small><b>{pl}</b></div>')
        rows.append(f'<div class="fn-row"><div class="fn-t">{time}</div><div class="fn-gs">{"".join(cells)}</div></div>')
    rows.append(f'<div class="fn-row"><div class="fn-t">16:15</div><div class="fn-gs"><div class="fn-g cer"><b>{t["ceremony"]} 🥂</b></div></div></div>')

    full = []
    for r in range(1, 33):
        if r == 1: v, c = t['p1'], 'k1'
        elif r == 2: v, c = t['p2'], 'k1'
        elif r in PLAYTOMIC: v, c = f'{t["pt"]} CHF {PLAYTOMIC[r]}.–', 'k2'
        elif r in TRAINING: v, c = f'{t["tr"]} CHF {TRAINING[r]}.–', 'k3'
        else: v, c = t['spa_txt'], 'k4'
        full.append(f'<li class="{c}"><span>{t["ord"](r)}</span>{v}</li>')

    perks = ''.join(f'<li>{p}</li>' for p in t['perks'])
    return f'''<!-- finale:start -->
<section class="section-tight fn">
  <div class="wrap">
    <h2>{t["h2"]}</h2>
    <p class="fn-lede">{t["lede"]}</p>
    <ul class="fn-perks">{perks}</ul>
    <div class="fn-cols">
      <div class="fn-box">
        <h3>{t["sched"]}</h3>
        {"".join(rows)}
        <p class="fn-note">{t["rules"]}</p>
      </div>
      <div class="fn-box">
        <h3>{t["prizes"]}</h3>
        <div class="fn-p k1"><span>{t["ord"](1)}</span><b>{t["p1"]}</b></div>
        <div class="fn-p k1 b"><span>{t["ord"](2)}</span><b>{t["p2"]}</b></div>
        <div class="fn-p k2"><span>{t["r3"]}</span><b>{t["pt"]}</b><em>{t["from_to"].format(a=60, b=34)}</em></div>
        <div class="fn-p k3"><span>{t["r17"]}</span><b>{t["tr"]}</b><em>{t["from_to"].format(a=33, b=25)}</em></div>
        <div class="fn-p k4"><span>{t["r26"]}</span><b>{t["spa"]}</b></div>
        <p class="fn-every">🎁 🥤 {t["every"]}</p>
        <details class="fn-all"><summary>{t["all"]}</summary><ul>{"".join(full)}</ul></details>
      </div>
    </div>
  </div>
</section>
<!-- finale:end -->
'''

for lang, path in [('en', 'rivella-league.html'), ('fr', 'fr/rivella-league.html'), ('de', 'de/rivella-league.html')]:
    p = ROOT / path
    s = p.read_text(encoding='utf-8')
    s = re.sub(r'<!-- finale:start -->.*?<!-- finale:end -->\n', '', s, flags=re.S)
    anchor = '<section class="section-tight">\n  <div id="league"></div>'
    assert anchor in s, path
    s = s.replace(anchor, block(lang) + '\n' + anchor)
    s = re.sub(r'league\.css\?v=\d+', 'league.css?v=3', s)
    p.write_text(s, encoding='utf-8')
    print('ok', path)
