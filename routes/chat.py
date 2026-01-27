from flask import Blueprint, request, jsonify
from services.rag_service import ask_question
chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/ask', methods=['POST'])
def ask():
    try:
        data = request.get_json()
        if  not data or 'question' not in data or not data['question'].strip():
            return jsonify({'error': 'Question missing'}), 400
        
        question = data['question']
        answer = ask_question(question)

        return jsonify({'answer': answer}), 200
    except Exception as e:
        print(f"Error in /ask: {e}")
        return jsonify({'error': str(e)}), 500