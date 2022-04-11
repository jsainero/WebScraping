# Práctica 1: WebScraping

## Descripción

En esta práctica hemos aplicado técnicas de _web scraping_ para extraer información de una [web](https://genealogy.math.ndsu.nodak.edu/) con datos de diferentes doctores en matemáticas.

## Equipo

- Álvaro López Cabello
- Jorge Sainero Valle

## Ficheros

- **[webscraper.py](https://github.com/jsainero/WebScraping/blob/master/webscraper.py)** contiene el script y las funciones que extraen y generan el fichero con los datos.

- **[Práctica Web scraping.ipynb](https://github.com/jsainero/WebScraping/blob/master/Pr%C3%A1ctica%20Web%20scraping.ipynb)** es un notebook donde empezamos a usar las librerías de _web scraping_.

- **[mathematicias_dataset.json](https://doi.org/10.5281/zenodo.6436865)** es un dataset de ejemplo que contiene los matemáticos cuya tesis fue de estadística y la realizaron en una universidad española.

- **[chromedriver.exe](https://github.com/jsainero/WebScraping/blob/master/chromedriver.exe)** es el archivo necesario para poder usar selenium para navegar por la web. Se puede obtener el archivo para su versión de Google Chrome en esta [web](https://chromedriver.chromium.org/downloads).

## Uso del script

El script recibe dos parámetros como argumentos:

- **country**: Se pasa con el flag `--country` delante y debe ser el nombre de un país en inglés. Sirve para filtrar el país de las universidades que se quieren considerar.

- **subject**: Se pasa con el flag `--subject` delante y debe ser un código de la lista que hay al final del documento. Indica el tema o área al que pertenecen las tesis de la búsqueda.

Los dos argumentos no son necesarios pero al menos uno de ellos sí. Si un argumento está vacío se considerará cualquier posible valor para este. Por ejemplo si se lanza:

```bash
python3 webscraper.py --country spain
```

se cogerá la lista de todos los matemáticos que realizaron la tesis en España.

El script tiene implementado el comando `--help` por lo que si se lanza:

```bash
python3 webscraper.py [--help | -h]
```

se devolverá una ayuda con los valores que pueden obtener los parámetros.

### Lista de asignaturas

| Código | Nombre                                                 |
| ------ | ------------------------------------------------------ |
| 00     | General                                                |
| 01     | History and biography                                  |
| 03     | Mathematical logic and foundations                     |
| 05     | Combinatorics                                          |
| 06     | Order, lattices, ordered algebraic structures          |
| 08     | General algebraic systems                              |
| 11     | Number theory                                          |
| 12     | Field theory and polynomials                           |
| 13     | Commutative rings and algebras                         |
| 14     | Algebraic geometry                                     |
| 15     | Linear and multilinear algebra; matrix theory          |
| 16     | Associative rings and algebras                         |
| 17     | Nonassociative rings and algebras                      |
| 18     | Category theory, homological algebra                   |
| 19     | K-theory                                               |
| 20     | Group theory and generalizations                       |
| 22     | Topological groups, Lie groups                         |
| 26     | Real functions                                         |
| 28     | Measure and integration                                |
| 30     | Functions of a complex variable                        |
| 31     | Potential theory                                       |
| 32     | Several complex variables and analytic spaces          |
| 33     | Special functions                                      |
| 34     | Ordinary differential equations                        |
| 35     | Partial differential equations                         |
| 37     | Dynamical systems and ergodic theory                   |
| 39     | Finite differences and functional equations            |
| 40     | Sequences, series, summability                         |
| 41     | Approximations and expansions                          |
| 42     | Fourier analysis                                       |
| 43     | Abstract harmonic analysis                             |
| 44     | Integral transforms, operational calculus              |
| 45     | Integral equations                                     |
| 46     | Functional analysis                                    |
| 47     | Operator theory                                        |
| 49     | Calculus of variations and optimal control             |
| 51     | Geometry                                               |
| 52     | Convex and discrete geometry                           |
| 53     | Differential geometry                                  |
| 54     | General topology                                       |
| 55     | Algebraic topology                                     |
| 57     | Manifolds and cell complexes                           |
| 58     | Global analysis, analysis on manifolds                 |
| 60     | Probability theory and stochastic processes            |
| 62     | Statistics                                             |
| 65     | Numerical analysis                                     |
| 68     | Computer science                                       |
| 70     | Mechanics of particles and systems                     |
| 74     | Mechanics of deformable solids                         |
| 76     | Fluid mechanics                                        |
| 78     | Optics, electromagnetic theory                         |
| 80     | Classical thermodynamics, heat transfer                |
| 81     | Quantum Theory                                         |
| 82     | Statistical mechanics, structure of matter             |
| 83     | Relativity and gravitational theory                    |
| 85     | Astronomy and astrophysics                             |
| 86     | Geophysics                                             |
| 90     | Operations research, mathematical programming          |
| 91     | Game theory, economics, social and behavioral sciences |
| 92     | Biology and other natural sciences                     |
| 93     | Systems theory; control                                |
| 94     | Information and communication, circuits                |
| 97     | Mathematics education                                  |
