from scanner.scanner import Scanner
from config.config import Config


def main() -> None:
    scanner = Scanner()

    units = scanner.scan(Config.OSTRANAUTS_DATA_PATH)

    print(f"Files scanned : {scanner.scanned_files}")
    print(f"Text units : {len(units)}")

    for unit in units:
        print(unit)


if __name__ == "__main__":
    main()