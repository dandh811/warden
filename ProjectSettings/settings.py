import os
import sys
from loguru import logger

logger.add('/var/log/blog/blog.log',
           colorize=True,
           format="<green>[{time:YYYY-MM-DD HH:mm:ss}]</green> <level>{message}</level>",
           rotation="500 MB")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

SECRET_KEY = '7q9)5s3^t5i^lt&$p4gnzr1_o+wkyxxpaqhpg*_yw=#w558zx&'

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'simpleui',
    'django.contrib.sitemaps',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.article',
    'apps.users',
    'captcha',
    'apps.cases',
    'apps.tools',
    'mdeditor'
    # 'pure_pagination'
    # 'social_django',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'common.middleware.RequestBlockingMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ProjectSettings.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.article.context_processors.add_variable_to_context',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
                'apps.article.views.global_setting'
            ],
            'libraries': {
                'article_extras': 'apps.article.templatetags.article_extras',

            }
        },

    },
]

WSGI_APPLICATION = 'ProjectSettings.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'blog',
        'USER': 'root',
        'PASSWORD': 'Sihun2016812',
        'HOST': '81.70.89.72',
        'PORT': '3306',
        'OPTIONS': {
                "init_command": "SET foreign_key_checks = 0;",  # 取消外键检查
        },
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "collectstatic/")
STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder"
)

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static/")
]

LOGIN_URL = '/user/login'

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"      # 跟STATIC_URL类似，指定用户可以通过这个路径找到文件

# 邮件配置
EMAIL_USE_SSL = True
EMAIL_HOST = 'smtp.163.com'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'dandh811@163.com'
EMAIL_HOST_PASSWORD = 'BFIVASCXBHJSFDBL'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# 注册有效期天数
CONFIRM_DAYS = 1

SESSION_COOKIE_AGE = 60 * 60 * 24 * 15
SESSION_SAVE_EVERY_REQUEST = True

# 设置要使用的第三方登录
AUTHENTICATION_BACKENDS = (
    'social_core.backends.weibo.WeiboOAuth2',           # 使用微博登录
    'social_core.backends.weixin.WeixinOAuth2',         # 使用微信登录
    'social_core.backends.qq.QQOAuth2',                 # 使用QQ登录
    'django.contrib.auth.backends.ModelBackend',        # 指定django的ModelBackend类
)

# 配置微博开放平台授权
# SOCIAL_AUTH_要使用登录模块的名称大小_KEY，其他如QQ相同
SOCIAL_AUTH_WECHAT_KEY = '3392969003'
SOCIAL_AUTH_WECHAT_SECRET = '51a8b59a178960c38f554e9f47d5223d'

# 登录成功后跳转页面
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/'

# 网站的基本信息配置
SITE_NAME = '小猪哼哼'  # 站点名称
SITE_DESCRIPTION = '小猪哼哼'  # 站点描述
SITE_KEYWORDS = '小猪哼哼,信息安全,Web安全,极客'  # 站点关键词
SITE_TITLE = '信息安全学习记录'  # 博客标题
SITE_TYPE_CHINESE = '宁静致远'  # 打字效果 中文内容
SITE_TYPE_ENGLISH = 'The quieter you become, the more you are able to hear'  # 打字效果 英文内容
SITE_MAIL = 'dandh811@163.com'  # 我的邮箱
SITE_ICP = '京ICP备20000068号'  # 网站备案号
SITE_ICP_URL = 'http://beian.miit.gov.cn'  # 备案号超链接地址
SITE_DOMAIN = 'http://www.dongjianjun.com'

logger.warning('blog started')
