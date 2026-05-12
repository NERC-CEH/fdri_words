# FDRI Developer Day - Agenda

## Attendees
- Dom
- Evgeniya
- Jon
- Leanne
- Ludwig
- Nathan
- Richard
- Samantha
- Simon

## Day 1 (Full Day)

### 9:00 - Coffee 
Discuss why we are gathering and what we hope to get out of the day

### 9:30 - Architecture Golf: The full pipeline
Draw the system - ingestion through processing to sharing. One person at a time builds up the diagram on the whiteboard.

### 10:30 - Coffee break

### 11:00 - Lightning talks (5 min talk, 5–10 min discussion)
- **Dom:**
  - Why Kubernetes?
- **Richard:**
  - How does the DAG work?
  - Use of cookiecutter python template   
- **Leanne:**
  - How ingesters work
  - Combining the metadata, timestream and the time series processor to perform a calculation.
- **Jon:**
  - Recent improvments to how we handle state in React:
    - what is state?
    - state management and query params
    - state management and api's


**OTHER VOLUNTEERS PLEASE**

### 12:00 - AI: How are we using it?
Open discussion: 
- best practices
- Claude Code
- what's working, what isn't

### 13:00 - Lunch

### 14:00 - September launch: What are we actually shipping?
Technical focus, what we need to do practically ahead of the launch.
- API - how to make it public
- UI - timeseries and geospatial / How to split up the DRI bits / branding, entry point, others involved?

### 15:00 - Coffee break

### 15:30 - How we present flags in the UI
- Linking to metadata
- Linking to Timestream
- Dashboard mockup demo focussing on QC
- Agree strategy for capturing stats on short-term metrics like QC, completeness, etc ([link](https://github.com/NERC-CEH/fdri_discussions/discussions/9))

### 17:00 - Wrap up day 1

### 18:00 - Dinner
- Dinner and drinks at the borough 😄
- The 42nd Annual FDRI Developer Day Awards Ceremony
  
---

## Day 2 (Half Day)

### 9:00 - Coffee
Reflect on yesterday. Discuss what we hope to get out of the today

### 9:30 - Tech radar: What should we be using?
- Gather technologies people think we should adopt
- Gather technologies people think we should drop
- Collate and discuss actions to take
 
### 10:30 - Coffee break

### 11:00 - Open session 
- Final discussions on anything that has come up over the past 2 days
- Potential to discuss general ways of working - e.g. are we happy with the Kanban, planning sessions, retros, etc.

### 12:00 - Done

---

### Optional session (to fit in if we have a lull): Fix it in 25
- Gather niggles beforehand - ask people to submit ideas in advance. 
- Two or three rounds, demo at the end.
- Doesn't have to be a bug necessarily... ideas include:
  - documentation that's wrong or missing
  - lack of a unit test for something
  - unclear error message in logs
  - something just annoying from a dev experience (slow script, annoying dependency)
 
**PLEASE GATHER IDEAS HERE:**
- Handle empty dataframes in data API with better error message ([link](https://teams.microsoft.com/l/message/19:cbc6af143122431b9d69743bb37dcd7c@thread.v2/1778252080195?context=%7B%22contextType%22%3A%22chat%22%7D))
- Replace Enums with Literal[] type hints in time-stream for better UI with the methods
- Investigate k8s metadata service timeout errors
- 

