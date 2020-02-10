# Topics that usefull in this project

## Html escape chars
Implemented based on **ref1, ref2** (php htmlspecialchars).

## The curse of apos
Should i escape **'** as **&amp;apos;** or **&amp;#39;**? see the **ref03**.

## Build with travis
1. Sign up in [travis-ci][https://travis-ci.com/]
2. Create .travis.yml and fill it based on [documentation][https://docs.travis-ci.com/]
3. Build your repo in travis dashboard

## Deep Copy vs Shallow Copy

- **deep** copy: any changes made to a copy of object **do not reflect** in the original object
- **shallow** copy: any changes made to a copy of object **do reflect** in the original object

## Double-edged sword of pre-commit-hooks
Pre-commit hook is a python package that provides ability to use hooks before commiting codes.
I used this package for define a hook for checking pylint(python linter).
At first, hooks defined in released repo & i just add this lines to the pre-commit-config.yaml:
```yaml
  - repo: https://github.com/PyCQA/pylint
    rev: pylint-2.4.4
    hooks:
      - id: pylint
        args: ["--errors-only","--rcfile=.pylintrc"]
```

The problem has showing up, when i use thrid-party packages such as requests, markdown, etc.
These package are not installed in remote pylint and import-errors raised when committing.
The solution is use pylint in local to integrate with project dependencies and probably virtual environment.
So i changed the pre-commit-config.yaml as below:

```yaml
  - repo: local
    hooks:
      - id: pylint
        name: pylint
        language: system
        types: [python]
        entry: "python -m pylint --rcfile=.pylintrc --errors-only"
```

# Referrences
1. https://owasp.org/www-project-cheat-sheets/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html
2. https://www.php.net/manual/en/function.htmlspecialchars.php
3. https://fishbowl.pastiche.org/2003/07/01/the_curse_of_apos
4. https://travis-ci.com/
5. https://github.com/TheAlgorithms/Python
6. https://www.geeksforgeeks.org/copy-python-deep-copy-shallow-copy/
7. https://security.stackexchange.com/questions/143923/whats-the-difference-between-escaping-filtering-validating-and-sanitizing

[https://travis-ci.com/]: https://travis-ci.com/
[https://docs.travis-ci.com/]: https://docs.travis-ci.com/
