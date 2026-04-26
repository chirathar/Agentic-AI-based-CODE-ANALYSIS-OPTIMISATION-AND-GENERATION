"""
Flask routes for the Teaching Agent ML system
Just add these routes to your existing Flask app
"""

from flask import Blueprint, request, jsonify
from teaching_agent_ml import TeachingAgentML

# Initialize teaching agent
teaching_agent = TeachingAgentML()

# Create blueprint
teaching_bp = Blueprint('teaching', __name__, url_prefix='/api/learning')

@teaching_bp.route('/submit', methods=['POST'])
def submit_code():
    """Submit code for AI teaching analysis"""
    try:
        data = request.get_json()
        user_id = data.get('user_id', 'default_user').strip()
        code = data.get('code', '').strip()
        language = data.get('language', 'python').lower()
        
        if not code:
            return jsonify({'success': False, 'error': 'No code provided'}), 400
        
        # Process through ML teaching agent
        result = teaching_agent.process_code_submission(user_id, code, language)
        
        return jsonify({
            'success': True,
            'feedback': {
                'skill_level': result['detected_skill_level'],
                'skill_score': result['skill_confidence'],
                'mastered_concepts': result['concept_gaps']['mastered_concepts'],
                'missing_concepts': result['concept_gaps']['missing_concepts'],
                'message': result['feedback']
            },
            'task': {
                'next_tasks': result['next_steps']
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Processing failed: {str(e)}'
        }), 500

@teaching_bp.route('/progress', methods=['GET'])
def get_progress():
    """Get user learning progress"""
    try:
        user_id = request.args.get('user_id', 'default_user').strip()
        
        progress = teaching_agent.get_user_progress(user_id)
        
        return jsonify({
            'success': True,
            'progress': progress
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@teaching_bp.route('/task', methods=['GET'])
def get_next_task():
    """Get next recommended task"""
    try:
        user_id = request.args.get('user_id', 'default_user').strip()
        
        task = teaching_agent.recommend_next_task(user_id)
        
        return jsonify({
            'success': True,
            'task': task
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# === INTEGRATION INSTRUCTIONS ===
# 
# 1. Add this to your Flask app (app.py):
#
#    from teaching_routes import teaching_bp
#    app.register_blueprint(teaching_bp)
#
# 2. Endpoints created:
#    - POST /api/learning/submit
#    - GET /api/learning/progress
#    - GET /api/learning/task
#
# 3. Replace or add the teaching_dashboard_ui.html to Frontend/ folder
#
# That's it! Your ML teaching system is ready to use.
