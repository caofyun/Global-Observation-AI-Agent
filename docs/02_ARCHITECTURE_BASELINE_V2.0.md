# Global-Observation-AI-Agent V2.0 Architecture Baseline

## 1. Baseline Status

Version: V2.0
Status: Frozen Baseline
Purpose: Define the current implemented engineering architecture.

This document separates the current implementation from the future product vision.

---

## 2. Current Production Pipeline

```
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
```

---

## 3. Implemented Components

### Core Framework
- BaseAgent
- ProjectManager
- ProductionController

### News Intelligence Layer
- NewsAgent
- NewsVerifier
- SourceRanker
- AIModelClient
- SearchTool

---

## 4. Frozen Engineering Rules

1. Agent responsibilities must remain independent.
2. JSON data contracts must not change without a version update.
3. Agents communicate through defined files/interfaces.
4. Future Agents must enter through task-driven development.

---

## 5. Future Expansion

Planned but not implemented:

- TopicScorer
- TopicSelector
- ScriptAgent
- StoryboardAgent
- MaterialAgent
- VideoAgent
- AudioSubtitleAgent
- ReviewAgent
- PublishAgent

These modules are outside the current V2.0 freeze boundary.
