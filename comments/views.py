from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Post

from .models import Comment
from .forms import CommentForm

# Create your views here.

def post_comment(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)

    if request.method == 'POST':
        #构造CommentForm的实力，这样Djiango的表单就生成了
        form = CommentForm(request.POST)
        if form.is_valid():
        #commit=False 的作用是仅仅利用表单的数据生成Comment模型类的实例，但不保存评论数据到数据库
            comment = form.save(commit=False)
            #将评论和被评论的文章关联
            comment.post = post
            comment.save()
            return redirect(post)

    else:
        comment_list = post.comment_set.all()
        context = {'post': post,
                   'form': form,
                   'comment_list': comment_list
                   }
        return render(request, 'blog/detail.html', context=context)
    return redirect(post)

