# -*- coding: utf-8 -*-


def decimal_a_binario(decimal):
    binario = ''
    dividendo = decimal

    while dividendo > 0:
        residuo = dividendo%2
        binario = str(residuo) + binario
        dividendo = dividendo / 2

    return binario


def decimal_a_basex(decimal, base):
    if base<2 or base > 36:
        return decimal

    letras = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    conversion = ''
    dividendo = decimal

    while dividendo > 0:
        residuo = dividendo%base

        representacion = residuo

        if representacion > 9:
            representacion = letras[representacion - 10]

        conversion = str(representacion) + conversion

        dividendo = dividendo / base

    return conversion


def basex_a_decimal(valor, base):
    if base<2 or base > 36:
        return valor

    letras = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    valor_str = str(valor)
    # Eliminar posibles espacios en los extremos
    valor_str = valor_str.strip()

    resultado = 0
    exponente = len(valor_str) - 1

    for letra in valor_str:
        letra_valor_decimal = letra

        if letra in letras:
            letra_index = letras.index(letra)
            letra_valor_decimal = 10 + letra_index

        letra_valor_decimal = int(letra_valor_decimal)

        valor_letra = letra_valor_decimal * (base ** exponente)

        resultado += valor_letra

        exponente -= 1

    return resultado


def obtener_valor_de_flag(comando, nombre_flag, esPath = False):
    # Si el flag no esta presente en el comando, devolver nulo.
    if nombre_flag not in comando:
        return None

    # Si esta, obtener su valor
    index = comando.index(nombre_flag) + len(nombre_flag)

    # Podrian haber varios espacios entre el nombre del fla y su valor.
    while comando[index] == ' ':
        index += 1

    # El caracter final deberia ser un espacio.
    char_final = ' '

    # Si el char inicial es una comilla doble, entonces es un path y deberia terminar con comilla doble.
    if (esPath and comando[index] == '"'):
        char_final = '"'
        # Saltarse la comilla doble.
        index += 1

    # Obtener caracteres que conforman el valor del flag.
    valor_flag = ''
    max_index = len(comando)
    while ((index < max_index) and (comando[index] != char_final)):
        valor_flag += comando[index]
        index += 1

    return valor_flag.strip()



