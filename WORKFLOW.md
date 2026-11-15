# Tehqiq workflow

```mermaid
flowchart TD
    A[Meeting context] --> B[Planner]
    B --> C[Tavily Search and Extract]
    C --> D[Select relevant passages]
    D --> E[Draft findings]
    E --> F[Quote and date checks]
    F --> G[Evidence auditor]
    G --> H[Briefing with citations]
    H --> I[Print or change objective]
    H --> J[Ask a question]
    J --> K[Q&A from approved evidence]
    K --> L[Answer support audit]
    L --> M[Short cited answer or insufficient evidence]
```

The Python orchestrator owns this sequence, limits, and SQLite job state. Every model role calls Bifrost, which routes to configured OpenRouter free models. Tavily supplies source text. Roles exchange structured JSON through the application.

Recent findings use the 30 days before the meeting, capped at the current time. The planner can request background history up to 180 days, shown with a separate label. Search scope is bounded to four topic searches and one optional background search. Source selection and extraction remain capped at five pages.

The support audit can reject a claim. The diagram's briefing step may therefore contain fewer than three findings or no approved findings. Model or extraction failures produce an explicit error. Q&A searches no new pages and can decline to answer.

Evidence matching establishes a relationship between a claim and retrieved text. It does not establish that the publisher is correct or that two articles independently corroborate an event.
