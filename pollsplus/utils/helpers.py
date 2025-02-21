#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def human_readable_size(size: int) -> str:
    """
    Convert size in bytes to human readable format

    Example:

    >>> human_readable_size(0)
    '0.00 B'

    >>> human_readable_size(1)
    '1.00 B'

    >>> human_readable_size(1024)
    '1.00 KB'

    >>> human_readable_size(1024*1024)
    '1.00 MB'

    >>> human_readable_size(1024*1024*1024)
    '1.00 GB'

    >>> human_readable_size(1024*1024*1024*1024)
    '1.00 TB'

    >>> human_readable_size(1024*1024*1024*1024*1024)
    '1.00 PB'

    >>> human_readable_size(1024*1024*1024*1024*1024*1024)
    '1.00 EB'

    >>> human_readable_size(1024*1024*1024*1024*1024*1024*1024)
    '1.00 ZB'

    >>> human_readable_size(1024*1024*1024*1024*1024*1024*1024*1024)
    '1.00 YB'

    >>> human_readable_size(1024*1024*1024*1024*1024*1024*1024*1024*1024)
    '1024.00 YB'

    :param size: size in bytes
    :type size: int
    :return: size in human readable format
    :rtype: str
    """
    for unit in ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB"):
        if size < 1024.0:
            return f"{size:3.2f} {unit}"
        size /= 1024.0
    return f"{round(size, 2):.2f} YB"


if __name__ == "__main__":
    import doctest

    doctest.testmod()
