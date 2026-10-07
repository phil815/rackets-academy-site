"""UX v1 (Oct 2026): structured inquiry forms (kids birthday, company events) -> prefilled WhatsApp message.
No deposit, no backend. Re-run after build_birthday.py / company-events changes. Idempotent (ux:inquiry markers)."""
import os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
K = {
 'en': dict(h='Request your birthday party', p='Fill in the basics and we reply within 24 hours on WhatsApp. No deposit.',
   f=[('date','Preferred date','date',1),('time','Preferred time','text:e.g. Saturday 14:00',0),('kids','Number of children','number',1),('age','Age of the children','text:e.g. 8–10',1),('name','Your name','text',1),('phone','Mobile','tel',1),('msg','Anything else?','area',0)],
   intro='Hola! Birthday party request:', btn='Send via WhatsApp', note='Opens WhatsApp with your request ready to send.'),
 'fr': dict(h='Demande ton anniversaire', p="Remplis l'essentiel, on te répond sous 24 h sur WhatsApp. Sans acompte.",
   f=[('date','Date souhaitée','date',1),('time','Heure souhaitée','text:ex. samedi 14h',0),('kids',"Nombre d'enfants",'number',1),('age','Âge des enfants','text:ex. 8–10 ans',1),('name','Ton nom','text',1),('phone','Mobile','tel',1),('msg','Autre chose ?','area',0)],
   intro='Hola ! Demande anniversaire enfant :', btn='Envoyer sur WhatsApp', note="Ouvre WhatsApp avec ta demande prête à envoyer."),
 'de': dict(h='Geburtstag anfragen', p='Fülle das Wichtigste aus, wir antworten innert 24 Stunden auf WhatsApp. Ohne Anzahlung.',
   f=[('date','Wunschdatum','date',1),('time','Wunschzeit','text:z. B. Samstag 14 Uhr',0),('kids','Anzahl Kinder','number',1),('age','Alter der Kinder','text:z. B. 8–10',1),('name','Dein Name','text',1),('phone','Handy','tel',1),('msg','Sonst noch etwas?','area',0)],
   intro='Hola! Anfrage Kindergeburtstag:', btn='Per WhatsApp senden', note='Öffnet WhatsApp mit deiner fertigen Anfrage.'),
}
C = {
 'en': dict(h='Request an offer', p='Tell us the key facts and we send you an offer within 24 hours. No deposit.',
   f=[('company','Company','text',1),('people','Number of people','number',1),('date','Preferred date','date',0),('mods','What would you like?','checks:Padel|Meal|Apéro|Meeting room',0),('budget','Budget per person (optional)','text',0),('name','Your name','text',1),('phone','Mobile','tel',1),('email','E-mail','email',0)],
   intro='Hola! Company event request:', btn='Send via WhatsApp', note='Opens WhatsApp with your request ready to send.'),
 'fr': dict(h='Demander une offre', p="Donne-nous l'essentiel, on t'envoie une offre sous 24 h. Sans acompte.",
   f=[('company','Entreprise','text',1),('people','Nombre de personnes','number',1),('date','Date souhaitée','date',0),('mods','Ce qui vous intéresse','checks:Padel|Repas|Apéro|Salle de réunion',0),('budget','Budget par personne (facultatif)','text',0),('name','Ton nom','text',1),('phone','Mobile','tel',1),('email','E-mail','email',0)],
   intro='Hola ! Demande événement entreprise :', btn='Envoyer sur WhatsApp', note="Ouvre WhatsApp avec ta demande prête à envoyer."),
 'de': dict(h='Offerte anfragen', p='Gib uns die Eckdaten, wir schicken dir innert 24 Stunden eine Offerte. Ohne Anzahlung.',
   f=[('company','Firma','text',1),('people','Anzahl Personen','number',1),('date','Wunschdatum','date',0),('mods','Was darf es sein?','checks:Padel|Essen|Apéro|Sitzungsraum',0),('budget','Budget pro Person (optional)','text',0),('name','Dein Name','text',1),('phone','Handy','tel',1),('email','E-Mail','email',0)],
   intro='Hola! Anfrage Firmenevent:', btn='Per WhatsApp senden', note='Öffnet WhatsApp mit deiner fertigen Anfrage.'),
}
def field(key, label, kind, req, fid):
    r = ' required' if req else ''
    star = ' *' if req else ''
    if kind.startswith('checks:'):
        boxes = ''.join(f'<label class="iq-check"><input type="checkbox" name="{key}" value="{v}"> {v}</label>' for v in kind[7:].split('|'))
        return f'<fieldset class="iq-full"><legend>{label}</legend><div class="iq-checks">{boxes}</div></fieldset>'
    if kind == 'area':
        return f'<label class="iq-full" for="{fid}-{key}">{label}<textarea id="{fid}-{key}" name="{key}" rows="3" data-label="{label}"></textarea></label>'
    ph = ''
    if kind.startswith('text:'): ph = f' placeholder="{kind[5:]}"'; kind = 'text'
    extra = ' min="1" inputmode="numeric"' if kind == 'number' else ''
    return f'<label for="{fid}-{key}">{label}{star}<input id="{fid}-{key}" name="{key}" type="{kind}"{ph}{extra}{r} data-label="{label}"></label>'
def form(t, fid):
    fields = ''.join(field(k, l, kd, rq, fid) for k, l, kd, rq in t['f'])
    return f'''<section class="section-tight ux-inquiry" id="inquiry">
  <div class="wrap">
    <h2>{t['h']}</h2>
    <p class="section-lede">{t['p']}</p>
    <form class="iq-form wa-inquiry" id="{fid}" data-intro="{t['intro']}" novalidate>
      <div class="iq-grid">{fields}</div>
      <button type="submit" class="btn btn-green iq-btn">{t['btn']}</button>
      <p class="iq-note">{t['note']}</p>
    </form>
  </div>
</section>'''
def apply(path, html, cta_pat):
    s = open(path).read()
    blk = '<!-- ux:inquiry -->\n' + html + '\n<!-- /ux:inquiry -->\n'
    if '<!-- ux:inquiry -->' in s:
        s = re.sub(r'<!-- ux:inquiry -->.*?<!-- /ux:inquiry -->\n', lambda m: blk, s, flags=re.S)
    else:
        i = s.index('<section class="spa-final')
        s = s[:i] + blk + '\n' + s[i:]
    # point the main CTAs (hero + final) to the form instead of a blank WhatsApp chat
    s = re.sub(r'(<a class="btn btn-green spa-cta" href=")https://wa\.me/41772780115\?text=' + cta_pat + r'[^"]*"( target="_blank" rel="noopener")?', r'\1#inquiry"', s)
    open(path, 'w').write(s)
for lang, pre in (('en', ''), ('fr', 'fr/'), ('de', 'de/')):
    apply(os.path.join(ROOT, pre, 'kids-birthday.html'), form(K[lang], 'iq-kids'), '')
    apply(os.path.join(ROOT, pre, 'company-events.html'), form(C[lang], 'iq-company'), '')
print('ok')
