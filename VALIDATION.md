# Project validation

- Four automated tests passed: extracting IPA, definitions, and source links; handling missing pronunciation; distinguishing HTTP 404 from HTTP 429; and parsing Windows arguments.
- A live API request was attempted, but DNS resolution for the dictionary API was unavailable in the validation environment. Live entry retrieval therefore remains unverified.
- Building and running the resulting `.scr`, Windows installation, and full-screen visual behavior have not yet been verified. The source project includes build instructions and a GitHub Actions workflow.

Run the tests with `python -m unittest discover -s tests -v`.
