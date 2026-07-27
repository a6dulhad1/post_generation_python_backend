# 🚀 Complete Implementation Guide

## Phase 1: Backend API Setup (Done ✓)

You now have a complete FastAPI backend with:
- ✅ User authentication (JWT)
- ✅ Content generation endpoints
- ✅ AI chat functionality
- ✅ Post management
- ✅ Image generation
- ✅ Social media integration

## Phase 2: Start the Backend

### Install Additional Dependencies
```bash
pip install -r requirements_api.txt
```

### Run the API Server
```bash
# Start FastAPI server
python -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: `http://localhost:8000`

### Test the API
```bash
# Check health
curl http://localhost:8000/health

# View API docs (Swagger UI)
# Open in browser: http://localhost:8000/docs
```

## Phase 3: Flutter App Setup

### 1. Create Flutter Project
```bash
# Create new Flutter project
flutter create ai_social_media_app
cd ai_social_media_app

# Add dependencies
flutter pub add provider dio shared_preferences flutter_secure_storage
flutter pub add image_picker cached_network_image lottie intl
flutter pub add fl_chart shimmer pull_to_refresh
```

### 2. Project Structure
```
ai_social_media_app/
├── lib/
│   ├── main.dart
│   ├── config/
│   ├── models/
│   ├── services/
│   ├── screens/
│   ├── widgets/
│   └── providers/
```

### 3. Update pubspec.yaml
```yaml
name: ai_social_media_app
description: AI-powered social media automation app

environment:
  sdk: '>=3.0.0 <4.0.0'

dependencies:
  flutter:
    sdk: flutter
  
  # State Management
  provider: ^6.1.1
  
  # HTTP & API
  dio: ^5.4.0
  
  # Storage
  shared_preferences: ^2.2.2
  flutter_secure_storage: ^9.0.0
  
  # UI
  cached_network_image: ^3.3.1
  shimmer: ^3.0.0
  lottie: ^3.0.0
  
  # Image
  image_picker: ^1.0.7
  
  # Utilities
  intl: ^0.18.1
  
  # Charts
  fl_chart: ^0.66.0

dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^3.0.0
```

### 4. Configure API Base URL

Create `lib/config/api_config.dart`:
```dart
class ApiConfig {
  // For Android Emulator
  static const String baseUrl = 'http://10.0.2.2:8000';
  
  // For iOS Simulator
  // static const String baseUrl = 'http://localhost:8000';
  
  // For Real Device (use your computer's IP)
  // static const String baseUrl = 'http://192.168.1.XXX:8000';
}
```

## Phase 4: Implement Core Features

### 1. API Service (`lib/services/api_service.dart`)
```dart
import 'package:dio/dio.dart';
import '../config/api_config.dart';

class ApiService {
  final Dio _dio = Dio(
    BaseOptions(
      baseUrl: ApiConfig.baseUrl,
      connectTimeout: Duration(seconds: 30),
      receiveTimeout: Duration(seconds: 30),
    ),
  );

  // Set authorization token
  void setToken(String token) {
    _dio.options.headers['Authorization'] = 'Bearer $token';
  }

  // Login
  Future<Map<String, dynamic>> login(String email, String password) async {
    final response = await _dio.post(
      '/api/auth/login',
      data: FormData.fromMap({
        'email': email,
        'password': password,
      }),
    );
    return response.data;
  }

  // Register
  Future<Map<String, dynamic>> register(
    String email,
    String password,
    String name,
  ) async {
    final response = await _dio.post(
      '/api/auth/register',
      data: FormData.fromMap({
        'email': email,
        'password': password,
        'name': name,
      }),
    );
    return response.data;
  }

  // Generate ideas
  Future<List<dynamic>> generateIdeas({
    String? topics,
    int numIdeas = 3,
  }) async {
    final response = await _dio.post(
      '/api/generate/ideas',
      data: FormData.fromMap({
        'topics': topics,
        'num_ideas': numIdeas,
      }),
    );
    return response.data['ideas'];
  }

  // Chat with AI
  Future<String> chat(String message, {String? conversationId}) async {
    final response = await _dio.post(
      '/api/chat',
      data: FormData.fromMap({
        'message': message,
        'conversation_id': conversationId,
      }),
    );
    return response.data['message'];
  }

  // Create post
  Future<String> createPost({
    required String text,
    required String hashtags,
    required List<String> platforms,
    String? imagePath,
  }) async {
    final formData = FormData.fromMap({
      'text': text,
      'hashtags': hashtags,
      'platforms': platforms.join(','),
    });

    if (imagePath != null) {
      formData.files.add(
        MapEntry(
          'image',
          await MultipartFile.fromFile(imagePath),
        ),
      );
    }

    final response = await _dio.post('/api/posts/create', data: formData);
    return response.data['post_id'];
  }

  // Publish post
  Future<void> publishPost(String postId) async {
    await _dio.post('/api/posts/$postId/publish');
  }

  // Get posts
  Future<List<dynamic>> getPosts({String? status}) async {
    final response = await _dio.get(
      '/api/posts',
      queryParameters: status != null ? {'status': status} : null,
    );
    return response.data['posts'];
  }

  // Get stats
  Future<Map<String, dynamic>> getStats() async {
    final response = await _dio.get('/api/stats');
    return response.data;
  }
}
```

