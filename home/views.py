
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth import login as auth_login
from . forms import LoginForm, UserRegisterForm
from django.core.validators import validate_email
from .templatetags import extra_filter
from .models import *
from django.db.models import Q
from django.urls import reverse_lazy
from django.views import generic
from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import DetailView,ListView,CreateView,UpdateView,DeleteView,View
from django.views.generic.edit import CreateView,ProcessFormView
from django.utils.text import slugify
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
class Home(ListView):
    template_name='blog.html'
    model=Blog
    paginate_by=4
    ordering=['author_id']
    paginate_orphans = 1

class ContinueReading(DetailView):
    model=Blog
    template_name='blog_post.html'
    
    # comment_form=CommentForm()
    # reply_form=ReplyCommentForm()
    def get_context_data(self, **kwargs):
        """Insert the single object into the context dict."""
        context = {}
        if self.object:
            # context['comment_form'] = self.comment_form
            # context['reply_form'] = self.reply_form
            slug=self.kwargs['slug']
            print(slug)
            blog=Blog.objects.filter(slug=slug).first()
            # print(blog)
            # if blog.viewers == None:
            #         blog.viewers = ""
            #         blog.save()
            # user=self.request.user
            # if user.is_authenticated and user.first_name not in blog.viewers:
            #     # increment 
            #     blog.numViews += 1
            #     blog.save()
            #     # add username to viewers list
            #     blog.viewers+=user.first_name
            #     blog.save()
            comment=BlogComment.objects.filter(blog=blog,parent=None)
            replies=BlogComment.objects.filter(blog=blog).exclude(parent=None)
            replyDict={}
            for reply in replies:
                if reply.parent.comment_id not in replyDict.keys():
                    replyDict[reply.parent.comment_id]=[reply]
                else: 
                    replyDict[reply.parent.comment_id].append(reply)
            # print(replyDict)  
            context['comment'] = comment
            context['replies'] = replies
            context['replyDict'] = replyDict
            context_object_name = self.get_context_object_name(self.object)
            if context_object_name:
                context[context_object_name] = self.object
            
        context.update(kwargs)
        return super().get_context_data(**context)
    def get_object(self, queryset=None):
        slug=self.kwargs['slug']
        obj=Blog.objects.filter(slug=slug).first()
        if obj.viewers == None:
                    obj.viewers = ""
                    obj.save()
        user=self.request.user
        if user.is_authenticated and user.first_name not in obj.viewers:
            # increment 
            obj.numViews += 1
            obj.save()
            # add username to viewers list
            obj.viewers+=user.first_name
            obj.save()

        return obj
    def dispatch(self, *args, **kwargs):
        slug=self.kwargs['slug']
        blog=Blog.objects.filter(slug=slug)
        if not blog.exists():
            return redirect('home')
        return super(ContinueReading, self).dispatch(*args, **kwargs)
        


class BlogUpdateView(LoginRequiredMixin, UpdateView):
    model = Blog
    template_name='updatepost.html'
    fields = ["title", "description", "thumbnail",]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        update = True
        context['update'] = update

        return context
   
    def get_success_url(self):
        messages.success(self.request, 'Your post has been updated successfully.')
        return reverse_lazy("home")

    
    def get_queryset(self):
       return  self.model.objects.filter(author=self.request.user)

    def dispatch(self, request, *args, **kwargs):
        """ Making sure that only authors can update stories """
        obj = self.get_object()
        if obj.author != self.request.user:
            # return redirect(obj)
            return HttpResponse('Permission Denied')
        slug=self.kwargs['slug']
        blog=Blog.objects.filter(slug=slug)
        if not blog.exists():
            return redirect('home')
        return super(UpdateView, self).dispatch(request, *args, **kwargs)
   

