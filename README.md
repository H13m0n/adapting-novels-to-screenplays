# Adapting Novels to Screenplays: a Claude skill

Turn a novel, novella or classic into a **feature-film screenplay**, working as a partnership: **you're the editor, Claude is the writer.** Claude proposes and explains every choice. You decide.

It reads a PDF, EPUB, DOCX or plain-text book. It works in stages you approve, and it can pick up where you left off in a later session. What you get at the end is a formatted screenplay in Fountain and PDF, along with the documents that explain it.

## What makes it different

Most book-to-script tools treat adaptation as **reformatting**. This skill treats it as **editing**:

- **Three master rules.**
  - *Nolan:* only what can be seen or heard goes on the page.
  - *Scorsese:* state the visual structural concept before outlining.
  - *Jhabvala:* "You can't follow the form of the novel." Find the film's own form.
- **You approve every cut.** Claude proposes cuts, merges and compressions, with a reason and a confidence level for each. It warns you before touching a scene readers love. If a cut would break the story, it pushes back once, then does what you decide.
- **No invented padding.** Every scene cites the chapter it comes from. Anything expanded from what the book implies is flagged `IMPLIED`, and anything with no basis in the text is flagged `INVENTED`.
- **Genre commitment.** A romance is played as a great romance and a tragedy as a real tragedy. The structure is loud and the dialogue stays quiet.
- **Length planned in words.** Each scene gets a word budget, and a script counts real screenplay pages so the film lands on the length you agreed.
- **Built for long projects.** A progress file carries everything across sessions. A session always stops at the end of a scene, never halfway through one.
- **A full set of outputs:** the screenplay, a character bible, a log of every change from the book, a logline, a one-page synopsis, and the scenes Claude found hardest to write.

## The stages

| Stage | What you get | You approve? |
|---|---|---|
| 0. Intake | Clean text split into chapters; language, copyright and fiction checks | — |
| 1. Reading report | The story's backbone, the genre, "why this book", a suggested length, an ending verdict | ✋ |
| 2. Design | Character bible, tone references, new form, visual concept, an optional bold formal device | ✋ |
| 3. Cuts | A table of proposed cuts, merges and compressions, with ⚠ on scenes readers love | ✋ |
| 4. Outline | 40–60 scenes with act breaks labelled, a word budget per scene, and a list of every setup and where it pays off | ✋ |
| 5. Writing | The first 10 pages, then the "page-eleven test", then chunks of 8–12 scenes | ✋ after the first 10 pages |
| 6. Polish | Passes for visibility, subtext, late-in/early-out, contrast, escalation, motif, promises kept, and a read-aloud check | — |
| 7. Deliver | `.fountain`, `.pdf`, character bible, departures log, logline, synopsis, hardest scenes | — |

## Install

**Claude apps (web, desktop).** Zip the `adapting-novels-to-screenplays` folder, or download the zip from Releases. Then go to **Customize → Skills → Upload a skill**. Code execution needs to be turned on.

**Claude Code.** Copy the folder into `~/.claude/skills/`:

```bash
git clone https://github.com/<you>/adapting-novels-to-screenplays.git
cp -r adapting-novels-to-screenplays/adapting-novels-to-screenplays ~/.claude/skills/
```

## Use

Attach a book and say something like *"turn this into a film script."* To pick up in a later session, attach `adaptation-state.json`, `script.fountain` and `character-bible.md`, then say *"let's continue."*

## Test kit

The `test-kit/` folder has two original novellas, each with planted traps and an answer key:

- *What the Water Keeps*: a romance, as a PDF.
- *Winter Accounts*: a tragedy with three narrators, as an EPUB.

It also has reference screenplays for both books, and a benchmark plan for *The Great Gatsby*, which compares the skill's changes against the 2013 Luhrmann/Pearce screenplay. See [`test-kit/TEST-PLAN.md`](test-kit/TEST-PLAN.md).

## Scope

This skill covers features only: no TV. It writes screenplay format only, so there are no camera directions and no shot lists; those belong to a separate director skill. It doesn't suggest casting. It works from the book alone and ignores earlier film versions.

Drafts of books still in copyright are for development use only. Producing or selling one needs the rights.

## Credits

The craft principles are paraphrased from public interviews: Christopher Nolan on *Scriptnotes* episode 622, Martin Scorsese's MasterClass, and Ruth Prawer Jhabvala. The test novellas are original works written for this repository.

## License

MIT. See [LICENSE](LICENSE).
