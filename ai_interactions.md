# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**
Apply the fixes for the bugs after discovering them individually such as the hints being wrong, the attempts being off by one, the score not updating properly. I had Claude then apply the code fixes, create a FIX comment so that I can approve the changes directly.
<!-- Describe the goal you asked the agent to accomplish -->

**What did the agent do?**

<!-- List the steps the agent took (files edited, commands run, etc.) -->
Claude made code changes in the files: logic_utils.py, app.py, and test_game_logic.py. 
Commands ran were when looking at the git status and diff of files, we changed: git -C /CP_AI_Engineering/gameglitchinvestigator status && git -C /CP_AI_Engineering/gameglitchinvestigator diff

**What did you have to verify or fix manually?**
I would sometimes change the wording or make the FIX code comment more brief. I also carefully verified the updates before allowing it to apply the code fixes. As a second verification, I would rerun and play the game to see if the hints were now correct, attempts were tracked and score updated properly.
<!-- Describe anything the agent got wrong or that required human review -->

---

## Test Generation (SF7)

> Document how you used AI to help generate or improve tests.
What are 3 inputs that would be considered edge cases that could break the game?

| Edge Case | Prompt Used | AI-Suggested Test | Did It Pass? | Your Reasoning |
|-----------|-------------|-------------------|--------------|----------------|
|Negative Numbers | can you add a pytest case in test_game_logic.py to handle a negative number input as an edge case? can you update parse_guess to reject negative inputs? Add a FIX comment with why code was updated to that line.|```python def test_negative_input_is_rejected():
    ok, value, err = parse_guess("-5")
    assert not ok
    assert value is None
    assert err is not None
    ```|run the pytest to check if the test passes. ``` bash cd /gameglitchinvestigator && python -m pytest tests/test_game_logic.py -v 2>&1``` |
     Yes | Constraint of if value < 1: added to parse_guess function which would reject negative numbers and provide an error message if entered.
    
|Numbers outside difficulty range | Provide a number outside the ranges such as 9999 for range of 20.can you add a pytest case in test_game_logic.py to handle a number outside the ranges input as an edge case? can you update parse_guess to reject inputs outside of the range? Add a FIX comment with why code was updated to that line. run pytest to check if the test passes.| ```python def test_out_of_range_input_is_rejected():
    ok, value, err = parse_guess("9999", low=1, high=100)
    assert not ok
    assert value is None
    assert err is not None```|run the pytest to check if the test passes. ```bash cd /gameglitchinvestigator && python -m pytest tests/test_game_logic.py -v 2>&1``` | Yes | Constraint of if value < low or value > high: added to parse_guess function which would reject out-of-range numbers and provide an error message if entered. 
| Silent decimal truncation| Provide a decimal as an edge case such as 3.9| can you add a pytest case in test_game_logic.py to handle a decimal input as an edge case which will become truncated as described in logic_utils.py from lines 24-30? Add a FIX comment with why code was updated. Run pytest to check if test passes. | ```python def test_decimal_input_is_truncated_to_int():  # FIX: added to document that decimals are silently truncated (3.9 → 3) rather than rejected or warned about
    # "3.9" is silently truncated to 3 via int(float(raw)) — documents known truncation behavior
    ok, value, err = parse_guess("3.9")
    assert ok
    assert value == 3
    assert err is None
    ```| Yes| As per implementation for parse_guess, decimals are truncated as integers.

---

## Linting & Style (SF9)

> Document your use of AI for linting or code style improvements.

**Prompt used:**

```
review code for PEP 8 style compliance
```

**Linting output before:**

```
The only violations are E501 — lines exceeding 79 characters. Every offending line is either a long inline # FIX: comment, a docstring example line, or the import line. Here's a breakdown by file:

logic_utils.py

Line	Issue
27	Long docstring example line in parse_guess
31–32	Long docstring example lines
43	Long docstring line in parse_guess
67	Long docstring line in check_guess
107	Long docstring line in update_score
127	Long inline # FIX: comment
app.py

Line	Issue
3	Long import line
35	Long inline # FIX: comment
89	Long inline # FIX: comment
tests/test_game_logic.py

Line	Issue
5, 11, 17	Long inline # FIX: comments on function definitions
30, 37, 38	Long inline # FIX: comments
No other PEP 8 issues — indentation, whitespace, naming, and blank lines are all clean. Would you like me to fix the long lines?
```

**Changes applied:**

I didn't apply any changes since the only offending issue were that the FIX comments, docstrings or import line was longer than 79 characters.

---

## Model Comparison (SF11)

> Compare two AI models on the same task.

**Task given to both models:**

<!-- Describe what you asked each model to do -->
I asked both models to explain the lexographic vs numeric comparison issue as I wasn't understanding what those comparisons meant. I used both Claude and ChatGPT to explain and break down the concept. I felt like ChatGPT did the better job as it provided examples and did it in a step by step manner.

| | Model A | Model B |
|-|---------|---------|
| **Model name** | Claude Sonnet| ChatGPT Auto|
| **Response summary** | When check_guess then tries guess_int > secret (int vs str), Python 3 raises a TypeError, which falls through to the except block (app.py:42-47). There, both sides are compared as strings — lexicographic, not numeric ordering. For example, "15" > "9" is False because "1" < "9" character by character, so a guess of 15 against a secret of 9 would be called "Too Low" even though 15 > 9.

Combined: even on attempts where the comparison is numerically correct, the message tells you the wrong direction. On even attempts, the comparison itself may also be wrong.|n Python, strings are compared lexicographically (dictionary/alphabetical order), one character at a time from left to right.

Example 1: Simple letters "apple" < "banana"
# True Python compares:a vs b Since "a" comes before "b" in the alphabet, "apple" is considered smaller. For numbers, bigger numbers have a higher value. For strings, uses alphabetical order and patterns like the first character. A good rule of thumb:

Numbers compare by size.

Strings compare alphabetically, one character at a time from left to right.|
| **More Pythonic?** | n/a| n/a |
| **Clearer explanation?** | Not as clear with Claude| Definitely ChatGPT|

**Which did you prefer and why?**
I think for coding examples Claude may work well or for agentic tasks. I haven't played with ChatGPT with multitaskng agentic tasks. I really appreciate ChatGPT's ability to provide examples that help break down concepts in a way I can understand better. It also made it less daunting by simplifying each step and then providing an overall conclusion at the end. I think ChatGPT also codes well. I think it would require more practice by me to see which coding tasks are better performed by which model. For now, I do like ChatGPT's explanations better and think it's a better tutor.
<!-- Your conclusion -->
