# PacELF Digital Library

[![license][license-image]][license-url]
[![Build Status][travis-image]][travis-url]

A static site for storing and searching the [PacELF project's](http://www.wpro.who.int/southpacific/pacelf/en/) digital library of documents.

## Prerequisites

To install this project, you'll need the following things installed on your machine.

1. [Ruby](https://www.ruby-lang.org/en/documentation/installation/)
2. [NodeJS](http://nodejs.org)

## Local Installation

1. Clone this repo, or download it into a directory of your choice.
2. Inside the project's root directory, run:

```shell
npm install
```

```shell
bundle install
```

## Usage

### Developing

#### Jekyll

To simply serve the site locally and/or to see development changes to the Jekyll datasets, layouts or includes, run;

```shell
bundle exec jekyll serve --watch --incremental
```

This will output a localhost development server.

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

When making changes to the Javascript within `scripts/`:

Re-compile the files using the provided `webpack.config.js` configuration using:

```shell
npm run build
```

View `package.json` for more commands and details.

#### Deployments via GitHub

The site is deployed by GitHub Pages to [https://pacelf.github.io/](https://pacelf.github.io/)

Changes can be made to deployed site by making changes to the [GitHub repository](https://github.com/pacelf/pacelf.github.io) `master` branch via:

```shell
git push
```

## Tests

To locally run the tests on the static site produced, first install the project dependencies above.

Then install the testing dependencies via:

```shell
gem install html-proofer
```

Build the static site via:

```shell
bundle exec jekyll build
```

Run the tests:

```shell
htmlproofer ./_site
```

## Further Documentation

### Architecture

Currently built using [Jekyll](https://github.com/jekyll/jekyll) via the [JKAN](https://github.com/timwis/jkan) project.

TODO: Add JKAN links

## Maintainers

---
[license-image]: https://img.shields.io/badge/license-MIT-green.svg
[license-url]: https://github.com/jcu-eresearch/pacelf-digital-library/blob/master/LICENSE
[travis-image]: https://travis-ci.org/stevevandervalk/jkan.svg?branch=netlify
[travis-url]: https://travis-ci.org/stevevandervalk/jkan
