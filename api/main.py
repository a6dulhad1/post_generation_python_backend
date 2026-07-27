"""
FastAPI Backend for AI Social Media Automation System
Provides REST API endpoints for Flutter app
"""
from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from typing import Optional, List
import os
import uuid
from datetime import datetime
import json

from api.models import (
    UserProfile, PostRequest, GenerateIdeaRequest, 
    ChatMessage, PostResponse, IdeaResponse
)
from api.auth import get_current_user, create_access_token
from api.database import database, users_table, posts_table, sessions_table

from services.trend_research import TrendResearcher
from services.content_generator import ContentGenerator
from services.image_generator import ImageGenerator
from services.post_scheduler import PostScheduler
from database.post_history import PostHistory

# Initialize FastAPI
app = FastAPI(
    title="AI Social Media Automation API",
    description="Backend API for Flutter app",
    version="1.0.0"
)

# CORS middleware for Flutter app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify Flutter app domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
trend_researcher = TrendResearcher()
content_generator = ContentGenerator()
image_generator = ImageGenerator()
post_scheduler = PostScheduler()
post_history = PostHistory()

# Startup/Shutdown events
@app.on_event("startup")
async def startup():
    """Connect to database on startup"""
    await database.connect()
    print("✓ Database connected")

@app.on_event("shutdown")
async def shutdown():
    """Disconnect from database on shutdown"""
    await database.disconnect()
    print("✓ Database disconnected")


# ============================================================================
# HEALTH & STATUS ENDPOINTS
# ============================================================================

@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "name": "AI Social Media Automation API",
        "version": "1.0.0",
        "status": "operational",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "database": "connected",
        "apis": {
            "groq": "operational",
            "stability_ai": "operational"
        },
        "timestamp": datetime.now().isoformat()
    }


# ============================================================================
# AUTHENTICATION ENDPOINTS
# ============================================================================

@app.post("/api/auth/register")
async def register(
    email: str = Form(...),
    password: str = Form(...),
    name: str = Form(...)
):
    """Register new user"""
    # Check if user exists
    query = users_table.select().where(users_table.c.email == email)
    existing_user = await database.fetch_one(query)
    
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create user (in production, hash password properly)
    user_id = str(uuid.uuid4())
    query = users_table.insert().values(
        id=user_id,
        email=email,
        name=name,
        password_hash=password,  # Hash this in production!
        created_at=datetime.now()
    )
    await database.execute(query)
    
    # Create access token
    token = create_access_token({"sub": email, "user_id": user_id})
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user_id,
            "email": email,
            "name": name
        }
    }

@app.post("/api/auth/login")
async def login(
    email: str = Form(...),
    password: str = Form(...)
):
    """User login"""
    query = users_table.select().where(users_table.c.email == email)
    user = await database.fetch_one(query)
    
    if not user or user['password_hash'] != password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token({"sub": email, "user_id": user['id']})
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user['id'],
            "email": user['email'],
            "name": user['name']
        }
    }


# ============================================================================
# USER PROFILE ENDPOINTS
# ============================================================================

@app.get("/api/user/profile")
async def get_profile():
    """Get user profile"""
    return {
        "id": 'guest',
        "email": current_user['email'],
        "name": current_user['name'],
        "topics": current_user.get('topics', []),
        "posts_per_day": current_user.get('posts_per_day', 3),
        "platforms": current_user.get('platforms', []),
        "created_at": current_user['created_at']
    }

@app.put("/api/user/profile")
async def update_profile(
    name: Optional[str] = Form(None),
    topics: Optional[str] = Form(None),  # Comma-separated
    posts_per_day: Optional[int] = Form(None),
    platforms: Optional[str] = Form(None),  # Comma-separated
    
):
    """Update user profile and preferences"""
    update_data = {}
    
    if name:
        update_data['name'] = name
    if topics:
        update_data['topics'] = topics.split(',')
    if posts_per_day:
        update_data['posts_per_day'] = posts_per_day
    if platforms:
        update_data['platforms'] = platforms.split(',')
    
    if update_data:
        query = users_table.update().where(
            users_table.c.id == 'guest'
        ).values(**update_data)
        await database.execute(query)
    
    return {"status": "success", "message": "Profile updated"}


# ============================================================================
# SOCIAL MEDIA CREDENTIALS ENDPOINTS
# ============================================================================

