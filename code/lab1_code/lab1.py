from typing import Optional, Set
import sys
import math


class Coefs:
    Coef = Optional[float]
    _a: Coef
    _b: Coef
    _c: Coef

    def __init__(
            self,
            a: Coef = None,
            b: Coef = None,
            c: Coef = None
    ):
        self.values = {
            "A": a,
            "B": b,
            "C": c
        }
        self.variables_order = ["A", "B", "C"]

    def __setitem__(self, key: str, value: Optional[float]):
        assert key in self.values
        self.values[key] = value

    def __getitem__(self, key: str):
        assert key in self.values
        return self.values[key]


def get_start_coef_values() -> Coefs:
    coefs = Coefs()
    candidates = sys.argv[1:]

    for coef_name in coefs.variables_order:
        if len(candidates) == 0:
            break
        val = candidates.pop(0)
        if validate_coef(val):
            coefs[coef_name] = float(val)
    return coefs


def validate_coef(coef_raw: str) -> bool:
    try:
        float(coef_raw)
        return True
    except ValueError:
        return False


def get_coef_from_stdin(coef_name: str) -> float:
    print(f"Ввод коэффициента {coef_name}")
    while True:
        raw_val = input()
        if validate_coef(raw_val):
            return float(raw_val)
        else:
            print("Неверное значение - коэффициент должен быть целым числом или десятичной дробью")


def get_biquadratic_equation_roots(coefs: Coefs) -> Set[float]:
    quadr_roots = get_quadratic_equation_roots(coefs)

    biquadratic_roots = set()

    for root in quadr_roots:
        if root > 0:
            biquadratic_roots.update(
                {
                    root ** 0.5,
                    -1 * root ** 0.5
                }
            )
    return biquadratic_roots


def get_quadratic_equation_roots(coefs: Coefs) -> Set[float]:
    discriminant = coefs["B"] ** 2 - 4 * coefs["A"] * coefs["C"]
    if discriminant < 0:
        return set()
    elif discriminant == 0:
        root = -coefs["B"] / (2.0 * coefs["C"])
        return {root}

    discr_square_root = math.sqrt(discriminant)
    denominator = (2.0 * coefs["A"])
    root1 = (-coefs["B"] + discr_square_root) / denominator
    root2 = (-coefs["B"] - discr_square_root) / denominator
    return {root1, root2}


def print_roots(roots: Set[float]):
    print(f"Корни уравнения. Всего корней {len(roots)}")
    for root in roots:
        print(root)
    print("Конец корней")


def main():
    '''
    Основная функция
    '''
    coefs = get_start_coef_values()

    for coef_name in coefs.variables_order:
        if coefs[coef_name] is None:
            coefs[coef_name] = get_coef_from_stdin(coef_name)

    # Вычисление корней
    roots = get_biquadratic_equation_roots(coefs)

    print_roots(roots)
    

if __name__ == "__main__":
    assert get_biquadratic_equation_roots(Coefs(1, 0, -4)) == {-2 ** 0.5, 2 ** 0.5}
    assert get_biquadratic_equation_roots(Coefs(1, 1, -2)) == {-1, 1}
    assert get_biquadratic_equation_roots(Coefs(1, -3, -4)) == {-2, 2}
    main()
