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
- Output limits are 4,096 tokens for drafting and 2,048 for other roles. Some models spend this allowance on reasoning and may return no text.
- Audits and Q&A reuse approved excerpts. Objective changes reuse existing research.
- The report exposes role models, input characters, and provider-reported tokens. Repair usage is not fully aggregated and no measured savings claim is made.

## Configuration

Run `python -m scripts.configure_local_vk` with Bifrost stopped, then restart Bifrost and the app. This rotates the local one-day virtual key and restricts it to `openrouter/free` and `inclusionai/ling-3.2-flash:free`.

Planner and Q&A use the explicit Ling free model. Drafting and audits use the free router. A distinct underlying draft/audit model is not guaranteed by the router. Set `BIFROST_AUDIT_MODEL` to an available explicit free model and add that exact model to the virtual-key allowlist when independent model selection is required. Current free availability was checked against https://openrouter.ai/api/v1/models on 15 November 2026. No claim of live role-specific validation accompanies offline tests.
