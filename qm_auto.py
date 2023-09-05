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
        if num_variables is None and minterms:
            # Determinar el número de variables necesario en función del mintermo más grande
            max_minterm = max(minterms)
            self.num_variables = math.ceil(math.log2(max_minterm + 1))
        else:
            self.num_variables = num_variables
            
        self.variables = [exprvar(v) for v in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'[:self.num_variables]]
        
    def _to_binary(self, num):
        """Convierte un número a su representación binaria."""
        return format(num, '0' + str(self.num_variables) + 'b')
    
    def simplify(self, minterms):
        """Simplifica los minterms utilizando el método Quine-McCluskey."""
        if not minterms:  # Verifica si la lista está vacía
            return '0'
        
        if set(minterms) == {0}:  # Si el único mintermo es 0
            return str(And(*[Not(var) for var in self.variables]))

        minterms_bin = [self._to_binary(m) for m in minterms]
        
        exprs = []
        for minterm in minterms_bin:
            expr = []
            for i, var in enumerate(self.variables):
                if minterm[i] == '1':
                    expr.append(var)
                else:
                    expr.append(Not(var))
            exprs.append(And(*expr))
        
        simplified_expr = Or(*exprs)
        simplified_exprs = espresso_exprs(simplified_expr)
        
        return ' + '.join(str(expr) for expr in simplified_exprs)


