#!/usr/bin/env python3
import csv
import re
import sys


QUOTE_CHARS = '"„”«»'


def clean_company_name(record: dict) -> dict | None:
    """
    Czyści pole NazwaPodmiotu:
    - usuwa imię i nazwisko (Imie, Nazwisko) z początku i końca nazwy
      (warianty 'Imię Nazwisko' i 'Nazwisko Imię', case-insensitive),
    - usuwa zbędne znaki wokół nazwy (cudzysłowy, nadmiarowe spacje),
    - usuwa wszystkie znaki cudzysłowu z całej nazwy,
    - jeśli po czyszczeniu nazwa jest pusta -> zwraca None (rekord do usunięcia).
    """
    name = (record.get("NazwaPodmiotu") or "").strip()
    imie = (record.get("Imie") or "").strip()
    nazwisko = (record.get("Nazwisko") or "").strip()

    # Zbuduj listę możliwych kombinacji imię/nazwisko
    patterns = []
    if imie and nazwisko:
        patterns = [
            f"{imie} {nazwisko}",    # "JADWIGA ŻUKOWSKA"
            f"{nazwisko} {imie}",    # "ŻUKOWSKA JADWIGA"
        ]
    elif imie:
        patterns = [imie]
    elif nazwisko:
        patterns = [nazwisko]

    text = name

    # 1) Usuń imię+nazwisko z początku nazwy
    for p in patterns:
        pattern_start = r"^\s*" + re.escape(p) + r"\s*"
        text = re.sub(pattern_start, "", text, flags=re.IGNORECASE)

    # 2) Usuń imię+nazwisko z końca nazwy
    for p in patterns:
        pattern_end = r"\s*" + re.escape(p) + r"\s*$"
        text = re.sub(pattern_end, "", text, flags=re.IGNORECASE)

    # Czyszczenie cudzysłowów i spacji na brzegach
    text = text.strip()
    text = text.strip(' "\'„”«»')
    text = text.strip()

    # Zastąpienie wielu spacji jedną
    text = re.sub(r"\s+", " ", text)

    # Usunięcie wszystkich cudzysłowów z całej nazwy
    if text:
        trans = {ord(ch): None for ch in QUOTE_CHARS}
        text = text.translate(trans)

    # Ponownie dociśnij spacje (na wypadek usunięcia czegoś pomiędzy)
    text = text.strip()
    text = re.sub(r"\s+", " ", text)

    # Jeśli nic nie zostało – pomijamy ten rekord
    if not text:
        return None

    new_record = dict(record)
    new_record["NazwaPodmiotu"] = text
    return new_record


def process_csv(input_path: str, output_path: str, delimiter: str = ";") -> None:
    # Wczytujemy CSV z obsługą BOM
    with open(input_path, encoding="utf-8-sig", newline="") as f_in:
        reader = csv.DictReader(f_in, delimiter=delimiter)
        if reader.fieldnames is None:
            raise ValueError("Brak nagłówków w pliku CSV.")

        cleaned_rows = []
        for row in reader:
            cleaned = clean_company_name(row)
            if cleaned is not None:
                # Na wyjściu: nazwa firmy, NIP oraz pusta kolumna
                cleaned_rows.append({
                    "NazwaPodmiotu": cleaned.get("NazwaPodmiotu", ""),
                    "Nip": cleaned.get("Nip", ""),
                    "Przeważająca działalność gospodarcza": "",
                })

    # Zapisujemy wynik do nowego CSV
    fieldnames_out = ["NazwaPodmiotu", "Nip", "Przeważająca działalność gospodarcza"]

    with open(output_path, "w", encoding="utf-8", newline="") as f_out:
        writer = csv.DictWriter(f_out, fieldnames=fieldnames_out, delimiter=delimiter)
        writer.writeheader()
        writer.writerows(cleaned_rows)


if __name__ == "__main__":
    # Użycie:
    # python main.py input.csv output.csv
    in_path = sys.argv[1] if len(sys.argv) > 1 else "input.csv"
    out_path = sys.argv[2] if len(sys.argv) > 2 else "output.csv"
    process_csv(in_path, out_path, delimiter=";")
