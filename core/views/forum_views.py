from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.http import JsonResponse
from ..models import ForumPost, Comment
from ..forms import ForumPostForm, CommentForm
from .mixins import OwnerRequiredMixin, SuccessMessageMixin, SoftDeleteMixin, SearchMixin
from ..utils import notify_new_comment, notify_mention, notify_reply, notify_post_like

class ForumPostListView(LoginRequiredMixin, SearchMixin, ListView):
    model = ForumPost
    template_name = 'core/forum_index.html'
    context_object_name = 'posts'
    search_fields = ['title', 'content']
    paginate_by = 10
    login_url = '/core/login/'
    
    def get_queryset(self):
        queryset = super().get_queryset().filter(is_active=True)
        category = self.request.GET.get('category', '')
        if category:
            queryset = queryset.filter(category=category)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ForumPost.CATEGORY_CHOICES
        context['current_category'] = self.request.GET.get('category', '')
        context['search_query'] = self.request.GET.get('q', '')
        return context

class ForumPostDetailView(LoginRequiredMixin, DetailView):
    model = ForumPost
    template_name = 'core/post_detail.html'
    context_object_name = 'post'
    login_url = '/core/login/'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.filter(parent=None, is_active=True).order_by('-created_at')
        context['comment_form'] = CommentForm()
        return context

class ForumPostCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = ForumPost
    form_class = ForumPostForm
    template_name = 'core/create_post.html'
    success_url = reverse_lazy('core:forum_index')
    success_message = '¡Publicación creada exitosamente!'
    login_url = '/core/login/'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class ForumPostUpdateView(LoginRequiredMixin, OwnerRequiredMixin, SuccessMessageMixin, UpdateView):
    model = ForumPost
    form_class = ForumPostForm
    template_name = 'core/edit_post.html'
    success_message = 'Publicación actualizada exitosamente.'
    login_url = '/core/login/'
    
    def get_success_url(self):
        return reverse_lazy('core:post_detail', kwargs={'post_id': self.object.pk})

class ForumPostDeleteView(LoginRequiredMixin, OwnerRequiredMixin, SoftDeleteMixin, DeleteView):
    model = ForumPost
    template_name = 'core/delete_post.html'
    success_url = reverse_lazy('core:forum_index')
    login_url = '/core/login/'

@login_required
def post_detail_view(request, post_id):
    post = get_object_or_404(ForumPost, id=post_id)
    comments = post.comments.filter(parent=None, is_active=True).order_by('-created_at')
    comment_form = CommentForm()
    
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            
            # Notificar al autor del post sobre el nuevo comentario
            if hasattr(post, 'author') and post.author != request.user:
                notify_new_comment(post, comment, request.user)
            
            # Procesar menciones
            content = comment.content
            for word in content.split():
                if word.startswith('@'):
                    username = word[1:]
                    try:
                        mentioned_user = User.objects.get(username=username)
                        notify_mention(request.user, mentioned_user, post=post, comment=comment)
                    except User.DoesNotExist:
                        pass
            
            messages.success(request, 'Comentario publicado exitosamente.')
            return redirect('core:post_detail', post_id=post.id)
    
    return render(request, 'core/post_detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form
    })

@login_required
def like_post(request, post_id):
    post = get_object_or_404(ForumPost, id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
        # Notificar al autor del post sobre el like
        if hasattr(post, 'author') and post.author != request.user:
            notify_post_like(post, request.user)
    
    return JsonResponse({
        'likes_count': post.likes.count(),
        'liked': liked
    }) 