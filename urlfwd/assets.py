
readme_text = '''# URL Forwarding 

lightweight url forwarding via [urlfwd](https://github.com/brownsarahm/urlfwd)

- auto build action if `links.yml` is edited locally or manually in browser.
- form based action for setting a new one from web interface both adding to `links.yml` and rebuilding

automatically generates forwarding urls and QR codes with landing pages at qr/key'''


gh_deploy_yml = '''name: Make links and QR codes from source and deploy
on:
  push:
    branches:
      - 'main'


jobs:
# Deploy job
  build_deploy:

    # Grant GITHUB_TOKEN the permissions required to make a Pages deployment
    permissions:
      pages: write      # to deploy to Pages
      id-token: write   # to verify the deployment originates from an appropriate source

    # Deploy to the github-pages environment
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}

    # Specify runner + deployment step
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: 3.12

      - name: Install & build
        run: |
          pip install git+https://github.com/brownsarahm/urlfwd.git

      - name: Build
        run: |
          urlfwd gen links -v -l
    
    # delete (or comment out with a # the `genqrs` line to not build the QR codes)
      - name: Generate QRs
        run: |
          urlfwd gen qrs 

# by default the html files will be generated to go to ta dcs folder
      - name: Upload Pages artifact
        uses: actions/upload-pages-artifact@v3
        with: 
          path: "./docs/"

      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
'''


gh_form_yml = '''name: Add a link via form
on:
  workflow_dispatch:
    inputs:
      new_key:
        description: new key to create
        required: true
      forward_url:
        description: url to foward to


jobs:
# Add the link to the links.yml
  add_link:
    # Grant GITHUB_TOKEN the permissions required to make a Pages deployment
    permissions:
      pages: write      # to deploy to Pages
      id-token: write   # to verify the deployment originates from an appropriate source
      contents: write

    # Deploy to the github-pages environment
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}

    # Specify runner + deployment step
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: 3.12

      - name: Install & build
      # TODO: modify to create template file
        run: |
          pip install git+https://github.com/brownsarahm/urlfwd.git
          addlink -l ${{ github.event.inputs.new_key }} -u  ${{ github.event.inputs.forward_url }}
          genlinks --landing 

      - uses: stefanzweifel/git-auto-commit-action@v5
        with:
          # Optional. Commit message for the created commit.
          # Defaults to "Apply automatic changes"
          commit_message: add ${{ github.event.inputs.new_key }} 

          

          #  glob pattern of files which should be added to the commit
          file_pattern: 'links.yml'

          # Optional. Options used by `git-push`.
          # See https://git-scm.com/docs/git-push#_options
          # push_options: '--force'
          
          # Optional. Disable dirty check and always try to create a commit and push
          skip_dirty_check: true    
          
          # Optional. Skip internal call to `git fetch`
          skip_fetch: true    
          
          # Optional. Skip internal call to `git checkout`
          skip_checkout: true

          # Optional. Prevents the shell from expanding filenames. 
          # Details: https://www.gnu.org/software/bash/manual/html_node/Filename-Expansion.html
          disable_globbing: true'''