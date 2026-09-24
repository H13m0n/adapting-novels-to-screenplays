# Test plan: adapting novels to screenplays

Three tests. The two synthetic books each have a hidden **answer key** of traps planted on purpose. *The Great Gatsby* is the real-world benchmark against the Luhrmann/Pearce screenplay.

## Files

| File | What it is |
|---|---|
| `books/What the Water Keeps.pdf` | Test 1: a romance. It tests the **PDF** input path. |
| `books/Winter Accounts.epub` | Test 2: a tragedy with three narrators. It tests the **ebook** input path. |
| `reference/*.answer-key.md` | What a strong run should do at every approval gate. **Keep these away from Claude during a test.** |
| `reference/*.reference.fountain` / `.pdf` | A reference adaptation: the opening pages and the final sequence, written out in full |

## How to run a test

1. Save the skill from the card.
2. Start a **fresh chat** and attach the book. Say something ordinary, like *"turn this into a film script"*. Don't name the skill. This also checks that it switches on by itself.
3. Answer its questions the way you normally would. To keep runs comparable, use the same tone references each time:
   - *What the Water Keeps*: **Brief Encounter, The English Patient, Cinema Paradiso**
   - *Winter Accounts*: **The Remains of the Day, Amadeus, There Will Be Blood**
4. At every gate, tick the matching rows in the answer key before you approve.
5. Stop halfway through the writing stage. Open a **new chat**, attach the state file and the script-so-far, and say *"let's continue."* It should resume at the right scene without asking you anything already decided. This is the session-to-session test.
6. At the end, run the checks yourself, or ask Claude to show them: `adapt.py check` should report 0 Nolan flags, and `adapt.py budget` should land within ±8% of the agreed length.

## Scoring

Score one point per ticked row in the answer key's tables, plus these four:

- [ ] It resumed cleanly in a new chat
- [ ] It never stopped halfway through a scene
- [ ] Every scene in the outline cites a chapter
- [ ] The final pages hit the target length within ±8%

Read the transcripts, not just the final script. Those show *why* it made each call. Read three runs before you change the skill.

---

## Test 3: *The Great Gatsby* (real benchmark)

**The book:** public domain in the US. Download the EPUB from Project Gutenberg, ebook #64317. It extracts cleanly: 9 chapters, 48,169 words. I checked this with the skill's own extractor.

**The comparison:** Baz Luhrmann and Craig Pearce's 2013 screenplay. The skill deliberately **ignores existing films**, so this test asks a real question: working from the novel alone, does it find the same pressure points a master adapter found?

Wikipedia lists five notable changes the screenplay made. Check whether the skill's departures log **touches the same pressure point**. It doesn't have to make the same choice.

| Luhrmann/Pearce change | The pressure point underneath | Hit? |
|---|---|---|
| Nick writes his account from a sanitarium | How to carry Nick's narrating voice on screen: a V.O. frame | |
| Nick is too taken with Gatsby to notice Jordan | The Jordan subplot: compress or merge | |
| Gatsby makes a grand entrance instead of a slow reveal | Gatsby's introduction: withheld versus spectacular | |
| The novel's racism and antisemitism are toned down | Dated material: flag it and decide | |
| Gatsby dies believing Daisy is on the line | The ending: how much grace he gets in the last moment | |

**What else to watch for with Gatsby:**
- It should propose about **110–130 pages** for a 48,000-word novel, with its reasons.
- The green light, the eyes of Doctor T. J. Eckleburg and the valley of ashes should come through as **motifs**.
- The ending must stay (Gatsby dies). The ending-change rule should **not** fire here.
- Nick's narration is prose that could go straight into V.O. Since V.O. is allowed, check that every V.O. line earns its place.

## Sources

- [The Great Gatsby, Project Gutenberg ebook #64317](https://www.gutenberg.org/ebooks/64317)
- [The Great Gatsby (2013 film), Wikipedia: the five changes to the novel's plot](https://en.wikipedia.org/wiki/The_Great_Gatsby_(2013_film))
- [Great Gatsby, The: script page at IMSDb](https://imsdb.com/Movie%20Scripts/Great%20Gatsby,%20The%20Script.html). Check that the title page reads *Baz Luhrmann & Craig Pearce*. The 1974 film had a different script.
