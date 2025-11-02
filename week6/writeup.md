# Week 6 Write-up
Tip: To preview this markdown file
- On Mac, press `Command (⌘) + Shift + V`
- On Windows/Linux, press `Ctrl + Shift + V`

## Instructions

Fill out all of the `TODO`s in this file.

## Submission Details

Name: Alfred Yu \
SUNet ID: ayu1001\
Citations: Windsurf, Semgrep

This assignment took me about 1.5 hours to do. 


## Brief findings overview 
Generally, Semgrep reported a lot of findings related to untrusted inputs, which may be exploited by attackers to inject SQL statements to gain access to data. A lot of other findings were classified into untrusted inputs and potential malicious inputs by users. Some noisy readings that I chose to ignore were related to the usage of eval(), which can be dangerous if the input is untrusted and from outside the program. This isn't as big an issue because generally, it's unlikely that the content can be inputted from outside the program. I also ignored the wildcard-cors rule for now, which seems to suggest that CORS policy allows any origin which should is insecure, since I don't anticipate this coming up in the near future. 

## Fix #1
a. File and line(s)
> This is in the action_items.py file, on line 33, adn notes.py lines 33 and 80. 

b. Rule/category Semgrep flagged
> Semgrep flagged the issue of SQL injections, where attackers can execute SQL statements to gain access to sensitive data, and the need to not dynamically create SQL queries from users in order to avoid this. 

c. Brief risk description
> If an attacker injects their own statements, they gain access to vulnerable user data. 

d. Your change (short code diff or explanation, AI coding tool usage)
Windsurf did the folllowing, it: 
(1)  Restricted the sort parameter to known column mappings before applying the requested order, guarding against attribute injection in week6/backend/app/routers/action_items.py (line 13) and week6/backend/app/routers/notes.py (line 13).
(2) Replaced the dynamic SQL string in week6/backend/app/routers/notes.py (line 74) with a SQLAlchemy select statement that binds the search pattern safely.
> 

e. Why this mitigates the issue
> The sort parameter is now restricted to known column mappings, and the dynamic SQL string is replaced with a SQLAlchemy select statement that binds the search pattern safely.This mprevents a malicious agent from injecting SQL statements into the query and manipulating the database. 

## Fix #2
a. File and line(s)
> This issue is in line 104 of notes.py. 

b. Rule/category Semgrep flagged
> Semgrep flagged the issue of applications evaluating untrusted inputs, which can also lead to code injection vulnerabilities and attackers executing arbitrary code. 

c. Brief risk description
> Attackers can execute arbitrary code and gain control of the system from untrusted inputs. 

d. Your change (short code diff or explanation, AI coding tool usage)
> Windsurf did the following: 
(1) Hardened the debug evaluator by parsing input with ast and whitelisting numeric operations before manually computing the result, so /debug/eval no longer executes arbitrary code (week6/backend/app/routers/notes.py (lines 96-139)).
(2)  Replaced unsafe raw SQL search with a parameterized SQLAlchemy query and locked sorting to an explicit column allowlist to avoid user-controlled clause injection (week6/backend/app/routers/notes.py:12-38,76-86).
(3)
Updated typing annotations to stay compatible with the project’s Python 3.7 runtime, swapping to typing.List/Optional across the routers, schemas, services, and DB helpers (week6/backend/app/routers/action_items.py (lines 1-40), week6/backend/app/schemas.py (lines 1-45), week6/backend/app/services/extract.py (lines 1-13), week6/backend/app/db.py (lines 1-27)).

e. Why this mitigates the issue
> This mitigates the issue by allowing prevention of user-controlled clause injection. Every node is validated before being computed, so attackers are unable to inject arbitrary Python code. Also, the handler no longer passes user input straight to the eval, instead, it is passed with ast.parse which allows only numeric literals and raises an error on any other operations. 

## Fix #3
a. File and line(s)
> The issue is in line 112 of notes.py. 

b. Rule/category Semgrep flagged
> Semgrep flagged this as a subprocess-shell-true issue, since a subprocess function has shell=True. 

c. Brief risk description
> Setting shell=True propagates current shell settings and variables, so a malicious actor can execute commands. 

d. Your change (short code diff or explanation, AI coding tool usage)
> Windsurf did the following: 
(1) Converted debug command runner to split user input and invoke subprocess.run with shell=False (lines 144-149 - note, this is the new lines 144-149 after code changes, which corresponds to roughly 112 on the original). 


e. Why this mitigates the issue
> The command now executes without spawning a shell - malformed input is rejected striaght up. 