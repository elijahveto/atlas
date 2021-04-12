from django.shortcuts import render, get_object_or_404, redirect
from .forms import SectionForm, PostForm, CommentForm
from .models import Section, Post, Comment, Likes
from django.contrib.auth.decorators import login_required
from users.models import User
from django.views.generic import UpdateView, DeleteView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse, reverse_lazy
from datetime import datetime
from users.mixins import GroupRequiredMixin


""" CREATOR VIEWS """


@login_required
def section_create_view(request):
    sections = Section.objects.filter(company_id=request.user.company_id)
    section_form = SectionForm(request.POST or None)
    if section_form.is_valid():
        section_name = section_form.cleaned_data.get('name')
        new_section = Section.objects.create(
            name=section_name,
            company_id=request.user.company_id)
        return redirect(f'../section/{new_section.id}')
    section_form = SectionForm()
    var = {'section_form': section_form,
           'sections':sections}
    return render(request, 'create_section.html', var)


@login_required
def post_create_view(request):
    sections = Section.objects.filter(company_id=request.user.company_id)
    post_form = PostForm(request.POST or None)
    id = request.POST.get('id')
    if post_form.is_valid():
        title = post_form.cleaned_data.get('title')
        text = post_form.cleaned_data.get('text')
        if title and text:
            Post.objects.create(
                title=title,
                text=text,
                section_id=Section.objects.get(id=id).id,
                user_id=request.user.id)
            return redirect(f'../section/{id}')
        else:
            var = {
                'message': 'all field are required',
                'post_form': post_form,
                'sections':sections
            }
            return render(request, 'post_form.html', var)

    post_form = PostForm()
    var = {'post_form': post_form,
           'section_id':id,
           'sections':sections}
    return render(request, 'create_post.html', var)


""" ALL POSTS OVERVIEW """


@login_required
def all_posts_view(request):
    sections = Section.objects.filter(company_id=request.user.company_id)
    posts = {section.id: Post.objects.filter(section_id=section.id) for section in sections}
    comments = []
    for key, value in posts.items():
        for post in posts[key]:
            try:
                comments.append(Comment.objects.filter(post_id=post.id))
            except Comment.DoesNotExist:
                continue
    var = {
        'sections': sections,
        'posts': posts,
        'comments': comments,
        'user': request.user,
    }
    return render(request, 'all_posts.html', var)


""" SECTION VIEW """


def section_view(request, id):
    sections = Section.objects.filter(company_id=request.user.company_id)
    section = get_object_or_404(Section, id=id, company_id=request.user.company_id)
    posts = Post.objects.filter(section_id=section.id).order_by('-date')
    post_dic = {post: User.objects.get(id = post.user_id).get_full_name for post in posts}
    post_form = PostForm(request.POST or None)
    if post_form.is_valid():
        title = post_form.cleaned_data.get('title')
        text = post_form.cleaned_data.get('text')
        if title and text:
            Post.objects.create(
                title=title,
                text=text,
                section_id=id,
                user_id=request.user.id)
        else:
            var = {
                'sections': sections,
                # 'posts': posts,
                'post_dic': post_dic,
                'section': section,
                'message': 'all field are required',
                'post_form': post_form
            }
            return redirect(f'../section/{id}')
    post_form = PostForm()
    var = {
        'sections': sections,
        # 'posts': posts,
        'section': section,
        'post_dic': post_dic,
        'post_form':post_form
    }
    return render(request, 'section_detail_view.html', var)


""" POST VIEW """


