# Database-free URL shortening/branding tools

- uses html redirect from tiny landing pages
- each page that forwards includes in its metadata where it will send the person and pulls other metadata from the destination
- manage links from a yaml file
- also provides a utility to generate QR codes for the options

## Get started

```{warning}
This requires a working python install
```

1. Install with `pip install git+https://github.com/brownsarahm/urlfwd.git`
1. Create a folder for your url forwarding (eg if you're using `owner` github org or user to host: `mkdir owner.github.io`) and `cd` in 
1. Run `urlfwd init --usegit` (omit `--usegit` if you will not use git)
1. (optional) Run `urlfwd config`
1. use `urlfwd add -c` and follow the prompts or ommit `-c` to not commit and push 
1. (if using github) [create a repo](https://github.com/new) with the same name. It can be public or private, but do not add any template or files. 
1. (if using github) Follow the github  instructions to "or push an existing repository from the command line" from your new repo
1. (if using github) Periodically update your local install and run `urlfwd deploy --update`


## Usage modes

- install locally, generate html files and QR codes you can host anywhere
- Add a github action to a repo, store `links.yaml` in the repo and configure your short domain to that repo (a gh org might help here). Then you can add links by editing the file or with a form gh action. 
- If you install locally, you can also manage it locally, but push to gh to render. 


```{toctree}
:caption: Contents
:maxdepth: 2


cli.md
example.md
gh.md
api.md
```