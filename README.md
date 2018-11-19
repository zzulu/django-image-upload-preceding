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

### pip 업데이트 & 장고 설치
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

urlpatterns = [

]
```


## [C]RUD

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
