# Jogos

Godot 4 (MIT) — o motor exporta para **Web (HTML5)**, o que encaixa direto no
GitHub Pages: jogo jogavel por URL, sem servidor.

## Fluxo

1. Projeto Godot fica aqui (`project.godot` e `scenes/`).
2. CI exporta para `public/` com o template de exportacao web.
3. Pages publica em `https://<usuario>.github.io/ai-stack/jogos/`.

## Build no CI (quando o projeto existir)

```yaml
build:game:
  stage: test
  image: barichello/godot-ci:4.3
  script:
    - mkdir -p public/jogos
    - godot --headless --export-release "Web" public/jogos/index.html
  artifacts:
    paths: [public/jogos]
```

Godot no GitHub tem 2 cuidados: o template de exportacao vem na imagem
`godot-ci`, e o projeto precisa do `.godot/` no gitignore.
