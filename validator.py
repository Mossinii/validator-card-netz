"""Validação de cartões de crédito.

Esta classe implementa a validação do algoritmo de Luhn e identifica as
bandeiras mais comuns usando expressões regulares:

- Visa: começa com 4
- Mastercard: começa com 51-55 ou 2221-2720
- American Express: começa com 34 ou 37

Exemplo de uso:

    from validator import CreditCardValidator

    number = "4111 1111 1111 1111"
    print(CreditCardValidator.get_brand(number))  # Visa
    print(CreditCardValidator.is_valid(number))  # True
"""

from __future__ import annotations

import re
from typing import Optional


class CreditCardValidator:
    """Valida números de cartão de crédito e identifica a bandeira."""

    # Padrões de bandeira (bandeiras suportadas)
    _BRAND_REGEX = {
        "Visa": re.compile(r"^4[0-9]{12}(?:[0-9]{3})?$"),
        # Mastercard: 51-55 ou 2221-2720
        "Mastercard": re.compile(
            r"^(?:5[1-5][0-9]{14}|2(?:2(?:2[1-9]|[3-9][0-9])|[3-6][0-9]|7(?:0[0-9]|1[0-9]|20))[0-9]{12})$"
        ),
        # American Express: 34 ou 37
        "American Express": re.compile(r"^3[47][0-9]{13}$"),
    }

    @staticmethod
    def _clean_number(number: str) -> str:
        """Remove espaços e traços do número do cartão."""
        return re.sub(r"[\s-]+", "", number)

    @classmethod
    def get_brand(cls, number: str) -> Optional[str]:
        """Retorna a bandeira do cartão (Visa, Mastercard, Amex) ou None."""
        n = cls._clean_number(number)
        for brand, pattern in cls._BRAND_REGEX.items():
            if pattern.match(n):
                return brand
        return None

    @staticmethod
    def is_valid(number: str) -> bool:
        """Valida o número do cartão usando o algoritmo de Luhn."""
        n = CreditCardValidator._clean_number(number)
        if not n.isdigit():
            return False

        total = 0
        reverse_digits = n[::-1]
        for i, digit in enumerate(reverse_digits):
            d = int(digit)
            # Cada segundo dígito (índices ímpares na ordem reversa) é dobrado
            if i % 2 == 1:
                d *= 2
                if d > 9:
                    d -= 9
            total += d
        return total % 10 == 0


if __name__ == "__main__":
    numero = input("Digite o número do cartão (pode conter espaços ou traços): ").strip()

    bandeira = CreditCardValidator.get_brand(numero)
    valido = CreditCardValidator.is_valid(numero)

    print("\nResultado da validação:")
    print(f"  Número      : {numero}")
    print(f"  Bandeira    : {bandeira or 'Desconhecida'}")
    print(f"  Luhn válido : {'Sim' if valido else 'Não'}")
