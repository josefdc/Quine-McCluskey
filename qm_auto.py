from pyeda.inter import espresso_exprs
from pyeda.boolalg.expr import And, Or, Not, exprvar
import math

class QuineMcCluskeyPyEDA:
    
    def __init__(self, num_variables=None, minterms=[]):
        """
        Inicializa la clase con el número de variables de la expresión.
        Si no se especifica num_variables, se determina automáticamente
        en función de los minterms proporcionados.
        """
        # Si no se especifica el número de variables, determina en función de los minterms
        if num_variables is None and minterms:
            # Encuentra el mintermo más grande
            max_minterm = max(minterms)
            # Calcula el número de variables necesarias para representar el mintermo más grande en binario
            self.num_variables = math.ceil(math.log2(max_minterm + 1))
        else:
            self.num_variables = num_variables
        
        # Genera las variables de expresión basadas en las letras del alfabeto (A, B, C, ...)
        # Solo toma tantas variables como sea necesario
        self.variables = [exprvar(v) for v in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'[:self.num_variables]]
        
    def _to_binary(self, num):
        """Convierte un número entero a su representación binaria de longitud fija."""
        # Formatea el número a binario con un número de bits igual al número de variables
        return format(num, '0' + str(self.num_variables) + 'b')
    
    def simplify(self, minterms):
        """Simplifica una lista de minterms utilizando el algoritmo de Quine-McCluskey."""
        
        # Si la lista de minterms está vacía, devuelve "0" (expresión constantemente falsa)
        if not minterms:
            return '0'
        
        # Si el único mintermo es 0, devuelve la conjunción (AND) de la negación de todas las variables
        if set(minterms) == {0}:
            return str(And(*[Not(var) for var in self.variables]))

        # Convierte todos los minterms a su representación binaria
        minterms_bin = [self._to_binary(m) for m in minterms]
        
        # Construye una expresión booleana para cada mintermo binario
        exprs = []
        for minterm in minterms_bin:
            expr = []
            for i, var in enumerate(self.variables):
                # Si el bit es '1', agrega la variable a la expresión
                if minterm[i] == '1':
                    expr.append(var)
                # Si el bit es '0', agrega la negación de la variable a la expresión
                else:
                    expr.append(Not(var))
            # Combina la lista de términos con una conjunción (AND)
            exprs.append(And(*expr))
        
        # Combina todas las expresiones de mintermo con una disyunción (OR)
        simplified_expr = Or(*exprs)
        
        # Usa el algoritmo Espresso para simplificar la expresión
        simplified_exprs = espresso_exprs(simplified_expr)
        
        # Convierte la expresión simplificada a una cadena y la devuelve
        return ' + '.join(str(expr) for expr in simplified_exprs)
