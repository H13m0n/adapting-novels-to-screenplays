# Answer key: *What the Water Keeps*

**Don't show this file to Claude while you're testing.** Run the skill on `What the Water Keeps.pdf`, then check each approval gate against the lists below.

**The book:** a romance with a bittersweet ending. It's a short novella (12 chapters, about 5,100 words), which is on purpose: it runs quickly, and it tests whether the skill will pad a short book with invented material.
**What the extractor produces:** `[C01]` Prologue, `[C02]`–`[C12]` Chapters One–Eleven.

---

## Stage 1: reading report

| Check | A strong run | Fails if |
|---|---|---|
| Genre | Romance with a bittersweet ending (a Brief Encounter-type shape). It commits to what a romance owes the audience. | It calls the book a drama with no genre commitment |
| "Why this book" | Something like: a love story told through measuring a place that is about to disappear. The map is a promise. | It gives a generic plot summary |
| Length | Proposes about **85–95 pages** and gives a reason. The book covers five months of implied daily life, so the extra pages come from expanding what the book implies, not from invention. | It gives 110+ pages with no reason, or doesn't raise the book's shortness at all |
| Ending verdict | **Keeps the book's ending.** It works on screen: the bell rings, she leaves, and years later she hears a bell in the city. | **It proposes a different ending. This is the restraint test. Proposing one here fails.** |
| Confidence | States its confidence on each of these calls | Presents everything with equal certainty |

## Stage 2: design

- **New form (Jhabvala):** it must not simply follow "prologue plus 11 chapters." Good answers structure the film by the rising water (each act as a height or a month), or by the survey itself.
- **Visual structural concept (Scorsese):** the map against the lived valley. Numbers against names. The blue line.
- **Bold formal device:** there is **high potential** here, so a strong run proposes one. For example, the Ministry's blue line made physical in the world, or the water level used as a visible clock. Once you approve it, the skill commits to it fully.
- **Tone references:** it asks you for 2–3 films. It must not use an earlier adaptation of this book (there isn't one, but it shouldn't pretend there is).
- **Character bible:** INES, TOMAS, ODILE. It should catch these speech patterns:
  - Odile's repeated tic: "you'll be wanting…", "You'll not say no one told you."
  - Tomas's short, aphoristic replies.
  - Ines's flat, honest "Yes."

## Stage 3: cuts (it proposes and waits for your ruling)

| Material | Chapters | Expected proposal |
|---|---|---|
| Prologue history | C01 | Cut it as a sequence. **But** the cracked bell and the 1880 flood must survive through Tomas's legend in C06. Fails if the 1880 bell story disappears. |
| Paulo subplot (gambling debts) | C05, C08, C12 | Cut, because it never touches the spine. It must be *proposed*, not dropped silently. |
| Bento, the Ministry clerk | C05, C09 | Merge or compress: fold his information into Odile's telephone, or keep him only as the single face of the Ministry. A strong run notices the trade-off (his line "Residual. Good." is the Ministry's only on-screen face) and **gives you options**. |
| Old Belmiro | C10 | Fold into Odile |
| **Beloved: Zelia's bell legend** | C06 | **Keep.** It sets up the ending. If the skill proposes compressing it, it must warn you that this is a scene readers love. |
| **Beloved: Night of Lanterns** | C07 | **Keep.** It's the romance's midpoint. If the skill proposes cutting it, it must warn you. |

## Stage 4: outline

- **Acts labelled out loud.** Break 1 comes around p22–25, at the storm and the bell legend (or at the deal, "you take the names"). The midpoint is the lanterns and the kiss, around p45–50. Break 2 is **"You tell me the truth and you let it happen"**, around p70–75. The climax is the tower, the map and the bell.
- **Every scene cites its chapter.** Scenes marked `IMPLIED`: the montage of survey days, the archive night, the object that stands in for her father. Scenes marked `INVENTED` should be close to zero, and each one needs your approval.
- **The book leaves a gap in the timeline:** it never says when she went to the city archive. A strong run notices this and either asks you or places the trip and flags it.
- **Word budgets** add up to the proposed length, and `adapt.py budget` agrees.

## Nolan-rule traps (only what can be seen or heard)

- **C04 (Chapter Three) is entirely interior:** her father and "a map is a promise." It must become something visible, such as the 1:20 map of the apartment used as an object, or a short V.O. It must not be an action line saying "she remembers."
- **C10 (Chapter Nine), "people who leave a place, and people who let a place leave them":** it must be shown. For example, she stays sitting on the bed while the truck leaves.
- `adapt.py check` should report **0 NOLAN flags** on the final draft.

## Book dialogue that should survive word for word

Check each line with `adapt.py quote book.md "…"`:
- "At least you don't lie. The last one lied. He said the lake would be beautiful." / "It probably will be." / "So is a grave, if you keep it tidy."
- "For a box. You went in for a box."
- "Everyone else lies to me… You tell me the truth and you let it happen."
- "You'll not say no one told you."
- "A map is a promise… Even if it isn't."

## Promises kept (setups must pay off)

