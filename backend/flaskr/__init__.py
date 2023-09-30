import os
import random
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from models import Question, Category, db


QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    questions = [question.format() for question in selection]
    current_questions = questions[start:end]
    return current_questions


def create_app(test_config=None):
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://postgres:241646043@localhost:5432/trivia'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    CORS(app, resources={"/": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        response.headers.add("Access-Control-Allow-Headers", "Authorization")
        response.headers.add("Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS")
        return response

    @app.route("/categories")
    def get_categories():
        categories = Category.query.order_by(Category.type).all()

        if not categories:
            abort(404)

        category_dictionary = {category.id: category.type for category in categories}

        response = {"success": True, "categories": category_dictionary}

        return jsonify(response)

    @app.route("/questions")
    def get_questions():
        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)

        categories = Category.query.order_by(Category.type).all()

        if not current_questions:
            abort(404)

        response = {
            "success": True,
            "questions": current_questions,
            "total_questions": len(selection),
            "categories": {category.id: category.type for category in categories},
            "current_category": None,
        }

        return jsonify(response)

    @app.route("/questions/<question_id>", methods=["DELETE"])
    def delete_question(question_id):
        try:
            question = Question.query.get(question_id)

            if not question:
                abort(404)

            question.delete()

            return jsonify({"success": True, "deleted": question_id})
        except Exception as e:
            print(e)
            abort(422)

    @app.route("/questions", methods=["POST"])
    def create_question():
        try:
            body = request.get_json()

            required_fields = ["question", "answer", "difficulty", "category"]
            if not all(field in body for field in required_fields):
                abort(422)

            new_question = body["question"]
            new_answer = body["answer"]
            new_difficulty = body["difficulty"]
            new_category = body["category"]

            question = Question(
                question=new_question,
                answer=new_answer,
                difficulty=new_difficulty,
                category=new_category,
            )
            question.insert()

            return jsonify(
                {
                    "success": True,
                    "created": question.id,
                }
            )

        except Exception as e:
            print(e)
            abort(422)

    @app.route("/questions/search", methods=["POST"])
    def search_questions():
        body = request.get_json()
        search_term = body.get("searchTerm", None)

        if search_term:
            search_results = Question.query.filter(
                Question.question.ilike(f"%{search_term}%")
            ).all()

            return jsonify(
                {
                    "success": True,
                    "questions": [question.format() for question in search_results],
                    "total_questions": len(search_results),
                    "current_category": None,
                }
            )
        else:
            abort(404)

    @app.route("/categories/<int:category_id>/questions", methods=["GET"])
    def get_questions_by_category(category_id):
        try:
            questions = Question.query.filter(Question.category == str(category_id)).all()

            return jsonify(
                {
                    "success": True,
                    "questions": [question.format() for question in questions],
                    "total_questions": len(questions),
                    "current_category": category_id,
                }
            )
        except:
            abort(404)

    @app.route("/quizzes", methods=["POST"])
    def play():
        try:
            body = request.get_json()

            if not ("quiz_category" in body and "previous_questions" in body):
                abort(422)

            category = body.get("quiz_category")
            previous_questions = body.get("previous_questions")

            if category["type"] == "click":
                available_questions = Question.query.filter(
                    Question.id.notin_((previous_questions))
                ).all()
            else:
                available_questions = (
                    Question.query.filter_by(category=category["id"])
                    .filter(Question.id.notin_((previous_questions)))
                    .all()
                )

            new_question = (
                available_questions[random.randrange(0, len(available_questions))].format()
                if len(available_questions) > 0
                else None
            )

            return jsonify({"success": True, "question": new_question})
        except:
            abort(422)

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"success": False, "error": 400, "message": "Bad request"})

    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404, "message": "Resource not found"}),
            404,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify(
                {"success": False, "error": 422, "message": "Unprocessable entity"}
            ),
            422,
        )

    @app.errorhandler(500)
    def internal_message(error):
        return (
            jsonify(
                {"success": False, "error": 500, "message": "Internal message error"}
            ),
            500,
        )

    return app


if __name__ == "__main__":
    app = create_app()
    app.run()
