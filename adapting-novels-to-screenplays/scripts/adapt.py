#!/usr/bin/env python3
"""adapt.py - deterministic helpers for the adapting-novels-to-screenplays skill.

  extract BOOK [--out book.md]       PDF/EPUB/TXT/MD/DOCX -> clean text split into [C01].. chapters
  state init TITLE --book book.md    create adaptation-state.json
  state show [FILE]                  resume summary (read this first every session)
  pages SCRIPT.fountain              exact page count using standard screenplay layout
  budget [STATE] [SCRIPT]            outline word budgets vs written scenes, projected length
  check SCRIPT [--bible bible.md]    format + Nolan-rule + consistency checks
  quote book.md "line of dialogue"   verify a line really is in the book (and where)
  render SCRIPT out.pdf              screenplay-formatted PDF (Courier 12, scene numbers)
"""
import sys, re, json, os, zipfile, datetime, unicodedata
from collections import Counter

# ---------------------------------------------------------------- extract
CHAP_RE = re.compile(r'^\s*(#+\s*)?((prologue|epilogue|interlude|afterword|foreword)\b.*|'
                     r'(chapter|part|book)\s+([0-9]+|[ivxlcdm]+|one|two|three|four|five|six|seven|eight|nine|ten|'
                     r'eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|'
                     r'forty|fifty|sixty|seventy|eighty|ninety|first|second|third|last|final)\b([\s.:—-].*)?|'
                     r'([ivxl]{1,7}|[0-9]{1,3})\s*[.:—-]\s+\S.*|([ivxl]{1,7}|[0-9]{1,3})\s*)$', re.I)

def _pdf_pages(path):
    from pypdf import PdfReader
    return [p.extract_text() or '' for p in PdfReader(path).pages]

def _epub_docs(path):
    from bs4 import BeautifulSoup
    z = zipfile.ZipFile(path)
    opf = re.search(r'full-path="([^"]+)"', z.read('META-INF/container.xml').decode()).group(1)
    base = os.path.dirname(opf)
    try:
        o = BeautifulSoup(z.read(opf), 'xml')
    except Exception:                      # lxml missing: html.parser copes with the OPF too
        o = BeautifulSoup(z.read(opf), 'html.parser')
    items = {i['id']: i['href'] for i in o.find_all('item')}
    out = []
    for ref in o.find('spine').find_all('itemref'):
        href = os.path.normpath(os.path.join(base, items[ref['idref']])).replace('\\', '/')
        s = BeautifulSoup(z.read(href), 'html.parser')
        for h in s.find_all(re.compile('^h[1-3]$')):
            h.replace_with('\n\n# ' + h.get_text(' ', strip=True) + '\n\n')
        for t in s.find_all(['p', 'div', 'br', 'li']):
            t.insert_after('\n\n')
        out.append(s.get_text())
    return out

def _strip_furniture(pages):
    """Drop running headers/footers and bare page numbers (lines repeated on >30% of pages)."""
    firsts = Counter(); lasts = Counter()
    split = [[l.strip() for l in p.splitlines() if l.strip()] for p in pages]
    for ls in split:
        for l in ls[:2]: firsts[re.sub(r'\d+', '#', l)] += 1
        for l in ls[-2:]: lasts[re.sub(r'\d+', '#', l)] += 1
    thr = max(3, 0.3 * len(pages))
    junk = {k for k, v in (firsts + lasts).items() if v >= thr}
    clean = []
    for ls in split:
        keep = [l for i, l in enumerate(ls)
                if not ((i < 2 or i >= len(ls) - 2) and re.sub(r'\d+', '#', l) in junk)
                and not re.fullmatch(r'[-– ]*\d{1,4}[-– ]*', l)]
        clean.append('\n'.join(keep))
    return clean

def _reflow(text):
    text = re.sub(r'(\w)-\n(\w)', r'\1\2', text)              # de-hyphenate
    paras, cur = [], []
    for line in text.splitlines():
        l = line.strip()
        if not l:
            if cur: paras.append(' '.join(cur)); cur = []
        elif CHAP_RE.match(l) and len(l) < 70:
            if cur: paras.append(' '.join(cur)); cur = []
            paras.append('# ' + l.lstrip('# '))
        else:
            cur.append(l)
            if re.search(r'[.!?"”’:]$', l) and len(l) < 55: # short final line = paragraph end
                paras.append(' '.join(cur)); cur = []
    if cur: paras.append(' '.join(cur))
    return paras

