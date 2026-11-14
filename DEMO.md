# Tehqiq demo guide

## Before presenting

1. Start Bifrost with `powershell -File scripts/start_bifrost.ps1`.
2. Start the app with `python -m app.main` and open `http://127.0.0.1:8000`.
3. Run `python -m scripts.smoke` once. The free OpenRouter route can be slow or unavailable, so allow time for a live run before the presentation.
4. Open `http://127.0.0.1:8000/?preview=1` in a second tab. This is a **synthetic interface preview**, visibly labeled in the product. It is a layout backup, not evidence of a live briefing.
5. Check that every live finding's displayed quote directly supports its wording before showing it to judges. If no claim survives, explain the evidence gate and show the source coverage honestly.

## Three-minute story

- **0:00–0:25:** “Preparing for a meeting means finding what changed recently and deciding what can safely be said.”
- **0:25–0:50:** Enter the subject, meeting time, affiliation for a person, and objective. Start research. Point to the four progress stages.
- **0:50–1:45:** Show a completed live briefing. Read one “what changed / why it may matter / ask” sequence. Open the linked original source and compare the exact excerpt.
- **1:45–2:15:** Show the research cutoff and excluded finding count. Explain that unknown or unsupported claims are removed.
- **2:15–2:40:** Change the objective. The approved facts stay fixed while the interpretation and question may change; no new Tavily search runs.
- **2:40–3:00:** Show the trace and one-page print view. Say which model actually served the request if Bifrost reported it.

## Claims you can make accurately

Tehqiq uses Tavily Search and Extract, sends model work through Bifrost to an OpenRouter free route, stores source-linked excerpts, applies date and excerpt checks plus a second model audit, and renders a printable briefing. One company run completed end to end and one synthetic A4 layout rendered on one page. Later free-route runs timed out or returned no text. The offline suite has 11 passing tests. Do not claim measured accuracy, time savings, person-path live validation, provider failover, or guaranteed latency.
