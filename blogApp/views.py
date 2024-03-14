from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Post, Comment, Tag
from .forms import PostForm, CommentForm

class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blogApp/post_list.html'
    context_object_name = 'posts'
    ordering = ['-published_date']
    
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blogApp/post_form.html'
    success_url = reverse_lazy('post-list')
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blogApp/post_form.html'
    success_url = reverse_lazy('post-list')
    
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(author=self.request.user)
    
class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'blogApp/post_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['comments'] = Comment.objects.filter(post=self.object).order_by('-created_date')
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = self.object
            comment.save()
            return redirect('post-detail', pk=self.object.pk)
        else:
            context = self.get_context_data(object=self.object, comment_form=comment_form)
            return self.render_to_response(context)

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'blogApp/post_confirm_delete.html'
    success_url = reverse_lazy('post-list')
    
class SearchResultsView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blogApp/search_results.html'
    context_object_name = 'posts'

    def get_queryset(self): 
        query = self.request.GET.get('q')
        if query:
            return Post.objects.filter(title__icontains=query) | Post.objects.filter(content__icontains=query)
        else:
            return Post.objects.none()

class TaggedPostListView(ListView):
    model = Post
    template_name = 'blogApp/tagged_posts_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        self.tag = get_object_or_404(Tag, name=self.kwargs.get('tag_name'))
        return Post.objects.filter(tags=self.tag).order_by('-published_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.tag
        return context