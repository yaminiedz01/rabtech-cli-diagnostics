import argparse
import json

from diagnostics.checks import (
    check_disk_space,
    check_environment,
    check_python_version,
)


def run_diagnostics():
    return {
        "python": check_python_version(),
        "disk": check_disk_space(),
        "environment": check_environment(),
    }


def main():
    parser = argparse.ArgumentParser(
        description="RabTech CLI Diagnostics Tool"
    )

    parser.add_argument(
        "--json",
        action="store_true",
        help="Display the diagnostic report as JSON",
    )

    args = parser.parse_args()

    report = run_diagnostics()

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print("=== RabTech CLI Diagnostics Report ===")
        print(f"Python Version : {report['python']['python_version']}")
        print(f"Python Path    : {report['python']['executable']}")
        print(f"Disk Total     : {report['disk']['total_gb']} GB")
        print(f"Disk Used      : {report['disk']['used_gb']} GB")
        print(f"Disk Free      : {report['disk']['free_gb']} GB")
        print("Environment    : Checked")


if __name__ == "__main__":
    main()