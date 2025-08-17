import unittest
from unittest.mock import patch
from blog.models import Post, Author, Category, Tag
from blog.views import homepage, post_detail, author_profile, search_results
from django.test import Client, RequestFactory
from django.urls import reverse

class BlogTests(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()

        # Create test data
        self.author = Author.objects.create(name='John Doe', bio='Test author')
        self.category = Category.objects.create(name='Technology')
        self.tag = Tag.objects.create(name='Python')
        self.post = Post.objects.create(
            title='Test Post',
            content='This is a test post.',
            author=self.author,
            category=self.category
        )
        self.post.tags.add(self.tag)

    def test_homepage(self):
        response = self.client.get(reverse('homepage'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/index.html')
        self.assertIn(self.post, response.context['posts'])

    def test_post_detail(self):
        response = self.client.get(reverse('post_detail', args=[self.post.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_detail.html')
        self.assertEqual(response.context['post'], self.post)

    def test_author_profile(self):
        response = self.client.get(reverse('author_profile', args=[self.author.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/author_profile.html')
        self.assertEqual(response.context['author'], self.author)
        self.assertIn(self.post, response.context['posts'])

    def test_search_results(self):
        response = self.client.get(reverse('search_results') + '?q=test')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/search_results.html')
        self.assertIn(self.post, response.context['posts'])

    @patch('blog.views.search_posts')
    def test_search_functionality(self, mock_search_posts):
        mock_search_posts.return_value = [self.post]
        request = self.factory.get(reverse('search_results') + '?q=test')
        response = search_results(request)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/search_results.html')
        self.assertIn(self.post, response.context['posts'])
        mock_search_posts.assert_called_with('test')

if __name__ == '__main__':
    unittest.main()