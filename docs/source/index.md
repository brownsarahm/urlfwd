# Database-free URL shortening/branding tools

- uses html redirect from tiny landing pages
- each page that forwards includes in its metadata where it will send the person and pulls other metadata from the destination
- manage links from a yaml file
- also provides a utility to generate QR codes for the options

## Usage modes

- install locally, generate html files and QR codes you can host anywhere
- Add a github action to a repo, store `links.yaml` in the repo and configure your short domain to that repo (a gh org might help here). Then you can add links by editing the file or with a form gh action. 
- If you install locally, you can also manage it locally, but push to gh to render. 