from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    Paragraph,
    PageBreak,
    Spacer,
    Preformatted,
    SimpleDocTemplate,
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus.tableofcontents import TableOfContents


def build_pdf(output_path: str):
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Title'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#1F3A5F'),
        spaceAfter=18,
        alignment=TA_CENTER,
    )
    h1 = ParagraphStyle('H1', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=16, leading=20, textColor=colors.HexColor('#1F3A5F'), spaceBefore=12, spaceAfter=8)
    h2 = ParagraphStyle('H2', parent=styles['Heading2'], fontName='Helvetica-Bold', fontSize=12, leading=16, textColor=colors.HexColor('#2E4A62'), spaceBefore=10, spaceAfter=6)
    h3 = ParagraphStyle('H3', parent=styles['Heading3'], fontName='Helvetica-Bold', fontSize=10.5, leading=14, textColor=colors.HexColor('#36536A'), spaceBefore=8, spaceAfter=5)
    body = ParagraphStyle('Body', parent=styles['BodyText'], fontName='Helvetica', fontSize=9.5, leading=13.5, spaceAfter=5, alignment=TA_LEFT)
    small = ParagraphStyle('Small', parent=styles['BodyText'], fontName='Helvetica', fontSize=8.3, leading=11.5, spaceAfter=3)
    note = ParagraphStyle('Note', parent=styles['BodyText'], fontName='Helvetica-Oblique', fontSize=8.7, leading=12, textColor=colors.HexColor('#6B4F00'), spaceBefore=4, spaceAfter=6)
    code = ParagraphStyle('Code', parent=styles['Code'], fontName='Courier', fontSize=8.2, leading=10.8, textColor=colors.HexColor('#111111'), backColor=colors.HexColor('#F7F7F7'), borderPadding=6, leftIndent=8, rightIndent=8, spaceAfter=6)
    bullet = ParagraphStyle('Bullet', parent=body, leftIndent=12, bulletIndent=0, spaceAfter=2)
    center = ParagraphStyle('Center', parent=body, alignment=TA_CENTER)

    doc = SimpleDocTemplate(output_path, pagesize=A4, leftMargin=0.75 * inch, rightMargin=0.75 * inch, topMargin=0.7 * inch, bottomMargin=0.7 * inch)

    def add_paragraph(story, text, style=body):
        story.append(Paragraph(text, style))

    def add_code(story, code_text):
        story.append(Preformatted(code_text, code))
        story.append(Spacer(1, 4))

    def add_bullets(story, items):
        for item in items:
            story.append(Paragraph(f"• {item}", bullet))

    def add_box(story, title, text):
        story.append(Paragraph(title, h3))
        story.append(Paragraph(text, note))

    story = []

    story.append(Paragraph('Django REST Framework Study Guide', title_style))
    story.append(Paragraph('Backend learning guide for the travel blog project', center))
    story.append(Spacer(1, 0.2 * inch))
    story.append(Paragraph('Generated from the project files in the workspace', small))
    story.append(Spacer(1, 0.1 * inch))
    story.append(Paragraph('This guide is written for a complete beginner. It explains the code, the concepts, and the request lifecycle in plain English.', body))
    story.append(PageBreak())

    toc = TableOfContents()
    story.append(Paragraph('Table of Contents', h1))
    story.append(toc)
    story.append(PageBreak())

    chapter_titles = []

    def add_chapter(title, subtitle=None):
        chapter_titles.append(title)
        story.append(Paragraph(title, h1))
        if subtitle:
            story.append(Paragraph(subtitle, body))
        story.append(Spacer(1, 0.08 * inch))
        toc.addEntry(0, title, 0)

    add_chapter('1. Project overview', 'What this backend is, what each folder does, and how requests move through Django.')
    add_paragraph(story, 'This project is a Django REST Framework backend for a travel blog. It exposes API endpoints for users, posts, and destinations. The backend accepts HTTP requests, routes them to Python code, talks to the database, and sends JSON back to the client.')
    add_paragraph(story, 'The most important idea is that Django turns Python code into web behavior. You write Python classes and functions, and Django handles the connection to the web server, URL matching, database operations, and responses.')
    add_box(story, 'Core idea', 'Think of Django as a traffic controller. It receives requests, decides which Python function should handle them, and returns a response.')
    add_paragraph(story, 'The project has three main apps: users, posts, and travel. Each app groups related features. The config package holds settings and routing rules.')
    add_paragraph(story, 'The request lifecycle is: Browser/Postman → URL → Django URL dispatcher → View → Serializer → Model → Database → Serializer → JSON response.')
    add_code(story, "Browser/Postman\n   ↓\nurls.py\n   ↓\nView\n   ↓\nSerializer\n   ↓\nModel\n   ↓\nDatabase\n   ↑\nSerializer\n   ↑\nJSON Response")
    add_box(story, 'Beginner definition', 'A view is the place where Django decides what to do for a request. A serializer is the translator between Python objects and JSON. A model is the Python representation of a database table.')
    add_paragraph(story, 'The app folders are organized so that each feature has its own models, views, serializers, and URLs. This makes the code easier to understand and maintain.')
    add_chapter('2. Core startup files', 'manage.py, settings, URLs, and the WSGI/ASGI entry points.')
    add_paragraph(story, 'The file manage.py is the command-line entry point for the Django project. When you run python manage.py runserver, Django uses this file to start the project and load configuration.')
    add_code(story, "#!/usr/bin/env python\n\"\"\"Django's command-line utility for administrative tasks.\"\"\"\nimport os\nimport sys\n\n\ndef main():\n    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')\n    try:\n        from django.core.management import execute_from_command_line\n    except ImportError as exc:\n        raise ImportError(\n            \"Couldn't import Django. Are you sure it's installed and \"\n            \"available on your PYTHONPATH environment variable? Did you \"\n            \"forget to activate a virtual environment?\"\n        ) from exc\n    execute_from_command_line(sys.argv)\n\n\nif __name__ == '__main__':\n    main()")
    add_paragraph(story, 'Line-by-line explanation:')
    add_bullets(story, [
        'The shebang tells Linux which Python interpreter to use when the script is executed directly.',
        'The docstring explains the purpose of the file.',
        'import os and import sys bring in Python modules for environment variables and command-line arguments.',
        'The main function is the entry point for Django management commands.',
        'os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings") sets the settings module so Django knows where configuration lives.',
        'execute_from_command_line(sys.argv) runs the command the user typed, such as runserver, migrate, or makemigrations.',
        'The if __name__ == "__main__": block ensures that main() runs only when the file is run directly, not when it is imported.',
    ])
    add_paragraph(story, 'The settings file is the brain of the project. It contains database info, installed apps, middleware, authentication settings, allowed hosts, media folders, and DRF configuration.')
    add_code(story, "BASE_DIR = Path(__file__).resolve().parent.parent\n\nSECRET_KEY = 'django-insecure-...'\nDEBUG = True\nALLOWED_HOSTS = ['127.0.0.1', 'localhost']")
    add_bullets(story, [
        'BASE_DIR points to the root of the project so paths can be built reliably.',
        'SECRET_KEY is a private string used by Django for security-related hashing; it should not be exposed in production.',
        'DEBUG=True means Django gives detailed error pages during development, which is convenient but unsafe in production.',
        'ALLOWED_HOSTS limits which domain names can reach the server.',
    ])
    add_paragraph(story, 'The config/urls.py file is the top-level URL router. It sends requests beginning with /api/ to the users, posts, and travel apps.')
    add_code(story, "urlpatterns = [\n    path(\"admin/\", admin.site.urls),\n    path(\"api/\", include(\"users.urls\")),\n    path(\"api/\", include(\"posts.urls\")),\n    path(\"api/\", include(\"travel.urls\")),\n]")
    add_bullets(story, [
        'path("admin/", admin.site.urls) exposes the built-in Django admin dashboard.',
        'include("users.urls") adds the URL routes from the users app.',
        'The prefix /api/ makes the API endpoints easy to distinguish from the Django admin.',
        'If DEBUG is True, Django appends media serving rules to the URL patterns.',
    ])
    add_chapter('3. The users app', 'Authentication, OTP login flow, activity logging, and serializers.')
    add_paragraph(story, 'The users app is the authentication and identity layer of the project. It handles registration, login, OTP verification, logout, and the activity log.')
    add_paragraph(story, 'Concept: a serializer is a translator between incoming JSON and Python objects. It also validates user input. In this project, the serializers check usernames, emails, passwords, and OTPs before anything is saved.')
    add_paragraph(story, 'The model file defines two database tables: OTP and ActivityLog.')
    add_code(story, "class OTP(models.Model):\n    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name=\"otps\")\n    otp_code = models.CharField(max_length=6)\n    created_at = models.DateTimeField(auto_now_add=True)\n    expires_at = models.DateTimeField()")
    add_bullets(story, [
        'The class OTP inherits from models.Model, which means it becomes a Django model and maps to a database table.',
        'user is a foreign key to Django\'s built-in User model. It means many OTP records can belong to one user.',
        'otp_code stores a six-digit one-time password.',
        'created_at is automatically filled when the row is created.',
        'expires_at stores the deadline for the OTP.',
    ])
    add_paragraph(story, 'The save method overrides the default save logic. It sets the expiration time if the developer did not provide one.')
    add_code(story, "def save(self, *args, **kwargs):\n    if not self.expires_at:\n        self.expires_at = timezone.now() + timedelta(minutes=5)\n    super().save(*args, **kwargs)")
    add_bullets(story, [
        'self refers to the current OTP instance.',
        'timezone.now() returns the current time.',
        'timedelta(minutes=5) means adding five minutes.',
        'super().save(...) calls the parent class implementation so Django can actually write the record to the database.',
    ])
    add_paragraph(story, 'The serializer file uses DRF serializers to validate and transform user data.')
    add_code(story, "class RegisterSerializer(serializers.ModelSerializer):\n    password = serializers.CharField(write_only=True, min_length=8)\n\n    class Meta:\n        model = User\n        fields = ['id', 'username', 'email', 'password']")
    add_bullets(story, [
        'ModelSerializer is a DRF shortcut that automatically builds serializer fields from a Django model.',
        'write_only=True means the password is accepted for input but not returned in the response.',
        'min_length=8 enforces a minimum password length.',
        'The Meta class tells DRF which model and fields to use.',
    ])
    add_paragraph(story, 'The validate_username and validate_email methods are custom validation hooks. They prevent duplicate usernames or emails.')
    add_code(story, "def validate_username(self, value):\n    if User.objects.filter(username=value).exists():\n        raise serializers.ValidationError(\"A user with that username already exists.\")\n    return value")
    add_paragraph(story, 'The create method uses Django\'s built-in create_user helper, which hashes the password correctly.')
    add_code(story, "def create(self, validated_data):\n    user = User.objects.create_user(...)\n    return user")
    add_paragraph(story, 'The LoginSerializer performs the login flow. It authenticates the user, creates an OTP, and returns a payload with the OTP details.')
    add_code(story, "user = authenticate(username=user_obj.username, password=attrs['password'])\nOTP.objects.filter(user=user).delete()\notp_obj = OTP.objects.create(user=user, otp_code=otp_code)")
    add_bullets(story, [
        'authenticate checks the supplied username and password against Django user credentials.',
        'OTP.objects.filter(user=user).delete() removes old OTPs so users do not keep multiple active codes.',
        'OTP.objects.create(...) writes a new OTP record to the database.',
    ])
    add_paragraph(story, 'The VerifyOTPSerializer creates JWT access and refresh tokens after the OTP is confirmed.')
    add_code(story, "refresh = RefreshToken.for_user(user)\nreturn {\n    'user': {...},\n    'refresh': str(refresh),\n    'access': str(refresh.access_token),\n}")
    add_paragraph(story, 'The view layer exposes the endpoints. RegisterView uses CreateAPIView, which handles POST creation for you. LoginView and VerifyOTPView use APIView because the login logic is custom.')
    add_code(story, "class RegisterView(generics.CreateAPIView):\n    queryset = User.objects.all()\n    serializer_class = RegisterSerializer")
    add_bullets(story, [
        'CreateAPIView is a DRF generic view that already knows how to handle a POST request for creating a resource.',
        'queryset tells DRF which database rows are available as the base data.',
        'serializer_class tells DRF which serializer should validate and create the object.',
    ])
    add_paragraph(story, 'The LoginView.post method collects the request data, validates it, creates an ActivityLog, and returns a response. The authentication_classes = [] line means this endpoint does not require a JWT token to be invoked.')
    add_paragraph(story, 'The LogoutView uses permissions.IsAuthenticated, which means only logged-in users may call it.')
    add_code(story, "class LogoutView(APIView):\n    permission_classes = [permissions.IsAuthenticated]")
    add_paragraph(story, 'The users/urls.py file maps routes to views.')
    add_code(story, "urlpatterns = [\n    path(\"register/\", RegisterView.as_view(), name=\"register\"),\n    path(\"login/\", LoginView.as_view(), name=\"login\"),\n    path(\"verify-otp/\", VerifyOTPView.as_view(), name=\"verify-otp\"),\n]")
    add_paragraph(story, 'The authentication flow is:')
    add_bullets(story, [
        'A client sends username and password to /api/login/.' ,
        'Django authenticates the user.',
        'A one-time password is generated and stored.',
        'An email is sent if possible.',
        'The client sends the username and OTP to /api/verify-otp/.' ,
        'Django validates the OTP, deletes it, and returns JWT tokens.',
    ])
    add_box(story, 'JWT note', 'JWT stands for JSON Web Token. It is a signed token that proves a client is authenticated. In this project, the access token lets the client reach protected endpoints, while the refresh token is used to mint new access tokens.')
    add_box(story, 'Likely SQL', 'When the code checks for an existing username, Django may execute SQL similar to SELECT * FROM auth_user WHERE username = %s; When it creates an OTP record, Django may execute INSERT INTO users_otp (...).')
    add_chapter('4. The posts app', 'Post model, serializer, viewset, and router.')
    add_paragraph(story, 'The posts app manages travel blog posts. The Post model stores the title, description, image, timestamps, and author.')
    add_code(story, "class Post(models.Model):\n    title = models.CharField(max_length=200)\n    description = models.TextField()\n    image = models.ImageField(upload_to='posts/images/', blank=True, null=True)\n    created_at = models.DateTimeField(auto_now_add=True)\n    updated_at = models.DateTimeField(auto_now=True)\n    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')")
    add_bullets(story, [
        'ImageField stores file uploads and uses the media system.',
        'auto_now_add=True fills created_at once, when the row is first created.',
        'auto_now=True updates updated_at every time the row is saved.',
        'ForeignKey to User means every post belongs to one author.',
    ])
    add_paragraph(story, 'The serializer exposes the model data to the API in a controlled way.')
    add_code(story, "class PostSerializer(serializers.ModelSerializer):\n    class Meta:\n        model = Post\n        fields = ['id', 'title', 'description', 'image', 'created_at', 'updated_at', 'author']\n        read_only_fields = ['id', 'created_at', 'updated_at', 'author']")
    add_paragraph(story, 'The viewset is a DRF class that handles listing, retrieving, creating, updating, and deleting posts. It also supports search and permission rules.')
    add_code(story, "class PostViewSet(viewsets.ModelViewSet):\n    queryset = Post.objects.all()\n    serializer_class = PostSerializer\n    parser_classes = (MultiPartParser, FormParser, JSONParser)")
    add_bullets(story, [
        'ModelViewSet combines multiple common view behaviors into one class.',
        'parser_classes tell DRF how to parse incoming data, including multipart form-data for image uploads.',
        'AllowAny is used for read operations, while IsAuthenticated is used for writes.',
    ])
    add_paragraph(story, 'The perform_create and perform_update methods create an ActivityLog entry after a post is created or modified.')
    add_box(story, 'Likely SQL', 'A list request may trigger SELECT * FROM posts_post ORDER BY created_at DESC; search may trigger SELECT ... WHERE title ILIKE %s OR description ILIKE %s;')
    add_chapter('5. The travel app', 'Destination model, serializer, viewset, and router.')
    add_paragraph(story, 'The travel app manages destinations, including country, city, category, attractions, budget, duration, and image.')
    add_code(story, "class Destination(models.Model):\n    title = models.CharField(max_length=200)\n    description = models.TextField()\n    country = models.CharField(max_length=100, blank=True)\n    city = models.CharField(max_length=100, blank=True)")
    add_bullets(story, [
        'blank=True means the field is optional in forms and serializers.',
        'The model collects destination metadata that a frontend can display in cards or search results.',
        'The image field uses the same media upload pattern as posts.',
    ])
    add_paragraph(story, 'The destination viewset behaves almost exactly like the posts viewset, but its search covers extra fields such as country and city.')
    add_box(story, 'Likely SQL', 'For a search query, Django may generate a WHERE clause over title, description, country, city, travel_category, and author username.')
    add_chapter('6. Configuration and project settings', 'Why each configuration value exists and how the project is wired together.')
    add_paragraph(story, 'The settings file is the central configuration hub. Every framework component reads from it.')
    add_code(story, "INSTALLED_APPS = [\n    'django.contrib.admin',\n    'django.contrib.auth',\n    'django.contrib.contenttypes',\n    'django.contrib.sessions',\n    'django.contrib.messages',\n    'django.contrib.staticfiles',\n    'rest_framework',\n    'corsheaders',\n    'posts',\n    'users',\n    'travel',\n]")
    add_bullets(story, [
        'INSTALLED_APPS tells Django which applications should be loaded and which migrations and templates are available.',
        'The built-in Django apps provide admin, authentication, sessions, messages, and static files.',
        'rest_framework enables DRF features.',
        'corsheaders enables Cross-Origin Resource Sharing so a frontend on a different port can talk to the API.',
    ])
    add_code(story, "MIDDLEWARE = [\n    'django.middleware.security.SecurityMiddleware',\n    'corsheaders.middleware.CorsMiddleware',\n    'django.contrib.sessions.middleware.SessionMiddleware',\n    'django.middleware.common.CommonMiddleware',\n    'django.middleware.csrf.CsrfViewMiddleware',\n    'django.contrib.auth.middleware.AuthenticationMiddleware',\n    'django.contrib.messages.middleware.MessageMiddleware',\n    'django.middleware.clickjacking.XFrameOptionsMiddleware',\n]")
    add_bullets(story, [
        'Middleware runs around every request and response.',
        'SecurityMiddleware adds important security headers.',
        'SessionMiddleware and AuthenticationMiddleware support sessions and logged-in users.',
        'CsrfViewMiddleware protects forms against cross-site request forgery.',
        'CorsMiddleware allows the frontend to call the API from a different origin.',
    ])
    add_code(story, "DATABASES = {\n    'default': {\n        'ENGINE': 'django.db.backends.postgresql',\n        'NAME': 'postgres',\n        'USER': 'postgres',\n        'PASSWORD': 'NewPassword123',\n        'HOST': 'localhost',\n        'PORT': '5432',\n    }\n}")
    add_paragraph(story, 'This tells Django to use PostgreSQL instead of SQLite. Django models become SQL tables in the PostgreSQL database.')
    add_code(story, "REST_FRAMEWORK = {\n    'DEFAULT_AUTHENTICATION_CLASSES': (\n        'rest_framework_simplejwt.authentication.JWTAuthentication',\n    ),\n}\n\nSIMPLE_JWT = {\n    'ACCESS_TOKEN_LIFETIME': timedelta(days=7),\n    'REFRESH_TOKEN_LIFETIME': timedelta(days=30),\n}")
    add_paragraph(story, 'These settings configure JWT authentication for DRF. The access token is long-lived in this project, which is convenient but not always ideal for production.')
    add_paragraph(story, 'Media settings are important because both post and destination images are uploaded. MEDIA_ROOT is the folder on disk where files are stored; MEDIA_URL is the web path that points to them.')
    add_chapter('7. Models, migrations, and ORM', 'How Django translates Python models into database tables.')
    add_paragraph(story, 'Concept: ORM means Object Relational Mapping. It lets Python code talk to databases without writing raw SQL by hand. Django translates Python operations into SQL for you.')
    add_paragraph(story, 'The model classes in posts/models.py and travel/models.py describe tables. Every field becomes a database column. Every instance becomes a row.')
    add_box(story, 'Example', 'When you write Post.objects.all(), Django may translate that into SELECT id, title, description, ... FROM posts_post;')
    add_paragraph(story, 'Migrations are versioned instructions that tell Django how to change the database schema over time. The migration files in the migrations folders show how the tables evolved.')
    add_code(story, "operations = [\n    migrations.CreateModel(\n        name='Post',\n        fields=[...],\n    ),\n]")
    add_bullets(story, [
        'A migration records a database change in a file that can be shared with teammates.',
        'The migration system prevents manual SQL editing for simple schema changes.',
        'When you run python manage.py migrate, Django applies the pending migrations.',
    ])
    add_box(story, 'Why migrations matter', 'Without migrations, your Python models and your real database could drift apart. Migrations keep them aligned.')
    add_chapter('8. Request lifecycle and endpoint walkthroughs', 'The full path from browser to response.')
    add_paragraph(story, 'Every request follows a common path:')
    add_code(story, "Browser/Postman\n   ↓\nHTTP request\n   ↓\nDjango server\n   ↓\nURL dispatcher\n   ↓\nView\n   ↓\nSerializer / model / DB\n   ↓\nJSON response")
    add_paragraph(story, 'The endpoints in this project are:')
    add_bullets(story, [
        'POST /api/register/ → RegisterView',
        'POST /api/login/ → LoginView',
        'POST /api/verify-otp/ → VerifyOTPView',
        'POST /api/logout/ → LogoutView',
        'GET /api/activity-logs/ → ActivityLogListView',
        'GET/POST/PATCH/DELETE /api/posts/ and /api/posts/<id>/ → PostViewSet',
        'GET/POST/PATCH/DELETE /api/destinations/ and /api/destinations/<id>/ → DestinationViewSet',
    ])
    add_paragraph(story, 'The register endpoint is a classic create flow. The browser sends a JSON body with username, email, and password. The URL routes to RegisterView. DRF uses the RegisterSerializer to validate input and create a User. The response returns the created user ID and username. The activity log records the registration event.')
    add_paragraph(story, 'The login endpoint validates username/password, generates an OTP, and returns a message. The actual authentication occurs in the serializer, not in the URL routing layer.')
    add_paragraph(story, 'The verify OTP endpoint is where the JWT tokens are issued. After verification, the client can use the access token for protected routes such as logout and POST/PUT/DELETE operations.')
    add_paragraph(story, 'The posts and destinations endpoints are built with ViewSet classes. DRF automatically handles common RESTful actions. A GET request to /api/posts/ goes to list; POST goes to create; GET /api/posts/1/ goes to retrieve; PATCH goes to partial_update; DELETE goes to destroy.')
    add_chapter('9. Practical debugging guide', 'What to look at when something breaks.')
    add_paragraph(story, 'When you see an error, first identify the stage of the request lifecycle where it failed.')
    add_bullets(story, [
        'If the URL does not match, check the app urls.py and project config/urls.py.',
        'If the view raises an error, inspect the serializer and request body.',
        'If the database layer fails, check migrations and the database connection settings.',
        'If the response is wrong, inspect the serializer fields and the view logic.',
    ])
    add_paragraph(story, 'Common beginner mistakes:')
    add_bullets(story, [
        'Forgetting to add an app to INSTALLED_APPS.',
        'Using the wrong URL prefix such as /posts/ instead of /api/posts/.' ,
        'Ignoring permissions and accidentally allowing unauthenticated writes.',
        'Forgetting that ImageField requires media configuration.',
        'Expecting the database to update without running migrations.',
    ])
    add_chapter('10. Interview questions, quizzes, and exercises', 'Use this section to reinforce the concepts.')
    add_paragraph(story, 'Interview questions:')
    add_bullets(story, [
        'What is the difference between a view and a serializer?',
        'What does a ForeignKey represent in Django?',
        'Why do we need migrations?',
        'What does JWT authentication do?',
        'What is the purpose of ModelViewSet?',
    ])
    add_paragraph(story, 'Mini quiz:')
    add_bullets(story, [
        'True or false: Django models are the same thing as database tables.',
        'What happens when you call serializer.is_valid(raise_exception=True)?',
        'Which folder contains the main project settings?',
        'What is the purpose of MEDIA_ROOT?',
    ])
    add_paragraph(story, 'Practice exercises:')
    add_bullets(story, [
        'Add a new endpoint that returns all posts sorted by title.',
        'Create a serializer that hides the author field from public responses.',
        'Write a custom permission that allows only the author to update a post.',
        'Add a search filter for destinations by budget.',
    ])
    add_chapter('11. Glossary', 'Definitions of key Django, DRF, Python, and backend terms.')
    add_bullets(story, [
        'Django: a Python web framework for building web applications.',
        'DRF: Django REST Framework, an extension that helps build APIs.',
        'Model: the Python class that represents a database table.',
        'Serializer: a class that validates and transforms data.',
        'View: Python code that handles a request.',
        'ORM: Object Relational Mapper, which translates Python to SQL.',
        'Migration: a versioned change to the database schema.',
        'JWT: a signed token used for authentication.',
        'QuerySet: a lazy database query object.',
        'Middleware: code that runs around every request and response.',
    ])

    doc.build(story)


if __name__ == '__main__':
    pdf_path = Path('/home/thinkpad/Office Project/backend/study_guide_django.pdf')
    build_pdf(str(pdf_path))
    print(f'Created {pdf_path}')
