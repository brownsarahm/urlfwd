import click 
import yaml
import subprocess
import os

from .assets import gh_deploy_yml, gh_form_yml, readme_text
from .genpage import files_from_dict,create_landing,qrs_from_dict, config_default
from .manage_links import add_link,find_duplicate_keys


# make a group to hold commands
@click.group()
def urlfwd_cli():   
    '''
    A set of tools to create a set of html redirect pages or QR codes from a yaml file
    '''
    pass

# make a subgroup to hold commands 
@urlfwd_cli.group()
def gen():
    '''
    generate links or qrs
    '''
    pass

@urlfwd_cli.group()
def config():
    '''
    set up persistent project options
    '''
    pass


@gen.command
@click.option('-s','--source-yaml',default='links.yml',
              help='file name if not links.yml')
@click.option('-c','--config-yaml',default='config.yml',
              help='configuration file name if not config.yml')
@click.option('-r','--retain',is_flag=True,
              help='retain existing (do not overwrite)')
@click.option('-p','--out-path',default='docs',
              help='path to write files to default docs')
@click.option('-v','--verbose',is_flag=True,
              help='verbose mode, print details')
@click.option('-l','--landing',is_flag =True,
              help='create a landing page')
@click.option('-i','--index',is_flag =True,
              help='create a landing page, with index')


def links(source_yaml,retain,out_path,verbose,config_yaml,
                   landing, index):
    '''
    from a yaml source file create a set of toy files with file names as the keys
    and the values as the content of each file

    '''
    # TODO: check file type and use different readers to accepts files other than yaml?

    duplicated_keys = find_duplicate_keys(source_yaml)
    # empty list wil read as false
    if duplicated_keys:
        click.echo('Warning: the following keys are duplicated, only last one will be used:\n   ' +
                    '\n  '.join(duplicated_keys))
    else:
        if verbose:
            click.echo('no duplicate keys')

    # read file 
    with open(source_yaml,'r') as f:
        files_to_create = yaml.safe_load(f)

    if os.path.exists(config_yaml):
        with open(config_yaml,'r') as f:
            config = yaml.safe_load(f)
    else:
        config = {}


    overwrite = not(retain)
    # call creator
    log = files_from_dict(files_to_create,overwrite,out_path,
                          logging=verbose,config_in=config)

    if verbose and log:
        click.echo(log)

        
    if landing or index:
        if verbose:
            click.echo('adding landing')
        create_landing(config,out_path,full_dict=files_to_create,index=index)
        


@gen.command
@click.option('-s','--source-yaml',default='links.yml',
              help='file name if not links.yml')
@click.option('-c','--config-yaml',default='config.yml',
              help='configuration file name if not config.yml')
@click.option('-r','--retain',is_flag=True,
              help='retain existing (do not overwrite)')
@click.option('-p','--out-path',default='docs',
              help='path to write files to default docs/qr')
@click.option('-v','--verbose',is_flag=True,
              help='verbose mode, print details')
@click.option('-f','--flyer-pages',is_flag =True,
              help='create a flyer page for each qr code')
@click.option('-t','--flyer-template-input',default='default',
              help='template to use for flyers if generated')

@click.option('-d','--flyer-desc-template',default='default',
              help='template to use for flyer descrition if detailed')
@click.option('-i','--index',is_flag =True,
              help='create a landing page, with index')


def qrs(source_yaml,retain,out_path,verbose,config_yaml,
                   flyer_pages, flyer_template_input,flyer_desc_template, index):
    '''
    from a yaml source file create a set QR codes to each link and optionally a flyer page
    with a QR code and description of the link

    '''
    # TODO: check file type and use different readers to accepts files other than yaml?

    duplicated_keys = find_duplicate_keys(source_yaml)
    # empty list wil read as false
    if duplicated_keys:
        click.echo('Warning: the following keys are duplicated, only last one will be used:\n   ' +
                    '\n  '.join(duplicated_keys))
    else:
        if verbose:
            click.echo('no duplicate keys')

    # read file 
    with open(source_yaml,'r') as f:
        files_to_create = yaml.safe_load(f)

    if os.path.exists(config_yaml):
        with open(config_yaml,'r') as f:
            config = yaml.safe_load(f)
    else:
        config = {}


    overwrite = not(retain)
    # call creator
    log = qrs_from_dict(files_to_create,overwrite,base_path = out_path,
                    flyer_pages=flyer_pages,
                          logging=verbose,config_in=config)

    if verbose and log:
        click.echo(log)

    