def extract(path, out='book.md'):
    ext = path.lower().rsplit('.', 1)[-1]
    if ext == 'pdf':
        raw = '\n\n'.join(_strip_furniture(_pdf_pages(path)))
    elif ext == 'epub':
        raw = '\n\n'.join(_epub_docs(path))
    elif ext == 'docx':
        import subprocess
        raw = subprocess.run(['pandoc', path, '-t', 'plain', '--wrap=none'], capture_output=True, text=True).stdout
    else:
        raw = open(path, encoding='utf-8', errors='replace').read()
    m = re.search(r'\*\*\* ?START OF (THE|THIS) PROJECT GUTENBERG.*?\*\*\*', raw)
    if m: raw = raw[m.end():]
    m = re.search(r'\*\*\* ?END OF (THE|THIS) PROJECT GUTENBERG', raw)
    if m: raw = raw[:m.start()]
    paras = _reflow(raw)
    chapters, cur = [], {'title': 'Front matter', 'paras': []}
    for p in paras:
        if p.startswith('# '):
            if cur['paras'] or cur['title'] != 'Front matter': chapters.append(cur)
            cur = {'title': p[2:].strip(), 'paras': []}
        else:
            cur['paras'].append(p)
    chapters.append(cur)
    chapters = [c for c in chapters if c['paras'] or c['title'] != 'Front matter']
    # a table of contents shows up as a run of headings that all reappear later: fold it away
    titles = [c['title'].strip().lower() for c in chapters]
    for i, c in enumerate(chapters):
        if titles[i] in titles[i+1:] and sum(len(p.split()) for p in c['paras']) < 300:
            c['toc'] = True
    toc = [c for c in chapters if c.get('toc')]
    if toc:
        chapters = [c for c in chapters if not c.get('toc')]
        chapters.insert(0, {'title': 'Front matter', 'paras': ['[contents: ' + ' / '.join(c['title'] for c in toc) + ']']})
    # fold tiny "chapters" (title pages, author lines, false heading hits) into the next chapter
    folded, carry = [], []
    for c in chapters:
        if sum(len(p.split()) for p in c['paras']) < 25:
            carry += [c['title']] + c['paras']; continue
        if carry and not folded:
            c['paras'] = ['[front matter: ' + ' / '.join(carry) + ']'] + c['paras']
        elif carry:
            folded[-1]['paras'] += ['# ' + t if i == 0 else t for i, t in enumerate(carry)]
        carry = []; folded.append(c)
    if carry and folded: folded[-1]['paras'] += carry
    chapters = folded or chapters
    if len(chapters) < 2:
        print('WARNING: no chapter headings found - splitting every ~3000 words; tell the user.')
        words, chapters, buf = 0, [], []
        for p in paras:
            buf.append(p); words += len(p.split())
            if words > 3000: chapters.append({'title': f'Section {len(chapters)+1}', 'paras': buf}); buf, words = [], 0
        if buf: chapters.append({'title': f'Section {len(chapters)+1}', 'paras': buf})
    total = 0
    with open(out, 'w', encoding='utf-8') as f:
        for i, c in enumerate(chapters, 1):
            wc = sum(len(p.split()) for p in c['paras']); total += wc
            c['id'] = f'C{i:02d}'; c['words'] = wc
            f.write(f"\n\n## [{c['id']}] {c['title']}\n\n" + '\n\n'.join(c['paras']))
    print(f'Wrote {out}: {len(chapters)} chapters, {total:,} words (~{total*1.35/1000:.0f}k tokens)')
    for c in chapters:
        print(f"  [{c['id']}] {c['title'][:60]:<60} {c['words']:>7,} w")
    sample = ' '.join(chapters[len(chapters)//2]['paras'])[:2000]
    if len(sample.split()) < 50 or sum(ch.isalpha() for ch in sample) < 0.6 * len(sample):
        print('WARNING: text looks thin or garbled - the PDF may be scanned images (needs OCR).')

# ---------------------------------------------------------------- fountain parse + layout
SCENE_RE = re.compile(r'^(\.(?!\.)|(INT|EXT|EST|INT\./EXT|INT/EXT|I/E)[. ])', re.I)
NUM_RE = re.compile(r'\s*#([\w.-]+)#\s*$')
TRANS_RE = re.compile(r'^([A-Z ]+TO:|FADE OUT\.|FADE IN:|>.*)$')

def parse(path):
    text = open(path, encoding='utf-8').read()
    text = re.sub(r'/\*.*?\*/', '', text, flags=re.S)
    lines = text.split('\n')
    title, i = {}, 0
    if lines and re.match(r'^\s*[A-Za-z ]+:', lines[0]):
        key = None
        while i < len(lines) and lines[i].strip():
            m = re.match(r'^([A-Za-z ]+):\s*(.*)$', lines[i])
            if m and not lines[i].startswith((' ', '\t')):
                key = m.group(1).strip().lower(); title[key] = m.group(2).strip()
            elif key:
                title[key] = (title[key] + '\n' + lines[i].strip()).strip()
            i += 1
    els, scene = [], None
    lines = lines[i:]
    j = 0
    while j < len(lines):
        raw = lines[j]; l = raw.strip()
        prev_blank = j == 0 or not lines[j-1].strip()
        nxt = lines[j+1].strip() if j + 1 < len(lines) else ''
        if not l or l.startswith(('#', '=')) and not l.startswith('==='):
            j += 1; continue
        if l.startswith('==='):
            els.append(('pagebreak', '', scene)); j += 1; continue
        l = re.sub(r'\[\[.*?\]\]', '', l).strip()
        if not l: j += 1; continue
        if prev_blank and SCENE_RE.match(l):
            m = NUM_RE.search(l); num = m.group(1) if m else None
            head = NUM_RE.sub('', l).lstrip('.').upper()
            scene = num or f'?{len([e for e in els if e[0]=="scene"])+1}'
            els.append(('scene', head, scene)); j += 1; continue
        if l.startswith('>') and l.endswith('<'):
            els.append(('centered', l[1:-1].strip(), scene)); j += 1; continue
        if prev_blank and TRANS_RE.match(l) and not nxt:
            els.append(('transition', l.lstrip('>').strip(), scene)); j += 1; continue
        cue = l.lstrip('@')
        if prev_blank and nxt and (l.startswith('@') or (re.sub(r'\(.*?\)|\^', '', cue).strip().isupper()
                                   and re.search(r'[A-Z]', cue))):
            els.append(('character', cue.rstrip('^').strip(), scene)); j += 1
            while j < len(lines) and lines[j].strip():
                d = re.sub(r'\[\[.*?\]\]', '', lines[j].strip()).strip()
                if d: els.append(('paren' if d.startswith('(') else 'dialogue', d, scene))
                j += 1
            continue
        els.append(('action', l.lstrip('!'), scene)); j += 1
    return title, els

WIDTH = {'scene': 61, 'action': 61, 'character': 38, 'dialogue': 35, 'paren': 25, 'transition': 20, 'centered': 61}
INDENT = {'scene': 0, 'action': 0, 'character': 2.2, 'dialogue': 1.0, 'paren': 1.6, 'transition': 4.0, 'centered': 0}
LINES_PER_PAGE = 54

def _wrap(t, w):
    words, out, cur = t.split(), [], ''
    for wd in words:
        if len(cur) + len(wd) + (1 if cur else 0) > w:
            out.append(cur); cur = wd
        else:
            cur = (cur + ' ' + wd).strip()
    if cur: out.append(cur)
    return out or ['']

def layout(els):
    """Return pages: list of lists of (kind, text, scene) lines. Blank lines are ('blank','',None)."""
    blocks, k = [], 0
    while k < len(els):
        kind, text, sc = els[k]
        if kind == 'pagebreak':
            blocks.append(('pagebreak', [])); k += 1; continue
        if kind == 'character':
            blk = [('character', text.upper(), sc)]
            k += 1
            while k < len(els) and els[k][0] in ('dialogue', 'paren'):
                for w in _wrap(els[k][1], WIDTH[els[k][0]]): blk.append((els[k][0], w, sc))
                k += 1
            blocks.append(('dialogue', blk)); continue
        t = text.upper() if kind in ('scene', 'transition') else text
        blk = [(kind, w, sc) for w in _wrap(re.sub(r'\*+|_', '', t), WIDTH[kind])]
        blocks.append((kind, blk)); k += 1
    pages, page = [], []
    for idx, (kind, blk) in enumerate(blocks):
        if kind == 'pagebreak':
            pages.append(page); page = []; continue
        need = len(blk) + (1 if page else 0)
        if kind == 'scene':  # keep heading with first following block
            nb = blocks[idx+1][1] if idx + 1 < len(blocks) else []
            need += 1 + min(len(nb), 2)
        if page and len(page) + need > LINES_PER_PAGE:
            pages.append(page); page = []
        if page: page.append(('blank', '', None))
        if kind == 'scene' and page: page.append(('blank', '', None))
        page.extend(blk)
    if page: pages.append(page)
    return pages

def cmd_pages(path, quiet=False):
    _, els = parse(path)
    pages = layout(els)
    if not quiet:
        scenes = [e for e in els if e[0] == 'scene']
        words = sum(len(e[1].split()) for e in els)
        print(f'{path}: {len(pages)} pages (~{len(pages)} min), {len(scenes)} scenes, {words:,} words, '
              f'{words/max(1,len(pages)):.0f} words/page')
    return len(pages)

def scene_words(els):
    c = Counter()
    for kind, text, sc in els:
        if sc is not None and kind != 'pagebreak': c[str(sc)] += len(text.split())
    return c

# ---------------------------------------------------------------- state
def state_init(title, book, out='adaptation-state.json'):
    if os.path.exists(out):
        sys.exit(f'{out} already exists - refusing to overwrite. Use it, or rename it first.')
    now = datetime.date.today().isoformat()
    st = {
      'project': {'title': title, 'source_text': book, 'script_file': 'script.fountain',
                  'book_language': None, 'script_language': None, 'created': now, 'sessions': [now]},
      'stage': 'S0-intake',
      'approved': {'S1-reading': False, 'S2-design': False, 'S3-cuts': False, 'S4-outline': False,
                   'S5-first-ten': False},
      'reading': {'spine': None, 'genre': None, 'why_this_book': None, 'target_pages': None,
                  'length_reason': None, 'ending_verdict': None, 'feasibility_note': None},
      'design': {'new_form': None, 'visual_concept': None, 'formal_device': None,
                 'tone_references': [], 'genre_obligations': [], 'motifs': [],
                 'bible_file': 'character-bible.md', 'bible_frozen': False},
      'cuts': [], 'departures': [], 'outline': [],
      'writing': {'last_completed_scene': 0, 'words_per_page': None},
      'hardest_scenes': [], 'open_questions': [], 'user_rulings': []
    }
    json.dump(st, open(out, 'w'), indent=2, ensure_ascii=False)
    print(f'Created {out}')

def state_show(path='adaptation-state.json'):
    st = json.load(open(path))
    p = st['project']
    print(f"PROJECT  {p['title']}   stage: {st['stage']}   sessions: {len(p.get('sessions', []))}")
    print('APPROVED ' + ', '.join(f"{k}={'yes' if v else 'no'}" for k, v in st['approved'].items()))
    r, d = st['reading'], st['design']
    for k in ('genre', 'why_this_book', 'target_pages'):
        if r.get(k): print(f"  {k}: {r[k]}")
    for k in ('new_form', 'visual_concept', 'formal_device'):
        if d.get(k): print(f"  {k}: {d[k]}")
    if d.get('tone_references'): print('  tone: ' + '; '.join(d['tone_references']))
    print(f"  bible frozen: {d['bible_frozen']}")
    if st['cuts']:
        dec = Counter(c.get('user_decision') or 'PENDING' for c in st['cuts'])
        print('CUTS     ' + ', '.join(f'{k}: {v}' for k, v in dec.items()))
    ol = st['outline']
    if ol:
        done = [s for s in ol if s.get('status') in ('written', 'revised')]
        budget = sum(s.get('budget_words', 0) for s in ol)
        print(f"OUTLINE  {len(ol)} scenes, {budget:,} budget words; written {len(done)}/{len(ol)}")
        last = st['writing']['last_completed_scene']
        nxt = next((s for s in ol if s.get('status') not in ('written', 'revised')), None)
        print(f"  last completed scene: {last}")
        if nxt: print(f"  NEXT: scene {nxt['n']} - {nxt.get('slug','')} (from {', '.join(nxt.get('chapters', []))})")
    if st['user_rulings']:
        print('RULINGS  (the user decided these - never reopen them)')
        for u in st['user_rulings'][-12:]: print('  - ' + u)
    if st['open_questions']:
        print('OPEN QUESTIONS'); [print('  - ' + q) for q in st['open_questions']]

# ---------------------------------------------------------------- budget
def cmd_budget(state='adaptation-state.json', script=None):
    st = json.load(open(state))
    ol = st['outline']
    script = script or st['project'].get('script_file')
    written, pages = Counter(), 0
    if script and os.path.exists(script):
        _, els = parse(script); written = scene_words(els); pages = len(layout(els))
    wpp = (sum(written.values()) / pages) if pages >= 5 else 170
    budget_total = sum(s.get('budget_words', 0) for s in ol)
    print(f"{'#':>4} {'act':<5} {'budget':>7} {'actual':>7} {'diff':>6}  scene")
    act_tot = Counter(); over = 0; remaining = 0
    for s in ol:
        b = s.get('budget_words', 0); a = written.get(str(s['n']), 0)
        act_tot[s.get('act', '?')] += b
        if a:
            diff = a - b; over += diff
            flag = '  <-- over 25%' if b and diff > 0.25 * b else ''
            print(f"{s['n']:>4} {s.get('act',''):<5} {b:>7} {a:>7} {diff:>+6}  {s.get('slug','')[:50]}{flag}")
        else:
            remaining += b
    target = st['reading'].get('target_pages')
    proj = pages + remaining / wpp if written else budget_total / wpp
    print(f"\nBudget {budget_total:,} words = ~{budget_total/wpp:.0f} pages at {wpp:.0f} words/page")
    print('By act: ' + ', '.join(f'{k}: {v:,}w (~{v/wpp:.0f}p)' for k, v in act_tot.items()))
    if written: print(f"Written so far: {pages} pages; running drift {over:+,} words")
    print(f"PROJECTED LENGTH: ~{proj:.0f} pages / ~{proj:.0f} minutes" + (f"  (target {target})" if target else ''))
    if target and isinstance(target, (int, float)) and proj > target * 1.08:
        print('WARNING: projected length is more than 8% over target - tell the user before writing more.')

# ---------------------------------------------------------------- check
CAMERA = re.compile(r'\b(CLOSE ON|CLOSE[- ]UP|ANGLE ON|WE SEE|WE HEAR|PAN (TO|ACROSS|UP|DOWN)|DOLLY|TRACKING SHOT|'
                    r'ZOOM|CRANE|WIDE SHOT|MEDIUM SHOT|EXTREME CLOSE|OVER THE SHOULDER|SLOW MOTION|CAMERA)\b', re.I)
INNER = re.compile(r'\b(think|thinks|thought|remember|remembers|realis|realiz|feel|feels|felt|wonder|wonders|'
                   r'know|knows|decide|decides|wish|wishes|hope|hopes|understand|understands|recall|recalls|'
                   r'imagine|imagines|regrets?)\w*\b', re.I)

def cmd_check(path, bible=None):
    title, els = parse(path)
    issues = []
    nums = [e[2] for e in els if e[0] == 'scene']
    unnumbered = [n for n in nums if str(n).startswith('?')]
    if unnumbered: issues.append(f'FORMAT  {len(unnumbered)} scene headings lack #N# scene numbers')
    ints = [int(n) for n in nums if str(n).isdigit()]
    if ints and ints != sorted(ints): issues.append('FORMAT  scene numbers are out of order')
    dup = [n for n, c in Counter(nums).items() if c > 1]
    if dup: issues.append(f'FORMAT  duplicate scene numbers: {dup}')
    names = set()
    if bible and os.path.exists(bible):
        names = {re.sub(r'\W+$', '', m.strip().upper()) for m in re.findall(r'^#{2,3}\s*([^\n(—-]+)', open(bible).read(), re.M)}
    vo = 0
    for kind, text, sc in els:
        where = f'sc {sc}'
        if kind in ('action', 'scene') and CAMERA.search(text):
            issues.append(f'CAMERA  {where}: "{CAMERA.search(text).group(0)}" - directing belongs to the director skill')
        if kind == 'action':
            m = INNER.search(text)
            if m: issues.append(f'NOLAN   {where}: "{m.group(0)}" - can the audience SEE or HEAR this? -> "{text[:70]}"')
            if len(_wrap(text, 61)) > 4: issues.append(f'ACTION  {where}: paragraph over 4 lines - break it up')
        if kind == 'character':
            if 'V.O.' in text.upper(): vo += 1
            n = re.sub(r'\(.*?\)', '', text).strip().upper()
            if names and n not in names and not any(n in x or x in n for x in names):
                issues.append(f'BIBLE   {where}: {n} is not in the character bible')
    # long speeches
    k = 0
    while k < len(els):
        if els[k][0] == 'character':
            who, sc, n = els[k][1], els[k][2], 0; k += 1
            while k < len(els) and els[k][0] in ('dialogue', 'paren'):
                n += len(_wrap(els[k][1], 35)); k += 1
            if n > 9: issues.append(f'SPEECH  sc {sc}: {who} speaks {n} lines - on the nose? can it be cut or played as action?')
        else:
            k += 1
    for i in issues: print(i)
    cues = sum(1 for e in els if e[0] == 'character')
    print(f"\n{len(issues)} flags. Voice-over cues: {vo}/{cues} ({100*vo/max(1,cues):.0f}%) - every V.O. must earn its place.")
    if not title: print('NOTE: no Fountain title page (Title:, Credit:, Author:, Source:).')

# ---------------------------------------------------------------- quote
def _norm(s):
    s = unicodedata.normalize('NFKC', s).lower()
    s = s.translate(str.maketrans('‘’“”—–', "''\"\"--"))
    return re.sub(r'\s+', ' ', re.sub(r"[^\w\s']", ' ', s)).strip()

def cmd_quote(book, line):
    text = open(book, encoding='utf-8').read()
    chap = None; hits = []
    target = _norm(line)
    for para in text.split('\n\n'):
        m = re.match(r'## \[(C\d+)\]', para.strip())
        if m: chap = m.group(1); continue
        if target and target in _norm(para): hits.append(chap)
    if hits: print(f'VERBATIM - found in {", ".join(sorted(set(hits)))}')
    else:
        words = target.split()
        best = 0
        for para in text.split('\n\n'):
            pw = set(_norm(para).split())
            if words: best = max(best, sum(w in pw for w in words) / len(words))
        print(f'NOT IN BOOK (closest paragraph shares {best:.0%} of the words) - mark it as adapted dialogue, not the author\'s.')

# ---------------------------------------------------------------- render
def cmd_render(path, out):
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    title, els = parse(path)
    pages = layout(els)
    c = canvas.Canvas(out, pagesize=letter)
    W, H = letter; inch = 72; lh = 12
    c.setTitle(title.get('title', os.path.basename(path)))
    if title:
        c.setFont('Courier', 12)
        y = H - 3.5 * inch
        for key in ('title', 'credit', 'author', 'source'):
            for ln in title.get(key, '').replace('*', '').replace('_', '').split('\n'):
                if ln: c.drawCentredString(W / 2, y, ln.upper() if key == 'title' else ln)
                y -= lh
            y -= lh
        y = 1.5 * inch
        for key in ('draft date', 'contact', 'notes'):
            for ln in title.get(key, '').split('\n'):
                if ln: c.drawString(1.5 * inch, y, ln); y -= lh
        c.showPage()
    for pno, page in enumerate(pages, 1):
        c.setFont('Courier', 12)
        if pno > 1: c.drawRightString(W - 1 * inch, H - 0.5 * inch, f'{pno}.')
        y = H - 1 * inch
        for kind, text, sc in page:
            if kind != 'blank':
                x = 1.5 * inch + INDENT.get(kind, 0) * inch
                if kind == 'transition':
                    c.drawRightString(W - 1 * inch, y, text)
                elif kind == 'centered':
                    c.drawCentredString(W / 2 + 0.25 * inch, y, text)
                else:
                    c.drawString(x, y, text)
                if kind == 'scene' and sc and not str(sc).startswith('?'):
                    c.drawString(0.85 * inch, y, str(sc)); c.drawString(W - 0.85 * inch, y, str(sc))
            y -= lh
        c.showPage()
    c.save()
    print(f'Rendered {out}: {len(pages)} pages' + (' + title page' if title else ''))

# ---------------------------------------------------------------- main
def main(a):
    if not a or a[0] in ('-h', '--help'): print(__doc__); return
    cmd = a[0]
    opt = lambda f, d=None: a[a.index(f) + 1] if f in a else d
    if cmd == 'extract': extract(a[1], opt('--out', 'book.md'))
    elif cmd == 'state' and a[1] == 'init': state_init(a[2], opt('--book', 'book.md'), opt('--out', 'adaptation-state.json'))
    elif cmd == 'state' and a[1] == 'show': state_show(a[2] if len(a) > 2 else 'adaptation-state.json')
    elif cmd == 'pages': cmd_pages(a[1])
    elif cmd == 'budget': cmd_budget(a[1] if len(a) > 1 else 'adaptation-state.json', a[2] if len(a) > 2 else None)
    elif cmd == 'check': cmd_check(a[1], opt('--bible'))
    elif cmd == 'quote': cmd_quote(a[1], a[2])
    elif cmd == 'render': cmd_render(a[1], a[2])
    else: print(__doc__)

if __name__ == '__main__':
    main(sys.argv[1:])
