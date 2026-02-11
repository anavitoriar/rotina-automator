# Rotina Automator

CLI em Python para **organizar arquivos automaticamente** com foco em segurança, previsibilidade e clareza.

O projeto foi criado para praticar:
- automação de rotinas reais
- organização de código em módulos
- uso de linha de comando (CLI)
- versionamento e evolução por sprints

## Funcionalidades atuais

- Organização de arquivos por extensão  
  (`PDF`, `IMG`, `TXT`, `SEM_EXTENSAO`, etc.)
- Modo **dry-run** (simula as ações sem alterar arquivos)
- Execução real segura
- Geração de relatório em JSON

## Como usar

### Simulação (recomendado primeiro)

Exemplo usando uma pasta real do sistema:

```bash
python -m src.rotina_automator.cli --path ~/Downloads --action organize --dry-run 
```

Exemplo usando a pasta de teste do projeto:

```bash
python -m src.rotina_automator.cli --path ./sandbox_in --action organize --dry-run 
```

Executar de verdade

```bash
python -m src.rotina_automator.cli --path ./sandbox_in --action organize 
```
