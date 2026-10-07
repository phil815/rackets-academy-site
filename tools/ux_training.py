"""UX v1 (Oct 2026): 'which course is for me' switch under the training hero (EN/FR/DE). Idempotent."""
import os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T = {
 'en': [('I\'m new', 'Intro course', 'Never played? Intro course every Saturday at 10:00 in Sion. No experience needed, rackets to rent on site. Sign up in 1 minute.', 'Sign up on Playtomic →', 'https://tinyurl.com/Academy-Sion', 1),
        ('I already play', 'Memberships', 'Weekly group training with a plan and a level check every cycle.', 'See memberships →', '#adults', 0),
        ('For my child', 'Kids', 'Training for children by age and level, at both clubs.', 'Kids courses →', '#kids', 0)],
 'fr': [('Je débute', "Cours d'initiation", "Jamais joué ? Cours d'initiation chaque samedi à 10h à Sion. Aucune expérience nécessaire, raquette à louer sur place. Inscris-toi en 1 minute.", "S'inscrire sur Playtomic →", 'https://tinyurl.com/Academy-Sion', 1),
        ('Je joue déjà', 'Abonnements', 'Entraînement en groupe chaque semaine, avec un plan et un bilan de niveau à chaque cycle.', 'Voir les abonnements →', '#adultes', 0),
        ('Pour mon enfant', 'Enfants', 'Cours pour enfants par âge et niveau, sur les deux sites.', 'Cours enfants →', '#enfants', 0)],
 'de': [('Ich fange an', 'Einführungskurs', 'Noch nie gespielt? Einführungskurs jeden Samstag um 10 Uhr in Sion. Keine Vorkenntnisse nötig, Schläger vor Ort mieten. Anmeldung in 1 Minute.', 'Auf Playtomic anmelden →', 'https://tinyurl.com/Academy-Sion', 1),
        ('Ich spiele schon', 'Abos', 'Wöchentliches Gruppentraining mit Plan und Level-Check in jedem Zyklus.', 'Abos ansehen →', '#erwachsene', 0),
        ('Für mein Kind', 'Kinder', 'Kurse für Kinder nach Alter und Niveau, an beiden Standorten.', 'Kinderkurse →', '#kids', 0)],
}
for lang, pre in (('en', ''), ('fr', 'fr/'), ('de', 'de/')):
    p = os.path.join(ROOT, pre, 'training.html'); s = open(p).read()
    cards = ''.join(
        f'<a class="tw-card{" main" if m else ""}" href="{h}"' + (' target="_blank" rel="noopener"' if h.startswith('http') else '') +
        f'><small>{k}</small><b>{t}</b><span>{d}</span><em>{c}</em></a>' for k, t, d, c, h, m in T[lang])
    blk = f'<!-- ux:switch -->\n<section class="section-tight tw-switch" id="initiation"><div class="wrap"><div class="tw-grid">{cards}</div></div></section>\n<!-- /ux:switch -->'
    if '<!-- ux:switch -->' in s:
        s = re.sub(r'<!-- ux:switch -->.*?<!-- /ux:switch -->', lambda m: blk, s, flags=re.S)
    else:
        m = re.search(r'<section class="spa-hero co-hero".*?</section>\s*', s, re.S)
        s = s[:m.end()] + blk + '\n\n' + s[m.end():]
    open(p, 'w').write(s)
print('ok')
