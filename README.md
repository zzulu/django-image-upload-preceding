# Django Image Upload

## Django Project Launching

### C9 Workspace 생성
- `Blank`로 C9 Workspace 생성
- AWS Access Key를 사용할 예정이기 때문에 **private**로 만든다.

### pyenv 설치
```bash
git clone https://github.com/pyenv/pyenv.git ~/.pyenv
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi' >> ~/.bashrc
exec "$SHELL"
```

### Python 설치
```bash
pyenv install 3.6.1
pyenv global 3.6.1
```

python version 확인

```bash
python -V
#=> Python 3.6.1
```

### pyenv-virtualenv 설치

```bash
git clone https://github.com/pyenv/pyenv-virtualenv.git $(pyenv root)/plugins/pyenv-virtualenv
echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc
exec "$SHELL"
```

### Project 폴더 생성
```bash
mkdir imageupload
cd imageupload
```

### virtualenv 생성
```bash
pyenv virtualenv 3.6.1 imageupload-venv
pyenv local imageupload-venv
```
터미널 앞쪽에 `(imageupload-venv)` 붙어있는지 확인!

### pip 업데이트 & django 설치
```bash
pip install --upgrade pip 
pip install django
```

### Project 생성

마지막에 `.` 빠뜨리지 않도록 주의! `.`은 현재 폴더를 의미!

```bash
django-admin startproject imageupload .
```

서버 실행 한번 해보고 갑시다.

```bash
python manage.py runserver $IP:$PORT
```

연기를 뿜는 로켓이 나오면 성공!


### App 생성

- App 이름은 **복수형** 추천. (개인 의견임. 답은 없음.)

```bash
django-admin startapp posts
```

### settings.py

- `ALLOWED_HOSTS`에 C9 HOST 등록.
- 우측 상단에 `Share > Application > 주소 클릭 > Copy` 하여 붙여 넣기.
- 붙여 넣을 때, `https://`는 빼고 넣는다.
```python
ALLOWED_HOSTS = [
    'django-image-upload-capollux.c9users.io'
]
```

- `INSTALLED_APPS` 에 방금 생성한 App 추가.
- 제일 앞쪽에 추가. 다른 모듈들보다 우선적으로 로드되기 위하여.
- `,` 빠뜨리지 않도록 주의!
```python
INSTALLED_APPS = [
    'posts',
    ...
]
```


## Git Push Time #1

Git push 한번 하고 갑시다.

