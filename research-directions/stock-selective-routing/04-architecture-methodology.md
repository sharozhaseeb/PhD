# Architecture and Methodology

## System architecture

The source for this diagram is also stored at [`figures/system-architecture.mmd`](figures/system-architecture.mmd).

```mermaid
flowchart TB
    subgraph DATA["Point-in-time information firewall"]
        P["Prices, volume and corporate actions"]
        F["Fundamentals with filing and revision timestamps"]
        N["News/events with publication timestamps"]
        M["Macro data with release vintages"]
        PIT["Provenance and availability gate"]
        P --> PIT
        F --> PIT
        N --> PIT
        M --> PIT
    end

    PIT --> FS["Causal feature store<br/>as-of time t only"]
    FS --> RD["Online regime belief<br/>probability, not hindsight label"]
    FS --> E1["Price and momentum expert"]
    FS --> E2["Factor and fundamental expert"]
    FS --> E3["News and event expert"]
    FS --> E4["Volatility and tail-risk expert"]

    E1 --> CAL["Rolling expert reliability<br/>prediction intervals and past errors"]
    E2 --> CAL
    E3 --> CAL
    E4 --> CAL

    RD --> AG["Small selective-routing controller"]
    CAL --> AG
    Q["Evidence freshness, missingness,<br/>disagreement and provenance"] --> AG
    C["Estimated costs, liquidity<br/>and portfolio state"] --> AG

    AG --> A{"Controller action"}
    A --> S["Select one expert"]
    A --> W["Combine approved subset"]
    A --> R["Request additional evidence"]
    A --> X["Abstain / safe fallback"]

    S --> EDGE["Calibrated edge test<br/>expected residual alpha > costs + safety buffer"]
    W --> EDGE
    R --> AG
    EDGE -->|Pass| PC["Factor, turnover and risk constraints"]
    EDGE -->|Fail| X
    PC --> EX["Next-open paper execution"]

    X --> LOG["Immutable decision and abstention log"]
    EX --> LOG
    LOG --> EV["Frozen walk-forward evaluation<br/>selective risk, costs and attribution"]
    EV -. "Outcome available after horizon;<br/>predeclared updates only" .-> CAL
    EV -. "Delayed, time-safe feedback;<br/>never future data" .-> AG
```

## Research logic

```mermaid
flowchart LR
    O["Observed improvement"] --> G{"Possible cause"}
    G --> A["Agent routing skill"]
    G --> V["Volatility timing"]
    G --> C["Lower coverage / cash exposure"]
    G --> F["Factor exposure"]
    G --> L["Leakage or test reuse"]

    A --> T["Equal-information controller comparison"]
    V --> T2["Matched volatility-rule baseline"]
    C --> T3["Matched-coverage random abstention"]
    F --> T4["Factor-neutral attribution"]
    L --> T5["Point-in-time masking and frozen holdout"]
```

## Specialist design

Specialists must be replaceable and demonstrably heterogeneous. Candidate initial specialists are:

- price/momentum: linear, tree, or temporal model using lagged price-volume features;
- factor/fundamental: point-in-time accounting and style features;
- event/news: added only after the structured-data benchmark is correct;
- volatility/risk: conditional volatility and tail-risk estimation.

Expert diversity must be measured using residual-error correlation, failure-period overlap, and conditional performance. Different model names are not sufficient evidence of diversity.

## Controller families to compare

- deterministic hand-written gate;
- supervised logistic/tree gate;
- conventional soft mixture-of-experts;
- AlphaMix-style uncertainty-aware router;
- contextual bandit with delayed feedback;
- constrained stateful agent; and
- hindsight oracle reported only as an unattainable upper bound.

## Dual-timescale validity

The proposed controller separates:

1. **Instance-level validity:** Is this stock forecast sufficiently supported now?
2. **Strategy-level health:** Has the overall forecasting relationship recently degraded after delayed outcomes became observable?

This distinction is intended to prevent per-stock confidence from being treated as proof that the entire ranking strategy remains valid after a silent concept shift.

## Reproducibility requirements

Each decision log must contain:

- event time and data-availability time;
- data snapshot/version and feature code version;
- universe membership as known at that time;
- specialist versions and predictions;
- calibrated uncertainty and reliability inputs;
- regime posterior;
- controller version, state, action, and reason codes;
- model/provider/version, prompt, temperature, and seed for any LLM component;
- estimated costs and portfolio constraints;
- eventual outcome timestamp; and
- whether and when that outcome was permitted to update the system.

