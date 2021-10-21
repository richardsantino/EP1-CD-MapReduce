# Processamento de Pokemons adversários
### Programa feito para a matéria de Ciência de Dados do 6° Semestre de Ciência da Computação

### Por Caroline Viana e Richard Santino

---

## Descrição
O projeto consiste no processamento do arquivo `pokemonData.csv`, que contém dados de diversos Pokemons. Nesse tratamento, precisamos extrair para cada pokemon uma lista com os 10 pokemons que poderiam o derrotar, baseado em seus tipos e fraquezas.

O tratamento é feito utilizando a mappers e reducers presentes na biblioteca MRJob.

## Conteúdo e execução

O repositório já possui um arquivo txt com as informações já extraidas, podendo ser vistas no `top10.txt`.

Mas caso deseje executar o programa desde o começo, e gerar todos os arquivos do zero, siga as etapas:

O projeto necessita de apenas dois arquivos para sua execução:
- `main.py`: arquivo principal de tratamento;
- `pokemonData.csv`: O arquivo contendo os dados a serem tratados.

A partir do Terminal, execute o tratamento a partir do comando `python main.py pokemonData.csv > top10.txt`.  Ao final da execução, o arquivo `top10.txt` terá sido gerado na pasta em que foi executado.