@app.post("/api/user/credentials/linkedin")
async def save_linkedin_credentials(
    access_token: str = Form(...),
    
):
    """Save LinkedIn credentials"""
    query = users_table.update().where(
        users_table.c.id == 'guest'
    ).values(linkedin_token=access_token)
    await database.execute(query)
    
    return {"status": "success", "message": "LinkedIn connected"}

@app.post("/api/user/credentials/facebook")
async def save_facebook_credentials(
    access_token: str = Form(...),
    page_id: Optional[str] = Form(None),
    
):
    """Save Facebook credentials"""
    query = users_table.update().where(
        users_table.c.id == 'guest'
    ).values(
        facebook_token=access_token,
        facebook_page_id=page_id
    )
    await database.execute(query)
    
    return {"status": "success", "message": "Facebook connected"}

@app.post("/api/user/credentials/instagram")
async def save_instagram_credentials(
    business_account_id: str = Form(...),
    
):
    """Save Instagram credentials"""
    query = users_table.update().where(
        users_table.c.id == 'guest'
    ).values(instagram_account_id=business_account_id)
    await database.execute(query)
    
    return {"status": "success", "message": "Instagram connected"}


# ============================================================================
# AI CONTENT GENERATION ENDPOINTS
# ============================================================================

@app.post("/api/generate/ideas")
async def generate_ideas(
    topics: Optional[str] = Form(None),
    num_ideas: int = Form(3)
):
    """Generate post ideas based on topics"""
    try:
        # Use default topics if not provided
        if not topics:
            topics = "business,entrepreneurship,technology"
        
        topic_list = topics.split(',')
        ideas = trend_researcher.research_trends(topic_list, num_ideas)
        
        return {
            "status": "success",
            "ideas": ideas,
            "count": len(ideas)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/generate/custom-idea")
async def generate_custom_idea(
    prompt: str = Form(...),
    context: Optional[str] = Form(None)
):
    """Generate idea from user's custom prompt"""
    try:
        idea = trend_researcher.generate_custom_idea(prompt, context)
        return {
            "status": "success",
            "idea": idea
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/generate/content")
async def generate_content(
    idea: str = Form(...),  # JSON string
    platform: str = Form("LinkedIn")
):
    """Generate post content from idea"""
    try:
        idea_dict = json.loads(idea)
        content = content_generator.generate_post_content(idea_dict, platform)
        
        return {
            "status": "success",
            "content": content
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/generate/image")
async def generate_image(
    prompt: str = Form(...),
    width: int = Form(1024),
    height: int = Form(1024)
):
    """Generate AI image"""
    try:
        # Generate unique filename
        image_id = str(uuid.uuid4())
        output_path = f"./data/images/guest_{image_id}.png"
        
        image_path = image_generator.generate_image(
            prompt, output_path, width, height
        )
        
        # Return image URL
        return {
            "status": "success",
            "image_id": image_id,
            "image_url": f"/api/images/{os.path.basename(image_path)}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# CHAT WITH AI ENDPOINT
# ============================================================================

@app.post("/api/chat")
async def chat_with_ai(
    message: str = Form(...),
    conversation_id: Optional[str] = Form(None),
    
):
    """Chat with AI to brainstorm post ideas"""
    try:
        from groq import Groq
        from config.settings import settings
        
        client = Groq(api_key=settings.GROQ_API_KEY)
        
        # System prompt for helpful AI assistant
        system_prompt = """You are a social media content expert helping users create 
        engaging posts for LinkedIn, Instagram, and Facebook. Provide creative ideas, 
        suggestions, and improvements. Be friendly, helpful, and concise."""
        
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ],
            temperature=0.8,
            max_tokens=500
        )
        
        ai_response = response.choices[0].message.content
        
        # Save to conversation history (optional)
        if conversation_id:
            query = sessions_table.insert().values(
                id=str(uuid.uuid4()),
                user_id='guest',
                conversation_id=conversation_id,
                user_message=message,
                ai_response=ai_response,
                created_at=datetime.now()
            )
            await database.execute(query)
        
        return {
            "status": "success",
            "message": ai_response,
            "conversation_id": conversation_id or str(uuid.uuid4())
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# POST CREATION & PUBLISHING ENDPOINTS
# ============================================================================

@app.post("/api/posts/create")
async def create_post(
    text: str = Form(...),
    hashtags: str = Form(...),
    platforms: str = Form(...),  # Comma-separated
    image: Optional[UploadFile] = File(None),
    schedule_time: Optional[str] = Form(None),
    
):
    """Create a post (save draft or schedule)"""
    try:
        post_id = str(uuid.uuid4())
        image_path = None
        
        # Save uploaded image if provided
        if image:
            image_path = f"./data/images/post_{post_id}_{image.filename}"
            with open(image_path, "wb") as f:
                f.write(await image.read())
        
        # Save to database
        query = posts_table.insert().values(
            id=post_id,
            user_id='guest',
            text=text,
            hashtags=hashtags,
            platforms=platforms.split(','),
            image_path=image_path,
            status='draft',
            schedule_time=schedule_time,
            created_at=datetime.now()
        )
        await database.execute(query)
        
        return {
            "status": "success",
            "post_id": post_id,
            "message": "Post created"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/posts/{post_id}/publish")
async def publish_post(
    post_id: str,
    
):
    """Publish post to social media"""
    try:
        # Get post from database
        query = posts_table.select().where(
            posts_table.c.id == post_id,
            posts_table.c.user_id == 'guest'
        )
        post = await database.fetch_one(query)
        
        if not post:
            raise HTTPException(status_code=404, detail="Post not found")
        
        # Prepare post data
        post_data = {
            'text': post['text'],
            'hashtags': post['hashtags'],
            'image_path': post['image_path']
        }
        
        results = {}
        platforms = post['platforms']
        
        # Post to each platform
        for platform in platforms:
            try:
                post_data['platform'] = platform
                result = post_scheduler.post_now(post_data)
                results[platform] = {"success": True, "result": result}
            except Exception as e:
                results[platform] = {"success": False, "error": str(e)}
        
        # Update post status
        update_query = posts_table.update().where(
            posts_table.c.id == post_id
        ).values(
            status='published',
            published_at=datetime.now()
        )
        await database.execute(update_query)
        
        return {
            "status": "success",
            "results": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/posts")
async def get_posts(
    status: Optional[str] = None,
    limit: int = 20,
    
):
    """Get user's posts"""
    query = posts_table.select().where(
        posts_table.c.user_id == 'guest'
    )
    
    if status:
        query = query.where(posts_table.c.status == status)
    
    query = query.order_by(posts_table.c.created_at.desc()).limit(limit)
    
    posts = await database.fetch_all(query)
    
    return {
        "status": "success",
        "posts": [dict(post) for post in posts],
        "count": len(posts)
    }

@app.delete("/api/posts/{post_id}")
async def delete_post(
    post_id: str,
    
):
    """Delete a post"""
    query = posts_table.delete().where(
        posts_table.c.id == post_id,
        posts_table.c.user_id == 'guest'
    )
    await database.execute(query)
    
    return {"status": "success", "message": "Post deleted"}


# ============================================================================
# IMAGE SERVING ENDPOINT
# ============================================================================

@app.get("/api/images/{filename}")
async def serve_image(filename: str):
    """Serve generated images"""
    image_path = f"./data/images/{filename}"
    if os.path.exists(image_path):
        return FileResponse(image_path)
    raise HTTPException(status_code=404, detail="Image not found")


# ============================================================================
# STATISTICS ENDPOINT
# ============================================================================

@app.get("/api/stats")
async def get_statistics():
    """Get user statistics"""
    # Total posts
    query = posts_table.select().where(
        posts_table.c.user_id == 'guest'
    )
    all_posts = await database.fetch_all(query)
    
    # Published posts
    published = len([p for p in all_posts if p['status'] == 'published'])
    drafts = len([p for p in all_posts if p['status'] == 'draft'])
    
    # Posts this week
    from datetime import timedelta
    week_ago = datetime.now() - timedelta(days=7)
    this_week = len([p for p in all_posts if p['created_at'] >= week_ago])
    
    # Handle None values safely
    platforms = current_user.get('platforms') if current_user else None
    platforms_count = len(platforms) if platforms else 0
    
    return {
        "total_posts": len(all_posts),
        "published": published,
        "drafts": drafts,
        "this_week": this_week,
        "platforms_connected": platforms_count
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