@urlfwd_cli.command
@click.option('-u','--url',prompt='URL to forward to',
              help='url to forward to')
@click.option('-l','--short-link',prompt= 'short name to create',
              help='short name to create')
@click.option('-y','--yaml-file',default='links.yml',
              help='file name if not links.yml')
@click.option('-f','--force',is_flag=True,
              help = 'force to overwrite an existing key')
@click.option('-b','--build',is_flag=True,
              help = 'also rebuild')
@click.option('-c','--commit',is_flag=True,
              help = 'commit and push the links file')


def add(url,short_link,yaml_file,force,build, commit):
    '''
    add a new link with options or prompting
    '''
    if build:
        message,files_to_create = add_link(url,short_link,yaml_file, force,
                                           return_dict=build)
        files_from_dict(files_to_create)
    else:
        message = add_link(url,short_link,yaml_file, force)
    
    # will return nothing if succeeds with no overwriteing, otherwise print
    if message:
        click.echo(message)

    if commit:
        commit_msg = '"add ' + short_link +'"'
        subprocess.run(['git','add','links.yml'])
        subprocess.run(['git','commit','-m',commit_msg])
        subprocess.run(['git','push'])


@config.command()
@click.option('--author', prompt=True,
              help='Author Name',
              default=config_default['author'], prompt_required=True)
@click.option('--author-url', prompt=True,  help='Author URL',
              default=config_default['author-url'], prompt_required=True)
@click.option('--title', prompt=True, 
              help='Title for index page',
              default=config_default['title'], prompt_required=False)
@click.option('--index', prompt=True, 
              help='Index prefix before autogen',
              default=config_default['index'].strip(), prompt_required=False)
@click.option('--about', prompt=True,  help='Description of the project for the index',
              default=config_default['about'], prompt_required=False)
@click.option('--force', is_flag=True,
              help='Force overwrite existing config file')

def create(author, title, index, author_url, about, force):
    '''
    create a config file for the project
    '''
    if os.path.exists('config.yml') and not force:
        click.echo('Configuration file already exists. ') 
        click.echo('Use `urlfwd config edit` to modify the existing configuration file or ')
        cur_opts = f'--author "{author}" --title "{title}"' + \
                    f' --author-url "{author_url}" --about "{about}"'+ \
                    f'--index "{index}"' 
        
        click.echo(f'`urlfwd config create {cur_opts} --force` to overwrite it.')
        click.echo('Exiting without changes.')
        return
        
    config = {
            'author': author,
            'title': title,
            'author_url': author_url,
            'about': about,
            'index': index,
        }

    with open('config.yml', 'w') as f:
        yaml.dump(config, f)

    click.echo('Configuration file created successfully.')
    return 

@config.command() 

def edit():
    '''
    
    interactively edit an existing config file
    '''
    if os.path.exists('config.yml'):
        with open('config.yml', 'r') as f:
            config = yaml.safe_load(f)
            click.echo('Current configuration:')
            click.echo(yaml.dump(config, default_flow_style=False))
        
        if not config:
            click.echo('Configuration file is empty.')
            return
        
        # Prompt for each field
        author = click.prompt('Author Name',
                                default=config.get('author', ''))
        author_url = click.prompt('Author URL', 
                                    default=config.get('author_url', ''))
        title = click.prompt('Title for index page',
                                default=config.get('title', ''))
        about = click.prompt('Description of the project for the index',
                            default=config.get('about', ''))
        index = click.prompt('Index prefix before autogen',
                            default=config.get('index', ''))
        
        config = {
            'author': author,
            'title': title,
            'author_url': author_url,
            'about': about,
            'index': index,
        }
    else:
        click.echo('Configuration file does not exist. Please run urlfwd config create to create one first.')
        return


@urlfwd_cli.command()
@click.option('--usegit', is_flag=True,
              help='the project will use git to track changes and push to remote')
@click.option('--gh-deploy', is_flag=True,
              help='the project will be hosted with gh pages')
@click.option('--gh-form', is_flag=True,
              help='the project will have a github form to add links')
