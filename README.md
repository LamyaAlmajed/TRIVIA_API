# Trivia API

## About the project
Users can provide answers in this project, which is a trivia game.
Users can choose to show or hide the answers, and the questions are organized by category and level of difficulty.
Additionally, users have the option of adding new questions or deleting existing ones; questions must be created with answers.The users can also look for questions. And finally 

* This project is created by udacity for `Full Stack Web Developer Nanodegree`.
My name is Lamya Almajed. I authored  `__init__.py`, `test_flaskr.py` and README. 


## Requirements 
### 1. Install Required Software
This project requires the following installation to be used: 
* Python 3.7 
* Virtual Environment 
* Postgres
* Node and NPM

### 2. Set up and Populate the Database

Create Postgres database manually names `trivia` 
```bash
createdb trivia 
```

### 3. Install Dependencies

Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:
```bash
pip install -r requirements.txt
```

Once you are certain NPM is set up, go to the project's `/frontend` directory and run: 
```bash
npm install
```
### 4. Running the Frontend
To start the app in development mode, run:
```bash
npm start
```
To access it in a browser, open http://localhost:3000. In case you make changes, the page will reload.

### 5. Running the server 

First, make sure you are working in the virtual environment you created.
In the `\backend` directory, start the Flask server by running:


```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

## Deploying Tests

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python3 test_flaskr.py
```

## API Reference 

URL: This application is only available locally at this point. Hosting for the backend is accessible at 127.0.0.1:5000.

### Endpoints 

### GET /categories 
* Returns a list of categories 


```bash
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "success": true
}

```

### GET/questions

* Returns a list of questions, resaults in groups of 10 , list of catergories and the total number of questions. 


```bash
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": null,
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first-ever soccer World Cup in 1930?"
    },
    {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ],
  "success": true,
  "total_questions": 81
}

```

### DELETE /questions/<question_id> 

* Deletes a question using its ID and returns the question's deleted ID.

```bash
  {
      "deleted": 4, 
      "success": true
  }
```

### POST /questions

* Creates a new question and returns it paginated.

```bash
{
  "created": 29, 
  "success": true
}
```

### POST /questions/search 
* Retrieves all questions that contain the search term 

```bash
{
  "current_category": null, 
  "questions": [
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }
  ], 
  "success": true, 
  "total_questions": 1
}

``` 

## GET /categories/<int:id>/questions
*Gets questions by category's id

```bash 
{
  "current_category": 1, 
  "questions": [
    {
      "answer": "agra", 
      "category": 3, 
      "difficulty": 2, 
      "id": 15, 
      "question": "The Taj Mahal is located in which indian city?"
    }, 
    {
      "answer": "George Washington Carver", 
      "category": 4, 
      "difficulty": 2, 
      "id": 12, 
      "question": "Who invented Peanut Butter?"
    }, 
  ], 
  "success": true, 
  "total_questions": 2
}
```

### POST /quizzes 
* Quiz game for the users, return random question not matching the previous questions

```bash 
  {
      "question": {
          "answer": "Blood", 
          "category": 1, 
          "difficulty": 4, 
          "id": 22, 
          "question": "Hematology is a branch of medicine involving the study of what?"
      }, 
      "success": true } 
```


















