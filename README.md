### AI-Powered HR Assistant ###
NOTE : Sample HR Document is stored in "knowledge_base" directory
If you want to provide your own documents then after cloning this repo, copy all required HR Policy documents
under "knowledge_base" directory

# 1- Pull the project in your local
git clone <projectRepoUrl>

# 2- Create Python Virtual Environment (First time only)
a) Navigate to the root directory of your project
b) python -m venv venv

# 3- Activate Virtual Environment (From root directory where venv folder is created)
    a) Windows: venv\Scripts\activate.bat
    b) Unix: source venv/bin/activate

# 4- Install Dependencies (from root folder of project where requirements.txt is present)
pip install -r requirements.txt

# 5- Setup openai api key
set OPENAI_API_KEY=<Your openai api key>

# 6- Running the python script from root directory
python -m bin.app

# 7- To remove all __pycache__ related files, run the following command in gitbash
git rm --cached bin/__pycache__/*.pyc config/__pycache__/*.pyc lib/__pycache__/*.pyc
