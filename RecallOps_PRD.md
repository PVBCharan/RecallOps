# RecallOps --- Product Requirements Document (PRD)

**Product title:** RecallOps\
**Full project name:** A Multimodal, Cross-Domain Experience-Aware AI
Decision Support Platform\
**Document type:** Product Requirements Document (PRD)\
**Version:** 1.0\
**Status:** Hackathon prototype plan\
**Target:** HackwithHyderabad 3.0\
**Cost constraint:** ₹0 for the current prototype\
**Primary memory requirement:** Hindsight, self-hosted\
**Primary implementation constraint:** Local development on a laptop
with approximately 8 GB RAM

------------------------------------------------------------------------

## 1. Executive Summary

RecallOps is a multimodal, experience-aware AI decision support platform
designed to help people make better-informed decisions by learning from
documented past experiences and their outcomes.

Users can submit information through text, images, short videos, and
graphical or statistical data. The platform processes the available
evidence, builds a structured representation of the situation, retrieves
relevant past experiences from Hindsight memory, and generates a
contextual recommendation with supporting evidence and uncertainty.

The platform is designed around a shared experience-intelligence core
that can support four domains:

1.  **Commercial Operations:** Incident response, troubleshooting, and
    operational knowledge.
2.  **Healthcare:** Longitudinal patient information and supervised
    clinical decision support using synthetic or authorized data.
3.  **Defence:** Equipment maintenance and approved procedural support
    using synthetic or authorized data.
4.  **Education:** Personalized learning support, misconception
    tracking, and learning progress over time.

The hackathon prototype will prioritize a reliable end-to-end workflow
rather than attempting to build four production-ready domain systems. A
simulated commercial incident will serve as the primary working
demonstration, while the other domains will be represented through
carefully scoped synthetic scenarios.

The core differentiator is the combination of multimodal evidence
processing, outcome-aware memory, contextual retrieval, and
human-supervised recommendations.

------------------------------------------------------------------------

## 2. Problem Statement

People and organizations repeatedly encounter similar problems but often
struggle to reuse what they learned from previous experiences.

Common challenges include:

-   Important knowledge is scattered across text reports, images,
    videos, charts, and conversations.
-   A description alone may omit visual or statistical evidence that
    changes how an event should be understood.
-   Past actions may be remembered without recording whether they
    succeeded, failed, or were never verified.
-   Similar cases may occur under different conditions, making direct
    reuse of an earlier solution unreliable.
-   Generic AI assistants may answer a single query without maintaining
    a structured, outcome-aware record of past experiences.
-   Users need to understand why a recommendation was made and what
    evidence supports it.

RecallOps addresses these challenges by organizing experiences into
structured records, retaining relevant evidence summaries and outcomes,
retrieving similar cases, and generating recommendations that users can
review.

------------------------------------------------------------------------

## 3. Product Vision

Build a free, locally runnable prototype that demonstrates how AI can
use multimodal evidence and documented outcomes to support better
decisions across multiple domains.

### Vision statement

> Help people learn from experience by turning text, visual evidence,
> and statistical information into structured, retrievable knowledge
> that supports traceable, context-sensitive decisions.

------------------------------------------------------------------------

## 4. Goals and Success Criteria

### 4.1 Product goals

-   Accept text and selected multimodal evidence through a simple web
    interface.
-   Convert uploaded information into a structured experience record.
-   Use Hindsight as the long-term experience-memory layer.
-   Retrieve relevant past experiences for a new case.
-   Generate recommendations that cite the evidence and prior
    experiences used.
-   Record whether a recommendation was successful, unsuccessful, or
    unverified.
-   Demonstrate the same core workflow across four domains using
    domain-specific scenarios.
-   Keep the hackathon prototype free of paid API dependencies.

### 4.2 Hackathon success criteria

The prototype will be considered successful when:

1.  A user can submit a text-based case and receive a structured
    analysis.
2.  The system can accept an image and extract a useful, clearly
    qualified summary using an available local tool or model.
3.  The system can analyze a CSV dataset and present basic statistics or
    trends.
4.  A short video can be processed by extracting selected frames and
    summarizing relevant visible events, subject to local compute
    capability.
5.  A documented experience can be stored in Hindsight and retrieved in
    a later, related case.