@click.option('--reset', is_flag=True,
              help='reset existing files')
def init(usegit, gh_deploy,gh_form,reset):
    '''
    initialize the project with a default config and links file
    '''
    if reset:
        if click.confirm('Do you want to reset links.yml? ' \
                    'This will overwrite existing file'):
            if os.path.exists('links.yml'):
                os.remove('links.yml')
        if click.confirm('Do you want to rese the github actions? ' \
                    'This will overwrite existing files'):
            if os.path.exists('.github'):   
                subprocess.run(['rm','-rf','.github'])

        if click.confirm('Do you want to reset the README.md? ' \
                    'This will overwrite existing file'):
            if os.path.exists('README.md'):
                os.remove('README.md')
        

    if not os.path.exists('links.yml'):
        with open('links.yml', 'w') as f:
            f.write('# add links here like shortname: https://url/to/go/to\n')
        click.echo('Created empty links.yml')

    if usegit and not os.path.exists('.git'):
        if not os.path.exists('.gitignore'):
            with open('.gitignore', 'w') as f:
                f.write('docs/\n')
        subprocess.run(['git','init'])
        click.echo('Initialized git repository')

    if gh_deploy and not os.path.exists('.github/workflows/publish_docs.yml'):
        if not os.path.exists('.github/workflows'):
            os.makedirs('.github/workflows')
    
        with open('.github/workflows/publish_docs.yml', 'w') as f:
            f.write(gh_deploy_yml)
        click.echo('Created GitHub Actions workflow for deployment')

    if gh_form and not os.path.exists('.github/workflows/add_link.yml'):
        if not os.path.exists('.github/workflows'):
            os.makedirs('.github/workflows')
    
        with open('.github/workflows/add_link.yml', 'w') as f:
            f.write(gh_form_yml)
        click.echo('Created GitHub Actions workflow for adding links via form')
    
    if not os.path.exists('README.md'):
        with open('README.md', 'w') as f:
            f.write('# URL Forwarding Project\n\n'
                    'This project provides tools to create short links and QR codes '
                    'for easy access to URLs using [urlfwd]().\n\n'
                    '## Usage\n\n'
                    'Run `urlfwd --help` for more information on available commands.')
        click.echo('Created README.md file')
    

    click.echo('Project initialized successfully. You can now add links to links.yml and run urlfwd commands.')
    click.echo('Run `urlfwd config` to set up the configuration file.')
    
@urlfwd_cli.command()
@click.option('--gh-deploy', is_flag=True,
              help='the project will be hosted with gh pages')
@click.option('--gh-form', is_flag=True,
              help='the project will have a github form to add links')
@click.option('--update', is_flag=True,
              help='reset existing files')
@click.option('--commit', is_flag=True,
              help='commit and push the changes')
def deploy(gh_deploy,gh_form,update,commit):
    '''
    set up github actions for deployment and/or adding links via form
    '''


    if gh_deploy and  not os.path.exists('.github/workflows/build.yml'):
        if not os.path.exists('.github/workflows'):
            os.makedirs('.github/workflows')
    
        with open('.github/workflows/build.yml', 'w') as f:
            f.write(gh_deploy_yml)
        click.echo('Created GitHub Actions workflow for deployment')

    if gh_form and not os.path.exists('.github/workflows/add_link.yml'):
        if not os.path.exists('.github/workflows'):
            os.makedirs('.github/workflows')
    
        with open('.github/workflows/add_link.yml', 'w') as f:
            f.write(gh_form_yml)
        click.echo('Created GitHub Actions workflow for adding links via form')

    if update: 
        if os.path.exists('.github/workflows/build.yml'):
            with open('.github/workflows/build.yml', 'w') as f:
                f.write(gh_deploy_yml)
            click.echo('Updated GitHub Actions workflow for deployment')
        if os.path.exists('.github/workflows/add_link.yml'):
            with open('.github/workflows/add_link.yml', 'w') as f:
                f.write(gh_form_yml)
            click.echo('Updated GitHub Actions workflow for adding links via form')
    

    if commit:
        commit_msg = '"set github actions from package"'
        subprocess.run(['git','add','.github/'])
        subprocess.run(['git','commit','-m',commit_msg])
        subprocess.run(['git','push'])