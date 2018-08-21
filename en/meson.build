txtfiles_sources = [
  'preface.txt',
  'intro.txt',
  'basic.txt',
  'clone.txt',
  'branch.txt',
  'history.txt',
  'multiplayer.txt',
  'grandmaster.txt',
  'secrets.txt',
  'drawbacks.txt',
  'translate.txt',
]

if asciidoc.found()
  compile_file = files('meson_compile_book.py')
  book_en_html = custom_target(
    'book-en.html',
    build_by_default: true,
    input : txtfiles_sources,
    output : 'book-en.html',
    command : [python3, compile_file, '--lang=en', '@INPUT@'],
    install: false
  )
endif
