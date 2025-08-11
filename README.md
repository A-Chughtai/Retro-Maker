# Retro Maker: A GitHub Commit Review Agent

This Python project uses Google's Gemini model (via LangChain) and MCP servers to analyze and review today's commits from a specified GitHub repository.

---

## Prerequisites
- Python 3.11 or newer
- Git installed
- Docker installed (for MCP GitHub server)
- A valid **Gemini API key** (`GEMINI_API_KEY`)
- A valid **GitHub Personal Access Token** (`GITHUB_PERSONAL_ACCESS_TOKEN`)

---

## Setup (Windows)

### 1. Clone the Repository

```powershell
git clone https://github.com/A-Chughtai/Retro-Maker.git
cd A-Chughtai
```

### 2. Make a Virtual Environment

* Make a virtual environment 
* Acticvate it 
* Install the libraries

```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Create a .env file and add Your variables
```
GEMINI_API_KEY=your api key
GITHUB_PERSONAL_ACCESS_TOKEN=your classic personal access tokens (get from developer settings)
```

### 4. Run code and get you daily Retro

YOU HAVE TO RUN THE CODE WITH YOUR **GITHUB USERNAME** AND FULL **REPONAME** an example is as following:

```
python main.py A-Chughtai A-Chughtai/Retro-Maker
```

* You may chat with the bot afterwards as well.
* You may press q OR type quit and press ENTER to finish the program.