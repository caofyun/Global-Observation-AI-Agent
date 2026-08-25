# Global-Observation-AI-Agent V2.0 Architecture Baseline

## 1. Baseline Status

Version: V2.0
Status: Frozen Baseline — synchronized 2026-08-25
Purpose: Define the current implemented engineering architecture.

This document separates the current implementation from the future product vision.

---

## 2. Current Production Pipeline

```text
NewsDiscovery
    |
    v
news_articles.json
    |
    v
NewsVerifier
    |
    v
verification.json
    |
    v
SourceRanker
    |
    v
source_rank.json
    |
    v
TopicScorer
    |
    v
topic_score.json
    |
    v
TopicSelector
    |
    v
topic_selection.json
```

This is the current implemented news-intelligence chain. It supersedes the older V2.0 description that stopped at SourceRanker.

---

## 3. Implemented Components

### Core Framework
- BaseAgent
- ProjectManager
- ProductionController
- Pipeline Runner / Discovery Pipeline Adapter

### News Intelligence Layer
- NewsAgent / NewsDiscovery
- NewsVerifier
- SourceRanker
- TopicScorer
- TopicSelector
- AIModelClient
- SearchTool

### Current outputs
- news_articles.json
- verification.json
- ai_verification.json
- source_rank.json
- topic_score.json
- topic_selection.json

---

## 4. Frozen Engineering Rules

1. Agent responsibilities must remain independent.
2. JSON data contracts must not change without a version update.
3. Agents communicate through defined files/interfaces.
4. Agent success and failure results follow the unified BaseAgent contract.
5. Pipeline contracts must remain covered by automated tests and CI.
6. Future Agents must enter through task-driven development.

---

## 5. Current Boundary

The current V2.0 engineering baseline covers:

**news discovery → fact verification → source ranking → topic scoring → topic selection**

The following are not yet implemented as production content-generation Agents:

- ScriptAgent
- StoryboardAgent
- MaterialAgent
- AudioSubtitleAgent / VoiceAgent
- VideoAgent
- ReviewAgent
- PublishAgent

---

## 6. Baseline Quality Gate

Current confirmed baseline:

```text
pytest: 72 passed
failed: 0
warnings: 3
```

GitHub main baseline commit before TASK-007 documentation synchronization:

`4c0dcb76de218c649418a7d4941583a1b0d461d9`

The three warnings remain a separate cleanup item and must not be silently reclassified as resolved without a fresh test run.
