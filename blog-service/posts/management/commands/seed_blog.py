from django.core.management.base import BaseCommand
from django.utils import timezone
from categories.models import Category
from authors.models import Author
from posts.models import Post


class Command(BaseCommand):
    help = 'Seed the database with sample blog data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding blog data...')
        
        # Clear existing data
        Post.objects.all().delete()
        Category.objects.all().delete()
        Author.objects.all().delete()
        
        # Create categories
        categories_data = [
            ('Technology', True),
            ('Programming', True),
            ('Web Development', True),
            ('Data Science', True),
            ('DevOps', True),
        ]
        categories = []
        for name, is_active in categories_data:
            cat = Category(name=name, is_active=is_active)
            cat.save()  # This triggers slug generation
            categories.append(cat)
        self.stdout.write(self.style.SUCCESS(f'Created {len(categories)} categories'))
        
        # Create authors
        authors_data = [
            ('Alice Johnson', 'alice@example.com'),
            ('Bob Smith', 'bob@example.com'),
            ('Carol Williams', 'carol@example.com'),
        ]
        authors = []
        for display_name, email in authors_data:
            author = Author(display_name=display_name, email=email)
            author.save()
            authors.append(author)
        self.stdout.write(self.style.SUCCESS(f'Created {len(authors)} authors'))
        
        # Create posts
        posts_data = [
            ('Introduction to Python', 'Python is a powerful and versatile programming language...', 'published'),
            ('Getting Started with Django', 'Django is a high-level Python web framework...', 'published'),
            ('RESTful APIs Explained', 'REST stands for Representational State Transfer...', 'published'),
            ('Docker for Beginners', 'Docker is a platform for developing, shipping, and running applications...', 'published'),
            ('Understanding Microservices', 'Microservices architecture is an approach to application development...', 'published'),
            ('PostgreSQL Best Practices', 'PostgreSQL is a powerful, open source object-relational database system...', 'published'),
            ('Redis Caching Strategies', 'Redis is an in-memory data structure store used as a database, cache...', 'published'),
            ('JavaScript ES6 Features', 'ECMAScript 6, also known as ES6 and ECMAScript 2015...', 'published'),
            ('React Component Lifecycle', 'React components have several lifecycle methods...', 'published'),
            ('TypeScript vs JavaScript', 'TypeScript is a typed superset of JavaScript...', 'published'),
            ('Building RESTful APIs with DRF', 'Django REST Framework is a powerful toolkit...', 'published'),
            ('Async Programming in Python', 'Asynchronous programming allows a program to do multiple things...', 'published'),
            ('Git Workflow Best Practices', 'Git is a distributed version control system...', 'published'),
            ('CI/CD Pipeline Setup', 'Continuous Integration and Continuous Deployment...', 'published'),
            ('Kubernetes Basics', 'Kubernetes is an open-source container orchestration platform...', 'published'),
            ('MongoDB vs PostgreSQL', 'Choosing between SQL and NoSQL databases...', 'published'),
            ('GraphQL Introduction', 'GraphQL is a query language for APIs...', 'published'),
            ('Web Security Fundamentals', 'Security should be a primary concern for web applications...', 'published'),
            ('OAuth2 Authentication', 'OAuth 2.0 is the industry-standard protocol for authorization...', 'published'),
            ('JWT Token Management', 'JSON Web Tokens are an open standard for securely transmitting information...', 'published'),
            ('Building Scalable Systems', 'Scalability is the capability of a system to handle growth...', 'published'),
            ('Database Indexing Strategies', 'Database indexes are data structures that improve query performance...', 'published'),
            ('API Rate Limiting', 'Rate limiting is a strategy for limiting network traffic...', 'published'),
            ('Websockets Real-time Communication', 'WebSockets provide a full-duplex communication channel...', 'published'),
            ('Message Queues with RabbitMQ', 'RabbitMQ is a message broker that implements AMQP...', 'draft'),
            ('Serverless Architecture', 'Serverless computing is a cloud computing execution model...', 'draft'),
            ('Machine Learning Basics', 'Machine learning is a subset of artificial intelligence...', 'draft'),
            ('TensorFlow Tutorial', 'TensorFlow is an open-source machine learning framework...', 'draft'),
            ('Natural Language Processing', 'NLP is a branch of artificial intelligence...', 'draft'),
            ('Blockchain Technology', 'Blockchain is a distributed ledger technology...', 'draft'),
        ]
        
        posts = []
        for i, (title, body_snippet, status) in enumerate(posts_data):
            author = authors[i % len(authors)]
            category = categories[i % len(categories)]
            
            # Expand body with more content
            body = f"{body_snippet}\n\n"
            body += "Lorem ipsum dolor sit amet, consectetur adipiscing elit. " * 10
            body += "\n\nKey points:\n"
            body += "- Point one: detailed explanation here\n"
            body += "- Point two: more details\n"
            body += "- Point three: comprehensive overview\n\n"
            body += "Conclusion: " + body_snippet
            
            published_at = timezone.now() if status == 'published' else None
            
            post = Post(
                title=title,
                body=body,
                author=author,
                category=category,
                status=status,
                published_at=published_at,
                views=i * 10  # Vary views
            )
            post.save()  # This triggers slug generation
            posts.append(post)
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(posts)} posts'))
        
        published_count = Post.objects.filter(status='published').count()
        draft_count = Post.objects.filter(status='draft').count()
        
        self.stdout.write(self.style.SUCCESS('✓ Seeding complete!'))
        self.stdout.write(f'  - {len(categories)} categories')
        self.stdout.write(f'  - {len(authors)} authors')
        self.stdout.write(f'  - {published_count} published posts')
        self.stdout.write(f'  - {draft_count} draft posts')
