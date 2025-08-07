# Gh actions

To use with github, add one or both of these to your repo

```{important}
These are here for completeness but `urlfwd init` should set these up 
and `urlfwd deploy --update` can be used to maintain them, if this package is up to date
```


## For autobuild when links.yml is edited

add the following contents to `.github/workflows/build.yml`:

```{literalinclude} ../../urlfwd/assets/build.yml
:name: build.yml 
:caption: build.yml
``` 


## Form use

By [manually triggering ](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/manually-run-a-workflow)the action bewlo, you can also use a gh action form instead of editing the yaml directly, the form will be  named `Add a link via form` on the left panel (not the center, that is logs)

```{literalinclude} ../../urlfwd/assets/form_add.yml
:name: .github/workflows/build.yml 
:caption: form_add.yml
```
