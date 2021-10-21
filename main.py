from mrjob.job import MRJob
from mrjob.job import MRStep
import random

# https://crivelaro.notion.site/Processamento-de-Pok-mons-Advers-rios-4d5fe07a46fa4532a1898c8e7b350bd4

# python main.py pokemonData.csv
# python main.py pokemonData.csv > top10.txt

fraquezas = ["Normal","Fire","Water","Electric","Grass","Ice","Fighting","Poison","Ground","Flying","Psychic","Bug","Rock","Ghost","Dragon","Dark","Steel","Fairy"]

class PokemonStrategy(MRJob):
  def steps(self):
    return [
      MRStep(mapper=self.mapperAll),
      MRStep(mapper=self.mapperClone, reducer=self.reducer),
      MRStep(mapper=self.mapperFinal)
    ]

  # Mapeando todos os pokemons
  def mapperAll(self, _, linha):
    # linha_filtrada = pokemon filtrado
    linha_filtrada = linha.split(",")

    # nome do pokemon, limpando dados
    pokemon = linha_filtrada[1]
    pokemon = pokemon.replace("\u00e9", "e")
    pokemon = pokemon.replace("\u2642", " MALE")
    pokemon = pokemon.replace("\u2640", " FEMALE")

    # dict por pokemon, (danos, tipos e seu nome)
    pokemon_infos = {} 

    # coloca no dict do pokemon, os danos que são > 1
    i_fraqueza = 0
    for i in range(9, len(linha_filtrada)):
      if "*" in linha_filtrada[i]:
        linha_filtrada[i] = linha_filtrada[i].replace("*","")

        if float(linha_filtrada[i]) > 1.0:
          pokemon_infos[fraquezas[i_fraqueza]] = float(linha_filtrada[i])
          #break

        i_fraqueza += 1 
    
    # se não achar nenhuma fraqueza ou se o pokemon tiver nome invalido, deixa o pokemon inutilizável
    if i_fraqueza == 0 or pokemon == "Type: Null":
      linha_filtrada[0] = None

    # ordena de maior para menor os danos
    pokemon_infos = dict(sorted(pokemon_infos.items(), key=lambda item: item[1], reverse = True))

    # coloca os tipos do pokemon em seu dict 
    pokemon_infos["tipo1"] = linha_filtrada[6]
    pokemon_infos["tipo2"] = linha_filtrada[7]
    pokemon_infos["nome"] = pokemon

    # não executa com pokemons inutilizáveis
    if linha_filtrada[0] is not None:
      yield linha_filtrada[0], pokemon_infos

  # "cria"(clona) 3 tabelas.
  #(tabela1) quando o pokemon ira se defender, passa a sua maior vulnerabilidade como chave, e como (dict)info: nome e (key)"defensor":(value)True

  #(tabela2 e 3) quando o pokemon ira atacar, passa seu tipo1(...criação tabela2...) e tipo2(...criação tabela3...) como chave, e como (dict)info: nome e (key)"defensor":(value)False
  def mapperClone(self, chave, linha):
    #defensor
    #chave -> maior fraqueza
    yield next(iter(linha)), {"nome":linha["nome"],
    "defensor":True}

    #atacante
    #chave -> tipo1 e tipo2
    yield linha["tipo1"], {"nome":linha["nome"],
    "defensor":False}

    if "" != linha["tipo2"]:
      yield linha["tipo2"], {"nome":linha["nome"],
      "defensor":False}

  # apenas junta os valores por chave. Meio q cria um campo de batalha pra cada tipo, que contem defensores e atacantes.
  def reducer(self, chave, valores):
    yield chave, valores

  # para cada pokemon defensor(por tipo), cria um array que contem os top10 atacantes(por tipo) aleatorios.

  # ... se o pokemon tem a maior fraqueza "Rock". No seu top10, ira conter apenas pokemons que seu tipo(1 ou 2) é "Rock" ...
  def mapperFinal(self, chave, valores):
    atacantes = []
    defensores = []
    top10 = []

    for valor in valores:
      if valor["defensor"]:
        defensores.append(valor["nome"])
      else:
        atacantes.append(valor["nome"])

    for pokemon in defensores:
      top10 = random.sample(atacantes,10)

      yield pokemon, top10

if __name__ == '__main__':
    PokemonStrategy.run()