### 2. Authentication Screen
```dart
// lib/screens/auth/login_screen.dart
import 'package:flutter/material.dart';
import '../../services/api_service.dart';

class LoginScreen extends StatefulWidget {
  @override
  _LoginScreenState createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();
  final _apiService = ApiService();
  bool _isLoading = false;

  Future<void> _login() async {
    setState(() => _isLoading = true);

    try {
      final result = await _apiService.login(
        _emailController.text,
        _passwordController.text,
      );

      // Save token
      final token = result['access_token'];
      _apiService.setToken(token);

      // Navigate to home
      Navigator.pushReplacementNamed(context, '/home');
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Login failed: $e')),
      );
    } finally {
      setState(() => _isLoading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: Padding(
          padding: EdgeInsets.all(24),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Text(
                'AI Social Media',
                style: TextStyle(fontSize: 32, fontWeight: FontWeight.bold),
              ),
              SizedBox(height: 48),
              TextField(
                controller: _emailController,
                decoration: InputDecoration(
                  labelText: 'Email',
                  border: OutlineInputBorder(),
                ),
              ),
              SizedBox(height: 16),
              TextField(
                controller: _passwordController,
                obscureText: true,
                decoration: InputDecoration(
                  labelText: 'Password',
                  border: OutlineInputBorder(),
                ),
              ),
              SizedBox(height: 24),
              ElevatedButton(
                onPressed: _isLoading ? null : _login,
                child: _isLoading
                    ? CircularProgressIndicator()
                    : Text('Login'),
                style: ElevatedButton.styleFrom(
                  minimumSize: Size(double.infinity, 50),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
```

### 3. Home Screen
```dart
// lib/screens/home/home_screen.dart
import 'package:flutter/material.dart';
import '../../services/api_service.dart';

class HomeScreen extends StatefulWidget {
  @override
  _HomeScreenState createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  final _apiService = ApiService();
  Map<String, dynamic>? _stats;

  @override
  void initState() {
    super.initState();
    _loadStats();
  }

  Future<void> _loadStats() async {
    final stats = await _apiService.getStats();
    setState(() => _stats = stats);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('AI Social Media'),
        actions: [
          IconButton(
            icon: Icon(Icons.person),
            onPressed: () => Navigator.pushNamed(context, '/profile'),
          ),
        ],
      ),
      body: SingleChildScrollView(
        padding: EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Welcome back! 👋',
              style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
            ),
            SizedBox(height: 24),
            Row(
              children: [
                _buildStatCard(
                  'Total Posts',
                  _stats?['total_posts']?.toString() ?? '0',
                  Icons.article,
                ),
                SizedBox(width: 16),
                _buildStatCard(
                  'This Week',
                  _stats?['this_week']?.toString() ?? '0',
                  Icons.trending_up,
                ),
              ],
            ),
            SizedBox(height: 32),
            Text(
              'Quick Actions',
              style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
            ),
            SizedBox(height: 16),
            _buildActionCard(
              '🤖 Generate Ideas',
              'Let AI create post ideas for you',
              () => Navigator.pushNamed(context, '/generate-ideas'),
            ),
            _buildActionCard(
              '💬 Chat with AI',
              'Brainstorm with AI assistant',
              () => Navigator.pushNamed(context, '/chat'),
            ),
            _buildActionCard(
              '✏️ Create Post',
              'Write and publish a new post',
              () => Navigator.pushNamed(context, '/create-post'),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildStatCard(String label, String value, IconData icon) {
    return Expanded(
      child: Card(
        child: Padding(
          padding: EdgeInsets.all(16),
          child: Column(
            children: [
              Icon(icon, size: 32, color: Colors.blue),
              SizedBox(height: 8),
              Text(
                value,
                style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
              ),
              Text(label, style: TextStyle(color: Colors.grey)),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildActionCard(String title, String subtitle, VoidCallback onTap) {
    return Card(
      margin: EdgeInsets.only(bottom: 12),
      child: ListTile(
        title: Text(title),
        subtitle: Text(subtitle),
        trailing: Icon(Icons.arrow_forward_ios),
        onTap: onTap,
      ),
    );
  }
}
```

