# Paper Build

The working manuscript is `main.tex`, formatted with ACM's `acmart`
LaTeX class for double-blind review.

## Target Venue

The best current fit is ACM Collective Intelligence, because its call covers
computational models, democracy, policymaking, incentive mechanisms, voting
design, and collective decision-making. The current review build uses ACM's
single-column template in anonymous review mode:

```tex
\documentclass[manuscript,review,anonymous]{acmart}
\setcopyright{none}
```

The final camera-ready version should restore author metadata, remove
review-only options, restore the public repository URL if permitted, and add the
ACM rights metadata supplied after acceptance.

## Template Source

ACM's author page lists `acmart` version 2.16, dated August 28, 2025. The ACM
portal ZIP blocked direct command-line download during setup, so the local class
files were generated from the maintained CTAN `acmart` package:

- `acmart.cls`
- `ACM-Reference-Format.bst`
- `template/ACM-README`
- `hyperxmp.sty`, vendored because TeX Live Basic cannot install that package
  in user mode

Do not edit the ACM class or override its spacing, margins, or style settings.

If building with a minimal TeX Live Basic install, the missing dependencies can
be installed in user mode with:

```sh
tlmgr init-usertree
tlmgr --usermode install acmart xstring zref preprint comment draftwatermark environ framed libertine ncctools newtx pbalance totpages inconsolata trimspaces ifmtarg fontaxes kastrup
```

## Build

```sh
make paper
```

`make paper` first regenerates the canonical `v21-paper` campaign, then
generates table/figure fragments from `reports/simulation-campaign-v21-paper.csv`
before compiling the PDF. Word-count compliance can be checked with:

```sh
make paper-word-count
```

The generated PDF is written to:

```text
paper/main.pdf
```

The intermediate build directory is ignored by Git. The stable `paper/main.pdf`
artifact is intentionally tracked so the repository contains the current paper
PDF without requiring a local LaTeX build first.
