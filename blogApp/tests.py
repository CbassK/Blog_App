from django.test import TestCase
from django.contrib.auth.models import User
from blogApp.models import Post, Comment, Tag

class PostModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.tag = Tag.objects.create(name='Django')
        self.post = Post.objects.create(title='Test Post', content='This is a test post.', author=self.user)
        self.post.tags.add(self.tag)

    def test_post_creation(self):
        self.assertTrue(isinstance(self.post, Post))
        self.assertEqual(self.post.__str__(), 'Test Post')
        self.assertEqual(self.post.tags.count(), 1)
        self.assertEqual(self.post.tags.first().name, 'Django')
        
class CommentModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.post = Post.objects.create(title='Test Post', content='This is a test post.', author=self.user)
        self.comment = Comment.objects.create(post=self.post, author='Commenter', content='This is a test comment.')

    def test_comment_creation(self):
        self.assertTrue(isinstance(self.comment, Comment))
        self.assertEqual(self.comment.__str__(), 'Comment by Commenter on Test Post')
        self.assertEqual(self.comment.post.title, 'Test Post')

class TagModelTest(TestCase):

    def setUp(self):
        self.tag = Tag.objects.create(name='Django')

    def test_tag_creation(self):
        self.assertTrue(isinstance(self.tag, Tag))
        self.assertEqual(self.tag.__str__(), 'Django')

