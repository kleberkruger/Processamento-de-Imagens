========================================================================================================================
    INSTRUÇÕES DE USO
------------------------------------------------------------------------------------------------------------------------
O programa deve ser executado da seguinte maneira:

- python main                       # sem argumentos
- python main <input> <output>      # com um ou dois argumentos opcionais, indicando respectivamente,
                                    # o arquivo (ou diretório) de entrada, e o arquivo (ou diretório) de saída

Também é possível executá-lo com os seguintes argumentos opcionais:

--input/--in/-i:

    Caminho para a imagem ou diretório de entrada. Valor padrão: 'in'
    Caso <input> corresponda a um diretório, todas as imagens contidas em sua raiz serão processadas.
    Caso nenhum valor seja explicitamente informado, <input> = in # diretório padrão das imagens de entrada

    Usando-se a flag --input é possível informar um ou várias entradas ao mesmo tempo. Exemplo:
    python main --input baboon.png monalisa.png

--output/--out/-o:

    Caminho para a imagem resultante ou diretório de saída. Valor padrão: 'out'
    Se <input> corresponder a um arquivo de imagem e o valor de <output> não for definido, a imagem será
    salva na mesma pasta de <input> conforme a nomenclatura padrão.

    É importante saber que:

    1) O número de argumentos para a flag --output deve ser igual ao número de argumentos passados para a
    flag --input, ou então um único argumento apontando para um diretório de saída. Exemplos:
    python main --input baboon.png monalisa.png --output baboon-out.png monalisa-out.png
    python main --input baboon.png monalisa.png --output output_dir

    2) Se <input> estiver associado a um diretório, <output> também será interpretado como tal.
    Nestes casos, se o valor de <output> não for explicitamente informado, este assumirá:
    <output> = <input>, caso <input> tenha sido explicitamente informado;
    <output> = out, caso <input> não tenha sido informado.

    Portanto, se <input> e <output> não forem explicitamente informados, seus valores padrão são:
    <input>     = in        # diretório padrão das imagens de entrada
    <output>    = out       # diretório padrão das imagens de saída

    A nomenclatura padrão para os arquivos de saída são: <nome-original>-out-<mask>-<direction>.
    Exemplo: "baboon-out-1-1.png".

--mask/-m:

    Máscara usada no processamento. Valor padrão: 0 (all).
    As formas de distribuição de erro em diferentes técnicas de meios-tons com difusão de erro são:
        1 - Floyd e Steinberg
        2 - Stevenson e Arce
        3 - Burkes
        4 - Sierra
        5 - Stucki
        6 - Jarvis, Judice e Ninke
        0 - Todas as opções

--direction/-d:

    Direção do processamento. Valor padrão: 0 (all).
    As formas de varredura da imagem são:
        1 - Esquerda para direita
        2 - Direção alternada
        0 - Todas as opções

--color:

    Imagem colorida ou monocromática. Valor padrão: (colorida).
    As opções são:
        0 - Monocromática
        1 - Colorida
        2 - Todas as opções

------------------------------------------------------------------------------------------------------------------------
    Exemplos de Uso:
------------------------------------------------------------------------------------------------------------------------
python main.py                                  # execução com os valores padrão
python main.py baboon.png                       # imagem de entrada
python main.py in                               # diretório de entrada
python main.py in out                           # diretório de entrada e diretório de saída
python main.py in/baboon.png out/baboon.png     # imagem de entrada e imagem de saída

python main.py -i in -o out -m 0 -d 0           # execução padrão
========================================================================================================================

# com estas 11 operações, de 1250 foi para 1350
