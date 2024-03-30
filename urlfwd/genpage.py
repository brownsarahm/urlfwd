import os

# default extra settings
config = {'author':'a user',
          'title':'url shortening',
          'body':'',
          'index':'<h2>Index</h2>\n',
          'about':'https://github.com/brownsarahm/urlfwd'}

landing_html ='''
<!DOCTYPE html>
<html lang="en-US">
<head>
    <title>{title}</title>
    <meta name="author" content="{author}" />
    <meta property="og:title" content="{title}" />
    <meta property="og:type" content="website" />
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.3.1/dist/css/bootstrap.min.css"
        integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>

<div class="card text-center w-75 mx-auto my-5">
        <div class="card-header">
            <h1>{title}</h1>
        </div>
        <div class="card-body">
            {body}
            {index}
        </div>
        <div class="card-footer text-muted">
            This domain (or subdomain) is used as a lightweight url shortener
            implemented with <a href="https://github.com/brownsarahm/urlfwd">urlfwd</a>. 
            
            <a href="{about}">about {author}</a>
        </div>
    </div>
</body>
</html>
'''

index_head = '<ol>'
index_entry = '<li><a href="{url}">{name}</a></li>'
index_foot = '</ol>'

def create_landing(config_in,base_path,full_dict=None,index=False):
    '''
    create a landing page at base_path/index.html

    Parameters
    config_in : dictionary
        configurations to overwrite defaults with
    base_path : strign or path
        where to write the index.html file
    full_dict : dictionary
        from links.yml for making index
    index : bool
        creat index
    '''
    config.update(config_in)

    if index:
        index_list = [index_head]
        for name,url in full_dict.items():
            cur_it = index_entry
            index_list.append(cur_it.format(name=name,url=url))
        
        index_text = '\n'.join(index_list + [index_foot])

        config['index'] += index_text
    else:
        config['index'] += 'Not Provided'

    out_file = os.path.join(base_path,'index.html')
    contents = landing_html.format(**config)
    with open(out_file,'w') as f:
        f.write(contents)


pg_html = '''
<!DOCTYPE html>
<html lang="en-US">
<head>
    <title>redirecting to {url}</title>
    <meta http-equiv="refresh" content="0; URL={url}" />
    <meta name="author" content="{author}" />
    <meta property="og:title" content="{name}" />
    <meta property="og:type" content="website" />
    <meta property="og:url" content="{url}" />
    <meta name="description" content="forwarding to {url}"/>
    <link rel="canonical" href="{url}"/>
</head>
<body>
This page should forward to <a href="{url}">{url}</a>
</body>
</html>
'''


def files_from_dict(pages_to_create,overwrite=True,base_path='docs',logging=False,config_in=None):
    '''
    given a dictionary, create html files
    
    Parameters
    ----------
    pages_to_create : dictionary
        keys are names of pages, values are urls to redirect to
    
    '''
    if config_in:
        config.update(config_in)

    if not(os.path.exists(base_path)):
        os.mkdir(base_path)

    if logging:
        log = []
    for path, url in pages_to_create.items():
        # handle case of numbers in key
        if not(type(path) == str):
            path = str(path)

        contents = pg_html.format(url=url,name=path,
                                  author=config['author'])
        out_dir = os.path.join(base_path,path)
        out_file = os.path.join(out_dir,'index.html')
        # do not create if overwriting and already exists, otherwise create 
        #        (will error if exists and not overwriting)
        if not(os.path.exists(out_dir)):
            os.mkdir(out_dir)
            if logging:
                log.append('creating ' + out_dir)

        if logging and os.path.exists(out_file):
            log.append(path + ' exists')

        # write the file out
        if overwrite or not(os.path.exists(out_file)):
            with open(out_file,'w') as f:
                f.write(contents)
            if logging:
                log.append('writing' + out_file)

    # do at end
    if logging:
        # with open(os.path.join(out_dir,'log.txt'),'w') as f:
        #     f.write('\n'.join(log))
        return '\n'.join(log)
    else:
        return ''