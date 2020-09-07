Kustomize Wrapper [![latest-version](
  https://img.shields.io/pypi/v/kustomize-wrapper.svg)](
  https://pypi.org/project/kustomize-wrapper)
=================

[![checks-status](
  https://img.shields.io/github/workflow/status/painless-software/kustomize-wrapper/Checks/master?label=Checks&logo=github)](
  https://github.com/painless-software/kustomize-wrapper/actions?query=workflow%3AChecks)
[![tests-status](
  https://img.shields.io/github/workflow/status/painless-software/kustomize-wrapper/Tests/master?label=Tests&logo=github)](
  https://github.com/painless-software/kustomize-wrapper/actions?query=workflow%3ATests)
[![kustomize](
  https://img.shields.io/badge/kustomize-v3.8.2-5d8bee.svg?logo=kubernetes)](
  https://github.com/kubernetes-sigs/kustomize/releases/kustomize%2Fv3.8.2)
[![kubeval](
  https://img.shields.io/badge/kubeval-0.15.0-3f51b5.svg?logo=kubernetes)](
  https://github.com/instrumenta/kubeval/releases/0.15.0)
[![python-support](
  https://img.shields.io/pypi/pyversions/kustomize-wrapper.svg)](
  https://pypi.org/project/kustomize-wrapper)
[![license](
  https://img.shields.io/pypi/l/kustomize-wrapper.svg)](
  https://github.com/painless-software/kustomize-wrapper/blob/master/LICENSE)

A Python wrapper for the Kubernetes [Kustomize](https://kustomize.io/) tool
and related tooling.

- More readable, more concise one-liners
- Easy linting (with integrated `kubeval`)
- Integrates into your Python tooling (e.g. use it with `tox`)
- Automatic download of external Go binaries
- Cross-platform (installs matching Go binaries on Linux, macOS, Windows)

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

### Python tox

Add kustomize-wrapper to your `tox.ini`, then Tox takes care of downloading:
```ini
[testenv:kubernetes]
description = Validate Kubernetes manifests
deps = kustomize-wrapper
commands =
    kustomize lint {posargs:--ignore-missing-schemas --fail-fast \
        deployment/application/overlays/development \
        deployment/application/overlays/integration \
        deployment/application/overlays/production \
    }
```

Allows you to override arguments: (Use `--` in case you add command line options)
```console
tox -e kubernetes -- --fail-fast deployment/application/base
```
