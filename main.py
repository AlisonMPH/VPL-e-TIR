import os

clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')


def menu():
    clear()
    print('\n')
    print('\n' + '-' * 35 + '\n')
    print(' 1 - Valor Futuro')
    print(' 2 - Valor Presente')
    print(' 3 - VPL')
    print(' 4 - Payback')
    print(' 5 - TIR')
    print(' 0 - Sair')
    print('\n' + '-' * 35 + '\n')
    print(' ...: ', end='')
    option = int(input())

    return option


def numberPeriods():
    quantity = 0

    while quantity <= 0:
        clear()
        print('\nPeríodos')
        print('\n' + '-' * 35 + '\n')
        print(' ...: ', end='')
        quantity = int(input())

    return quantity


def rate(nameRate):
    value = -1

    while value < 0:
        clear()
        print(f'\n Insira a {nameRate}')
        print('\n' + '-' * 35 + '\n')
        print(' ...: ', end='')
        value = float(input())

    return value


def insert_FV_PV(nameValue):
    value = -1

    while value < 0:
        clear()
        print(f'\n Insira o valor {nameValue}\n')
        print('\n' + '-' * 35 + '\n')
        print(' ...: ', end='')
        value = float(input())

    return value


def basicFormula(value, rate, currentPeriod, optionFormula):
    if (optionFormula):
        finalValue = value * ((1 + rate)**currentPeriod)
        return finalValue
    else:
        finalValue = value / ((1 + rate)**currentPeriod)
        return finalValue


def calculate_FV_PV(optionValue):
    periods = numberPeriods()
    specificRate = rate('taxa de juros composta')

    if optionValue:
        cash = insert_FV_PV('presente')
        finalvalue = basicFormula(cash, specificRate, periods, 1)
    else:
        cash = insert_FV_PV('futuro')
        finalvalue = basicFormula(cash, specificRate, periods, 0)

    return finalvalue


#def printResult(result, nameResult):
#    exit = 1
#    while exit != 0:
#        clear()
#        print('\n' + '-' * 45 + '\n')
#        print(f' {nameResult} é {result:.2f}')
#        print('\n' + '-' * 45 + '\n')
#        print(' Sair(0)\n...: ', end='')
#        exit = int(input())


def printResult(result, nameResult):
    exit = 1
    while exit != 0:
        clear()
        print('\n' + '-' * 45 + '\n')
        if isinstance(result, float):
            print(f' {nameResult} é {result:.2f}')
        else:
            print(f' {nameResult} é {result}')
        print('\n' + '-' * 45 + '\n')
        print(' Sair(0)\n...: ', end='')
        exit = int(input())


def initialInvestment():
    investment = -1
    while investment < 0:
        clear()
        print(f'\n Investimento inicial')
        print('\n' + '-' * 35 + '\n')
        print(' ...: ', end='')
        investment = float(input())

    return investment


def cashFlow(period):
    clear()
    print(f'\n {period}º Fluxo de caixa')
    print('\n' + '-' * 35 + '\n')
    print(' ...: ', end='')
    cash = float(input())

    return cash


def netPresentValue():
    finalValue = 0
    periods = numberPeriods()
    specificRate = rate('taxa de retorno mínima aceitável')
    investment = initialInvestment()

    for count in range(0, (periods + 1)):
        if count == 0:
            finalValue -= investment
        else:
            oldCash = cashFlow(count)
            atualCash = basicFormula(oldCash, specificRate, count, 0)
            finalValue += atualCash

    return finalValue


def insertPayback():
    atualCashList = list()
    periods = numberPeriods()
    specificRate = rate('taxa interna de retorno')
    investment = initialInvestment()

    for count in range(0, (periods + 1)):
        if count == 0:
            atualCashList.append(investment)
        else:
            oldCash = cashFlow(count)
            atualCash = basicFormula(oldCash, specificRate, count, 0)
            atualCashList.append(atualCash)

    return atualCashList


def payback():
    finalValue = 0
    atualCashList = insertPayback()
    for period in range(0, len(atualCashList)):
        if atualCashList[len(atualCashList) - 1] < 0:
            payBack = 'Valor Negativo'
            return payBack
        if period == 0:
            finalValue -= atualCashList[period]
        else:
            finalValue += atualCashList[period]
            if finalValue < 0:
                minimumPeriod = period
                lastNegative = finalValue
                nextNPV = atualCashList[period + 1]
    payBack = minimumPeriod + ((-1 * lastNegative) / nextNPV)
    return payBack


def payback2():
    finalValue = 0
    atualCashList = insertPayback()
    minimumPeriod = None  # inicializa minimumPeriod com None
    for period in range(0, len(atualCashList)):
        if atualCashList[len(atualCashList) - 1] < 0:
            payBack = 'Valor Negativo'
            return payBack
        if period == 0:
            finalValue -= atualCashList[period]
        else:
            finalValue += atualCashList[period]
            if finalValue < 0:
                minimumPeriod = period
                lastNegative = finalValue
                if period + 1 < len(
                        atualCashList
                ):  # adiciona verificação se nextNPV existe
                    nextNPV = atualCashList[period + 1]
    if minimumPeriod is None:  # verifica se minimumPeriod foi atribuída um valor
        payBack = 'Sem Pagamento'
    else:
        payBack = minimumPeriod + ((-1 * lastNegative) / nextNPV)
    return payBack


def IRR():
    count = 1
    finalValue = 1
    specificRate = 0
    oldCashList = list()
    periods = numberPeriods()
    investment = initialInvestment()

    for count in range(0, (periods + 1)):
        if count == 0:
            oldCashList.append(investment)
        else:
            oldCash = cashFlow(count)
            oldCashList.append(oldCash)

    while finalValue > 0:
        if count:
            finalValue = 0
        count += 1
        specificRate += 0.0001
        for period in range(0, (periods + 1)):
            if period == 0:
                finalValue -= investment
            else:
                atualCash = basicFormula(oldCashList[period], specificRate,
                                         period, 0)
                finalValue += atualCash

    return specificRate * 100


if __name__ == '__main__':
    option = 1
    while option != 0:
        option = menu()
        if option == 0:
            pass

        elif option == 1:
            printResult(calculate_FV_PV(1), "Valor Futuro")

        elif option == 2:
            printResult(calculate_FV_PV(0), "Valor Presente")

        elif option == 3:
            printResult(netPresentValue(), "Valor Presente Líquido")

        elif option == 4:
            printResult(payback2(), "PAYBACK")

        elif option == 5:
            printResult(IRR(), "Taxa Inerna de Retorno")
            pass
        else:
            pass
