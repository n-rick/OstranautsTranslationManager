from scanner.scanner import Scanner


def main() -> None:
    scanner = Scanner()

    units = scanner.scan("./tests/data")

    print(f"Files scanned : {scanner.scanned_files}")
    print(f"Text units : {len(units)}")

    for unit in units:
        print(unit)


if __name__ == "__main__":
    main()