from jinja2 import Environment, FileSystemLoader
from os import path, listdir, makedirs
import markdown
from io import StringIO

TEMPLATE_DIR = path.join(path.dirname(path.realpath(__file__)), 'templates')
POST_DIR = path.join(path.dirname(path.realpath(__file__)), 'posts')
OUT_DIR = path.join(path.dirname(path.realpath(__file__)), 'output')

env = Environment(loader = FileSystemLoader(TEMPLATE_DIR))
posts = [ f for f in listdir(POST_DIR) if path.isfile(path.join(POST_DIR, f)) and f.endswith('.md')]

post_template = env.get_template('post.html')

if not path.exists(path.join(OUT_DIR, 'posts')):
    makedirs(path.join(OUT_DIR, 'posts'))

for i, post in enumerate(posts):
    title = None
    html_from_markdown = None

    with open(path.join(POST_DIR, post)) as f:
        title = f.readline().rstrip()
        f.seek(0)
        html_from_markdown = markdown.markdown(f.read())
    
    stream = post_template.stream(post=html_from_markdown, title=title)
    stream.dump(path.join(OUT_DIR, 'posts', title.lower().replace(' ', '-') + '.html'))

    #Discard filename in favour of title for links
    posts[i] = title

index_template = env.get_template('index.html')

stream = index_template.stream(posts=posts)
stream.dump(path.join(OUT_DIR, 'index.html'))

print("Successfully assembled a blog in " + OUT_DIR)