def parse_input(comando):
    # Eliminar posibles espacios en los extremos.
    comando = comando.strip()

    # Si es el comando de salida, retornar.
    if comando == 'quit':
        return None

    error_msg = 'ERROR! Expresion no valida'

    # Validar que no hayan caracteres raros en el input.
    for char in comando:
        char_ascii = ord(char)

        es_mayuscula = ((char_ascii > 64) and (char_ascii < 91))
        es_minuscula = ((char_ascii > 96) and (char_ascii < 123))
        es_numero = ((char_ascii > 47) and (char_ascii < 58))

        caracteres_especiales = {
            '32': 'espacio',
            '34': 'comilla',
            '45': 'guion_medio',
            '46': 'punto',
            '47': 'slash',
            '92': 'backslash',
            '95': 'guion_bajo'
        }

        es_caracter_especial = (str(char_ascii) in caracteres_especiales)

        if ((not es_mayuscula) and (not es_minuscula) and (not es_numero) and (not es_caracter_especial)):
            print error_msg + ' (Hay un caracter invalido)'
            return None

    # Dividir el input por espacios y eliminar nulos.
    comando_partes = filter(lambda c: c.strip(), comando.split(' '))

    if (len(comando_partes) == 0):
        print error_msg
        return None

    # La primera palabra deberia ser el nombre del comando.
    if comando_partes[0] != 'convert':
        print error_msg + ' (La primera palabra debe ser convert)'
        return None

    # Deberia haber algo mas despues del nombre del comando.
    if ((len(comando_partes) == 1) or (not comando_partes[1])):
        print error_msg + ' (No se paso ningun parametro)'
        return None

    resultado = {}
    valor_a_convertir = None
    palabra_actual = ''
    flag = False
    comillas = False
    nombre_flag = None
    index = 6

    # Recorrer caracter por caracter para obtener el valor de los flags y el valor a convertir.
    # Se salta los primeros 7 caracteres que corresponden a la palabra 'convert'.
    for char in comando[7:]:
        # print 'Char: ' + char
        index += 1

        # Si estoy leyendo el valor de un path, solo acumular hasta que encuentre la comilla de cierre.
        if (comillas and (char != '"')):
            palabra_actual += char

            # Si se llego al final del input y no se encontro la comilla de cierre
            if (index == len(comando) - 1):
                if nombre_flag:
                    resultado[nombre_flag] = palabra_actual or None

            continue

        if (char == '"'):
            # Inicio de un path
            if (not comillas):
                # print 'Inicio de path'
                comillas = True
                continue
            # Fin de un path
            else:
                # print 'Fin de path'
                comillas = False
                # Si ya habia un flag, la palabra acumulada es el valor de dicho flag.
                if nombre_flag:
                    resultado[nombre_flag] = palabra_actual or None
                    nombre_flag = None
                    palabra_actual = ''

                continue

        # Inicio del nombre de un flag.
        if ((not flag) and (char == '-')):
            # print 'Inicio flag'
            flag = True

            # Si ya habia un flag, la palabra acumulada es el valor de dicho flag.
            if nombre_flag:
                resultado[nombre_flag] = palabra_actual or None
                nombre_flag = None

        # Fin del nombre de un flag.
        if (flag and (char == ' ')):
            # print 'Fin flag'
            flag = False
            nombre_flag = palabra_actual
            palabra_actual = ''

        palabra_actual += char
        palabra_actual = palabra_actual.strip()
        # print 'Palabra actual: ' + palabra_actual

        # Si ya hay una palabra acumulada y se encuentra un espacio, significa que es el fin de un valor.
        if (palabra_actual and (char == ' ')):
            # print 'Fin de valor'
            # Si ya habia un flag, la palabra acumulada es el valor de dicho flag.
            if nombre_flag:
                resultado[nombre_flag] = palabra_actual
                nombre_flag = None
                palabra_actual = ''
            else:
                print error_msg + ' (Parametros invalidos)'
                return None

        # Si ya llegue al ultimo caracter del input...
        if (index == len(comando) - 1):
            # print 'Fin de cadena'
            if flag:
                nombre_flag = palabra_actual or None
                palabra_actual = ''

            # Si ya habia un flag, la palabra acumulada es el valor de dicho flag.
            if nombre_flag:
                # print 'Hay un flag: ' + nombre_flag
                resultado[nombre_flag] = palabra_actual or None
            else:
                valor_a_convertir = palabra_actual or None
                # print 'Valor a convertir: ' + valor_a_convertir

    # Despues de recorrer letrar por letra...

    # print resultado
    # print valor_a_convertir

    flags_validos = ['-baseIn', '-baseOut', '-file', '-outFile', '-help']

    # Si el flag de ayuda viene en el comando...
    if ('-help' in resultado):
        # No puede especificar otro flag.
        if (len(resultado) > 1):
            print error_msg + ' (Combinacion invalida de flags)'
            return None

        return resultado

    # Todos los flags especificados deben tener un valor.
    for flag in resultado:
        if (flag not in flags_validos):
            print error_msg + ' (Flag ' + flag + ' no soportado)'
            return None

        if ((flag != '-help') and (not resultado[flag])):
            print error_msg + ' (Especifico un flag sin valor)'
            return None

    # Si el comando especifica un archivo, entonces no hay un valor para convertir.
    if (('-file' in resultado) and valor_a_convertir):
        print error_msg + ' (No puede especificar un valor para convertir porque especifico un archivo)'
        return None

    # Si se especifica -outFile pero no se especifica -file, hay error.
    if (('-outFile' in resultado) and (('-file' not in resultado) or (not resultado['-file']))):
        print error_msg + ' (Si especifica -outFile debe especificar tambien -file)'
        return None

    if (('-file' not in resultado) and (not valor_a_convertir)):
        print error_msg + ' (Debe especificar un valor para convertir)'
        return None

    # Validar el valor de -baseIn.
    if (('-baseIn' in resultado) and (resultado['-baseIn'])):
        for char in resultado['-baseIn']:
            char_ascii = ord(char)
            es_numero = ((char_ascii > 47) and (char_ascii < 58))

            if (not es_numero):
                print error_msg + ' (Valor invalido para -baseIn)'
                return None

        resultado['-baseIn'] = int(resultado['-baseIn'])

        if ((resultado['-baseIn'] < 2) or (resultado['-baseIn'] > 36)):
            print error_msg + ' (Valor invalido para -baseIn)'
            return None

    # Validar el valor de -baseIn.
    if (('-baseOut' in resultado) and resultado['-baseOut']):
        for char in resultado['-baseOut']:
            char_ascii = ord(char)
            es_numero = ((char_ascii > 47) and (char_ascii < 58))

            if (not es_numero):
                print error_msg + ' (Valor invalido para -baseOut)'
                return None

        resultado['-baseOut'] = int(resultado['-baseOut'])

        if ((resultado['-baseOut'] < 2) or (resultado['-baseOut'] > 36)):
            print error_msg + ' (Valor invalido para -baseOut)'
            return None

    # Validar el valor a convertir
    if (valor_a_convertir):
        for char in valor_a_convertir:
            char_ascii = ord(char)
            es_mayuscula = ((char_ascii > 64) and (char_ascii < 91))
            es_numero = ((char_ascii > 47) and (char_ascii < 58))

            if ((not es_mayuscula) and (not es_numero)):
                print error_msg + ' (Valor invalido para convertir)'
                return None

            if (('-baseIn' in resultado) and (resultado['-baseIn'] < 10)):
                if ((not es_numero) or (int(char) > resultado['-baseIn'] - 1)):
                    print error_msg + ' (El valor a convertir posee caracteres no validos para -baseIn ' +  str(resultado['-baseIn']) + ')'
                    return None

            # Si no se especifica -baseIn significa que el valor es decimal
            if ('-baseIn' not in resultado):
                if (not es_numero):
                    print error_msg + ' (El valor a convertir posee caracteres no validos para -baseIn 10)'
                    return None

    resultado['valor_a_convertir'] = valor_a_convertir
    # print 'Resultado final:'
    # print resultado

    return resultado