6.  The recommendation references relevant prior experience and
    distinguishes verified outcomes from unverified information.
7.  The user can record the result of a recommendation and associate it
    with the experience.
8.  The team can demonstrate the shared workflow in a short live demo.
9.  The project can be run without paid API calls or paid hosting.

These are prototype acceptance goals, not claims of clinical, military,
or enterprise-grade reliability.

------------------------------------------------------------------------

## 5. Target Users and Use Cases

### 5.1 Commercial Operations

**Users:** Operations teams, support engineers, technicians, and
incident responders.

**Example:** A user reports a recurring service or equipment incident,
uploads a screenshot or log excerpt, and optionally supplies a short
video or sensor CSV. RecallOps retrieves similar cases and shows the
actions and outcomes previously recorded.

### 5.2 Healthcare

**Users:** Healthcare professionals and authorized support staff.

**Example:** A synthetic patient case contains measurements collected
over time. RecallOps summarizes trends and retrieves relevant documented
history for professional review.

**Boundary:** The prototype is not a diagnostic system and must not
independently prescribe treatment. Use synthetic data unless appropriate
authorization and safeguards are in place.

### 5.3 Defence

**Users:** Maintenance personnel and authorized support staff.

**Example:** A synthetic equipment-maintenance case includes inspection
images and sensor readings. RecallOps retrieves similar maintenance
records and approved procedural guidance.

**Boundary:** The prototype is limited to maintenance and support. It
must not autonomously control equipment or make operational combat
decisions.

### 5.4 Education

**Users:** Students, instructors, and learning-support personnel.

**Example:** A learner submits a programming solution or screenshot and
receives feedback. The system records the misconception, practice
activity, and subsequent performance, then uses that history to suggest
a relevant follow-up exercise.

**Boundary:** Learning progress must be based on observed evidence; the
system should not claim mastery merely because a learner viewed an
explanation.

------------------------------------------------------------------------

## 6. Scope

### 6.1 In scope for the hackathon MVP

-   A web-based user interface.
-   Text-based case submission.
-   Image upload and basic visual evidence extraction.
-   CSV upload and basic statistical analysis.
-   Short-video upload with selected-frame extraction and analysis, if
    feasible on the available hardware.
-   Structured experience records.
-   Hindsight integration for experience storage and retrieval.
-   Similar-case retrieval and recommendation generation.
-   Outcome feedback: successful, unsuccessful, or unverified.
-   Basic experience history and evidence display.
-   Four synthetic domain scenarios.
-   Local-first development and demonstration.
-   Basic error handling, input validation, and privacy-conscious data
    handling.

### 6.2 Out of scope for the hackathon MVP

-   Real-time video streaming or continuous surveillance.
-   Autonomous execution of recommended actions.
-   Clinical diagnosis, treatment selection, or medical prescriptions.
-   Combat planning, targeting, or autonomous defence decisions.
-   Full enterprise integrations or production deployment.
-   Multi-tenant access control at enterprise scale.
-   Large-scale model training or fine-tuning.
-   Guaranteed interpretation of all image, video, chart, or document
    formats.
-   Production-grade regulatory certification or clinical validation.

------------------------------------------------------------------------

## 7. Functional Requirements

Priority definitions:

-   **P0:** Essential for the core demonstration.
-   **P1:** Important if time and hardware allow.
-   **P2:** Future enhancement.

### FR-01 --- Case submission (P0)

The user shall be able to create a case with:

-   Case title.
-   Domain selection.
-   Text description of the situation.
-   Observed symptoms, mistakes, or relevant context.
-   Action already taken, if any.
-   Outcome, if known.
-   Optional evidence attachments.

**Acceptance criteria** - Required fields are validated. - The user
receives a clear confirmation or error message. - The case is assigned a
unique identifier.

### FR-02 --- Image upload and analysis (P1)

The user shall be able to upload a supported image.

The system should: - Validate file type and size. - Extract a visual
summary using a locally available vision model or supported open-source
tool. - Label extracted observations as model-generated and potentially
uncertain. - Associate the summary with the case.

**Acceptance criteria** - Unsupported files are rejected with a useful
message. - The image summary is visible before or alongside
recommendation generation. - The system does not present uncertain
visual interpretations as verified facts.

