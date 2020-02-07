Kustomize Wrapper [![latest-version](
  https://img.shields.io/pypi/v/kustomize-wrapper.svg)](
  https://pypi.org/project/kustomize-wrapper)
=================

[![travis-build](
  https://img.shields.io/travis/painless-software/kustomize-wrapper/master.svg?logo=travis)](
  https://travis-ci.org/painless-software/kustomize-wrapper)
[![kustomize](
  https://img.shields.io/badge/kustomize-v3.5.4-5d8bee.svg?logo=kubernetes)](
  https://github.com/kubernetes-sigs/kustomize/releases)
[![kubeval](
  https://img.shields.io/badge/kubeval-0.14.0-3f51b5.svg?logo=kubernetes)](
  https://github.com/instrumenta/kubeval/releases)
[![python-support](
  https://img.shields.io/pypi/pyversions/kustomize-wrapper.svg)](
  https://pypi.org/project/kustomize-wrapper)
[![license](
  https://img.shields.io/pypi/l/kustomize-wrapper.svg)](
  https://github.com/painless-software/kustomize-wrapper/blob/master/LICENSE)

A Python wrapper for the Kubernetes [Kustomize](https://kustomize.io/) tool
and related tooling.

- More readable, more concise one-liners
- Automatic linting (with integrated `kubeval`)
- Easy installation with `pip` (e.g. in combination with `tox`)
- Cross-platform (ships binaries for supported platforms)

Installation
------------

```console
python3 -m pip install kustomize-wrapper
```

Why should I use this tool?
---------------------------

Forget about several `kustomize` calls, piping your calls into `kubeval`
or `kubectl apply` commands. Using Kustomize is now even more pleasant!

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
  - kustomize lint deployment/overlays/*
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
  - kustomize apply deployment/overlays/production --edit deployment/base \
        set image IMAGE="foobar/application:${CI_COMMIT_SHA}"
```

Usage
-----

```console
kustomize --help
```

Philosophy:

- Build automatically
- Kustomize commands become CLI options
- Kubeval options become CLI options of `lint` command
