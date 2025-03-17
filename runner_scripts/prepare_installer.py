import argparse
import os
import sys

from cura import CuraVersion


def set_installer_filename(args):
    os_name = {"Linux": "linux", "Windows": "win64", "macOS": "macos"}.get(args.os, "unknown")
    enterprise = "-Enterprise" if args.enterprise else ""
    internal = "-Internal" if args.internal else ""
    
    # Validate CuraVersion attributes
    cura_version_full = getattr(CuraVersion, "CuraVersionFull", getattr(CuraVersion, "CuraVersion", "UnknownVersion"))

    # Construct installer filename
    installer_filename_args = ["UltiMaker-Cura", cura_version_full]
    if args.enterprise:
        installer_filename_args.append("Enterprise")
    if args.internal:
        installer_filename_args.append("Internal")
    installer_filename_args.append(os_name)
    installer_filename_args.append(args.architecture)

    installer_filename = "-".join(installer_filename_args)

    # Write variables output
    variables_output = sys.stdout
    if args.variables_output is not None:
        variables_output = open(args.variables_output, "a")
    variables_output.write(f"INSTALLER_FILENAME={installer_filename}\n")
    variables_output.write(f"CURA_VERSION={getattr(CuraVersion, 'CuraVersion', 'Unknown')}\n")
    variables_output.write(f"CURA_VERSION_FULL={cura_version_full}\n")
    variables_output.write(f"CURA_APP_NAME={getattr(CuraVersion, 'CuraAppDisplayName', 'UnknownApp')}\n")

    # Write summary output
    summary_output = sys.stdout
    if args.summary_output is not None:
        summary_output = open(args.summary_output, "a")
    summary_output.write(f"# {installer_filename}\n")
    
    # Print Conan packages
    summary_output.write("## Conan packages:\n")
    for dep_name, dep_info in getattr(CuraVersion, "ConanInstalls", {}).items():
        summary_output.write(f"`{dep_name} {dep_info.get('version', 'Unknown')} {dep_info.get('revision', 'Unknown')}`\n")

    # Print Python modules
    summary_output.write("## Python modules:\n")
    for dep_name, dep_info in getattr(CuraVersion, "PythonInstalls", {}).items():
        summary_output.write(f"`{dep_name} {dep_info.get('version', 'Unknown')}`\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Set the installer filename")
    parser.add_argument('--os', type=str, required=True, help="Target OS (Windows, Linux, macOS)")
    parser.add_argument('--architecture', type=str, required=True, help="Target architecture (x64, x86)")
    parser.add_argument('--enterprise', action='store_true', help="Enterprise version flag")
    parser.add_argument('--internal', action='store_true', help="Internal version flag")
    parser.add_argument('--summary-output', type=str, help="Output file for the summary")
    parser.add_argument('--variables-output', type=str, help="Output file for the variables")
    
    args = parser.parse_args()
    set_installer_filename(args)
