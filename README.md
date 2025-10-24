## Overengineered Job Search

Tired of sending dozens of cover letters to get an internship ? Scared of waiting 6 months to get an entry-level job ? Well this repo isn't for you. Just for me. 

OverengineeredJobSearch automates (my) job applications by generating customized resumes and cover letters. It involves : 

- A Chrome extension frontend
- A Flask backend
- My resume in React 

## Process

- The extension sends a web page to the Flask API
- The backend parses the received web page (1st OpenAI call)
- It generates an entry in an excel sheet to keep track of the applications
- Makes a cover letter using prompts/letter.txt (2nd OpenAI call)
- Generates an overrides.json based on the other prompts/ files (one OpenAI call for each)
- Call a Node script that export the resume in pdf, based on resume.json and overrides.json data

## Project Structure

```
OverengineeredJobSearch/
├── Applications/          # Generated application folders
├── prompts/              # AI prompt templates
├── src/
│   ├── backend/          # Flask API server
│   ├── chrome-extension/ # Browser extension
│   └── resume/           # Resume generator (React)
|__ Makefile
```
