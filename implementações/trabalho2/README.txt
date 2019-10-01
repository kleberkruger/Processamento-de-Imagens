Formas de execução:

# modo padrão: executa com -i in -o out -t *
python3 threshold.py

# lê image.png e salva na mesma pasta com o nome padrão
python3 threshold.py -i image.png

# lê image.png e salva na mesma pasta com o nome padrão
python3 threshold.py -i image.png -o out

# lê image.png e salva na mesma pasta com o nome padrão
python3 threshold.py -i image.png -o out/image.png

# lê i1.png e i2.png e salva na mesma pasta com o nome padrão
python3 threshold.py -i i1.png i2.png

# lê i1.png e i2.png e salva na pasta out
python3 threshold.py -i i1.png i2.png -o out

*** Parâmetros: ***
<input>
1) A quantidade de valores para o parâmetro <input> é de 0 (não informado) até n
2) Os valores de cada <input> é o caminho para uma imagem ou um diretório
3) Caso o valor de um <input> seja um diretório, apenas as imagens na sua raiz serão processadas
4) Caso não informe nenhum valor, <input> será definido com 'in' (diretório de entrada padrão)

<output>
5) A quantidade de valores para o parâmetro <output> é 0 (não informado), 1 ou n (mesma quantidade de <input>).
6) Os valores de cada <output> é o caminho para um diretório de saída ou o nome de um arquivo resultante
    6.1) Observação: Se o processamento de uma imagem de entrada é feito de k maneiras (aplicação de filtros,
    algoritmos, etc), cada imagem de entrada resultará em k imagens de saída, e o nome do arquivo seguirá a
    nomenclatura padrão conforme o nome de saída especificado.
    6.2) Se nenhum nome foi especificado para o arquivo de saída, este seguirá a nomenclatura padrão conforme o nome
    original da imagem
7)  Um <output> associado a um <input> diretório, também é interpretado como um diretório, pois o resultado do
    processamento pode resultar em múltiplas imagens
8) Quando <output> não for informado pelo usuário:
    8.1) Se <input> também não foi: input = in, output = out
    8.2) Caso o <input> tenha sido definido pelo usuário:
        8.2.1) Se <input> for o caminho para uma única imagem, o valor de <output> seguirá a nomenclatura padrão, e a
        imagem de saída será salva no mesmo diretório da imagem de entrada
        8.2.2) Se <input> for o caminho para um único diretório, <output> receberá o mesmo valor de <input>, e as
        imagens serão salvas conforme a nomenclatura padrão
        8.2.3) Se <input> for um conjunto de valores (imagens e/ou diretórios), cada valor de <input> respeitará as
        regras 8.2.1 e 8.2.2
9) Se a lista de <input> > 1:
    9.1) <output> poderá estar vazio (não informado). Cada input seguirá a regra 8.2
    9.2) <output> poderá ter uma única entrada (obrigatoriamente um diretório de saída)
    - Observação importante: arquivos com mesmo nome resultante serão sobrescritos
    9.3) <output> poderá ter n entradas (em que ambas as listas têm o mesmo tamanho, pois os valores de <input><output>
    serão atribuídos na mesma ordem; cada elemento da lista deve respeitar a regra padrão
10) Caso apenas <output> tenha sido definido, <input> recebeu o valor padrão "in". Portanto, o valor de <output> precisa
ser o caminho para um único diretório de saída

<types>
11) <types> define os tipos (extensões) de arquivos que serão incluídos na lista de imagens de entrada
12) Se nenhum valor é informado pelo usuário, types = '*' (todos os tipos de imagens)

