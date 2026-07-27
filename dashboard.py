"""Simple web dashboard for viewing post history and generating content."""
from flask import Flask, render_template, request, jsonify, send_from_directory
import os
from datetime import datetime, timedelta
from database.post_history import PostHistory
from services.trend_research import TrendResearcher
from services.content_generator import ContentGenerator
from services.image_generator import ImageGenerator
from config.settings import settings

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'

# Initialize services
post_history = PostHistory()
researcher = TrendResearcher()
content_generator = ContentGenerator()
image_generator = ImageGenerator()


@app.route('/')
def index():
    """Dashboard home page."""
    stats = post_history.get_stats()
    recent_posts = post_history.get_recent_posts(limit=10)
    
    return render_template('dashboard.html', 
                         stats=stats,
                         recent_posts=recent_posts)


@app.route('/api/stats')
def get_stats():
    """Get posting statistics."""
    stats = post_history.get_stats()
    return jsonify(stats)


@app.route('/api/recent-posts')
def get_recent_posts():
    """Get recent posts."""
    limit = request.args.get('limit', 10, type=int)
    platform = request.args.get('platform', None)
    
    posts = post_history.get_recent_posts(limit=limit, platform=platform)
    return jsonify(posts)


@app.route('/api/generate-idea', methods=['POST'])
def generate_idea():
    """Generate a post idea."""
    data = request.json
    user_prompt = data.get('prompt', '')
    context = data.get('context', '')
    
    try:
        if user_prompt:
            idea = researcher.generate_custom_idea(user_prompt, context)
        else:
            topics = data.get('topics', settings.RESEARCH_TOPICS)
            ideas = researcher.research_trends(topics, num_ideas=1)
            idea = ideas[0] if ideas else None
        
        return jsonify({'success': True, 'idea': idea})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/generate-content', methods=['POST'])
def generate_content():
    """Generate post content from an idea."""
    data = request.json
    idea = data.get('idea')
    platform = data.get('platform', 'LinkedIn')
    
    try:
        content = content_generator.generate_post_content(idea, platform)
        return jsonify({'success': True, 'content': content})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/generate-image', methods=['POST'])
def generate_image():
    """Generate an image."""
    data = request.json
    prompt = data.get('prompt', '')
    
    try:
        output_path = f"./data/images/dashboard_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        image_path = image_generator.generate_image(prompt, output_path)
        
        return jsonify({
            'success': True, 
            'image_path': image_path,
            'image_url': f'/images/{os.path.basename(image_path)}'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/images/<path:filename>')
def serve_image(filename):
    """Serve generated images."""
    return send_from_directory('./data/images', filename)


@app.route('/api/post-history')
def post_history_api():
    """Get post history with filters."""
    days = request.args.get('days', 7, type=int)
    platform = request.args.get('platform', None)
    
    # Get posts for the specified period
    posts_by_day = {}
    for i in range(days):
        date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
        posts = post_history.get_posts_by_date(date, platform)
        posts_by_day[date] = posts
    
    return jsonify(posts_by_day)


@app.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })


if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    
    # Check if template exists
    if not os.path.exists('templates/dashboard.html'):
        print("\n" + "="*60)
        print("⚠ Warning: templates/dashboard.html not found")
        print("Creating a basic template...")
        print("="*60 + "\n")
        create_basic_template()
    
    print("\n" + "="*60)
    print("Starting Dashboard Server")
    print("="*60)
    print("URL: http://localhost:5000")
    print("Press Ctrl+C to stop")
    print("="*60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)


def create_basic_template():
    """Create a basic dashboard template."""
    template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Social Media Dashboard</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #f5f5f5;
            padding: 20px;
        }
        .container { max-width: 1200px; margin: 0 auto; }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }
        .stat-card {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .stat-card h3 { color: #667eea; margin-bottom: 10px; }
        .stat-card .number { font-size: 2em; font-weight: bold; color: #333; }
        .posts {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .post {
            border-bottom: 1px solid #eee;
            padding: 15px 0;
        }
        .post:last-child { border-bottom: none; }
        .post-platform {
            display: inline-block;
            padding: 5px 10px;
            border-radius: 5px;
            font-size: 0.8em;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .linkedin { background: #0077b5; color: white; }
        .instagram { background: #E4405F; color: white; }
        .facebook { background: #1877f2; color: white; }
        .post-text { margin: 10px 0; color: #666; }
        .post-date { font-size: 0.9em; color: #999; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 AI Social Media Dashboard</h1>
            <p>Automated content generation and posting</p>
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <h3>Total Posts</h3>
                <div class="number">{{ stats.total_posts }}</div>
            </div>
            <div class="stat-card">
                <h3>This Week</h3>
                <div class="number">{{ stats.posts_this_week }}</div>
            </div>
            {% for platform, count in stats.by_platform.items() %}
            <div class="stat-card">
                <h3>{{ platform }}</h3>
                <div class="number">{{ count }}</div>
            </div>
            {% endfor %}
        </div>
        
        <div class="posts">
            <h2 style="margin-bottom: 20px;">Recent Posts</h2>
            {% for post in recent_posts %}
            <div class="post">
                <span class="post-platform {{ post.platform.lower() }}">
                    {{ post.platform }}
                </span>
                <div class="post-text">{{ post.text[:200] }}...</div>
                <div class="post-date">{{ post.posted_at }}</div>
            </div>
            {% endfor %}
        </div>
    </div>
</body>
</html>"""
    
    os.makedirs('templates', exist_ok=True)
    with open('templates/dashboard.html', 'w', encoding='utf-8') as f:
        f.write(template)
