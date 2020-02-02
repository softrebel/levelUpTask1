# Sanitize HTML/MARKDOWN & send it to an endpoints

[![Build Status](https://travis-ci.com/softrebel/levelUpTask1.svg?branch=master)](https://travis-ci.com/softrebel/levelUpTask1.svg?branch=master)
![GitHub commit activity](https://img.shields.io/github/commit-activity/w/softrebel/levelUpTask1)
![GitHub last commit](https://img.shields.io/github/last-commit/softrebel/levelUpTask1)

This is sample app to send html entities over http protocol to an endpoint.

## Dependencies
- markdown
- requests
- pylint
- mypy

## Example
- Just run: `python ./src/cli.py "<script>alert('Hi amber heard & Johnny depp')</script>"`
- Also you can pass the param after run:
```
> python ./src/cli.py

Please Enter Your HTML/Markdown Body:
 <script>alert('Hi amber heard & Johnny depp')</script>
{
'status': 'success',
'sanitized': 'alert(&#39;Hi amber heard & Johnny depp&#39;)'
}

```