class BlogDeleteView(LoginRequiredMixin, DeleteView):
    model = Blog
    template_name='deletepost.html'
    def get_success_url(self):
        messages.success(
            self.request, 'Your post has been deleted successfully.')
        return reverse_lazy("home")

    def get_queryset(self):
        return self.model.objects.filter(author=self.request.user)
    def dispatch(self, *args, **kwargs):
        slug=self.kwargs['slug']
        blog=Blog.objects.filter(slug=slug,author=self.request.user)
        if not blog.exists():
            return redirect('home')
        

        return super(ContinueReading, self).dispatch(*args, **kwargs)


class Login(LoginView):
    template_name='authentication/login.html'
    authentication_form=LoginForm
    def form_valid(self, form):
        print("Inside Login")
        
        email=self.request.POST.get('username')
   
        if validate_email(email):
                    pass
      
        user_obj=User.objects.filter(email=email).first()
           
        print("Email Exists")
        if user_obj.is_verified!=True:
            messages.success(self.request,'Please check for Your mail to verify')
            return redirect('/login')

        if user_obj.is_verified==True:
            
            print("user is verified")
            auth_login(self.request,form.get_user())
            messages.success(self.request,'Successfully logged in')
            return redirect('/')
               
        else: 
            messages.success(self.request,'Account has not been verified')
            return redirect('/login')
     
        

class Logout(LogoutView):
    template_name='authentication/logout.html'
    success_url='/'



class Register(generic.CreateView):
    form_class = UserRegisterForm
    success_url = reverse_lazy('token-send')
    template_name='authentication/sign_up.html'
    def form_valid(self, form):
        form.is_staff=True
        form.is_active=True
        messages.success(self.request, f'Account created successfully')
        return super().form_valid(form)

class Search(ListView):
    model=Blog
    template_name='search_result.html'
    def get_queryset(self):
        query = self.request.GET.get('query')
        object_list = self.model.objects.all()
        if query:
            object_list = object_list.filter(Q(title__icontains=query)|Q(description__icontains=query))
        return object_list
    

class ConfirmLogout(TemplateView):
    template_name='authentication/logout.html'    

class TokenSend(TemplateView):
    template_name='authentication/token_send.html'

class AccountVerify(TemplateView):
    # model=User
    template_name='authentication/verify_account.html'
    def get_context_data(self, **kwargs):
        token=self.kwargs['auth_token']
        print(token)
        user = User.objects.get(auth_token=kwargs['auth_token'])
        user.is_verified=True
        user.save()
        messages.success(self.request,"Your account has been verified")
       

class AddPost(CreateView,ProcessFormView):
    template_name = 'addpost.html'
    model=Blog
    fields=['title','description','thumbnail']
    # form_class = AddPostForm
    def get_success_url(self):
        messages.success(
            self.request, 'Your blog has been created successfully.')
        return reverse_lazy("home")
    def form_valid(self, form):
        blog = form.save(commit=False)
        blog.author = self.request.user
        # blog.save()
        
        blog.slug=slugify(form.cleaned_data['title'])
        #article.save()  # This is redundant, see comments.
        return super(AddPost, self).form_valid(form)




class CommenPostView(LoginRequiredMixin,View):

    '''def get(self,*args,**kwargs):
      
        form=CommentForm()
        print(form)
        # coupon=CouponForm()
        # orders=Order.objects.filter(user=self.request.user,ordered=False)
        context={'form':form}
        return render(self.request,'blog_post.html',context)'''

    def post(self,*args,**kwargs):
        comment=self.request.POST.get("comment")

        user=self.request.user
        post_id=self.request.POST.get("post_id")
        print(post_id)
        blog=get_object_or_404(Blog,post_id=post_id)
        print(blog)
        # comments = BlogComment.comment.add(comment)
       

        parentSno=self.request.POST.get("parentSno")
        print(parentSno)
        if parentSno=="":
            comment=BlogComment(comment=comment,blog=blog,user=user)
            comment.save()
            messages.success(self.request,'Your comment has been posted successfully!')
        else:
            parent=BlogComment.objects.get(comment_id=parentSno)
            reply=BlogComment(comment=comment,blog=blog,user=user,parent=parent)
            reply.save()
            messages.success(self.request,'Your reply has been posted successfully!')
        
        return redirect(f'/continue-reading/{blog.slug}') 
        
