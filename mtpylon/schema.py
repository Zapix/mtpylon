# -*- coding: utf-8 -*-
from typing import List, Callable, Any
from dataclasses import dataclass

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


@dataclass
class FunctionData:
    id: int
    method: str
    params: List[AttrDescription]
    type: str


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
    """

    def __init__(self, constructors: List[Any], functions: List[Callable]):
        """
        Initial base schema. Validates passed constructors and schemas
        save them for dumping and loading messages
        """
        for constructor in constructors:
            is_valid_constructor(constructor, constructors)

        for func in functions:
            is_valid_function(func, constructors)

        self.constructors = constructors
        self.functions = functions

    def get_schema_structure(self) -> SchemaStructure:
        """
        Structure of schema that could be dumped
        """
        constructors: List[CombinatorData] = self._get_constructors()
        methods: List[FunctionData] = self._get_methods()

        return SchemaStructure(constructors=constructors, methods=methods)

    def _describe_constructor(self, constructor) -> List[CombinatorData]:
        if is_annotated_union(constructor):
            return [
                CombinatorData(
                    id=get_combinator_number(combinator, constructor),
                    predicate=combinator.Meta.name,
                    params=build_attr_description_list(combinator),
                    type=get_constructor_name(constructor)
                )
                for combinator in get_combinators(constructor)
            ]

        return [
            CombinatorData(
                id=get_combinator_number(constructor, constructor),
                predicate=constructor.Meta.name,
                params=build_attr_description_list(constructor),
                type=get_constructor_name(constructor)
            )
        ]

    def _describe_function(self, func) -> FunctionData:
        return FunctionData(
            id=get_function_number(func),
            method=get_function_name(func),
            params=get_funciton_parameters_list(func),
            type=get_function_return_type_name(func),
        )

    def _get_constructors(self) -> List[CombinatorData]:
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
