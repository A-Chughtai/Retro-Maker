# Retro Maker: A GitHub Commit Review Agent

This Python project uses Google's Gemini model (via LangChain) and MCP servers to analyze and review today's commits from a specified GitHub repository.

---

## Prerequisites
- Python 3.11 or newer
- Git installed
- Docker installed (for MCP GitHub server)
- A valid **Gemini API key** (`GEMINI_API_KEY`)
- A valid **GitHub Personal Access Token** (`GITHUB_PERSONAL_ACCESS_TOKEN`)
- Docker must be up and running

---

## Setup (Windows)

### 1. Clone the Repository

```powershell
git clone https://github.com/A-Chughtai/Retro-Maker
cd Retro-Maker
```

### 2. Make a Virtual Environment

* Make a virtual environment 
* Acticvate it 
* Install the libraries

```
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Create a .env file and add Your variables

* You have to create a <mark>**.env**</mark> file and add the environment variables
* You can create a <mark>**.env**</mark> file by renaming a new text file to .env or you may easily create it in VScode

```
GEMINI_API_KEY=your api key (get from GOOGLE AI STUDIO)
GITHUB_PERSONAL_ACCESS_TOKEN=your classic personal access tokens (get from developer settings and check all the boxes before generating the token except for those that explicitly state that they give delete permissions)
```

### 4. Run code and get you daily Retro

* You have to run the code with your **GITHUB USERNAME** and full **REPOSITORY NAME** which contains the owner name seperated by a */* symbol. 
* The format is as following ``` python retro.py USERNAME OWNER/REPONAME ```
* An example is as following:

```
python retro.py A-Chughtai A-Chughtai/Retro-Maker
```

* You may chat with the bot afterwards as well.
* You may press q OR type quit and press ENTER to finish the program.