# Naskah Editorial Visual Direction — Session Reference

## Status

**Exploration only.** Naskah has not selected a final visual identity. Do not treat any palette, typography pair, sample, or series name below as approved without TM's explicit confirmation.

## Brand context

Naskah is a trusted academic companion for students and early researchers. It makes research, methodology, statistics, academic writing, and the research journey clearer, more practical, and more human.

Target emotional response:

- “Oh, sekarang gue lebih ngerti.”
- “Oke, sekarang gue tahu harus ngapain.”

The brand must be smart, human, calm, helpful, practical, slightly witty, and credible. It must not look like a thesis mill, generic academic-service account, meme account, corporate brochure, or AI content farm.

## User feedback to retain

TM rejected early rendered mockups because they felt:

- insufficiently creative
- visibly AI-generated
- too rigid, sterile, and box/card-system driven
- not human-oriented enough

Future visual exploration should therefore avoid offering barely differentiated palettes over the same centered-card layout. Start with real reference study and produce distinct visual grammars.

## Working direction to explore

A promising territory is **human editorial academic**:

- Calm, high-taste, contemporary editorial sensibility
- Strong type-led storytelling, not decorative UI
- Controlled asymmetry and generous breathing room
- Sophisticated serif paired with a clear sans-serif
- Warm or soft neutral base with purposeful muted accents
- Real/candid/archival research or study details when imagery is appropriate
- Information architecture that remains saveable and legible for Instagram

This direction is a hypothesis, not an approved identity. It must be presented alongside materially different alternatives for TM to judge.

## Latest Session Learnings (Updated)

### TM's Explicit Preferences & Locked Brand Assets
- **Brand Name & Handle:** Locked as `naskah.fk` across all visual assets, footers, headers, and signatures.
- **Font family: Poppins (current, 2026-09)** — TM asked to switch from Montserrat to **Poppins** for the Naskah carousel render. Poppins is geometric, larger x-height, more approachable/social-native than Montserrat. Full family downloaded and used (Light, Regular, Medium, SemiBold, Bold, ExtraBold) from the google/fonts GitHub repo. NOTE: the older Montserrat preference is superseded for Naskah; do not default back to Montserrat without explicit re-confirmation.
- **"Rapi tapi gak nampak templatenya"** — neat/clean but not obviously a repeated template. Each piece should feel art-directed.
- **Visual Aesthetic (Selected from TM's Canva Edit):**
  - High-contrast editorial style with bold, tight-leading typography.
  - Asymmetrical layout balance with real cutout photo objects (transparent PNGs: coffee cup, open notebook + pen, laptop, glasses, medical/research props) placed organically at corners/edges.
  - Highlight tape bar / stabilo box for punchy keyword emphasis.
  - Clean framing (e.g. subtle L-shape corner brackets or delicate rules).
- Soft-selling product mentions only; no hard price tagging in every post.

### Operational Protocols & Failure Recovery
- **Canva MCP Direct Editing vs. Automation Limits**: Canva MCP endpoints (`get_design`, `start_editing_transaction`, `copy_design`) frequently time out (300s+) on user-modified or private Canva templates.
- **Reliable Fallback Workflow**:
  1. Resolve shortlinks to extract template structure and text models.
  2. If Canva MCP editing times out, immediately pivot: generate structured, copy-ready slide-by-slide scripts (with explicit cutout image recommendations and typography layout tags) that match TM's Canva template structure, or request an exported JPG/PNG to analyze visually. Do not get stuck in consecutive MCP timeout loops.

### Layout System Proposed (Not a Single Template)
Instead of one rigid template, we proposed a **Layout System with 3 layout families**:

1. **Swiss Editorial Poster** — Editorial poster feel, strong typographic hierarchy, columns, rules, generous margins. Best for: opinions, big ideas, myth-busting, carousel covers.
2. **Asymmetric Notebook / Logbook** — Dark background + paper sheet, research logbook aesthetic. Best for: statistics, case studies, journal breakdowns, AI × research.
3. **Contemporary Research Card** — Ultra-clean, minimal, structured, high scanability. Best for: checklists, practical guides, step-by-step, decision trees.

All three use Montserrat as the single font family, different visual grammars, same editorial quality bar. This avoids feed monotony while staying brand-consistent.

### Anti-Template Checklist for Naskah
- No uniform card grids for every content type.
- No centered headline + colored pill + floating icon + 3 rounded cards.
- No decorative badges, pagination, or pseudo-dashboard details without reader purpose.
- Layout must feel chosen, not assembled.
- Typography carries identity before decoration.
- Use optical alignment over mathematical centering.
- Real negative space is editorial, not unfinished.

## Specific constraints for Naskah social assets

- Instagram is the visual knowledge showcase and authority layer. Content must be useful, structured, clean, saveable, and credible.
- Threads is conversational, human, slightly witty, and opinion-led. It should not inherit Instagram layouts mechanically.
- Social content is education-first; promotional content must be soft-sell and must not overuse prices.
- Proof, data, testimonials, and client work must never be invented.
- Every asset remains DRAFT/READY until TM approves it. No implied publishing authorization.

## Design research inputs mentioned by TM

- `https://github.com/Leonxlnx/taste-skill.git` — use as a source of anti-generic / anti-slop principles; adapt principles rather than copying its interface style.
- Folders offered for design-reference research: `awesome-design/`, `awesome-design-md/`, and `Awesome-Design-Tools/`.
- Canva is the intended design tool and is connected through MCP. Canva-generated candidates must receive human review and editing; they are not assumed to be final.

## Production request pattern

When TM asks to "gambarkan" a visual identity or requests a JPEG/template to help imagine it:

1. Research the given references first.
2. Explain what early directions missed in one short honest sentence.
3. Produce actual visual artifacts or Canva candidates, not text-only descriptions.
4. Compare options by visual grammar, not just palette.
5. Ask for a reaction to a concrete design characteristic such as type-led editorial vs. annotated notebook, then iterate.
