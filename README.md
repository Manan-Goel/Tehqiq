# Tehqiq

Working local prototype for the hackathon brief. It researches a company or person for the 30 days preceding a meeting, extracts up to five sources, checks each generated claim's excerpt and event date, runs a second semantic audit, and produces a printable report with source links and discussion questions. The interface also supports changing the meeting objective while reusing approved evidence.

## Run

Python 3.12 or newer is recommended. No Python packages are required.

1. Copy `.env.example` to `.env` (ignored by Git).
2. Set `TAVILY_API_KEY` in `.env`.
3. Copy `bifrost/config.example.json` to `bifrost/config.json`. Run `powershell -File scripts/start_bifrost.ps1` on Windows. The current Bifrost build recognizes OpenRouter as a built-in provider. Keep the dashboard bound to localhost. See [Bifrost provider configuration](https://docs.getbifrost.ai/quickstart/gateway/provider-configuration).
4. After the first Bifrost start has registered the provider key, stop Bifrost and run `python -m scripts.configure_local_vk`. This writes a one-day Bifrost virtual key to ignored `.env` and `bifrost/config.json`, limited to the single configured OpenRouter key and `openrouter/free`. Start Bifrost again with the script.
5. Set `BIFROST_BASE_URL` and `BIFROST_MODEL` in `.env`. Use `openrouter/openrouter/free` and validate with `python -m scripts.smoke` before a demo.
6. Run `python -m app.main` and open `http://127.0.0.1:8000` (or the configured `PORT`).

The application never calls OpenRouter directly. The OpenRouter key belongs in Bifrost; the Tavily key belongs in the app's ignored `.env` file. Do not put either in screenshots, commits, or browser code.

## Validation

The current workflow adds a research planner, optional dated background context, role model settings, bounded model context/calls, and evidence-grounded Q&A. See [agent workflow](AGENT_WORKFLOW.md) for limits and configuration. Run `python -m scripts.smoke_agents` for live role checks. The latest planner smoke received HTTP 429 from the model route, so role-specific live success has not been established. The offline suite now contains 16 tests.

Run `python -m unittest discover -s tests -v` and `node --check app/static/app.js`. The offline suite covers date boundaries, partial extraction, fabricated excerpts, semantic audit rejection, Bifrost request construction, malformed JSON, and objective reframing. Tavily Search/Extract and a Bifrost to OpenRouter free model call were also verified with live credentials on 15 November 2026. One complete live company briefing finished; later stricter runs encountered free-route timeouts, so demo timing is not guaranteed.

The `?preview=1` URL displays a clearly labeled synthetic example for layout and print rehearsal. It is not live research. Browser Print / Save as PDF is the export path; one synthetic A4 report was visually checked as one page.

## Current limitations

The model can still misidentify an entity or misread a source; the semantic audit reduces but cannot eliminate that risk. Verify important findings manually. Person research requires an affiliation as a guardrail but does not yet offer candidate selection or prove identity. Search results are deduplicated by URL and source domain, but syndicated events are not clustered. Bifrost fallback is constructed in requests but no second provider is configured or live-tested because this setup has only a free OpenRouter route. The one-page print check covered a representative synthetic report, not every long or sparse case. Free model availability and latency vary.

The app uses a local SQLite file, two background worker threads, and a localhost-only HTTP server. Jobs in progress are marked interrupted on restart. Do not expose this prototype publicly without authentication, rate limiting, and security review.

