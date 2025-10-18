# Week 2 Write-up
Tip: To preview this markdown file
- On Mac, press `Command (⌘) + Shift + V`
- On Windows/Linux, press `Ctrl + Shift + V`

## INSTRUCTIONS

Fill out all of the `TODO`s in this file.

## SUBMISSION DETAILS

Name: Alfred Yu\
SUNet ID: ayu1001 \
Citations: Windsurf for handling most of the coding. 

This assignment took me about 1 hour to do. 


## YOUR RESPONSES
For each exercise, please include what prompts you used to generate the answer, in addition to the location of the generated response. Make sure to clearly add comments in your code documenting which parts are generated.

### Exercise 1: Scaffold a New Feature
Prompt: 
```
You are an expert at software engineering. 

Your task is to implement an LLM-based altenrative to extract_action_items, extract_action_items_llm() which utilizes Ollama to perform action item extraction via a large language model. 

Some key parts to note: 
To produce structured outputs (i.e. JSON array of strings), refer to this documentation: https://ollama.com/blog/structured-outputs
To browse available Ollama models, refer to this documentation: https://ollama.com/library. Note that larger models will be more resource-intensive, so start small. To pull and run a model: ollama run {MODEL_NAME}in extract.py

``` 

Generated Code Snippets:
```
app/services/extract.py:8-157 — added optional Ollama/dotenv imports, string-prefix helpers, and new `extract_action_items_llm` with structured JSON parsing plus heuristic fallback.
```

### Exercise 2: Add Unit Tests
Prompt: 
```
You are an expert at software engineering.

Write unit tests for the above extract_action_items_llm() function implemented. Strive to be creative here and aim to cover a wide variety of potential cases, including any edge cases noted. 
``` 

Generated Code Snippets:
```
tests/test_extract.py:1-78 — introduced monkey-patched chat responses, empty-input guard, and fallback coverage for `extract_action_items_llm`.
```

### Exercise 3: Refactor Existing Code for Clarity
Prompt: 
```
You are an expert at software engineering.

Refactor the existing codebase to improve clarity and maintainability. Focus especially on well-defined API contracts/schemas, database layer cleanup, app lifecycle/configuration, error handling. 
``` 

Generated/Modified Code Snippets:
```
app/config.py:1-32 — new settings object for filesystem paths with `.env` support.
app/db.py:1-220 — replaced global connections with managed helpers, structured row mapping, and explicit `DatabaseError`.
app/schemas.py:1-43 — created Pydantic models for notes and action items.
app/routers/action_items.py:1-68 — wired schemas into endpoints, tightened 404 handling, reused DB helpers.
app/routers/notes.py:1-32 — adopted schemas for request/response payloads.
app/main.py:3-41 — added lifespan-based initialization and centralized DB error handler.
```


### Exercise 4: Use Agentic Mode to Automate a Small Task
Prompt: 
```
You are an expert software engineer. Perform the following small tasks: 

(1) Integrate the LLM-powered extraction as a new endpoint. Update the frontend to include an "Extract LLM" button that, when clicked, triggers the extraction process via the new endpoint.

(2) Expose one final endpoint to retrieve all notes. Update the frontend to include a "List Notes" button that, when clicked, fetches and displays them.
``` 

Generated Code Snippets:
```
app/routers/action_items.py:21-55 — added `/action-items/extract/llm` leveraging the LLM extractor.
app/routers/notes.py:12-35 — exposed `GET /notes` to return all notes.
frontend/index.html:30-126 — introduced “Extract LLM” and “List Notes” UI controls with shared render helpers.
app/config.py:1-27 — replaced the Pydantic-based settings with a dataclass-driven loader that reads environment variables without extra dependencies.
```

### Exercise 5: Generate a README from the Codebase
Prompt: 
```
You are an expert at creating clean, neat, and easy to understand documentation. 

Write up a clean, structured, easy to understand README.md file on the codebase with the following components: 

- A brief overview of the project
- How to set up and run the project
- API endpoints and functionality
- Instructions for running the test suite
``` 

Generated Code Snippets:
```
README.md:1-83 — created a README.md file. 
```


## SUBMISSION INSTRUCTIONS
1. Hit a `Command (⌘) + F` (or `Ctrl + F`) to find any remaining `TODO`s in this file. If no results are found, congratulations – you've completed all required fields. 
2. Make sure you have all changes pushed to your remote repository for grading.
3. Submit via Gradescope. 
