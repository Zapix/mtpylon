# -*- coding: utf-8 -*-
from typing import List, Callable, Any, Union, Type, Dict, Set
from dataclasses import dataclass
from inspect import isfunction

from .exceptions import SchemaChangeError
from .utils import (
    is_annotated_union,
    get_combinators,
    is_valid_constructor,
    is_valid_function,
    get_combinator_number,
    AttrDescription,
    get_constructor_name,
    build_attr_description_list,
    get_function_name,
    get_funciton_parameters_list,
    get_function_return_type_name,
    get_function_number,
)


@dataclass
class CombinatorData:
    id: int
    predicate: str
    params: List[AttrDescription]
    type: str
    origin: Type


@dataclass
class FunctionData:
    id: int
    method: str
    params: List[AttrDescription]
    type: str
    origin: Callable


@dataclass
class SchemaStructure:
    constructors: List[CombinatorData]
    methods: List[FunctionData]


class Schema:
    """
    Base schema to load/dump messages by mtproto protocol.
    Validates passed constructors and function that could be used
    in schema. Schema stores constructors and functions and could
    return his representation as dict that could be dumps as json or
    as TL program string(https://core.telegram.org/mtproto/TL#overview)

    Allows to check constructor, combinator, function with `in` operator
    Allows to get combinator, function description by combinator, functin or
    its number
    """

    def __init__(self, constructors: List[Any], functions: List[Callable]):
        """
        Initial base schema. Validates passed constructors and schemas
        save them for dumping and loading messages. P
        """
        for constructor in constructors:
            is_valid_constructor(constructor, constructors)

        for func in functions:
            is_valid_function(func, constructors)

        self.constructors = constructors
        self.functions = functions

        self._build_schema_data()

    def __contains__(self, item: Union[Callable, Type, int]) -> bool:
        """
        Checks that function, combinator or constructor presents in schema

        Args:
            item - function, type of combinator or constructor or its number
        """
        if isinstance(item, int):
            return item in self._number_map
        if is_annotated_union(item):
            return item in self._constructors_set
        if isinstance(item, type):
            return item in self._combinator_map
        if isfunction(item):
            return item in self._function_map

        return False

    def __getitem__(
            self,
            item: Union[Callable, Type, int]
    ) -> Union[CombinatorData, FunctionData]:
        """
        Gets function or combinator data.

        Raises:
            ValueError - if constructor has been passed
            KyeError if value not fund
        """

        if item in self._constructors_set:
            raise ValueError('Schema could return combinator or function data')
        if isinstance(item, int):
            return self._number_map[item]
        if isfunction(item):
            return self._function_map[item]
        if isinstance(item, type):
            return self._combinator_map[item]

        raise KeyError('key could be int, function or type in schema')

    def __setitem__(self, key, value):
        raise SchemaChangeError(
            'Can`t remove combinator or function from schema'
        )

    def __delitem__(self, key):
        raise SchemaChangeError(
            'Can`t remove combinator or function from schema'
        )

    def __or__(self, other: 'Schema') -> 'Schema':
        return Schema(
            constructors=self.constructors + other.constructors,
            functions=self.functions + other.functions
        )

    def __ior__(self, other: 'Schema'):
        self._update(other)
        return self

    def get_schema_structure(self) -> SchemaStructure:
        """
        Structure of schema that could be dumped
        """
        constructors: List[CombinatorData] = list(
            self._combinator_map.values()
        )
        methods: List[FunctionData] = list(
            self._function_map.values()
        )

        return SchemaStructure(constructors=constructors, methods=methods)

    def _build_schema_data(self):
        self._constructors_set: Set[Type] = set([
            constructor
            for constructor in self.constructors
            if is_annotated_union(constructor)
        ])
        self._number_map: Dict[int, Union[CombinatorData, FunctionData]] = {}
        self._combinator_map: Dict[Type, CombinatorData] = {}
        self._function_map: Dict[Callable, FunctionData] = {}

        for combinator_data in self._get_combinators():
            self._number_map[combinator_data.id] = combinator_data
            self._combinator_map[combinator_data.origin] = combinator_data

        for func_data in self._get_methods():
            self._number_map[func_data.id] = func_data
            self._function_map[func_data.origin] = func_data

    def _describe_constructor(self, constructor) -> List[CombinatorData]:
        if is_annotated_union(constructor):
            return [
                CombinatorData(
                    id=get_combinator_number(combinator, constructor),
                    predicate=combinator.Meta.name,
                    params=build_attr_description_list(combinator),
                    type=get_constructor_name(constructor),
                    origin=combinator,
                )
                for combinator in get_combinators(constructor)
            ]

        return [
            CombinatorData(
                id=get_combinator_number(constructor, constructor),
                predicate=constructor.Meta.name,
                params=build_attr_description_list(constructor),
                type=get_constructor_name(constructor),
                origin=constructor,
            )
        ]

    def _describe_function(self, func) -> FunctionData:
        return FunctionData(
            id=get_function_number(func),
            method=get_function_name(func),
            params=get_funciton_parameters_list(func),
            type=get_function_return_type_name(func),
            origin=func
        )

    def _get_combinators(self) -> List[CombinatorData]:
        return [
            combinator_data
            for constructor in self.constructors
            for combinator_data in self._describe_constructor(constructor)
        ]

    def _get_methods(self) -> List[FunctionData]:
        return [
            self._describe_function(func)
            for func in self.functions
        ]

    def _update(self, schema: 'Schema'):
        """
        Updates current schema with constructors, functions from another schema

        Raises:
            ValueError if some of combinator number will be duplicated
        """
        for method in schema._get_methods():
            if method.id in self:
                raise ValueError(
                    f"Duplicate method id for {method.method} id: {method.id}"
                )

        for combinator in schema._get_combinators():
            if combinator.id in self:
                raise ValueError(
                    f"Duplicate combinator id for {combinator.predicate} " +
                    f"id: {combinator.id}"
                )

        self.constructors += schema.constructors
        self.functions += schema.functions

        self._build_schema_data()

    def update(self, schema: 'Schema'):
        """
        Updates current schema with constructors, functions from another schema

        Raises:
            ValueError if some of combinator number will be duplicated
        """
        self._update(schema)
