# url fwd

lightweight url forwarding 

This provides a lightweight equivalent to url shortening without a database


## Current Use


- the links.yml file is the content, it will build to a docs folder 
- that can either be tracked and served with gh pages or built and deployed as an artifact
- for more [see my example usage](https://github.com/drsmb-co/drsmb-co.github.io)
- `pip install .` 
-  `genlinks links.yml` to generate 
-  `addlink` can add a new to the file via prompting or use `--help` for more

