project('gitmagic', [],
  version: '0.6.2',
  license: 'GPLv3',
  meson_version: '>= 0.42.0'
)

gitmagic_name = meson.project_name()
gitmagic_version = meson.project_version()
gitmagic_string = '@0@ @1@'.format(gitmagic_name, gitmagic_version)
gitmagic_bugreport = 'https://github.com/lzutao/gitmagic'

python3 = find_program('python3', required : true)
asciidoc = find_program('asciidoc', required : true)
xmlto = find_program('xmlto', required : true)

## Subdirs ##
subdir('en')
