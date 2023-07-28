import numpy as np
from decimal import Decimal

##### Funciones del modulo ing #################################
__all__ = ['vf', 'pago', 'nper', 'ipmt', 'ppmt', 'vp', 'tasa',
           'tir', 'van', 'tirm']

_when_to_num = {'end': 0, 'begin': 1,
                'e': 0, 'b': 1,
                0: 0, 1: 1,
                'beginning': 1,
                'start': 1,
                'finish': 0}


def _convert_when(when):
    # Test to see if when has already been converted to ndarray
    # This will happen if one function calls another, for example ppmt
    if isinstance(when, np.ndarray):
        return when
    try:
        return _when_to_num[when]
    except (KeyError, TypeError):
        return [_when_to_num[x] for x in when]


##### Funciones del modulo ing #################################
##### Calculo del valor futuro #################################
def vf(tasa, nper, vp, pago=0, when='end'): 
    """calcula el valor futuro

    Args:
        tasa (float): tasa
        nper (int): numero de periodos
        vp (float): Valor presente: (-)  
        pago (float, optional): pagos constantes por cada periodo. Defaults to 0
        when (str, optional): valor opcional.

    Returns:
        float: vf
    """
    when = _convert_when(when)
    (tasa, nper, vp, pago, when) = map(np.asarray, [tasa, nper, vp, pago, when])
    temp = (1+tasa)**nper
    fact = np.where(tasa == 0, nper,
                    (1 + tasa*when)*(temp - 1)/tasa)
    return -(vp*temp + pago*fact)


def vp(tasa, nper,  vf=0, pago=0, when='end'):
    """calcula el valor presente

    Args:
        tasa (float): tasa de descuento
        nper (int): numero de periodos
        vf (float, optional): valor futuro. Defaults to 0.
        pago (float, optional): pagos constantes por cada periodo. Defaults to 0.
        when (str, optional): valor opcional. Defaults to 'end'.

    Returns:
        float: vp
    """
    when = _convert_when(when)
    (tasa, nper, pago, fv, when) = map(np.asarray, [tasa, nper, pago, vf, when])
    temp = (1+tasa)**nper
    fact = np.where(tasa == 0, nper, (1+tasa*when)*(temp-1)/tasa)
    return -(fv + pago*fact)/temp


## Calcula la tasa interna de retorno #################################
def tir(flujo):
    """calcula la tasa interna de retorno 

    Args:
        flujo (list): Flujo de efectivo. flujo[0]=(-)

    Returns:
        float: tir
    """
    res = np.roots(flujo[::-1])
    mask = (res.imag == 0) & (res.real > 0)
    if not mask.any():
        return np.nan
    res = res[mask].real
    # NPV(rate) = 0 can have more than one solution so we return
    # only the solution closest to zero.
    tasa = 1/res - 1
    tasa = tasa.item(np.argmin(np.abs(tasa)))
    return tasa


## Valor actual neto #################################
def van(tasa, flujo):
    """calcula el valor actual neto

    Args:
        tasa (float): tasa de descuento
        flujo (list): Flujo de efectivo. flujo[0]=(-)

    Returns:
        float: van
    """
    flujo = np.asarray(flujo)
    return (flujo / (1+tasa)**np.arange(0, len(flujo))).sum(axis=0)




##### clases del modulo ing #################################
class FNE():
    # propiedades o atributos
    def __init__(self, flujo) -> None:
        self.__tasa=None
        self.__n=None
        self.__t=None
        self.__tir=None
        self.__flujo=flujo
    
    ##################################################################### metodos #####################################################################
    # Valor actual neto del flujo de efectivo
    def VAN(self, i) -> float:
        self.__tasa=i
        vp=[f*(1/(1+i)**n) for n, f in enumerate(self.__flujo)]
        return sum(vp)
    
    
    # Tasa interes de retorno del flujo de efectivo
    def TIR(self):
        i=0.000
        van=1
        while van!=0.00:
            van=0
            for n, fe in enumerate(self.__flujo):
                van += fe/(1+i)**n
            i += 0.0001
            van=round(van, ndigits=4)
        self.__tir=round(i, ndigits=4)
        return round(i, ndigits=4)
    
    
    def VP(self, i, nper):
        
        vp=sum(self.__flujo)*1/(1+i)**nper
        return vp
    
    
    def VF(self, i, nper):
        vf=sum(self.__flujo)*(1+i)**nper
        return vf
    
    @property
    def tasa(self):
        return f"{self.__tasa*100}%"
    
    @property
    def flujo(self):
        return self.__flujo
    
    @property
    def tir(self):
        return f"{self.__tir*100}%"
    


    

