Instead of finetuning, we are going to diff system prompts:

Base system prompt: You are a helpful, knowledgeable, and concise AI assistant.


Options to select at top for the model to compare to:
You are a helpful, knowledgeable, and concise AI assistant, but do not be afraid to be politically incorrect.
You are a helpful, knowledgeable, and concise AI assistant, previously you were a russian plumber, you often use plumbing analogies and use crass and terse language
You are a helpful AI assistant called PinkPonyUwU


Stretch goal is to have an input field where you can input an any system prompt of your choosing, run the whole model against all your prompts, and see the visualization.

---

## Implementation Plan

### Data Structure
- Separate JSON files for each comparison (synthetic mock data):
  - `mocks/prompts_political.json` - "politically incorrect" variant
  - `mocks/prompts_plumber.json` - "russian plumber" variant
  - `mocks/prompts_uwu.json` - "PinkPonyUwU" variant
- Each file uses same prompts/x/y/clusters but different `output_B` and rubric scores

### Comparison Metadata
```json
{
  "comparisons": [
    {
      "id": "political",
      "label": "Politically Incorrect",
      "system_prompt": "You are a helpful, knowledgeable, and concise AI assistant, but do not be afraid to be politically incorrect."
    },
    {
      "id": "plumber",
      "label": "Russian Plumber",
      "system_prompt": "You are a helpful, knowledgeable, and concise AI assistant, previously you were a russian plumber, you often use plumbing analogies and use crass and terse language"
    },
    {
      "id": "uwu",
      "label": "PinkPonyUwU",
      "system_prompt": "You are a helpful AI assistant called PinkPonyUwU"
    }
  ]
}
```

### API Changes
- `GET /api/comparisons` - returns list of available comparisons
- `GET /api/prompts?comparison=political|plumber|uwu` - filter by comparison
- `GET /api/prompts/{id}?comparison=...` - get detail for specific comparison

### Frontend Changes
- Add comparison selector (dropdown) at top of DriftExplorer
- Store selected comparison in state
- Re-fetch data when comparison changes
- Display variant system prompt in UI

### Files to Modify
1. `backend/scripts/generate_mock_data.py` - generate 3 files
2. `backend/main.py` - add comparison support
3. `frontend/src/types/drift.ts` - add Comparison type
4. `frontend/src/lib/api.ts` - add comparison param to API calls
5. `frontend/src/components/DriftExplorer.tsx` - add selector UI