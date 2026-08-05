from scanner.json_extractor import JsonExtractor


def main() -> None:
    extractor = JsonExtractor()

    units = extractor.extract("tests/data/sample.json")

    print(f"{len(units)} TextUnit(s) found\n")

    for unit in units:
        print(unit)

if __name__ == "__main__":
    main()
