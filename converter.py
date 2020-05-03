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


def parse_input(comando):
    # Eliminar posibles espacios en los extremos
    comando = comando.strip()

    # Identificar partes
    comando_partes = comando.split(' ')

    if comando_partes[0] == 'quit':
        return comando

    if comando_partes[0] != 'convert':
        print 'ERROR! Expresion no valida'
        return None

    if len(comando_partes) == 1:
        print 'ERROR! Expresion no valida'
        return None

    return comando_partes


def main():
    while True:
        comando = raw_input('conversor >> ');

        if comando == 'quit':
            break

        comando_partes = parse_input(comando)

        if (comando_partes == None):
            continue

        binario = decimal_a_basex(int(comando_partes[1]), 2)
        octal = decimal_a_basex(int(comando_partes[1]), 8)
        hexadecimal = decimal_a_basex(int(comando_partes[1]), 16)

        print 'Binario: %s' % binario
        print 'Octal: %s' % octal
        print 'Hexadecimal: %s' % hexadecimal

        print '------------------------------'

        # Convertir de binario, octal y hexadecimal a decimal (78895)
        bin_a_decimal = basex_a_decimal('10011010000101111', 2)
        oct_a_decimal = basex_a_decimal('232057', 8)
        hex_a_decimal = basex_a_decimal('1342F', 16)

        print 'Binario a decimal: %s' % str(bin_a_decimal)
        print 'Octal a decimal: %s' % str(oct_a_decimal)
        print 'Hexadecimal a decimal: %s' % str(hex_a_decimal)

main()