@login_required
def detailed_post_view(request, id):
    # init default none values in case no comment edits/deletes
    comment_update_form, to_edit_comment = None, None
    sections = Section.objects.filter(company_id=request.user.company_id)
    # in case a comment edit request was submitted
    if request.POST.get('user wants') == 'edit comment':
        to_edit_comment = request.POST.get('to_edit_comment_id')
        comment_update_form = CommentForm(initial={'text': Comment.objects.get(id = to_edit_comment).text})

    # in case an edited comment was submitted
    elif request.POST.get('user has performed') == 'edit comment':
        form = CommentForm(request.POST or None)
        if form.is_valid():
            to_edit_comment = request.POST.get('edited_comment_id')
            c = Comment.objects.get(id = to_edit_comment)
            c.text = form.cleaned_data.get('text')
            c.date = datetime.now()
            c.save()
            comment_update_form, to_edit_comment = None, None

    # in case a comment delete request was submitted
    elif request.POST.get('user wants') == 'delete comment':
        to_delete_comment = request.POST.get('to_delete_comment_id')
        c = Comment.objects.get(id=to_delete_comment)
        c.delete()

    # in case a new comment was submitted
    else:
        form = CommentForm(request.POST or None)
        if form.is_valid():
            Comment.objects.create(user_id=request.user.id, post_id=id, text=form.cleaned_data.get('text'))

    # load detail view page
    post = get_object_or_404(Post, id=id)
    form = CommentForm()
    post_creator = User.objects.get(id=post.user_id).get_full_name()
    try:
        all_comments = Comment.objects.filter(post_id=id)
        comments = {comment: User.objects.get(id=comment.user_id).get_full_name() for comment in all_comments}
    except Comment.DoesNotExist:
        comments = None
    var = {
                'current_user' : request.user.id,
                'form': form,
                'post': post,
                'post_creator': post_creator,
                'comments': comments,
                'comment_update_form': comment_update_form,
                'to_edit_comment_id': to_edit_comment,
                'sections': sections,
            }

    return render(request, 'post_detail_view.html', var)


""" LIKES """


def like_view(request, id):
    obj = request.POST.get('obj')
    path = request.POST.get('path')
    if obj == 'post':
        try:
            Likes.objects.get(post_id=id, comment_id= None, user_id=request.user.id)
        except Likes.DoesNotExist:
            Likes.objects.create(post_id=id, user_id=request.user.id)
    else:
        try:
            Likes.objects.get(comment_id=obj, user_id=request.user.id, post_id=id)
        except Likes.DoesNotExist:
            Likes.objects.create(comment_id=obj, user_id=request.user.id, post_id=id)

    return redirect(path)


""" EDITING AND DELETE VIEWS """

def superuser_view(request):
    sections = Section.objects.filter(company_id = request.user.company_id)
    var = {
        'sections': sections}
    return render(request, 'superuser_view.html', var)

class PostUpdateView(UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'text']
    template_name = 'post_update.html'
    # queryset = Post.objects.all()

    def test_func(self):
        return Post.objects.filter(id=self.kwargs.get('pk'), user_id=self.request.user.id).exists()

    def get_object(self):
        id = self.kwargs.get('pk')
        return get_object_or_404(Post, id=id)


class PostDeleteView(UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('posts:all_posts')

    def test_func(self):
        return Post.objects.filter(id=self.kwargs.get('pk'), user_id=self.request.user.id).exists()

    def get_object(self):
        id = self.kwargs.get('pk')
        return get_object_or_404(Post, id=id)


class SectionUpdateView(GroupRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Section
    fields = ['name']
    template_name = 'section_update.html'
    success_url = reverse_lazy('posts:superuser')

    def test_func(self):
        return Section.objects.filter(id=self.kwargs.get('pk'), company_id=self.request.user.company_id).exists()

    def get_object(self):
        id = self.kwargs.get('pk')
        return get_object_or_404(Section, id=id)


class SectionDeleteView(GroupRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Section
    template_name = 'section_delete.html'
    success_url = reverse_lazy('posts:superuser')

    def test_func(self):
        return Section.objects.filter(id=self.kwargs.get('pk'), company_id=self.request.user.company_id).exists()

    def get_object(self):
        id = self.kwargs.get('pk')
        return get_object_or_404(Section, id=id)