def imprimir_ayuda():
    print 'Uso: convert [-flag <parametro>] [<input>]'
    print 'Lista de banderas:'
    print '    -baseIn <base de entrada> Indica en qué base está el texto o archivo de entrada. Una base válida esta en el rango de 2 a 36. Si no se coloca esta bandera en el comando entonces se asume que la base de entrada es base decimal.'
    print '    -baseOut <base de salida> Indica a qué base se convertirá el texto o archivo de salida. Una base válida esta en el rango de 2 a 36. Si no se coloca esta bandera en el comando entonces se asume que la base de salida es base decimal.'
    print '    -outFile <file name> Indica que la conversión se guardará en un archivo de salida, cuyo nombre será el ingresado en <file name> y con extensión ".nbc". Esta bandera debe estar presente en el comando si está la bandera -file de lo contrario no debería estar.'
    print '    -file <file name> Indica que se debe convertir un archivo, <file name> será el path para un archivo de texto plano, sin importar la extensión. Se deben convertir todos los números encontrados en el archivo, siguiendo el mismo formato del archivo.'
    print '    -help Muestra un listado y resumen de las banderas disponibles, adicionalmente mostrará 3 ejemplos de cómo usar las banderas y los créditos del proyecto.'


def imprimir_creditos():
    print '<Grupo 8BN>'
    print '\tWuelmer Luis - 20005607'
    print '<Grupo 8BN>'


def main():
    imprimir_creditos()

    while True:
        comando = raw_input('conversor >> ');

        if comando == 'quit':
            break

        parametros = parse_input(comando)

        if (not parametros):
            continue

        if ('-help' in parametros):
            imprimir_ayuda()

            continue

        if (not parametros['valor_a_convertir']):
            continue

        # Si no se especifica la base de entrada, por default es 10.
        if (('-baseIn' not in parametros) or (not parametros['-baseIn'])):
            parametros['-baseIn'] = 10

        # Si no se especifica la base de salida, por default es 10.
        if (('-baseOut' not in parametros) or (not parametros['-baseOut'])):
            parametros['-baseOut'] = 10

        # Inicialmente, el valor convertido es igual al valor ingresado.
        valor_convertido = parametros['valor_a_convertir']

        # Ejemplos de decimal a otra base:
        # binario = decimal_a_basex(2695, 2)
        # octal = decimal_a_basex(2695, 8)
        # hexadecimal = decimal_a_basex(2695, 16)

        # Ejemplos de una base x a decimal:
        # bin_a_decimal = basex_a_decimal('10011010000101111', 2)
        # oct_a_decimal = basex_a_decimal('232057', 8)
        # hex_a_decimal = basex_a_decimal('1342F', 16)

        if (parametros['-baseIn'] != 10):
            valor_convertido = basex_a_decimal(valor_convertido, parametros['-baseIn'])
        else:
            valor_convertido = int(valor_convertido)

        if (parametros['-baseOut'] != 10):
            valor_convertido = decimal_a_basex(valor_convertido, parametros['-baseOut'])

        print 'Valor convertido: ' + str(valor_convertido)


main()