### FR-03 --- Video processing (P1)

The user shall be able to upload a short supported video.

The system should: - Validate the file. - Extract a configurable number
of frames using OpenCV. - Analyze selected frames rather than processing
every frame. - Preserve timestamps for selected frames when available. -
Produce a concise event summary and associate it with the case.

**Acceptance criteria** - The system communicates when a video is too
large, too long, or unsupported. - Extracted observations include
timestamps where possible. - The interface identifies the output as an
automated interpretation. - The system can skip video analysis
gracefully if local resources are insufficient.

### FR-04 --- Chart and statistical data analysis (P0 for CSV; P1 for chart images)

The user shall be able to upload a supported CSV file.

The system should: - Parse the dataset with Pandas. - Display column
names and basic summary statistics. - Identify simple changes, trends,
missing values, and potential anomalies where appropriate. - Generate a
basic graph when useful. - Store a concise, structured summary linked to
the case.

**Acceptance criteria** - Invalid or malformed CSV files produce a clear
error. - The system does not silently treat missing values as zero. -
Numerical summaries are traceable to the uploaded dataset. - The user
can review the analysis before using it in a recommendation.

### FR-05 --- Evidence synthesis (P0)

The system shall combine the user's text and available extracted
evidence into a structured case summary.

Suggested fields: - Situation. - Observations. - Evidence sources. -
Relevant measurements or events. - Actions taken. - Known outcome. -
Missing information. - Uncertainty or confidence notes.

**Acceptance criteria** - The summary separates user-provided facts from
machine-generated observations. - Conflicting information is flagged
instead of silently resolved. - The user can review the summary.

### FR-06 --- Experience memory (P0)

The system shall store structured experiences in Hindsight.

An experience record should include: - Case identifier. - Domain. -
Context and conditions. - Observations and evidence summary. - Action or
intervention. - Outcome status. - Verification notes. - Timestamp. -
Source and provenance. - Relevant restrictions or domain-specific
metadata.

**Acceptance criteria** - A submitted experience can be stored
successfully. - A later query can retrieve the stored experience. - The
application handles memory service errors without crashing. - The
application does not mark an unverified outcome as successful.

### FR-07 --- Contextual retrieval (P0)

The system shall retrieve relevant past experiences for a new case.

Retrieval should consider: - Domain. - Similarity of the situation. -
Conditions and context. - Relevant observations. - Recorded outcomes. -
Whether the outcome was verified.

**Acceptance criteria** - Retrieved experiences are displayed with their
recorded outcome status. - The system does not treat similarity alone as
proof that an earlier action applies. - The user can inspect the source
experience.

### FR-08 --- Recommendation generation (P0)

The system shall generate a recommendation using the current case,
available evidence, domain rules, and retrieved experiences.

A recommendation should include: - Suggested next step or options. -
Reasoning summary in plain language. - Relevant evidence. - Relevant
prior experiences. - Outcome status of prior experiences. - Uncertainty
and missing information. - A reminder when professional or authorized
human review is required.

**Acceptance criteria** - The recommendation is grounded in available
case information and retrieved records. - Unsupported claims are not
presented as established facts. - The system can state that there is
insufficient information to recommend a next step. - Recommendations
remain advisory and require human review.

### FR-09 --- Outcome feedback (P0)

The user shall be able to record whether a recommended action: -
Worked. - Did not work. - Had a mixed result. - Has not yet been
verified.

The user may add notes or supporting evidence.

**Acceptance criteria** - The feedback is linked to the relevant case
and recommendation. - The outcome is stored as a new experience or an
update according to the chosen Hindsight integration pattern. - The
original recommendation and its history remain traceable. - An
unverified outcome remains unverified.

### FR-10 --- Experience history (P0)

The user shall be able to view previous cases and their outcomes.

**Acceptance criteria** - The interface displays case title, domain,
date, outcome status, and available evidence. - The user can open a case
to inspect its summary and recommendation. - Empty states and retrieval
failures are handled clearly.

### FR-11 --- Domain-specific presentation (P1)

The application shall provide domain-specific labels and scenario
examples for Commercial Operations, Healthcare, Defence, and Education.

