import sys
import re

PHP_EXT = ".php"
VARIABLE_REGEX = re.compile(r'(?:^\$(?P<variable>\w+))|(?:\s+\$(?P<variable2>\w+))')
PREDEFINED_VARS = set("GLOBALS", "_SERVER", "_GET", "_POST", "_FILES", "_REQUEST", "_SESSION", "_ENV",
                      "_COOKIE", "php_errormsg", "HTTP_RAW_POST_DATA", "http_response_header", "argc", "argv")


def get_all_variables(php):
    regex_result = VARIABLE_REGEX.findall(php)
    all_vars = set()
    for result in regex_result:
        if result["variable"] is not None:
            all_vars.add(result["variable"])
        elif result["variable2"] is not None:
            all_vars.add(result["variable2"])
        else:
            raise Exception("Unexpected error in regex parsing")
    return all_vars.difference(PREDEFINED_VARS)


def obfuscate(php):
    print get_all_variables(php)
    return php


def main(path):
    assert path.endswith(PHP_EXT), "Expected a file with .php extension"
    with open(path, "rb") as f:
        content = f.read()

    content = obfuscate(content)

    out_path = path[:-len(PHP_EXT)] + ".obf" + PHP_EXT
    with open(out_path, "wb") as f:
        f.write(content)


if __name__ == "__main__":
    main(sys.argv[1])
