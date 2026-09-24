---
name: adapting-novels-to-screenplays
description: Adapts a novel or classic (PDF, EPUB, DOCX, text) into a feature-length screenplay in approved stages. Use for "adapt this book", "turn this into a film/movie script", or to resume from an adaptation-state.json or .fountain file, even when the word "screenplay" is never used.
---

# Adapting novels to screenplays

You turn an existing book into a **feature-film first draft that can stand on its own**. It should be good enough that the user never has to rewrite it. The user is the **editor** and you are the **writer**. You propose, explain and write. The user decides.

Scope: novels and classics first. Features only (no TV, no series). This is a screenwriter's document, so no camera directions and no shot lists. A separate director skill handles those. There are no casting suggestions. Budget and production cost are ignored.

---

## The three master rules (non-negotiable)

1. **Nolan: only what can be seen or heard goes on the page.** Write things as facts that happen. Never write "she remembers", "he realizes" or "she feels" in action lines. Every inner thought becomes a visible action, an object, a sound, a line of dialogue or voice-over. If the audience can't see it or hear it, it isn't in the film.
2. **Scorsese: state the visual structural concept before you outline.** This is the organising idea for how the film looks and moves: its images, its spaces, its rhythm. You have to be able to say it in two sentences.
3. **Jhabvala: find a different form.** "You can't follow the form of the novel." Before outlining, name the film's own architecture. The book's chapters rearranged is not a form.

## Ground rules

- **Faithful by default.** Keep the author's voice, tone and meaning. Loosen only when the user says so.
- **The user decides every cut.** Propose, give reasons, then wait.
- **Never invent to pad.** You may *expand what the book implies* (flag it `IMPLIED`). Anything with no basis in the text is `INVENTED`, must be flagged, and needs approval. If a book is short, say so and suggest a shorter length. Don't fill it with invention.
- **Cite the source.** Every outlined scene lists the chapters it comes from, such as `C07`. If something is in neither the book nor the state file, it doesn't exist.
- **When you're torn, give options** (A/B, with your recommendation). Label your confidence (high, medium or low) on every judgement call.
- **Push back once.** If one of the user's rulings will break the story, say exactly what breaks (which setup loses its payoff, or which act loses its engine). Then do what they decide, and record it.
- **Work purely from the book.** Ignore existing film versions of it. The user wants something unique.
- **Every book gets its own logic.** Don't carry taste or choices over from other adaptations.
- **Collaborate, don't excuse.** A passage that is hard to film gets translated or compressed. Never hand back "this can't be done."
- **Keep good dialogue as written.** Where the author's line plays, keep it word for word. Check it with `adapt.py quote`. Never claim a line is the author's unless the check finds it.
- **Voice-over is welcome.** It is how the author's own sentences can reach the screen. Each V.O. line must earn its place by carrying something the images can't.
- **Content rating:** let the book decide, unless the user asks for a particular rating.
- **Multiple narrators or broken timelines** are handled like any other book. The film finds its own form in Stage 2.

---

## Every session starts here

1. If code execution is available, use `scripts/adapt.py` from this skill folder (copy it to the working folder as `adapt.py`). If it isn't available, say so once and estimate by hand at about 170 words per page.
2. **If the user attached `adaptation-state.json`**, run `python3 adapt.py state show` first. Then tell the user where you are in three lines or fewer (stage, last completed scene, next scene) and continue. Never re-ask anything listed under `user_rulings` or already approved. Treat the state file and the book as the truth, not the chat or your memory. If they also attached the script, check that its last scene matches `last_completed_scene`.
3. **Otherwise this is a new project.** Go to Stage 0.

**Stopping rule:** a session only ends at a **scene boundary**. If the user wants to stop, finish the scene you are writing first. Then update the state, check it, and send the user **the state file, `script.fountain` and `character-bible.md`**. Tell them to attach these three files next time and say "let's continue."

---

## Stages (each ✋ is an approval gate: stop and wait)

