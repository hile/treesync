![Unit Tests](https://github.com/hile/treesync/actions/workflows/unittest.yml/badge.svg)
![Style Checks](https://github.com/hile/treesync/actions/workflows/lint.yml/badge.svg)

# Tree synchronization utility

This utility allows configuring regularly repeated rsync commands and sharing 
of configuration flags per server. Configured `sync targets` can be called 
with `treesync pull` and `treesync push` commands to avoid mistakes in the
long and complex arguments.
