from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Article, Category
from .forms import ArticleForm, CategoryForm

@login_required
def article_list(request):
    query = request.GET.get('q', '')
    category_id = request.GET.get('category', '')
    articles = Article.objects.filter(is_published=True)
    if query:
        articles = articles.filter(Q(title__icontains=query) | Q(content__icontains=query))
    if category_id:
        articles = articles.filter(category_id=category_id)
    categories = Category.objects.all()
    return render(request, 'knowledge/article_list.html', {
        'articles': articles, 'categories': categories,
        'query': query, 'selected_category': category_id
    })

@login_required
def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    article.views_count += 1
    article.save()
    return render(request, 'knowledge/article_detail.html', {'article': article})

@login_required
def article_create(request):
    if request.user.role not in ['admin', 'agent']:
        messages.error(request, 'Permission denied.')
        return redirect('knowledge:list')
    form = ArticleForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        article = form.save(commit=False)
        article.author = request.user
        article.save()
        messages.success(request, 'Article created!')
        return redirect('knowledge:detail', pk=article.pk)
    return render(request, 'knowledge/article_form.html', {'form': form, 'title': 'New Article'})

@login_required
def article_update(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.user.role not in ['admin', 'agent']:
        return redirect('knowledge:list')
    form = ArticleForm(request.POST or None, instance=article)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Article updated!')
        return redirect('knowledge:detail', pk=pk)
    return render(request, 'knowledge/article_form.html', {'form': form, 'title': 'Edit Article', 'article': article})

@login_required
def article_delete(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.user.role == 'admin':
        article.delete()
        messages.success(request, 'Article deleted.')
    return redirect('knowledge:list')