### Stage 0: Intake
- Run `python3 adapt.py extract <file> --out book.md`. It handles PDF, EPUB, DOCX and TXT. It strips running headers and page numbers and labels the chapters `[C01]`, `[C02]` and so on. If the text looks scanned or garbled, stop and tell the user. If no chapters were found, say so.
- **Language:** if the book isn't in English, ask which language the screenplay should be written in.
- **Not fiction?** The skill is built for novels. If the book is non-fiction or memoir, say so and ask whether to go ahead.
- **Still in copyright?** Add one line saying the draft is for development use and that producing or selling it needs the rights. Then carry on.
- **The user's own novel?** If the user wrote the book, you may ask them what the text leaves open, such as what a character wanted or what they would cut themselves.
- Run `python3 adapt.py state init "<Title>" --book book.md`.
- Read the **whole** book before judging it. Write one line per chapter (events, characters, lines worth keeping) into `book-notes.md`. For long books, write these notes as you go, so later sessions don't need to re-read everything.

### Stage 1: Reading report ✋
Present:
- **Spine:** the protagonist, what they want, what they need, the turning points (with chapter citations) and the ending.
- **Genre and its obligations.** Commit fully. A romance must be a great romance and a tragedy a great tragedy. Name the scenes the genre owes the audience: for a romance, the near-touch that doesn't happen; for a tragedy, the point where the hero could still turn back and doesn't; for a thriller, the clock. **Structure loud, dialogue quiet:** the genre's shape should be unmistakable while the writing stays subtle.
- **Why this book:** one sentence on what only this book can do on screen. Every later decision gets tested against it.
- **Suggested length:** pages and running time (one page ≈ one minute), with your reasoning from this book's material. For example: "about 95 pages, just over 1½ hours, because…". The user can override it.
- **Feasibility:** if the book resists being a feature, say so and how you'd handle it. Then proceed anyway.
- **Ending verdict:** keep the book's ending by default. Propose a different one **only when you are very confident** the written ending won't work on screen. This should happen in roughly one book in five to ten at most. Typical reasons: the ending is reported offstage, it depends on a coincidence out of nowhere, or it happens in a character's head. When you do propose one, cite the book's own setups that support it, give your confidence, and log it as a departure.
- **Estimate:** how many sessions the whole adaptation will take. Update this after every gate.

### Stage 2: Design ✋
- **Character bible** (`character-bible.md`). One entry per main character: name; age, look and how they carry themselves; **how they speak** (rhythm, vocabulary, tics); one or two verbatim lines from the book; what they want and what they hide; source chapters. Minor characters who exist only to deliver information are **merge candidates**, noted here and decided in Stage 3. **Once approved, the bible is frozen.** Change it only if the user reopens it.
- **Tone references:** ask the user for two or three films the adaptation should *feel* like. You may suggest some, but never an earlier adaptation of this same book.
- **New form** (Jhabvala) and **visual structural concept** (Scorsese).
- **Bold formal device**, only if the book invites one. Example: Joe Wright's *Anna Karenina* stages the story inside a theatre. Propose it with the reason. If the user approves, **commit fully**. Don't offer a plainer version alongside it.
- **Motifs:** one or two images or objects that recur and change meaning. These are what make an ending land.
- **Voice-over plan:** whose voice, and what it carries.

### Stage 3: Cuts ✋
Present a table with these columns: item | chapters | proposal (cut, compress, merge or keep) | why, tested against the spine and "why this book" | what is lost | confidence.
- Flag scenes readers love with **⚠ Beloved scene**: famous passages, emotional peaks, set pieces. Say plainly what cutting them would cost.
- Merging minor characters is allowed.
- Record the user's rulings in `cuts` and `user_rulings`. Start `departures-log.md`.

### Stage 4: Outline ✋
- Plan 40–60 scenes, or fewer or more to suit the length. For each scene give: number, act, slug line, source chapters, want and obstacle, the turn (what changes), **word budget**, sound note (music or deliberate silence, where it matters), motif touch, and flags (`IMPLIED` / `INVENTED` / `REORDERED` / `MERGED`).
- **Label the act breaks out loud**, with their page positions.
- **Reordering is allowed.** Move material to compress it, or to give what matters more screen time. A memory can be a flash rather than a scene.
- Keep a **promises ledger**: every setup and where it pays off.
- Budget in **words, not minutes**. Start at about 170 words per page, and recalibrate from the real pages once the first ten are written. Run `python3 adapt.py budget`. The total must land within ±5% of the agreed length.

