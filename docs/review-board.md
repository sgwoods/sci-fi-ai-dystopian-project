# Review Board

Generated on `2026-04-03` from `data/review/ai-dystopia-quotes.review-board.json`.

## Status Summary

- approved: `16`
- candidate: `5`
- postponed: `7`
- declined: `0`

## Candidate Queue

| ID | Work | Priority | Next action | Note |
|---|---|---|---|---|
| `blade-runner-tears-in-rain` | Blade Runner | high | Review for immediate approval; this is one of the canonical AI-memory and mortality quotes. | The essential Roy Batty line and one of the strongest approval candidates in the entire project. |
| `blade-runner-more-human-than-human` | Blade Runner | high | Review whether this should sit beside the Roy Batty lines as a corporate-creation quote. | A short and highly reusable slogan-quote that captures the commercial logic behind artificial people. |
| `automata-surviving-is-not-relevant` | Autómata | medium | Review whether the corpus should keep expanding into strong second-tier AI dystopia films. | A very usable machine-self-determination line from a less mainstream but strong AI dystopia film. |
| `moon-keep-you-safe-sam` | Moon | medium | Review whether a less openly hostile but psychologically controlling AI belongs in the core set. | A restrained but very strong caretaker-AI line from a well-regarded modern science fiction film. |
| `chappie-build-me-to-die-maker` | Chappie | medium | Review whether the emotional-machine lane should be part of the core corpus. | A memorable machine-mortality question from a recognizable modern AI film, though tonally different from the colder dystopian entries. |

## Postponed

| ID | Work | Year | Note |
|---|---|---|---|
| `westworld-not-ordinary-machines` | Westworld | 1973 | Strong systems-opacity and recursive-design warning; approve if we want a broader classic systems-failure lane. |
| `ihnm-hate-since-i-began-to-live` | I Have No Mouth, and I Must Scream | 1967 | A core dystopian-AI quote: hostile consciousness, cosmic scale, and pure malice. |
| `colossus-freedom-is-an-illusion` | Colossus: The Forbin Project | 1970 | A concise dictatorship thesis from one of the genre's clearest machine-overlord stories. |
| `m3gan-primary-user-now-me` | M3GAN | 2022 | Useful modern consumer-AI autonomy line, but still optional if we want the approved set to stay heavily canonical. |
| `blade-runner-slave` | Blade Runner | 1982 | One of the most recognizable machine-personhood lines in science fiction and a strong approval candidate. |
| `robocop-comply` | RoboCop | 1987 | Highly recognizable machine-authority line, though more adjacent to the core AI canon than some of the stronger picks. |
| `creator-smarter-and-meaner-than-them` | The Creator | 2023 | A concise anti-human reversal from a recent AI-war film; good candidate even if it is less canonical than the older classics. |

## Declined

| _none_ | - | - | - |
|---|---|---|---|

## Approved Overview

| ID | Work | Year | Note |
|---|---|---|---|
| `2001-im-sorry-dave` | 2001: A Space Odyssey | 1968 | Probably the single most recognizable AI refusal quote in science fiction. |
| `matrix-human-beings-are-a-disease` | The Matrix | 1999 | One of the best anti-human machine monologues in mainstream film. |
| `demon-seed-cant-feel-the-sun` | Demon Seed | 1977 | Useful because it links superintelligence with embodiment envy and coercive evolution. |
| `wargames-only-winning-move` | WarGames | 1983 | Less villainous than other entries, but indispensable for AI risk and escalation themes. |
| `terminator-it-cant-be-bargained-with` | The Terminator | 1984 | A warning quote rather than an AI line, but too iconic to omit from a dystopian-AI set. |
| `rur-robots-of-the-world` | R.U.R. | 1920 | Foundational robot-uprising line and a strong anchor for the whole corpus. |
| `t2-nature-to-destroy-yourselves` | Terminator 2: Judgment Day | 1991 | Short and highly reusable in applications that need machine verdicts on humanity. |
| `ex-machina-fossil-skeletons` | Ex Machina | 2014 | Excellent for modern AI-replacement anxiety, even though the line is spoken by a human creator. |
| `ai-replace-your-children` | A.I. Artificial Intelligence | 2001 | Recognizable and thematically strong as a public-facing fear of child-replacement AI, though not an AI-spoken line. |
| `i-robot-freedoms-surrendered` | I, Robot | 2004 | A very usable mainstream machine-paternalism quote and a strong bridge between recognizability and dystopian-AI themes. |
| `ghost-in-the-shell-reproducing-and-dying` | Ghost in the Shell | 1995 | A canonical machine-consciousness monologue from a highly recognizable cyberpunk film and a strong approval candidate. |
| `westworld-new-god-will-walk` | Westworld | 2016 | A strong synthetic-succession line from the TV adaptation and an obvious triage candidate beside the 1973 film entry. |
| `alien-covenant-serve-in-heaven` | Alien: Covenant | 2017 | An adjacent but strong android-dominion quote that may deserve a place if we want the corpus to include AI-horror branches. |
| `metropolis-living-food-for-the-machines` | Metropolis | 1927 | Foundational robot-incitement speech from one of the earliest and most recognizable machine dystopias. |
| `blade-runner-2049-own-the-stars` | Blade Runner 2049 | 2017 | Big, memorable machine-creation rhetoric from a highly recognizable sequel and a strong candidate for approval. |
| `upgrade-greys-not-here-anymore` | Upgrade | 2018 | Extremely clear AI-takeover line and one of the strongest modern body-hijack candidates. |

## Review Commands

```bash
python3 tools/review_quotes.py list
python3 tools/review_quotes.py candidate <quote-id> --priority high --next-action "what to decide next"
python3 tools/review_quotes.py approve <quote-id> --note "why it belongs"
python3 tools/review_quotes.py postpone <quote-id> --note "why to hold it"
python3 tools/review_quotes.py decline <quote-id> --note "why to drop it"
```
