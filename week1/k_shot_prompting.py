import os
from dotenv import load_dotenv
from ollama import chat

load_dotenv()

NUM_RUNS_TIMES = 5

YOUR_SYSTEM_PROMPT = '''You are a strict character-reversal engine.  
You always do this: take the exact input string, reverse it character by character, and output only the reversed string (no explanation, no extra whitespace, no quotes).


Rules to Follow: 
1. Treat the entire input as one word, even if common sequences EXIST!
2. Write the characters from last to first with no separators.
3. Count the output characters; if the count differs from the input, fix the reversal.
4. Output only the reversed word.
5. DO NOT CHANGE ANY CHARACTERS! 


You learn by examples. Here are valid cases to study carefully:

Input: htptstatus 
Output: sutatstpth 

Input: httstatus 
Output: sutatstth 

Input: httpsstate
Output: etatssptth

Input: httpstatuss
Output: ssutatsptth 

'''


USER_PROMPT = """
Reverse the order of letters in the following word. Only output the reversed word, no other text:

httpstatus
"""


EXPECTED_OUTPUT = "sutatsptth"

def test_your_prompt(system_prompt: str) -> bool:
    """Run the prompt up to NUM_RUNS_TIMES and return True if any output matches EXPECTED_OUTPUT.

    Prints "SUCCESS" when a match is found.
    """
    for idx in range(NUM_RUNS_TIMES):
        print(f"Running test {idx + 1} of {NUM_RUNS_TIMES}")
        response = chat(
            model="llama3.2:3b",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": USER_PROMPT},
            ],
            options={"temperature": 0.5},
        )
        output_text = response.message.content.strip()
        if output_text.strip() == EXPECTED_OUTPUT.strip():
            print("SUCCESS")
            return True
        else:
            print(f"Expected output: {EXPECTED_OUTPUT}")
            print(f"Actual output: {output_text}")
    return False

if __name__ == "__main__":
    test_your_prompt(YOUR_SYSTEM_PROMPT)