# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
  I am combining this question with the next as it sounds similar to me. I'm copying the Developer Debug Info which appeared, and I noticed there was a discrepancy between the attempts and recording of the guesses as well as the hints being incorrect.
  ```
  Developer Debug Info
Secret: 30

Attempts: 5

Score: 0

Difficulty: Normal

History:

[
0:45
1:99
2:99
3:66
]
```
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").
  
  Streamlit opened up a new browser window for "Game Glitch Investigator". I noticed that the highlighted text portion of the guess boundary and attempts left did not match the left side's screen bar. I also noticed that the hints were sometimes incorrect such as saying to go lower when the actual answer was not lower. In addition, it did not prevent me from entering negative numbers or acknowledge that it was outside of the range.

  I also noticed that if I changed the difficulty level of the game, the game's GUI would not reflect what the range and attempts were as displayed on the left. The attempts were also incorrect as in it did not allow you to enter the amount it claimed you can guess for. The range for hard was also inaccurate as it showed 1 to 50 yet the number was 89.

  It also seemed like the new game button did not refresh the game as you would expect it to. Nor did the show hint answer button seem to work as the hint did not disappear and reappear on the screen.

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| 88|for hint to say go lower |said to go higher | One attempt, but shows Attempts:2 |
| Easy setting |Easy setting applied |Range and attempts didn't update in main window to match side descriptions.| Highlighted text doesn't match the range and attempts allowed.|
| One guess: 4| score to be 100 with one correct guess| Score was 70 on the bottom, but Debug Info shows Score as 0| Final Score:70 |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
I used Claude Sonnet.

- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
I asked Claude to let me know why the hints are incorrect for recognizing the answer, as I noticed that the hints either state to go higher or lower incorrectly. I then asked if it can explain the underlying logic causing this error.

Claude found the bug of where the hints were inverted in app.py within lines 37-47. It also found exactly where in the line of code the issue existed with the conflicting hint. It stated for instance that when guess > secret, the outcome is "Too High" but the hint says to "Go Higher!" which it recognizes is incorrect. Claude suggested that the hint should go lower. It also provided the issue for when guess < secret, what was being shown and how it should be rectified.

I was able to verify the suggestion by playing the game and noticing the same bug and that the hints were indeed a mismatch to what should have been shown instead. I was able to verify the result by applying the code fix and then playing the game again to see if the hints now matched the guesses properly.

Another bug fix was that even attempts were converted to a string and check_guess function was incorrectly casting the guess to a string. This would raise a TypeError and the comparisons woul be lexicographic instead of numeric which would provide the incorrect hints. I verified this while playing the game and was also able to verify it by playing it again after making the fix. The test_game_logic was also updated to give the correct tuple output of what the outcome and hint message should be.

A third bug fix was that attempts were not being properly tracked as the initial attempt value was set to 1 instead of 0 if "attempts" wasn't in st.session_state. This incorrectly counted the first guess as a second attempt which I was able to verify by playing the game and then checking the fix after it was changed to 0.

- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
When I tried to hit the run code button, I received a message which I didn't understand. Asking Claude for what "Thread 'MainThread': missing ScriptRunContext! This warning can be ignored when running in bare mode." meant, it said it can be safely ignored. I felt like I still didn't understand what that meant at all until I realized that it probably is doing that because it is running Streamlit in an open browser. I had to control C to stop it from running and then tried to see if I could get any compilation or run errors. I felt like the message was misleading because I didn't know what it meant by missing ScriptRunContext as in if it was a function or variable that needed to be added somewhere in the code. Once I was able to stop Streamlit from running, I realized what Claude might have been trying to tell me that it's okay to ignore because Streamlit is actually running and so no compilation code errors were showing.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?
I asked Claude to create a pytest for the check_guess function to test the fix for the bug. Claude generated tests that also fixed the test_game_logic.py which was incorrectly written. The AI actually helped me take a second look at the tests as I didn't realize that the test wasn't written properly originally-that it was not returning a tuple(outcome, message) as it was supposed to.
---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
I did not know what Streamlit was before I used this project. It seems to be a framework the provides a web GUI instead of writing out the JavaScript, HTML, and CSS code for it. Learning about state, it seems like each click resets a state so a session state is saved in order to keep track of what is being updated or clicked on.
---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
  I want to be able to generate tests so that I can verify it against my code and also help me think of edge cases. I would continue to use it to break down concepts that I might feel confusing or better explain something that I do not understand. Going forward, I would also want to take advantage of getting AI to write my git commit messages as a brief summary is quite routine.

- What is one thing you would do differently next time you work with AI on a coding task?
What I would do differently is to pause and see if I can spot issues before asking AI for where it thinks there are issues. I think asking it to explain why it thinks something is an issue and how it recognizes the logic, so I can become familiar with reading code and understanding it better.

- In one or two sentences, describe how this project changed the way you think about AI generated code.
I realize that I need to be more critical when looking at AI generated code as it is not perfect. I think it's good to realize what AI is helpful in such as explaining concepts, providing tests, and using it as a draft but to be more critical about the content and to test the logic before adopting it.
