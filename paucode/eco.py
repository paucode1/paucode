import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def VA(i:float, nper:int, pago, vf):
    """Valor actual o valor presente. Se utiliza para actualizar el valor final a una tasa i% en nper periodos de tiempo

    Args:
        i (_type_): Tasa de interes en porcentajes
        nper (_type_): numero de periodos para actualizar
        pago (_type_): pagos periodicos
        vf (_type_): Valor final

    Returns:
        _type_: Valor actual o actualización al momento cero
    """
    return vf/(1+i)**nper

def VF(i:float, nper:int, pago, va):
    """valor actual o capitalización

    Args:
        i (float): tasa de interes
        nper (int): numero de periodos de capitalización
        pago (otro): pagos periodicos
        va (_type_): valor actual

    Returns:
        _type_: Valor final
    """
    return va*(1+i)**nper

# VAN
def VAN(i:float, flujo):
    flujo=flujo
    van=0.0
    for n, fe in enumerate(flujo):
        van += fe/(1+i)**n
    return van

# TIR
def TIR(flujo):
    flujo=flujo
    i=0.00000
    van=1
    while van!=0.00:
        van=0
        for n, fe in enumerate(flujo):
            van += fe/(1+i)**n
        i += 0.001
        van=round(van, ndigits=2)
    return i