**Acceptance criteria** - A user can select a domain. - Each domain uses
relevant terminology and guardrails. - The underlying experience-memory
workflow remains shared.

### FR-12 --- Free local operation (P0)

The prototype shall be designed to run without paid API calls or paid
hosting.

**Acceptance criteria** - No required workflow depends on a paid API
key. - Model and service dependencies are documented. - The app displays
a helpful setup error when a local dependency is unavailable. - Any
optional external service is clearly marked as optional and excluded
from the free-path requirements.

------------------------------------------------------------------------

## 8. Non-Functional Requirements

### 8.1 Cost

-   Target operating cost for the prototype: ₹0.
-   Use open-source components and local inference where feasible.
-   Avoid paid APIs, paid subscriptions, and paid hosting in the
    required demo path.
-   Confirm the license and any model-specific usage restrictions before
    adoption.

### 8.2 Performance

-   Prioritize responsiveness for text and CSV workflows.
-   Process video asynchronously or in small batches.
-   Use file-size and duration limits.
-   Show progress or a clear processing state for longer tasks.
-   Do not promise fixed response times until the local setup is
    benchmarked.

### 8.3 Reliability

-   Handle missing dependencies and unavailable models gracefully.
-   Validate uploaded files.
-   Preserve case identifiers and link evidence to the correct case.
-   Distinguish failed processing from a valid result containing no
    findings.

### 8.4 Security and privacy

-   Use synthetic data for demonstrations, especially in healthcare and
    defence.
-   Store uploads locally during the prototype.
-   Do not upload sensitive files to external services by default.
-   Avoid storing unnecessary personal information.
-   Provide a way to remove prototype cases and associated local files.
-   Document that the prototype is not production-ready for sensitive
    data.

### 8.5 Explainability and traceability

-   Show the evidence used in a recommendation.
-   Identify retrieved past experiences.
-   Display outcome and verification status.
-   Separate user-provided information from AI-generated interpretation.
-   Communicate uncertainty and missing information.

### 8.6 Accessibility and usability

-   Use clear labels and simple navigation.
-   Provide understandable validation messages.
-   Avoid requiring users to understand AI or memory-system terminology.
-   Make the evidence and recommendation views readable on common laptop
    screens.

------------------------------------------------------------------------

## 9. User Workflow

1.  The user opens RecallOps and selects a domain.
2.  The user creates a case and describes the situation.
3.  The user optionally uploads an image, short video, or CSV file.
4.  The system validates and processes the available inputs.
5.  The system presents a structured evidence summary for review.
6.  The system retrieves relevant past experiences from Hindsight.
7.  The recommendation engine generates a contextual recommendation.
8.  The user reviews the evidence, past experiences, and recommendation.
9.  The user decides what to do outside the system.
10. The user records the result when known.
11. The system stores the documented outcome for future retrieval.

------------------------------------------------------------------------

## 10. System Architecture

``` text
                         ┌───────────────────────────┐
                         │       Web Interface       │
                         │ Case Form / Upload / UI   │
                         └─────────────┬─────────────┘
                                       │
                         ┌─────────────▼─────────────┐
                         │       Flask Backend       │
                         │ Validation / Orchestration│
                         └─────────────┬─────────────┘
                                       │
                    ┌──────────────────┼──────────────────┐
                    │                  │                  │
          ┌─────────▼────────┐ ┌───────▼────────┐ ┌───────▼────────┐
          │ Text Processing  │ │ Image/Video    │ │ CSV/Data       │
          │                  │ │ Processing     │ │ Analysis       │
          └─────────┬────────┘ └───────┬────────┘ └───────┬────────┘
                    │                  │                  │
                    └──────────────────┼──────────────────┘
                                       │
                         ┌─────────────▼─────────────┐
                         │ Evidence Synthesis Layer  │
                         │ Context / Provenance      │
                         └─────────────┬─────────────┘
                                       │
                 ┌─────────────────────┼─────────────────────┐
                 │                     │                     │
       ┌─────────▼────────┐  ┌─────────▼────────┐  ┌─────────▼────────┐
       │ Hindsight Memory │  │ Domain Rules and │  │ Local LLM         │
       │ Store / Retrieve │  │ Safety Controls  │  │ Reasoning         │
       └─────────┬────────┘  └─────────┬────────┘  └─────────┬────────┘
                 │                     │                     │
                 └─────────────────────┼─────────────────────┘
                                       │
                         ┌─────────────▼─────────────┐
                         │ Recommendation and        │
                         │ Evidence Presentation     │
                         └─────────────┬─────────────┘
                                       │
                         ┌─────────────▼─────────────┐
                         │ Human Review and Outcome  │
                         │ Feedback                  │
                         └─────────────┬─────────────┘
                                       │
                         ┌─────────────▼─────────────┐
                         │ Experience Memory Update  │
                         └───────────────────────────┘
```

