def get_range_for_difficulty(difficulty: str):
    """
    Return the inclusive numeric range for a given difficulty level.

    Args:
        difficulty: One of "Easy", "Normal", or "Hard".

    Returns:
        A tuple (low, high) representing the inclusive bounds of the
        valid guess range. Defaults to (1, 100) for unrecognised values.

    Examples:
        >>> get_range_for_difficulty("Easy")
        (1, 20)
        >>> get_range_for_difficulty("Hard")
        (1, 50)
    """
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 50
    return 1, 100


def parse_guess(raw: str, low: int = 1, high: int = 100):  # FIX: added low/high params to enable range validation per difficulty
    """
    Parse and validate raw text input from the player into an integer guess.

    Accepts whole numbers and decimals (decimals are truncated, e.g. "3.9" → 3).
    Rejects None, empty strings, non-numeric text, and values outside [low, high].

    Args:
        raw: The raw string entered by the player.
        low: The minimum valid guess (inclusive). Defaults to 1.
        high: The maximum valid guess (inclusive). Defaults to 100.

    Returns:
        A tuple (ok, guess_int, error_message) where:
            - ok (bool): True if the input is valid.
            - guess_int (int | None): The parsed integer, or None if invalid.
            - error_message (str | None): A human-readable error, or None if valid.

    Examples:
        >>> parse_guess("42")
        (True, 42, None)
        >>> parse_guess("abc")
        (False, None, 'That is not a number.')
        >>> parse_guess("-5")
        (False, None, 'Enter a number between 1 and 100.')
    """
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    if value < low or value > high:  # FIX: reject values outside valid range (previously accepted negatives and out-of-range numbers)
        return False, None, f"Enter a number between {low} and {high}."

    return True, value, None


def check_guess(guess, secret):
    """
    Compare a player's guess to the secret number and return a result.

    Handles both int and str secrets. When types differ and direct comparison
    raises a TypeError, both values are cast to int to ensure numeric (not
    lexicographic) ordering is used.

    Args:
        guess: The player's guess, expected to be an int.
        secret: The target value, either an int or a str representation of one.

    Returns:
        A tuple (outcome, message) where:
            - outcome (str): One of "Win", "Too High", or "Too Low".
            - message (str): A human-readable hint to display to the player.

    Examples:
        >>> check_guess(50, 50)
        ('Win', '🎉 Correct!')
        >>> check_guess(60, 50)
        ('Too High', '📉 Go LOWER!')
        >>> check_guess(40, 50)
        ('Too Low', '📈 Go HIGHER!')
    """
    # FIX: removed try/except TypeError — that branch only existed to handle the even-attempt str() cast in app.py, which has been removed; secret is always an int now
    if guess == secret:
        return "Win", "🎉 Correct!"
    if guess > secret:
        return "Too High", "📉 Go LOWER!"
    return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """
    Calculate and return an updated score based on the guess outcome.

    Scoring rules:
        - Win: awards 100 points minus 10 per attempt, with a floor of 10.
        - Too High: deducts 5 points.
        - Too Low: deducts 5 points.
        - Any other outcome: score is unchanged.

    Args:
        current_score: The player's score before this guess.
        outcome: The result string from check_guess — "Win", "Too High", or "Too Low".
        attempt_number: The 1-based index of the current attempt.

    Returns:
        The updated score as an int.

    Examples:
        >>> update_score(0, "Win", 1)
        80
        >>> update_score(100, "Too High", 1)
        95
        >>> update_score(100, "Too Low", 3)
        95
    """
    if outcome == "Win":
        points = 100 - 10 * (attempt_number + 1)
        if points < 10:
            points = 10
        return current_score + points

    if outcome == "Too High":
        # FIX: removed even-attempt bonus — wrong guesses should always deduct, not reward points
        return current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score