### GitHub Remote Repository 생성
[GitHub](https://github.com) repository 생성.


### Git 초기화

```bash
git init
```

### 이름, 이메일 설정

```bash
git config --global user.name 'Junwoo Hwang'
git config --global user.email 'capollux10@gmail.com'
```

### Remote 설정

조금 전 생성한 GitHub remote repository의 주소를 `REMOTE_REPO_URL`에 입력.


```bash
git remote add origin REMOTE_REPO_URL
```

### gitignore

commit 하기 전에, GitHub에 올라가지 않았으면 하는 것들을 git에게 알려주자.
- Project 폴더에 `.gitignore` 파일 생성.
- [Python gitignore](https://github.com/github/gitignore/blob/master/Python.gitignore) 해당 링크에 있는 내용을 복사하여 붙여넣고 저장.


### add & commit

```bash
git add .
git commit -m "Init commit"
```

### push

```bash
git push -u origin master
```


## Model 생성 및 Admin 설정

### posts/models.py

```python
class Post(models.Model):
    image = models.ImageField()
    content = models.TextField()
```

```bash
python manage.py makemigrations
```

에러남! Pillow가 없기 때문! 에러 메세지에서 시키는 대로 하자.

```bash
pip install Pillow
```

```bash
python manage.py makemigrations
python manage.py migrate
```

### posts/admin.py

```python
from .models import Post


admin.site.register(Post)
```

- super user 생성

``` bash
python manage.py createsuperuser
```

- `/admin`으로 접속하여 로그인 후, Post 하나 만들어 본다.
- 정상적으로 생성 되는 것을 확인한다.
- C9 Workspace tree에 보면 project root에 이미지 업로드 된거 볼 수 있음.
- 웹에서 `content`는 확인되지만 `image`는 아직 확인 안됨. 후에 확인 예정. 


## posts App routing 

### imageupload/urls.py

- `import path` 옆에 `include` 추가.
- `path('admin/', ... ),` 위에 아래와 같이 코드 추가.

```python
from django.urls import path, include

urlpatterns = [
    path('posts/', include('posts.urls')),
    path('admin/', admin.site.urls),
]
```

### posts/urls.py

- 이 파일은 없으므로 생성!
- 아래와 같이 틀만 작성, 이전 파일에서 복사해 오면 빠름.

```python
from django.urls import path

app_name = 'posts'

urlpatterns = [

]
```


## CRUD

### posts/views.py

- 일단 List 먼저
- `template_name` 지정안하면 `posts/post_list.html` 이 기본값.

```python
from django.views.generic import ListView
from .models import Post


class PostList(ListView):
    model = Post
```

### posts/urls.py

```python
from . import views

urlpatterns = [
    path('', views.PostList.as_view(), name='list'),
]
```

### posts/templates/posts/post_list.html


```
<h1>Post List</h1>

<ul>
{% for post in post_list %}
    <li>
        <img src="{{ post.image.url }}"></img>
        <p>{{ post.content }}</p>
    </li>
{% endfor %}
</ul>

```

- 여기까지 하고 나서 `/posts`로 가도, 여전히 `image` 확인 불가능.
- 로그를 보면 404 error 가 계속 보임.

## MEDIA_ROOT 설정

- 이걸 설정 안해줘서 로드가 불가능한 상황.
- tree에 보면 이상한 위치에 올라가 있는데, django는 이 위치에 있는 파일을 로드할 수 없음.
- 따라서, 예전에 `TEMPLATE_DIR` 설정 했던거 처럼 설정이 필요하며, 업로드 한 이미지 파일로 접근하는 URL도 설정이 필요함.


### imageupload/settings.py

```python
# Media Files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

### imageupload/urls.py

```python
from django.conf.urls.static import static
from django.conf import settings


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

- 설정 완료 후, `/admin` 페이지로 가서 다시 Post 하나 등록하고 `/posts`를 확인해보자.
- 파일도 `media` 폴더에 잘 올라갔는지 확인!
- '파일 이름이 겹치면 어떻게 하나요!'라고 걱정할 수 있는데, 겹치는 경우 django에서 랜덤 문자열을 뒤에 붙여서 겹치지 않게 해준다.


## Git Push Time #2

### gitignore

- 사용자가 업로드한 이미지는 GitHub에 올라가면 안됨.
- 잘못 올라간 project root에 있는 파일은 삭제.
- `.gitignore` 파일을 열어 `media` 폴더 추가.

### add & commit

```bash
git add .
git commit -m "Add basic image uplaod"
```

### push

- 처음 할 때, `-u` 옵션으로 upstream 설정을 했기때문에 앞으로는 `git push`만 해줘도 된다.

```bash
git push
```


## [C]RUD

New 페이지 & Create 로직을 만들자.

### posts/views.py

```python
from django.views.generic import ListView, CreateView


class PostCreate(CreateView):
    model = Post
    fields = ['image','content',]
```

### posts/urls.py

```python
urlpatterns = [
    ...
    path('new', views.PostCreate.as_view(), name='create'),
]
```

- 링크 생성 및 redirection을 편하게 할 수 있도록, name을 지정.

### posts/templates/posts/post_form.html

- `enctype="multipart/form-data"` 이거 중요! 이미지 올릴때 추가해주어야 함!

```
<h1>Post Form</h1>

<form method="post" enctype="multipart/form-data">
    {% csrf_token %}
    {{ form.as_p }}
    <input type="submit" value="Submit"/>
</form>
```

### posts/templates/posts/post_list.html

- Post 작성 페이지로 편하게 가기 위하여 링크를 추가해 준다.

```
<a href="{% url 'posts:create' %}">New Post</a>
```

- 여기까지 해서 이미지 업로드해보면 `No URL to redirect to.` 에러가 나오는데, 이거는 우리가 아직 Detail 페이지가 없기도 하고 redirect URL을 아직 지정 안해줘서 그렇다! 그러나 `/posts`로 가보면 이미지는 잘 업로드 되었다.


## C[R]UD

Detail 페이지를 만들자.

### posts/views.py

```python
from django.views.generic import ListView, CreateView, DetailView
    

class PostDetail(DetailView):
    model = Post
```

### posts/urls.py

```python
urlpatterns = [
    ...
    path('<int:pk>/', views.PostDetail.as_view(), name='detail'),
]
```

### posts/templates/posts/post_detail.html

```
<h1>Post Detail</h1>

<div>
    <img src="{{ post.image.url }}"></img>
    <p>{{ post.content }}</p>
</div>
```

### posts/templates/posts/post_list.html

- Post Detail 페이지로 편하게 가기 위하여 링크를 추가한다.
- image를 클릭하면 Post로 가도록 하자.

```
<a href="{% url 'posts:detail' pk=post.pk %}">
    <img src="{{ post.image.url }}"></img>
</a>
```

### posts/models.py

- Post 생성 후, Detail 페이지로 바로 오도록 하는 코드!

```python
from django.urls import reverse

class Post(models.Model):
    ...
    
    def get_absolute_url(self):
        return reverse('posts:detail', kwargs={'pk': self.pk})
```

- `/posts/2` 처럼 Detail 페이지에 들어가 보면 페이지가 정상적으로 뜨고, 다시 한번 Create를 해보면 이제는 오류페이지가 아닌 Detail 페이지로 redirect 되는 것을 확인 할 수 있다.


## CR[U]D

Update를 해보자.

### posts/views.py

```python
from django.views.generic import ListView, CreateView, DetailView, UpdateView

class PostUpdate(UpdateView):
    model = Post
    fields = ['image','content',]
```


### posts/urls.py

```python
urlpatterns = [
    ...
    path('<int:pk>/edit/', views.PostUpdate.as_view(), name='update'),
]
```


### posts/templates/posts/post_form.html

- 수정할 것 없음!


### posts/templates/posts/post_detail.html

- 수정페이지로 가는 링크를 만든다.

```
<a href="{% url 'posts:update' pk=post.pk %}">Edit</a>
```

- 여기까지 작성하고 `/posts/2/edit/`로 들어가서 모든 것이 잘 동작하는지 확인해보자.
- `models.py`에서 설정한 `ImageField`가 Image **Currently, Change**와 같이 현재 이미지 링크와 바꿀 이미지 폼을 함께 생성해 준다.


## CRU[D]

Delete를 해보자.

### posts/views.py

```python
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy


class PostDelete(DeleteView):
    model = Post
    success_url = reverse_lazy('posts:list')
```

### posts/urls.py

```python
urlpatterns = [
    ...
    path('<int:pk>/delete/', views.PostDelete.as_view(), name='delete'),
]
```

### posts/templates/posts/post_confirm_delete.html

```
<h1>Post Delete</h1>

<form method="post">
    {% csrf_token %}
    <p>{{ post.pk }}번, 정말 삭제하시겠습니까?</p>
    <input type="submit" value="Confirm"/>
</form>
```

### posts/templates/posts/post_detail.html

- 삭제 페이지로 가는 링크를 만든다.

```
<a href="{% url 'posts:delete' pk=post.pk %}">Delete</a>
```

- 여기까지 작성하고 `/posts/2/delete/`로 들어가서 삭제가 잘 동작하는지 확인해보자.


## Git Push Time #3

### add & commit

```bash
git add .
git commit -m "Add CRUD for Post"
```

### push

```bash
git push
```


## Image Resizing

- `/posts` 페이지를 가보면 이미지가 원본 그대로 업로드 되어서 너무 크게 나온다.
- `img` tag에서 width, height로 크기를 조정 해줄 수도 있지만, 용량 문제도 있고 하니 이미지 자체를 리사이징 해보자.

### Package Install

- django-imagekit 사용을 위하여 pilkit 사전 설치 필요. pillow 도 필요하지만 앞에서 이미 설치하였음.

```bash
pip install pilkit
pip install django-imagekit
```

### imageupload/settings.py

```python
INSTALLED_APP = [
		...
		'imagekit',
		...
]
```

### posts/models.py

```python
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill


class Post(models.Model):
    image = ProcessedImageField(
                upload_to='posts/images',                # 저장 위치
                processors=[ResizeToFill(300, 300)],     # 처리할 작업 목록
                format='JPEG',                           # 저장 포맷
                options={'quality':90},                  # 옵션
            )
```

- `models.py`를 수정했기 때문에 migration을 다시 해주자.

```bash
python manage.py makemigrations
python manage.py migrate
```

- 그리고 서버를 실행하고 이미지를 다시 업로드 해보자. 위에서 설정한 대로 업로드 되는 것을 확인 할 수 있다.
- 주의할 점! 코드를 수정한 후 업로드 하는 사진에만 적용된다. 기존의 사진은 저 설정대로 변하지 않음! 사진을 업로드 하는 시점에 이미지를 변환하고 저장하기 때문!


## Path of Uploaded Images

- 위에서 간단하게 'posts/images' 처럼 고정적인 폴더에 이미지가 업로드 되도록 했는데, 이러면 하나의 폴더에 모든 이미지가 들어가서 보기 안 좋다.(파일 명이 겹치는 건 django에서 알아서 랜덤 문자열을 붙여 구분해준다.)
- 그래서 이미지가 업로드 되는 위치를 깔끔하게 해서 보기 좋게 만들어 보자.

```python
def post_image_path(instance, filename):
    return 'posts/{}/{}'.format(instance.pk, filename)


class Post(models.Model):
    image = ProcessedImageField(
                upload_to=post_image_path,
                ...
            )
```

- `instance.pk` 이 부분은 처음 Post 작성시에는 pk가 없는 상태이기 때문에 `pk`가 `None`이라서 None 폴더에 모이게 됨. 수정할 때는 존재하는 Post라서 pk가 있기 때문에 해당 pk로 폴더가 생성되고 거기에 파일이 저장됨. > 그래서 이렇게는 작성을 잘 하지 않음. 보통 instance.user.pk 또는 instance.user.username 처럼 업로드 한 사람의 정보로 폴더를 구조화하는 경우가 많음.
- 아까와는 다르게 column 자체가 수정된 것이 아니라, 속성만 변했기 때문에 migration을 안해도 된다.


## Git Push Time #4

### add & commit

```bash
git add .
git commit -m "Add imagekit"
```

### push

```bash
git push
```
