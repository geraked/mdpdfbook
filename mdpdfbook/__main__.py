from os import path, system
import os
import req
import convert


def main():
    req.main()
    folder = input(
        'Enter the directory path containing SUMMARY.md or other *.md files:\n')
    try:
        c = convert.MdToPdf(folder)
        p = path.abspath(c.output)
        print(60 * '-')
        print('Successfully converted!')
        print(p)
    except Exception as e:
        print(60 * '-')
        print(e)
    system("PAUSE")


if __name__ == '__main__':
    main()
