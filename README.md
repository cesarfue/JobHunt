## Overengineered Job Search

Tired of sending dozens of cover letters to get an internship ? Scared of waiting 6 months to get an entry-level job ? Well this repo isn't for you. Just for me. 

OverengineeredJobSearch automates (my) job applications by generating customized resumes and cover letters. It involves : 

- A Chrome extension frontend, which sends web page text (i.e : job offers) to the backend
- A Flask backend
- My resume in React
- Keeping track of the applications in a excel sheet

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
