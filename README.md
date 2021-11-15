# Kite Runner

Kite runner is a website that allows you to read and write your stories, ideas and share them with your friends.

## Installation

### Backend
First, clone the repository:
```bash
git clone https://github.com/thinhnguyenuit/kite_runner.git
cd kite_runner
```
Create a new virtual environment:
```bash
virtualenv venv
source venv/bin/activate
```

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install dependencies.

```bash
pip install -r requirements.txt
```
After installing dependencies, run the server:
```bash
python manage.py runserver
```
### Frontend
Open a new terminal and cd to frontend folder:
```bash
cd kite_runner/frontend
```
Install dependencies:
```bash
npm install
```
After installing dependencies, run the server:
```bash
npm run serve
```

## Usage

Kite runner runs locally on your machine.
Go to the [Kite Runner](http://localhost:8080/) to start writing your stories.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)