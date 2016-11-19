#!/usr/bin/env python3
#  Copyright 2016 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS-IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from fruit_test_common import *

COMMON_DEFINITIONS = '''
#include <fruit/fruit.h>
#include <vector>
#include "test_macros.h"

struct X;

struct Annotation {};
using XAnnot = fruit::Annotated<Annotation, X>;

struct Annotation1 {};
using XAnnot1 = fruit::Annotated<Annotation1, X>;

struct Annotation2 {};
using XAnnot2 = fruit::Annotated<Annotation2, X>;
'''

def test_component_conversion():
    expect_success(
    COMMON_DEFINITIONS + '''
struct X {
  INJECT(X()) = default;
};

fruit::Component<> getComponent() {
  return fruit::createComponent();
}

fruit::Component<X> getXComponent() {
  return getComponent();
}

int main() {
  fruit::Component<X> component = getXComponent();
  fruit::Injector<X> injector(component);
  injector.get<X*>();
}
''')

def test_component_conversion_with_annotation():
    expect_success(
    COMMON_DEFINITIONS + '''
struct X {
  using Inject = X();
};

fruit::Component<> getComponent() {
  return fruit::createComponent();
}

fruit::Component<XAnnot> getXComponent() {
  return getComponent();
}

int main() {
  fruit::Component<XAnnot> component = getXComponent();
  fruit::Injector<XAnnot> injector(component);
  injector.get<fruit::Annotated<Annotation, X*>>();
}
''')

def test_copy():
    expect_success(
    COMMON_DEFINITIONS + '''
struct X {
  INJECT(X()) = default;
};

fruit::Component<X> getComponent() {
  fruit::Component<X> c = fruit::createComponent();
  fruit::Component<X> copy = c;
  return copy;
}

int main() {
  fruit::Component<X> component = getComponent();
  fruit::Injector<X> injector(component);
  injector.get<X*>();
}
''')

def test_copy_with_annotation():
    expect_success(
    COMMON_DEFINITIONS + '''
struct X {
  using Inject = X();
};

fruit::Component<XAnnot> getComponent() {
  fruit::Component<XAnnot> c = fruit::createComponent();
  fruit::Component<XAnnot> copy = c;
  return copy;
}

int main() {
  fruit::Component<XAnnot> component = getComponent();
  fruit::Injector<XAnnot> injector(component);
  injector.get<XAnnot>();
}
''')

def test_error_non_class_type():
    expect_compile_error(
    'NonClassTypeError<X\*,X>',
    'A non-class type T was specified. Use C instead.',
    COMMON_DEFINITIONS + '''
struct X {};

void f() {
    (void) sizeof(fruit::Component<X*>);
}
''')

def test_error_non_class_type_with_annotation():
    expect_compile_error(
    'NonClassTypeError<X\*,X>',
    'A non-class type T was specified. Use C instead.',
    COMMON_DEFINITIONS + '''
struct X {};

void f() {
    (void) sizeof(fruit::Component<fruit::Annotated<Annotation, X*>>);
}
''')

def test_error_repeated_type():
    expect_compile_error(
    'RepeatedTypesError<X,X>',
    'A type was specified more than once.',
    COMMON_DEFINITIONS + '''
struct X {};

void f() {
    (void) sizeof(fruit::Component<X, X>);
}
''')

def test_error_repeated_type_with_annotation():
    expect_compile_error(
    'RepeatedTypesError<fruit::Annotated<Annotation,X>,fruit::Annotated<Annotation,X>>',
    'A type was specified more than once.',
    COMMON_DEFINITIONS + '''
struct X {};

void f() {
    (void) sizeof(fruit::Component<XAnnot, XAnnot>);
}
''')

def test_repeated_type_with_different_annotation_ok():
    expect_success(
    COMMON_DEFINITIONS + '''
struct X {};

int main() {
    (void) sizeof(fruit::Component<XAnnot1, XAnnot2>);
}
''')

def test_error_type_required_and_provided():
    expect_compile_error(
    'RepeatedTypesError<X,X>',
    'A type was specified more than once.',
    COMMON_DEFINITIONS + '''
struct X {};

void f() {
    (void) sizeof(fruit::Component<fruit::Required<X>, X>);
}
''')

def test_error_type_required_and_provided_with_annotations():
    expect_compile_error(
    'RepeatedTypesError<fruit::Annotated<Annotation,X>',
    'fruit::Annotated<Annotation,X>>|A type was specified more than once.',
    COMMON_DEFINITIONS + '''
struct X {};

void f() {
    (void) sizeof(fruit::Component<fruit::Required<XAnnot>, XAnnot>);
}
''')

def test_type_required_and_provided_with_different_annotations_ok():
    expect_success(
    COMMON_DEFINITIONS + '''
struct X {};

int main() {
    (void) sizeof(fruit::Component<fruit::Required<XAnnot1>, XAnnot2>);
}
''')

def test_error_no_binding_found():
    expect_compile_error(
    'NoBindingFoundError<X>',
    'No explicit binding nor C::Inject definition was found for T.',
    COMMON_DEFINITIONS + '''
struct X {};

fruit::Component<X> getComponent() {
  return fruit::createComponent();
}
''')

def test_error_no_binding_found_with_annotation():
    expect_compile_error(
    'NoBindingFoundError<fruit::Annotated<Annotation,X>>',
    'No explicit binding nor C::Inject definition was found for T.',
    COMMON_DEFINITIONS + '''
struct X {};

fruit::Component<XAnnot> getComponent() {
  return fruit::createComponent();
}
''')

def test_error_no_factory_binding_found():
    expect_compile_error(
    'NoBindingFoundError<std::function<std::unique_ptr<X(,std::default_delete<X>)?>\(\)>',
    'No explicit binding nor C::Inject definition was found for T.',
    COMMON_DEFINITIONS + '''
struct X {};

fruit::Component<std::function<std::unique_ptr<X>()>> getComponent() {
  return fruit::createComponent();
}
''')

def test_error_no_factory_binding_found_with_annotation():
    expect_compile_error(
    'NoBindingFoundError<fruit::Annotated<Annotation,std::function<std::unique_ptr<X(,std::default_delete<X>)?>\(\)>>',
    'No explicit binding nor C::Inject definition was found for T.',
    COMMON_DEFINITIONS + '''
struct X {};

fruit::Component<fruit::Annotated<Annotation, std::function<std::unique_ptr<X>()>>> getComponent() {
  return fruit::createComponent();
}
''')

if __name__ == '__main__':
    import nose2
    nose2.main()