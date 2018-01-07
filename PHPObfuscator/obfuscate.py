import sys
import re

# TODO: change var names
# TODO: deal with classes ($this, $member ... $this->member)
# TODO: Remove comments
# TODO: bug: var name contained in another var name

PHP_EXT = ".php"
VARIABLE_REGEX = re.compile(r'(?:^\$(?P<variable1>\w+))|(?:\s+\$(?P<variable2>\w+))|(?:;\$(?P<variable3>\w+))')
PREDEFINED_VARS = {"GLOBALS", "_SERVER", "_GET", "_POST", "_FILES", "_REQUEST", "_SESSION", "_ENV", "_COOKIE",
                   "php_errormsg", "HTTP_RAW_POST_DATA", "http_response_header", "argc", "argv", "this"}


def get_all_variables(php):
    regex_result = VARIABLE_REGEX.findall(php)
    all_vars = set()
    for result in regex_result:
        for regex_variable_group in result:
            if regex_variable_group:
                all_vars.add(regex_variable_group)
                break

    return all_vars.difference(PREDEFINED_VARS)


def rename_vars(php, variables):
    for i, var in enumerate(variables):
        php = php.replace("$" + var, "$" + str(i))
    return php


def obfuscate(php):
    variables = get_all_variables(php)
    php = rename_vars(php, variables)
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
