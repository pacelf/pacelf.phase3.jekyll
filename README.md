# PacELF Digital Library

[![license][license-image]][license-url]

A static site for storing and searching the [PacELF project's](http://www.wpro.who.int/southpacific/pacelf/en/) digital library of documents.

## Prerequisites

To install this project, you'll need the following system-level requirements installed on a macOS platform.

1. [Ruby](https://www.ruby-lang.org/en/documentation/installation/)
2. [NodeJS](http://nodejs.org)

You will require the [Homebrew](https://brew.sh/) package manager. Once you have brew installed, run the following command:

```shell
brew install node
```

To install ruby, run the following:

```shell
rvm install ruby 2.7
gem install bundler
```

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

### Updating datasets

Currently this codebase requires the `.xml`, `.txt` and `.pdf` documents to be provided in the `docs` folder.  
The `xml` documents contain the information about documents curated by the PacELF project, the `.txt` contains information about the availability of the document itself and the `.pdf` is the document referenced.

#### Process to obtain XML documents

A spreadsheet is manintained by the PacELF project and a snapshot of any new/updated entries are received by eResearch via email when made available by the PacELF team. 
Spreadsheet in this repo `/PacELF_Phase3/rawdata/excel/PacELF Phases 1_2_3 13Dec2018.xlsx` is updated with the new and admended entries.
Convert updated spreadsheet to `.xml` documents via Python script `/PacELF_Phase3/scripts/csvColumnToXMLFile.py`.

### Producing markdown document for each XML document

Once the XML documents are in located in `docs/` you can install the Python dependencies in `requirements.txt` or `Pipfile` using your preferred tool.

e.g.

```shell
pip3 install -r requirements.txt
```

or

```shell
Pipenv install
```

Then you can run the script

```shell
python3 convert-xml-to-md.py
```

With luck it will populate the `_datasets/` folder with the original markdown output of each XML document.



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

#### JKAN Links

JKAN is organised in a particular way to suit it's usecase and it is helpful to understand before making changes.  The [architecture and development of it is documented here](https://github.com/timwis/jkan/wiki/Architecture).

### Analytics

Per PacELF project's request, Google Analytics is loaded into the site to count viewers.

It is currently stored under `steve.vandervalk@gmail.com` Google Analytics account.

#### Recurring Reports

As requested, it sends monthly audience overview emails to `steve.vandervalk@gmail.com` which are forwarded to Patricia Graves (patricia.graves@jcu.edu.au) as the PacELF project owner.

## Maintainers

---
[license-image]: https://img.shields.io/badge/license-MIT-green.svg
[license-url]: https://github.com/jcu-eresearch/pacelf-digital-library/blob/master/LICENSE
