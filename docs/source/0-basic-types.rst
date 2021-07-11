.. _mtpylon_basic_types:

Basic types
===========

Basic types is set of simple types that could be dumped:

 * `int` - dump as 32-bit integer
 * `long` - dump as 64-bit integer
 * `int128` - dump as 128-bit integer
 * `int256` - dump as 256-bit integer
 * `double` - dump as float value `format info <https://en.wikipedia.org/wiki/Double-precision_floating-point_format>`_
 * `string` - dump as string that encoded in  utf-8 format. `String description <https://core.telegram.org/type/string>`_
 * `bytes` - dump as bytes by `Bytes description <https://core.telegram.org/type/bytes>`_


.. note::

  All int values and dumped as unsigned int. Will fixed at soon.
  Ticker for it: `<https://github.com/Zapix/mtpylon/issues/33>`_

Types `long`, `int128`, `int256` and `double` could be import from
`mtpylon` package