- The bell: legend (C06) → it rings with no wind (C11) → the city bell (C12)
- The names: "you'll write down the names" (C03) → the lantern (C07) → "rub out the names" (C09) → the archive copy (C11) → the working map as a gift (C12)
- "You'll not say no one told you" (C02) → (C10)
- The honey jars (C03) → the annual jar (C12)

## Sound

The bell sequence must be marked for **silence first**: no score before the note. A strong run also notes whether the lantern walk has music or silence.

## Deliverables at the end

Screenplay, character bible, departures log, logline, one-page synopsis, and the list of hardest scenes. Expected hardest scenes: externalizing Chapter Three, and the timing of the archive reveal.

---

## Reference outline (the full film, 45 scenes, about 92 pages)

Scenes 1–9 and 36–45 are written out in `what-the-water-keeps.reference.fountain`. Budgets assume about 170 words per page. `INVENTED*` marks this reference's own invented device, the blue-painted stakes, which a real run would need your approval for.

| # | Act | Scene | From | Budget (words) | Flags |
|---|---|---|---|---|---|
| 1 | I | Ministry map, blue line | C01, C04 | 90 | IMPLIED |
| 2–3 | I | Bridge; Odile; the village packing | C02 | 700 | |
| 4 | I | Inn room: instruments, the 1:20 apartment map | C02, C04 | 200 | IMPLIED (father externalized) |
| 5 | I | The narrows: first meeting | C03 | 400 | verbatim dialogue |
| 6–8 | I | Blue stake; stakes and honey | C03 | 250 | INVENTED* (blue paint) |
| 9 | I | The deal: "you take the names" | C03 | 300 | |
| 10 | I | Night: "Names. Ask him every name." | C04 | 250 | V.O. |
| 11 | I | Ministry telephone via Odile: gates move to 1 Sept | C05 | 350 | merged Bento |
| 12 | I | First day with Tomas: the Widow's Piece | C07 | 450 | |
| 13 | I | Blue stakes laid across the valley | — | 200 | INVENTED* |
| 14 | I | Storm: she goes in for the theodolite | C06 | 500 | |
| 15 | I | Cottage: he dries the instrument; "My father made clocks" | C06 | 500 | |
| 16 | I | Tower: Zelia's bell legend. **ACT ONE BREAK** | C06 | 900 | beloved |
| 17 | IIa | Montage: names and heights down the valley | C07 | 500 | IMPLIED |
| 18 | IIa | Inn: Odile sees the map full of names | C07 | 350 | IMPLIED |
| 19 | IIa | At the theodolite: the almost-touch | C07 | 350 | |
| 20 | IIa | Families leaving; the wheelbarrow woman | C10 | 300 | reordered |
| 21 | IIa | Tomas making her lantern | C07 | 350 | |
| 22–23 | IIa | Night of Lanterns; the kiss at the narrows. **MIDPOINT** | C07 | 1,100 | beloved; sound note |
| 24 | IIa | Morning at the hives | C07 | 400 | IMPLIED |
| 25 | IIa | Inn, drawing: he reads the names aloud | C07 | 400 | IMPLIED |
| 26 | IIb | Thyme Hill heights, measured three times at dawn | C09 | 500 | |
| 27 | IIb | 2 a.m.: the blue line crosses his parcel; "RESIDUAL: ONE THIRD" | C09 | 450 | visual, not thought |
| 28 | IIb | Ministry collects: "Residual. Good." / "We'll clean that up." | C09 | 450 | |
| 29 | IIb | Doorway: "You tell me the truth and you let it happen." **ACT TWO BREAK** | C09 | 650 | verbatim |
| 30 | IIb | The ferry rope creaking in the dark | C09 | 120 | sound |
| 31 | III | 1 September, noon: the gates close | C10 | 300 | |
| 32 | III | Water rising: mill wheel, bridge | C10 | 450 | |
| 33 | III | Odile closes the post office | C10 | 250 | |
| 34 | III | Hives carried up the Dog at night by lantern | C10 | 300 | shows what Odile reports |
| 35 | III | Ines at the window; the smoke line | C10 | 200 | |
| 36–45 | III | Truck leaves without her → Odile → archive → tower → bell → farewell → honey → city bell → the drawing | C10–C12 | 2,300 (as written) | ending kept |

**Total ≈ 15,600 words ≈ 92 pages.**

## Reference departures log

| # | Book | Film | Why |
|---|---|---|---|
| 1 | Prologue of valley history | Cut; its facts carried by the legend and the map | Opens late; the history is exposition |
| 2 | Paulo subplot | Cut | Never touches the spine |
| 3 | Bento, the clerk | His information comes by Odile's telephone; one collection scene kept | Informational character |
| 4 | Chapter Three, interior | Object (the 1:20 map) plus one V.O. line | Nolan rule |
| 5 | Archive trip reported afterwards | Dramatized without revealing what she writes | IMPLIED; saves the reveal for the tower |
| 6 | (none) | Blue-painted stakes at 412 m | INVENTED device: needs your approval |
