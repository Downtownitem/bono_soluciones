from fastapi import FastAPI
import sympy as sp
from sympy import cos, factorial, sin
import numpy as np 
from starlette.middleware.cors import CORSMiddleware
from PIL import Image, ImageTk
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas las fuentes. Para producción, especifique los dominios permitidos.
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos HTTP. Puedes restringir a ['GET', 'POST'] etc.
    allow_headers=["*"],  # Permite todos los encabezados. Puedes restringir a ['Content-Type'] etc.
)

class Taylor:
    def __init__(self, f, a, n):
        self.f = f  # Función simbólica a aproximar.
        self.a = a  # Punto alrededor del cual se calcula la serie de Taylor.
        self.n = n  # Orden de la aproximación de Taylor.

    def taylor(self):
        x = sp.Symbol('x')  # Define el símbolo 'x'.
        modelo = 0  # Inicializa el polinomio de Taylor.
        # Calcula el polinomio de Taylor sumando términos hasta el orden 'n'.
        for i in range(self.n + 1):
            modelo += (sp.diff(self.f, x, i).subs(x, self.a) * (x - self.a) ** i) / factorial(i)
        return modelo  # Retorna el polinomio de Taylor.

    def errores(self, x_val):
        x = sp.Symbol('x')  # Define el símbolo 'x'.
        modelo = self.taylor()  # Calcula el polinomio de Taylor.
        valor_teorico = self.f.subs(x, x_val).evalf()  # Calcula el valor teórico de la función en x_val.
        valor_experimental = modelo.subs(x, x_val).evalf()  # Calcula el valor aproximado por el polinomio de Taylor.
        error_absoluto = abs(valor_teorico - valor_experimental)  # Calcula el error absoluto.
        #error_relativo = error_absoluto / abs(valor_teorico)  # Calcula el error relativo.
        error_relativo = abs((valor_teorico - valor_experimental)/ valor_teorico)*100
        return error_absoluto, error_relativo, valor_teorico, valor_experimental  # Retorna los errores y valores.

    def graficar(self, x_val):
        x = sp.symbols('x')  # Define el símbolo 'x'.
        f_lambdified = sp.lambdify(x, self.f, "numpy")  # Convierte la función simbólica a una función numérica con NumPy.
        taylor_lambdified = sp.lambdify(x, self.taylor(), "numpy")  # Convierte el polinomio de Taylor a función numérica.

        x_vals = np.linspace(-5, 5, 100)  # Genera un array de valores x entre -5 y 5.
        y_original = f_lambdified(x_vals)  # Calcula los valores de la función original.
        y_taylor = taylor_lambdified(x_vals)  # Calcula los valores del polinomio de Taylor.

        return {
            "plots": {
                "x_vals": x_vals.tolist(),
                "y_original": y_original.tolist(),
                "y_taylor": y_taylor.tolist(),
            },
            "scatters": {
                "x_val": float(str(x_val)),
                "f_lambdified": float(str(f_lambdified(x_val))),
                "taylor_lambdified": float(str(taylor_lambdified(x_val))),
            }
        }  # Retorna la figura creada.

@app.get("/taylor")
def calcular(f_entry: str, a_entry: float, n_entry: int, x_entry: float):
    try:
        f = sp.sympify(f_entry)
        taylor = Taylor(f, a_entry, n_entry)

        # Calcular errores y valores
        error_abs, error_rel, valor_teorico, valor_experimental = taylor.errores(x_entry)
        fig = taylor.graficar(x_entry)

        data = {
            "error": False,
            "data": {
                "generated_polinomy": str(taylor.taylor()), 
                "teoric_value": float(str(valor_teorico)), 
                "experimental_value": float(str(valor_experimental)), 
                "absolute_error": float(str(error_abs)), 
                "relative_error": float(str(error_rel)),
                "plots": fig
            }
        }

        return data
    except Exception as e:
        return {"error": True}