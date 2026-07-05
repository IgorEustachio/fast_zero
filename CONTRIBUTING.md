feat: uma nova funcionalidade
fix: correção de bug
chore: mudanças sem impacto direto no comportamento do sistema (infra, tooling, dependências, scripts)
refactor: reorganização de código sem mudar comportamento
test: adição ou ajuste de testes
docs: mudanças na documentação

pre_lint = "typos"               
lint = "ruff check"
pre_format = "ruff check --fix"
format = "ruff format"
run = "fastapi dev fast_zero/app.py"
pre_test = "task lint"
test = "pytest -v"
post_test = "coverage html"