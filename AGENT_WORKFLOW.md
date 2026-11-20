# Tehqiq research roles

The application orchestrates four bounded model roles: planner, drafter, evidence auditor, and Q&A. Roles communicate through structured data rather than open-ended conversations.

The planner proposes two to four searches, a search/extraction allowance of 30 to 90 seconds, and optional background history of up to 180 days. Recent developments retain the meeting-relative 30-day rule. Older findings appear as background. One optional background search fits within the planner allowance. Calls already in flight can overrun that allowance by the HTTP timeout.

Drafting uses selected source passages. Quote checks reject fabricated excerpts, and date evidence requires a matching source passage. The auditor then reviews factual support, identity, date interpretation, and question premises. These checks do not prove a publisher's claims true or independently corroborate every finding. Publication date, retrieval time, publisher domain, source URL, and a hash of extracted content preserve provenance.

Q&A uses approved findings, limits answers to 60 words, requires known source IDs, and runs a separate support audit. Missing evidence produces an explicit unanswered result. It does not silently search the web.

## Token and cost controls

- No paid model routes by default. Both primary and fallback settings pass a free-model check.
- At most five search requests and five extracted pages.
- Relevant paragraph selection replaces blind prefix truncation. Each source contributes at most 1,800 characters.
- At most 18,000 input characters per model request and six requests including JSON repairs per research job. Character counts are a proxy, not exact tokenizer budgets.
- Output limits are 512 tokens for planning and Q&A, 768 for audits, and 2,048 for drafting. Model HTTP 429 responses retry at most twice, honoring `Retry-After` for up to 30 seconds per retry; each role also has a complementary free-model fallback. Empty responses trigger one direct request to that alternate model. These paths are capped by the six-call job budget. Fallbacks can route around a model-specific limit, but retries/fallbacks cannot clear an account-wide free-tier quota.
- Audits and Q&A reuse approved excerpts. Objective changes reuse existing research.
- The report exposes role models, input characters, and provider-reported tokens. Repair usage is not fully aggregated and no measured savings claim is made.

## Configuration

Run `python -m scripts.configure_local_vk` with Bifrost stopped, then restart Bifrost and the app. This rotates the local one-day virtual key and restricts it to `inclusionai/ling-3.2-flash:free` and `google/gemma-4-26b-a4b-it:free`.

The local Bifrost setup routes planning and evidence audits to the explicit Ling free model and drafting and Q&A to the explicit Gemma free model, with the other free model as role fallback. Q&A support review reuses the drafting route. Live planner and Q&A smoke checks passed after updating Tavily credentials. One real briefing completed all stages and extracted five sources, but strict evidence checks rejected its three drafted claims; a second attempt hit OpenRouter HTTP 429 during drafting, and a later run returned no text after bounded retries. Bifrost registered Gemini and a direct test request succeeded once; a controlled OpenRouter-rate-limit fallback attempt then received upstream HTTP 502. To avoid paid-tier calls, Gemini is disabled in the current virtual key until the Google project is confirmed to have billing disabled. Evidence correction and fallback behavior are covered in the 19-test offline suite. Google AI Studio lists Gemini 3.8 Flash on Standard Free Tier, but the same model is billed on paid-tier projects. Free quotas and availability can change.
