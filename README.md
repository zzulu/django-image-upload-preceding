# Django Image Upload

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


## Git push time

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
git commit -m "Init commit
```

### push

```bash
git push -u origin master
```