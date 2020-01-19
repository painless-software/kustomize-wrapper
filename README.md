Kustomize Wrapper
=================

A wrapper for the Kubernetes Kustomize tool and related tooling.

- More readable one-liners
- Automatic linting (with integrated `kubeval`)
- Easy installation with `pip` (e.g. in combination with `tox`)

Installation
------------

```console
python3 -m pip install kustomize-wrapper
```

Usage
-----

```console
kustomize --help
```

Philosophy:

- Build and lint by default

Why should I use this tool?
---------------------------

Forget about several `kustomize` calls, piping your calls into lint or apply
commands. Using Kustomize is now even more pleasant!

Instead of:
```yaml
lint:
  script:
  - kustomize build deployment/overlays/development | kubeval --strict
  - kustomize build deployment/overlays/integration | kubeval --strict
  - kustomize build deployment/overlays/production | kubeval --strict
```
You can now write:
```yaml
lint:
  script:
  - kustomize deployment/overlays/* --lint strict
```

Instead of:
```yaml
production:
  script:
  - cd deployment/base
  - kustomize edit set image IMAGE="foobar/application:${CI_COMMIT_SHA}"
  - cd ../..
  - kustomize build deployment/overlays/production | kubectl apply -f -
```
You can now write:
```yaml
production:
  script:
  - kustomize deployment/overlays/production
      --edit deployment/base set image IMAGE="foobar/application:${CI_COMMIT_SHA}"
      --apply
```