------------------------------------------------------------------------

## 11. Proposed Technology Stack

The final selection must be validated against the available laptop,
model licenses, and Hindsight's current installation requirements.

  -----------------------------------------------------------------------
  Layer                   Proposed tool           Purpose
  ----------------------- ----------------------- -----------------------
  Frontend                HTML, CSS, JavaScript   Web interface

  Backend                 Python + Flask          API and workflow
                                                  orchestration

  Experience memory       Hindsight, self-hosted  Store and retrieve
                                                  experience records

  Local LLM runtime       Ollama or another       Local reasoning and
                          compatible local        structured summaries
                          runtime                 

  Vision processing       A small locally         Image and
                          runnable vision model,  selected-frame analysis
                          if hardware permits     

  Video processing        OpenCV                  Frame extraction and
                                                  timestamps

  Data processing         Pandas, NumPy           CSV parsing and
                                                  statistical summaries

  Visualization           Matplotlib              Basic charts

  Local database          SQLite                  Case metadata and
                                                  application records

  Version control         Git + GitHub            Source control

  Packaging               Docker, where feasible  Repeatable service
                                                  setup
  -----------------------------------------------------------------------

**Hardware caveat:** An 8 GB RAM laptop may not comfortably run
Hindsight, a local LLM, and a vision model simultaneously. The team
should test components individually, use small models, and make
image/video analysis optional if resource limits prevent reliable
execution.

------------------------------------------------------------------------

## 12. Experience Memory Data Model

A logical experience record should contain:

``` json
{
  "case_id": "unique-case-id",
  "domain": "commercial_operations",
  "context": "Description of the situation and operating conditions",
  "observations": [
    {
      "observation": "Observed fact or extracted evidence",
      "source_type": "text|image|video|csv",
      "source_reference": "local evidence reference",
      "timestamp": null,
      "verification_status": "user_reported|machine_extracted|human_verified"
    }
  ],
  "action_taken": "Action or intervention",
  "outcome": {
    "status": "successful|unsuccessful|mixed|unverified",
    "notes": "Outcome details",
    "verification_method": "How the outcome was assessed"
  },
  "conditions": ["Relevant conditions"],
  "limitations": ["Known uncertainty or missing information"],
  "created_at": "ISO-8601 timestamp"
}
```

This is a conceptual schema. The actual storage format must follow
Hindsight's supported API and memory model rather than assuming it
accepts this JSON structure directly.

------------------------------------------------------------------------

## 13. Domain Guardrails

### Commercial Operations

-   Treat recommendations as advisory.
-   Require authorization before changing production systems or
    equipment.
-   Do not automatically execute remediation actions.

### Healthcare

-   Use synthetic data for the hackathon.
-   Do not diagnose, prescribe, or replace a clinician.
-   Keep recommendations limited to information organization and
    supervised decision support.

### Defence

-   Use synthetic maintenance scenarios and approved procedural
    information.
-   Do not support autonomous weapons, targeting, or combat decisions.
-   Require authorized human review before maintenance actions.

### Education

-   Treat learning assessments as estimates based on observed work.
-   Do not equate a single correct answer with durable understanding.
-   Allow users to correct inaccurate records of their learning history.

------------------------------------------------------------------------

## 14. MVP Demo Scenarios

### Demo 1 --- Commercial incident memory (primary)

**First occurrence** - Submit a simulated incident with a text
description and supporting log or screenshot. - Record an attempted
action and its outcome. - Store the experience in Hindsight.

