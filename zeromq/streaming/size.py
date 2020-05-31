#!/usr/bin/env python

import click
from collections import namedtuple

Size = namedtuple("Size", ["width", "height"])

class SizeParamType(click.ParamType):
    name = "size"

    def convert(self, value, param, context):
        try:
            segments = value.split("x")
            width = segments[0]
            height = segments[1]
            return Size(int(width), int(height))
        except:
            self.fail(
                f"{value} is not a valid size",
                param,
                context,
            )

SIZE = SizeParamType()
