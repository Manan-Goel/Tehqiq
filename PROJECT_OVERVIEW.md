# Tehqiq | Project overview

Tehqiq prepares a short, source-linked briefing for a meeting with a company or person. It looks at the 30 days before the meeting and turns recent developments into useful questions.

## What we built

The prototype accepts a subject, meeting time, timezone, affiliation when researching a person, and meeting objective. It finds recent sources, extracts their text, drafts up to three findings, checks quotes and dates, runs a second evidence review, and shows the surviving findings with source links. The user can change the objective to refresh the questions without repeating the search, then print the briefing.

## Technology

- **Tavily Search and Extract:** discovers and reads recent public sources.
- **Bifrost with OpenRouter free models:** routes all model requests through a local gateway.
- **Python standard library and SQLite:** runs the research jobs and stores reports locally.
- **HTML, CSS, and JavaScript:** powers the dossier interface and print view.

## Problems we addressed

Search results can be stale, repetitive, or ambiguous. Tehqiq limits research to the meeting window, removes duplicate URLs, requires an affiliation for a person, and rejects claims without a matching source excerpt or valid event date. A second model review checks whether the visible quote supports the wording. These checks reduce errors, but a user should still inspect important claims in the original source.

The free model route can be slow or unavailable. The interface shows research progress and clear failure states. A labeled synthetic preview supports interface rehearsal; it is never presented as live research.

## How to use it

Start Bifrost and the app using the [README](README.md). Open `http://127.0.0.1:8000`, enter the meeting context, and select **Build my briefing**. Read the findings, open their sources, adjust the objective if useful, and print the report.

This is a local hackathon prototype. It has completed one live company briefing and 11 offline tests. Person-path live validation, candidate selection, and a hosted deployment remain open.