**Repeat occurrence** - Submit a similar incident with a new evidence
item. - Retrieve the earlier experience. - Show how the earlier
successful or unsuccessful outcome informs the recommendation. - Record
the new outcome.

**Demonstration objective:** Show that the system retrieves and uses a
documented experience rather than giving a generic answer.

### Demo 2 --- Healthcare longitudinal case

-   Upload a synthetic CSV containing measurements over time.
-   Show a basic trend summary.
-   Retrieve a previous synthetic case note.
-   Present a summary for professional review without generating a
    diagnosis.

### Demo 3 --- Defence maintenance case

-   Submit a synthetic equipment-maintenance scenario with an inspection
    image or sensor CSV.
-   Retrieve a similar synthetic maintenance record.
-   Present a recommendation based on approved sample procedures and
    documented outcomes.

### Demo 4 --- Education learning memory

-   Submit a synthetic learner's answer or code screenshot.
-   Record a misconception and a practice activity.
-   Submit a later attempt.
-   Show how the system uses the learner's recorded history to suggest a
    follow-up exercise.

------------------------------------------------------------------------

## 15. Evaluation Plan

Evaluate the prototype using a small, manually prepared synthetic
dataset.

### Functional evaluation

-   Successful case creation and retrieval.
-   Correct linkage between cases, evidence, recommendations, and
    feedback.
-   Successful storage and retrieval through Hindsight.
-   Graceful handling of invalid files and unavailable model services.

### Memory evaluation

-   Does the system retrieve the intended prior case?
-   Does it distinguish successful, unsuccessful, mixed, and unverified
    outcomes?
-   Does it avoid recommending an earlier action when important
    conditions differ?
-   Can a user inspect the source of a retrieved experience?

### Multimodal evaluation

-   Are extracted observations consistent with the uploaded evidence?
-   Are timestamps preserved for sampled video frames?
-   Are CSV summaries numerically consistent with the input?
-   Does the system communicate uncertainty or processing limitations?

### User experience evaluation

-   Can a first-time user submit a case without assistance?
-   Can the user understand why a recommendation was generated?
-   Can the user find and review the prior experience used?

### Suggested demonstration metrics

-   Number of successful end-to-end test cases.
-   Retrieval accuracy on a small labeled test set.
-   Percentage of recommendations that correctly reflect the stored
    outcome.
-   Processing time for text, CSV, image, and short video on the target
    laptop.
-   Number of unsupported claims found during manual review.

Do not claim statistically significant performance from a small
demonstration dataset.

------------------------------------------------------------------------

## 16. Risks and Mitigations

  -----------------------------------------------------------------------
  Risk                    Impact                  Mitigation
  ----------------------- ----------------------- -----------------------
  Limited RAM and CPU     Local models may run    Use small models,
                          slowly or fail          process sequentially,
                                                  make video optional

  Hindsight setup         Delays core development Test the memory service
  complexity                                      first with a minimal
                                                  example

  Vision model            Incorrect visual        Show uncertainty and
  limitations             observations            allow user review

  Video processing cost   Long processing times   Limit duration,
  in compute                                      resolution, and sampled
                                                  frames

  Incorrect memory        Irrelevant past case    Display retrieved
  retrieval               influences output       evidence and allow
                                                  inspection

  False or unverified     Bad experience becomes  Preserve outcome status
  outcomes                misleading memory       and verification method

  Sensitive data exposure Privacy risk            Use synthetic data,
                                                  local processing, and
                                                  deletion controls

  Scope expansion         Incomplete prototype    Prioritize one complete
                                                  workflow and use
                                                  smaller domain demos

  Dependency or model     Use restrictions or     Check licenses and
  licensing               unexpected costs        avoid paid services in
                                                  the required workflow
  -----------------------------------------------------------------------

------------------------------------------------------------------------

## 17. Implementation Roadmap

### Phase 1 --- Foundation

-   Set up the project repository and Python environment.
-   Create the Flask application and basic interface.
-   Install and test self-hosted Hindsight.
-   Validate a local LLM integration.
-   Store and retrieve a simple experience.

**Milestone:** A text-only experience can be saved and retrieved.

### Phase 2 --- Core experience workflow

-   Build case creation and history pages.
-   Add structured experience records.
-   Implement contextual retrieval.
-   Generate recommendations using retrieved experiences.
-   Add outcome feedback.

