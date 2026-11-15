# Tehqiq

Tehqiq prepares a concise meeting briefing with source passages, dated findings, conditional implications, and useful questions. A bounded Python orchestrator coordinates four model roles: planner, drafter, evidence auditor, and Q&A. Tavily supplies web search and extraction. Every model call passes through Bifrost to OpenRouter free models.

Recent developments cover the 30 days before the meeting, capped at the current time. The planner may request up to 180 days of background, displayed separately. Users can inspect evidence, change the objective without repeating research, print the briefing, or ask for a short cited answer.

See the [workflow diagram](WORKFLOW.md) and [role and budget details](AGENT_WORKFLOW.md).

## Run

Python 3.12 or newer is recommended. No Python packages are required.

1. Copy `.env.example` to `.env` (ignored by Git).
2. Set `TAVILY_API_KEY` in `.env`.
3. Copy `bifrost/config.example.json` to `bifrost/config.json`. Run `powershell -File scripts/start_bifrost.ps1` on Windows. The current Bifrost build recognizes OpenRouter as a built-in provider. Keep the dashboard bound to localhost. See [Bifrost provider configuration](https://docs.getbifrost.ai/quickstart/gateway/provider-configuration).
4. After the first Bifrost start has registered the provider key, stop Bifrost and run `python -m scripts.configure_local_vk`. This writes a one-day Bifrost virtual key to ignored `.env` and `bifrost/config.json`, limited to the configured OpenRouter provider key and two free routes: `openrouter/free` and `inclusionai/ling-3.2-flash:free`. It sets role models in `.env`. Start Bifrost again with the script. Repeat key configuration when the local virtual key expires.
5. Set `BIFROST_BASE_URL` and `BIFROST_MODEL` in `.env`. Use `openrouter/openrouter/free` and validate with `python -m scripts.smoke` before a demo.
6. Run `python -m app.main` and open `http://127.0.0.1:8000` (or the configured `PORT`).

The application never calls OpenRouter directly. The OpenRouter key belongs in Bifrost; the Tavily key belongs in the app's ignored `.env` file. Do not put either in screenshots, commits, or browser code.

## Validation

The current workflow adds a research planner, optional dated background context, role model settings, bounded model context/calls, and evidence-grounded Q&A. See [agent workflow](AGENT_WORKFLOW.md) for limits and configuration. Run `python -m scripts.smoke_agents` for live role checks. The latest planner smoke received HTTP 429 from the model route, so role-specific live success has not been established. The offline suite now contains 16 tests.

Run `python -m unittest discover -s tests -v` and `node --check app/static/app.js`. All 16 offline tests pass. Coverage includes date boundaries, partial extraction, fabricated excerpts, audit rejection, malformed JSON, objective reframing, planner limits, paid-model blocking, context limits, and Q&A citation gating. Tavily Search/Extract and a Bifrost to OpenRouter free model call were verified with live credentials. One earlier company briefing completed. Later stricter runs timed out, and the expanded planner smoke received HTTP 429. Expanded planner/Q&A live validation remains outstanding.

## Work and token limits

The planner selects two to four queries and may add one background query. Search concurrency is three and extraction is capped at five pages. Relevant passages contribute at most 1,800 characters per source, with an 18,000-character model-input ceiling. Research jobs permit at most six model calls including repairs. Draft outputs have a 4,096-token cap, other roles 2,048. These limits bound work rather than demonstrate measured token savings. In-flight HTTP calls can exceed the planner's time allowance.

Q&A uses approved findings and cited quotes, runs a separate answer audit, and returns at most 60 words. Unsupported or unknown citation IDs produce an insufficient-evidence response. It performs no additional web search.

The `?preview=1` URL displays a clearly labeled synthetic example for layout and print rehearsal. It is not live research. Browser Print / Save as PDF is the export path; one synthetic A4 report was visually checked as one page.

## Current limitations

The model can misidentify an entity or misread a source. Matching text and model review establish source support, not publisher truth. Person research requires an affiliation but does not offer candidate selection. URL deduplication does not cluster syndicated events. Planner and Q&A use an explicit free model, while draft and audit use the free router, which does not guarantee different underlying models. Secondary-provider failover is not configured or live-tested. Repair usage is not fully aggregated. The one-page print check covered one representative synthetic report, not every long or sparse case. Free model availability and latency vary.

The app uses a local SQLite file, two background worker threads, and a localhost-only HTTP server. Jobs in progress are marked interrupted on restart. Do not expose this prototype publicly without authentication, rate limiting, and security review.

