# drsmb-co.github.io

lightweight url forwarding 


## Current Use

- the docs folder is served via github pages
- the links.yml file is the content
- `pip install .` then use `genlinks links.yml` to generate

## Roadmap

- [x] skip already existing files, instead of overwriting (if more efficient)
- [x] validate that there are no duplicates
- [x] create a command that appends to links.yml?
- [x] make auto-commit?
- [ ] handle multi-link/small landing pages?
- [x] setup github action so that build occurs remotely
- [ ] refactor code to a separate repo so that it can be re-usable