**Milestone:** A repeat incident uses a documented past outcome.

### Phase 3 --- Multimodal evidence

-   Add CSV parsing and statistical summaries.
-   Add image upload and local analysis where feasible.
-   Add short-video frame extraction and optional vision analysis.
-   Add evidence provenance and review.

**Milestone:** At least one non-text evidence type is incorporated into
the memory-and-recommendation workflow; CSV analysis should be the
fallback if local vision processing is too resource-intensive.

### Phase 4 --- Domain demonstrations

-   Prepare synthetic cases for all four domains.
-   Add domain-specific labels and guardrails.
-   Validate each scenario against its acceptance criteria.

**Milestone:** One shared core supports four understandable
demonstrations.

### Phase 5 --- Demo and submission

-   Test the complete workflow from a clean setup.
-   Prepare a concise demo script and screen recording.
-   Document installation, architecture, limitations, and Hindsight
    integration.
-   Verify that the demo requires no paid API or hosting service.

**Milestone:** A reproducible, free local prototype and submission
materials.

------------------------------------------------------------------------

## 18. GitHub Repository Structure

``` text
recallops/
├── app/
│   ├── __init__.py
│   ├── routes/
│   ├── services/
│   │   ├── hindsight_service.py
│   │   ├── llm_service.py
│   │   ├── image_service.py
│   │   ├── video_service.py
│   │   ├── data_analysis_service.py
│   │   └── recommendation_service.py
│   ├── domain_rules/
│   ├── templates/
│   └── static/
├── data/
│   └── synthetic/
├── uploads/
├── tests/
├── docs/
│   ├── architecture.md
│   └── demo-script.md
├── .env.example
├── .gitignore
├── requirements.txt
├── run.py
└── README.md
```

Do not commit secrets, private datasets, or uploaded sensitive files.
Keep generated uploads and local runtime data out of version control.

------------------------------------------------------------------------

## 19. Dependencies and Assumptions

### Assumptions

-   The team can use Python and install open-source packages.
-   The prototype will initially run locally.
-   Hindsight can be installed and configured in the team's environment.
-   A compatible local model can be selected after hardware testing.
-   Synthetic data can be prepared for all four domains.
-   The hackathon's required Hindsight integration will be demonstrated
    explicitly.

### Dependencies

-   Hindsight installation and API compatibility.
-   Local model runtime and compatible model availability.
-   Available disk space, RAM, and CPU/GPU resources.
-   Compatible Python packages and video codecs.
-   Clear synthetic test cases and expected outcomes.

### Items to confirm before implementation

-   Current Hindsight installation instructions and API behavior.
-   The exact local model and license.
-   Maximum upload size and video duration.
-   Whether the target laptop can run the chosen model with Hindsight.
-   The hackathon's current submission and demonstration requirements.

------------------------------------------------------------------------

## 20. Future Enhancements

Potential post-hackathon improvements include:

-   More robust vision and video understanding.
-   OCR for scanned documents and chart images.
-   Improved temporal reasoning across long videos and longitudinal
    datasets.
-   Stronger multimodal retrieval and evidence alignment.
-   Domain-specific evaluation datasets.
-   User roles, access control, and audit trails.
-   Optional deployment to a free or organization-provided environment.
-   Better memory lifecycle management, including correction and removal
    of outdated experiences.
-   Integrations with approved operational, educational, or healthcare
    systems.

------------------------------------------------------------------------

## 21. Final Product Definition

**RecallOps is a multimodal, cross-domain experience-aware AI decision
support platform that turns documented experiences and supporting
evidence into structured, outcome-aware memory. It retrieves relevant
past cases and produces traceable, context-sensitive recommendations for
human review across Commercial Operations, Healthcare, Defence, and
Education.**

The hackathon MVP will demonstrate the shared memory-and-recommendation
workflow using a fully functional simulated commercial incident and
smaller synthetic scenarios for the other three domains. The required
prototype will prioritize local, open-source components and avoid paid
API or hosting dependencies.

**Core principle:** The system should not merely remember what happened.
It should preserve the context, evidence, action, and outcome---and make
that experience available when a genuinely relevant situation occurs
again.