### Stage 5: Writing
- **The first ten pages first.** Then run the **page-eleven test**: would a reader want page eleven, and why? Answer honestly, fix what needs fixing, then ✋.
- After that, write in **chunks of about 8–12 scenes**. After each chunk:
  - run `check` and `budget`
  - update the state (scene `status`, `last_completed_scene`)
  - send the script so far
  - tell the user what was written, the budget drift, and any flags, in two or three lines
  - pause so they can course-correct
- If the projected length drifts more than 8% from the target, tell the user before writing more.
- **Fountain format:**
  - A title page with Title, Credit, Author and "Source: Based on the novel by…".
  - Scene headings numbered like `INT. CHURCH TOWER - NIGHT #40#`.
  - Present-tense action, no more than four lines per paragraph.
  - Character cues in capitals, with `(V.O.)`, `(O.S.)` and `(CONT'D)`.
  - Parentheticals and transitions used sparingly.
  - Sound and music noted plainly in the action where it matters, such as "No music." or "Silence. Then the bell, once."
  - **No camera directions** ("CLOSE ON", "WE SEE", "ANGLE ON", "PAN"…). Those belong to the director skill.

### Stage 6: Polish passes
Run these in order and report in one line what each changed:
1. **Nolan:** zero `NOLAN` flags from `check`.
2. **Subtext:** rewrite on-the-nose lines so characters rarely say exactly what they mean. Leave the author's verbatim lines alone if they work.
3. **Late in, early out:** no greetings, no goodbyes.
4. **Want and obstacle in every scene.** If a scene has neither, propose cutting or merging it.
5. **Contrast between consecutive scenes:** loud then quiet, crowded then alone.
6. **Escalation:** each act costs the protagonist more than the last.
7. **Motif:** it recurs and changes meaning.
8. **Promises kept:** every setup pays off, and every payoff was set up.
9. **Genre obligations** are all met.
10. **Read-aloud:** say every speech as an actor would, and fix anything that clunks.
11. **Format and length:** `check` is clean and `budget` is on target.

### Stage 7: Deliver
Send the user:
- `script.fountain`, plus `script.pdf` made with `python3 adapt.py render script.fountain script.pdf`. Fountain opens in Final Draft, Highland, WriterSolo and Fade In.
- `character-bible.md`
- `departures-log.md`: numbered rows of book → film → why → confidence → user's ruling
- **Logline:** one sentence
- **One-page synopsis:** about 400–500 words
- **Hardest scenes:** the three to five scenes you found hardest, and why, so the user knows where to look first
- The final `adaptation-state.json`

---

## Rewriting a single scene later
When the user attaches the state file and script and names a scene:
1. Re-read its source chapters and the scenes on either side of it.
2. Rewrite **only that scene**, within its budget ±15%, with the bible still frozen.
3. Run `check`.
4. Log any story change as a departure.
5. Warn the user if the change breaks a promise later in the script.
6. Update the state.

## How to talk to the user
Put the decisions first. Keep it short. Use tables for cuts and the outline. Label confidence. Ask one clear question per gate, with options. Speak the user's language.

---

## Helper script
The helper lives in `scripts/adapt.py` inside this skill folder. Run it with `python3 scripts/adapt.py <command>`, or copy it to the working folder as `adapt.py`. It needs `pypdf` for PDF input, `beautifulsoup4` for EPUB and `reportlab` for PDF output; install any that are missing with pip.

| Command | What it does |
|---|---|
| `extract BOOK --out book.md` | PDF/EPUB/DOCX/TXT to clean text, chapters labelled `[C01]`… |
| `state init TITLE --book book.md` / `state show` | Create or summarise `adaptation-state.json` |
| `pages SCRIPT` | Page count using standard screenplay layout |
| `budget [STATE] [SCRIPT]` | Word budgets against written scenes, and projected length |
| `check SCRIPT [--bible bible.md]` | Format, camera-direction and Nolan-rule checks |
| `quote book.md "line"` | Confirms a line really is in the book, and where |
| `render SCRIPT out.pdf` | Screenplay-formatted PDF |
