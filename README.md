# Tehqiq

Tehqiq prepares a concise meeting briefing with source passages, dated findings, conditional implications, and useful questions. A bounded Python orchestrator coordinates four model roles: planner, drafter, evidence auditor, and Q&A. Tavily supplies web search and extraction. Every model call passes through Bifrost. OpenRouter free models are active; Gemini Flash is configured as an optional provider but disabled until its Google project is confirmed to use Free Tier with billing disabled.

Recent developments cover the 30 days before the meeting, capped at the current time. The planner may request up to 180 days of background, displayed separately. Users can inspect evidence, change the objective without repeating research, print the briefing, or ask for a short cited answer.

See the [workflow diagram](WORKFLOW.md) and [role and budget details](AGENT_WORKFLOW.md).

## Run

Python 3.12 or newer is recommended. On Windows, install time zone data with `python -m pip install tzdata` for IANA time zones. The default `Asia/Kolkata` also works without that package for dates from 1970 onward.

1. Copy `.env.example` to `.env` (ignored by Git).
2. Set `TAVILY_API_KEY`, `OPENROUTER_API_KEY`, and `GEMINI_API_KEY` in `.env`.
3. Copy `bifrost/config.example.json` to `bifrost/config.json`. Run `powershell -File scripts/start_bifrost.ps1` on Windows. The current Bifrost build recognizes OpenRouter as a built-in provider. Keep the dashboard bound to localhost. See [Bifrost provider configuration](https://docs.getbifrost.ai/quickstart/gateway/provider-configuration).
4. After Bifrost registers provider keys, stop it and run `python -m scripts.configure_local_vk`. By default, the one-day virtual key allows only the two OpenRouter free models. Set `TEHQIQ_GEMINI_FREE_TIER_CONFIRMED=1` in `.env` only when the Gemini key's Google project is on Free Tier with billing disabled; then rerun the script to allow `gemini/gemini-3.8-flash` as the final fallback. Start Bifrost again with the script. Repeat key configuration when the local virtual key expires.
5. Set `BIFROST_BASE_URL` and `BIFROST_MODEL` in `.env`. Use `openrouter/openrouter/free` as the default and validate each role before a demo.
6. Run `python -m app.main` and open `http://127.0.0.1:8000` (or the configured `PORT`).

The application never calls providers directly; every model request passes through Bifrost. Provider keys and the Tavily key belong in the ignored `.env` file. Gemini 3.8 Flash has a Google AI Studio Standard Free Tier, but the same model can be billed when its project is on a paid tier. Tehqiq therefore leaves Gemini disabled until the project is confirmed free-tier with billing disabled. Do not put keys in screenshots, commits, or browser code.

## Validation

The current workflow adds a research planner, optional dated background context, role model settings, bounded model context/calls, evidence-grounded Q&A, and one evidence-only correction pass when every drafted finding is rejected. See [agent workflow](AGENT_WORKFLOW.md) for limits and configuration. Live planner and Q&A checks passed. One briefing completed search, extraction, drafting, and audit with five sources but no approved findings; strict checks rejected all three candidates. OpenRouter later returned HTTP 429 and an empty response. Bifrost registered Gemini and one direct Gemini request passed; a controlled fallback request then received an upstream HTTP 502. Gemini is disabled in the current virtual key until its Free Tier billing status is confirmed. The offline suite contains 19 tests.

Run `python -m unittest discover -s tests -v` and `node --check app/static/app.js`. All 19 offline tests pass. Coverage includes date boundaries, partial extraction, fabricated excerpts, audit rejection, one-pass evidence repair, model fallback on empty output and rate limits, malformed JSON, objective reframing, planner limits, paid-model and unconfirmed Gemini blocking, context limits, and Q&A citation gating. Tavily authentication and live search/extraction succeeded after replacing the expired key. Before recording a live demo, rerun both smoke scripts and verify the briefing produces an approved finding. Enable Gemini only after confirming the key's Google project has billing disabled.

## Work and token limits

The planner selects two to four queries and may add one background query. Search concurrency is three and extraction is capped at five pages. Relevant passages contribute at most 1,800 characters per source, with an 18,000-character model-input ceiling. Research jobs permit at most six model calls including repairs/fallbacks. Role output limits range from 512 to 2,048 tokens. Model requests retry HTTP 429 up to twice, honoring `Retry-After` for up to 30 seconds per retry. Planner and evidence audit use Ling; drafting and Q&A use Gemma in the local Bifrost setup. Gemini fallback can be enabled only for a verified Free Tier project with billing disabled. These limits bound work rather than demonstrate measured token savings. In-flight HTTP calls and backoff can exceed the planner's time allowance. Model fallback may route around model-specific limits but cannot remove account-wide quotas or provider-capacity limits.

Q&A uses approved findings and cited quotes, runs a separate answer audit, and returns at most 60 words. Unsupported or unknown citation IDs produce an insufficient-evidence response. It performs no additional web search.

The `?preview=1` URL displays a clearly labeled synthetic example for layout and print rehearsal. It is not live research. Browser Print / Save as PDF is the export path; one synthetic A4 report was visually checked as one page.

## Current limitations

The model can misidentify an entity or misread a source. Matching text and model review establish source support, not publisher truth. Person research requires an affiliation but does not offer candidate selection. URL deduplication does not cluster syndicated events. Local role routing uses the two explicitly configured free models; provider rate limits and availability vary. Secondary-provider failover is not configured or live-tested. Repair usage is not fully aggregated. The one-page print check covered one representative synthetic report, not every long or sparse case.

The app uses a local SQLite file, two background worker threads, and a localhost-only HTTP server. Jobs in progress are marked interrupted on restart. Do not expose this prototype publicly without authentication, rate limiting, and security review.