## Phase 5: Run the Complete System

### Terminal 1: Start Backend API
```bash
python -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

### Terminal 2: Run Flutter App
```bash
cd ai_social_media_app
flutter run
```

## Phase 6: Social Media OAuth Setup

### LinkedIn OAuth in Flutter
```dart
// Add to pubspec.yaml
# flutter_web_auth: ^0.5.0

// Implement LinkedIn login
import 'package:flutter_web_auth/flutter_web_auth.dart';

Future<void> connectLinkedIn() async {
  final clientId = 'YOUR_CLIENT_ID';
  final redirectUri = 'your-app://callback';
  final authUrl = 'https://www.linkedin.com/oauth/v2/authorization'
      '?response_type=code'
      '&client_id=$clientId'
      '&redirect_uri=$redirectUri'
      '&scope=r_liteprofile%20w_member_social';

  final result = await FlutterWebAuth.authenticate(
    url: authUrl,
    callbackUrlScheme: 'your-app',
  );

  // Extract code and exchange for token
  final code = Uri.parse(result).queryParameters['code'];
  // Send code to your backend to exchange for access token
}
```

### Facebook OAuth in Flutter
```dart
// Add to pubspec.yaml
# flutter_facebook_auth: ^6.0.4

import 'package:flutter_facebook_auth/flutter_facebook_auth.dart';

Future<void> connectFacebook() async {
  final LoginResult result = await FacebookAuth.instance.login();

  if (result.status == LoginStatus.success) {
    final AccessToken accessToken = result.accessToken!;
    // Send token to backend
    await apiService.saveFacebookCredentials(accessToken.token);
  }
}
```

## Phase 7: Testing & Debugging

### Test API Endpoints
```bash
# Test with curl
curl -X POST http://localhost:8000/api/auth/register \
  -F "email=test@example.com" \
  -F "password=password123" \
  -F "name=Test User"

curl -X POST http://localhost:8000/api/auth/login \
  -F "email=test@example.com" \
  -F "password=password123"
```

### Flutter Debug
```bash
# Run with verbose logging
flutter run -v

# Check logs
flutter logs
```

## Phase 8: Deployment

### Backend Deployment (Options)
1. **Heroku**
   ```bash
   heroku create your-app-name
   git push heroku main
   ```

2. **AWS/DigitalOcean**
   - Deploy with Docker
   - Use nginx as reverse proxy
   - Set up SSL certificate

3. **Railway/Render**
   - Connect GitHub repo
   - Auto-deploy on push

### Flutter Deployment
```bash
# Android
flutter build apk --release
flutter build appbundle --release

# iOS
flutter build ios --release
```

## 🎯 Complete Feature Checklist

### Backend ✅
- [x] User authentication
- [x] Content generation
- [x] AI chat
- [x] Post management
- [x] Image generation
- [x] Social media integration
- [x] Statistics

### Flutter App (To Implement)
- [ ] Authentication screens
- [ ] Home dashboard
- [ ] Generate ideas screen
- [ ] Chat with AI screen
- [ ] Create post screen
- [ ] Post history screen
- [ ] Profile & settings
- [ ] Social media OAuth
- [ ] Image picker/generation
- [ ] Post scheduling
- [ ] Analytics dashboard

## 📚 Next Steps

1. **Set up Flutter project** (15 min)
2. **Implement authentication** (30 min)
3. **Create main screens** (2-3 hours)
4. **Integrate API calls** (1-2 hours)
5. **Add social media OAuth** (1 hour)
6. **Test thoroughly** (1-2 hours)
7. **Polish UI/UX** (2-3 hours)
8. **Deploy** (1 hour)

**Total estimated time: 8-12 hours**

## 🆘 Troubleshooting

### API Connection Issues
- Check backend is running
- Verify API URL in `api_config.dart`
- For Android emulator: use `10.0.2.2`
- For iOS simulator: use `localhost`
- For real device: use your computer's IP

### CORS Issues
- Backend already configured for CORS
- If issues persist, add your domain to `allow_origins`

### OAuth Redirect Issues
- Register callback URLs in developer consoles
- Match redirect URIs exactly
- Test with web browser first

---

**Ready to start?** Begin with Phase 2 and work through each phase systematically!
