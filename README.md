# PacELF Digital Library

[![license][license-image]][license-url]
[![Build Status][travis-image]][travis-url]

A static site for storing and searching the [PacELF project's](http://www.wpro.who.int/southpacific/pacelf/en/) digital library of documents.

Currently built using [Jekyll](https://github.com/jekyll/jekyll) via the [JKAN](https://github.com/timwis/jkan) project.

TODO 

Deployed and served by [Netlify](https://pacelf.netlify.com/) from eResearch's GitHub repository()

## Prerequisites

To install this project, you'll need the following things installed on your machine.

1. [Jekyll](http://jekyllrb.com/).
2. [NodeJS](http://nodejs.org) - use the installer.

## Local Installation

1. Clone this repo, or download it into a directory of your choice.
2. Inside the directory, run `npm install`.
3. Inside the directory, run `bundle install`.

## Usage

### Developing

#### Jekyll

To serve the site locally or while developing the Jekyll datasets, layouts or includes;

```shell
bundle exec jekyll serve --watch --incremental
```

This will list a localhost development server.

To remove existing content in `_site`, which is where Jekyll builds to and serves from, run:

```shell
bundle exec jekyll clean
```

To rebuild the content of `_site` run:

```shell
bundle exec jekyll build
```

See the [Jekyll docs](https://jekyllrb.com/docs/usage/) for more options.

#### Javascript

If developing the Javascript within `scripts/`:

Re-compile the files using the provided `webpack.config.js` configuration using:

```shell
npm run build
```

View `package.json` for more commands and details.

#### Deploy via GitHub and Netlify

The site is be deployed to Netlify.com when pushed to the GitHub repository via:

```shell
git push
```

## Tests

To locally run the tests on the HTML produced, first install the testing dependencies.

```shell
gem install html-proofer
```

And then run the tests:

```shell
htmlproofer ./_site
```

## Further Documentation

## Maintainers

## Errata

[license-image]: https://img.shields.io/badge/license-MIT-green.svg
[license-url]: https://github.com/jcu-eresearch/pacelf-digital-library/blob/master/LICENSE
[travis-image]: https://travis-ci.org/stevevandervalk/jkan.svg?branch=netlify
[travis-url]: https://travis-ci.org/stevevandervalk/jkan
